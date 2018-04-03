from datetime import datetime

from bs4 import BeautifulSoup

from lxml import etree as ET

import requests

from podcasts.models import Episode


class BasePodcastParser:
    xml_data = None
    nsmap = None
    episode_identifier = Episode.title.field_name

    def __init__(self, podcast_feed, *args, **kwargs):
        response = requests.get(podcast_feed)
        self.xml_data = ET.fromstring(response.content)
        self.nsmap = self.xml_data.nsmap

    def parse(self):
        episodes = []
        for episode in self.xml_data.findall('.//item'):
            parsed_episode = self.parse_episode(episode)
            if parsed_episode:
                episodes.append(parsed_episode)
        return episodes

    def parse_episode(self, episode_xml):
        episode = {
            'title': self.parse_title(episode_xml),
            'description': self.parse_description(episode_xml),
            'published_datetime': self.parse_published_datetime(episode_xml),
            'audio': self.parse_audio(episode_xml),
            'url': self.parse_url(episode_xml),
        }
        return episode

    def parse_title(self, episode_xml):
        raise NotImplementedError

    def parse_description(self, episode_xml):
        raise NotImplementedError

    def parse_published_datetime(self, episode_xml):
        raise NotImplementedError

    def parse_audio(self, episode_xml):
        raise NotImplementedError

    def parse_url(self, episode_xml):
        raise NotImplementedError


class DefaultPodcastParser(BasePodcastParser):

    def parse_title(self, episode_xml):
        return episode_xml.find('title', namespaces=self.nsmap).text.strip()

    def parse_description(self, episode_xml):
        return episode_xml.find('description', namespaces=self.nsmap).text

    def parse_published_datetime(self, episode_xml):
        datetime_string = episode_xml.find('pubDate', namespaces=self.nsmap).text.strip()
        return datetime.strptime(datetime_string, '%a, %d %b %Y %H:%M:%S %z')

    def parse_audio(self, episode_xml):
        enclosure = episode_xml.find('enclosure')
        if enclosure is not None:
            return enclosure.get('url')

    def parse_url(self, episode_xml):
        url = episode_xml.find('guid').text.strip()
        if 'mp3' in url:
            return
        return url

    def parse_author(self, episode_xml):
        return episode_xml.find('dc:author', namespaces=self.nsmap).text.strip()


class ZakulisjeParser(BasePodcastParser):

    def parse_title(self, episode_xml):
        return episode_xml.find('title', namespaces=self.nsmap).text.strip()

    def parse_description(self, episode_xml):
        return ''

    def parse_published_datetime(self, episode_xml):
        datetime_string = episode_xml.find('pubDate', namespaces=self.nsmap).text.strip()
        return datetime.strptime(datetime_string, '%a, %d %b %Y %H:%M:%S %z')

    def parse_audio(self, episode_xml):
        html_string = episode_xml.find('description', namespaces=self.nsmap).text.strip()
        dom = ET.HTML(html_string)
        for link in dom.findall('.//a'):
            href = link.attrib.get('href')
            if href and href.endswith('.mp3'):
                return href

    def parse_url(self, episode_xml):
        return episode_xml.find('link').text.strip()


class FilmStartParser(BasePodcastParser):

    def parse_title(self, episode_xml):
        return episode_xml.find('title', namespaces=self.nsmap).text.strip()

    def parse_description(self, episode_xml):
        html_string = episode_xml.find('description', namespaces=self.nsmap).text
        dom = ET.HTML(html_string)
        description = dom.findall('.//p')[0].text.replace('[…]', '...')
        return description

    def parse_published_datetime(self, episode_xml):
        datetime_string = episode_xml.find('pubDate', namespaces=self.nsmap).text.strip()
        return datetime.strptime(datetime_string, '%a, %d %b %Y %H:%M:%S %z')

    def parse_audio(self, episode_xml):
        html_string = episode_xml.find('content:encoded', namespaces=self.nsmap).text.strip()
        dom = ET.HTML(html_string)
        for link in dom.findall('.//a'):
            href = link.attrib.get('href')
            if href and href.endswith('.mp3'):
                return href

    def parse_url(self, episode_xml):
        return episode_xml.find('link').text.strip()


class TorpedoParser(BasePodcastParser):

    def parse_title(self, episode_xml):
        return episode_xml.find('title', namespaces=self.nsmap).text.strip()

    def parse_description(self, episode_xml):
        html_string = episode_xml.find('description', namespaces=self.nsmap).text.strip()
        soup = BeautifulSoup(html_string, "lxml")
        text = soup.get_text()
        paragraphs = text.split('\n')

        good_paragraphs = []
        bad_words = ['na facebooku', 'click play below', 'prisluhnite pogovoru']
        has_bad_word = False
        for paragraph in paragraphs:
            if has_bad_word:
                has_bad_word = False
                continue

            for bad_word in bad_words:
                if bad_word in paragraph.lower():
                    has_bad_word = True

            if not has_bad_word:
                good_paragraphs.append(paragraph)

        stringify = ' '.join(good_paragraphs)
        return ' '.join(stringify.split())

    def parse_published_datetime(self, episode_xml):
        datetime_string = episode_xml.find('pubDate', namespaces=self.nsmap).text.strip()
        return datetime.strptime(datetime_string, '%a, %d %b %Y %H:%M:%S %z')

    def parse_audio(self, episode_xml):
        enclosure = episode_xml.find('enclosure')
        if enclosure is not None:
            return enclosure.get('url')

    def parse_url(self, episode_xml):
        url = episode_xml.find('guid').text.strip()
        if 'mp3' in url:
            return
        return url

    def parse_author(self, episode_xml):
        return episode_xml.find('dc:author', namespaces=self.nsmap).text.strip()


class MembranjeParser(TorpedoParser):
    pass


class FotkastParser(TorpedoParser):
    pass


class TheTranzistorijParser(TorpedoParser):
    pass


class BitniPogovoriParser(DefaultPodcastParser):

    def parse_description(self, episode_xml):
        return episode_xml.find('itunes:subtitle', namespaces=self.nsmap).text or ''

    def parse_url(self, episode_xml):
        return episode_xml.find('link').text.strip()


class NaPoteziParser(BitniPogovoriParser):
    pass


class FeedBurnerParser(BasePodcastParser):

    def parse_title(self, episode_xml):
        return episode_xml.find('title', namespaces=self.nsmap).text.strip()

    def parse_description(self, episode_xml):
        return episode_xml.find('itunes:summary', namespaces=self.nsmap).text.strip()

    def parse_published_datetime(self, episode_xml):
        datetime_string = episode_xml.find('pubDate', namespaces=self.nsmap).text.strip()
        return datetime.strptime(datetime_string, '%a, %d %b %Y %H:%M:%S %z')

    def parse_audio(self, episode_xml):
        return episode_xml.find('media:content', namespaces=self.nsmap).get('url')

    def parse_url(self, episode_xml):
        return episode_xml.find('feedburner:origLink', namespaces=self.nsmap).text


class BimPogovoriParser(FeedBurnerParser):
    pass


class SoundcloudParser(DefaultPodcastParser):
    def parse_url(self, episode_xml):
        return


class TandemParser(DefaultPodcastParser):

    def parse_description(self, episode_xml):
        description = super().parse_description(episode_xml)
        return description.strip().replace('\n', '')

    def parse_url(self, episode_xml):
        return


class RadioGaGaParser(DefaultPodcastParser):

    episode_identifier = Episode.audio.field_name

    def parse_title(self, episode_xml):
        title = episode_xml.find('title', namespaces=self.nsmap).text.strip()
        if title.lower().replace(' ', '').replace('-', '') == 'radiogaga':
            # add date to identify episode
            episode_date = self.parse_published_datetime(episode_xml).strftime('%d.%m.%Y')
            return f'{title} {episode_date}'
        else:
            return title

    def parse_episode(self, episode_xml):
        if 'RadioGA-GA' in episode_xml.find('guid').text:
            return super().parse_episode(episode_xml)
        return
