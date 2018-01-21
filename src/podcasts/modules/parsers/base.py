# -*- coding: utf-8 -*-
from datetime import datetime

from bs4 import BeautifulSoup

from lxml import etree as ET

import requests


class BasePodcastParser():
    xml_data = None
    nsmap = None

    def __init__(self, podcast_feed, *args, **kwargs):
        response = requests.get(podcast_feed)
        self.xml_data = ET.fromstring(response.content)
        self.nsmap = self.xml_data.nsmap

    def parse(self):
        episodes = []
        for episode in self.xml_data.findall('.//item'):
            episodes.append(self.parse_episode(episode))
        return episodes

    def parse_episode(self, episode_xml):
        episode = {
            'title': self.parse_title(episode_xml),
            'description': self.parse_description(episode_xml),
            'published_datetime': self.parse_published_date(episode_xml),
            'audio': self.parse_audio(episode_xml),
            'url': self.parse_url(episode_xml),
        }
        return episode

    def parse_title(self):
        raise NotImplementedError

    def parse_description(self):
        raise NotImplementedError

    def parse_published_date(self):
        raise NotImplementedError

    def parse_audio(self):
        raise NotImplementedError

    def parse_url(self):
        raise NotImplementedError


class DefaultPodcastParser(BasePodcastParser):

    def parse_title(self, episode_xml):
        return episode_xml.find('title', namespaces=self.nsmap).text.strip()

    def parse_description(self, episode_xml):
        return episode_xml.find('description', namespaces=self.nsmap).text

    def parse_published_date(self, episode_xml):
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
        return episode_xml.find('description', namespaces=self.nsmap).text.strip().replace('\n', '')

    def parse_published_date(self, episode_xml):
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


class FilmStartParser(BasePodcastParser):

    def parse_title(self, episode_xml):
        return episode_xml.find('title', namespaces=self.nsmap).text.strip()

    def parse_description(self, episode_xml):
        html_string = episode_xml.find('description', namespaces=self.nsmap).text
        dom = ET.HTML(html_string)
        description = dom.findall('.//p')[0].text.replace('[…]', '...')
        return description

    def parse_published_date(self, episode_xml):
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

    def parse_published_date(self, episode_xml):
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


class BitniPogovoriParser(DefaultPodcastParser):

    def parse_description(self, episode_xml):
        return episode_xml.find('itunes:subtitle', namespaces=self.nsmap).text or ''

    def parse_url(self, episode_xml):
        return episode_xml.find('link').text.strip()


class FeedBurnerParser(BasePodcastParser):

    def parse_title(self, episode_xml):
        return episode_xml.find('title', namespaces=self.nsmap).text.strip()

    def parse_description(self, episode_xml):
        return episode_xml.find('itunes:summary', namespaces=self.nsmap).text.strip()

    def parse_published_date(self, episode_xml):
        datetime_string = episode_xml.find('pubDate', namespaces=self.nsmap).text.strip()
        return datetime.strptime(datetime_string, '%a, %d %b %Y %H:%M:%S %z')

    def parse_audio(self, episode_xml):
        return episode_xml.find('media:content', namespaces=self.nsmap).get('url')

    def parse_url(self, episode_xml):
        return episode_xml.find('feedburner:origLink', namespaces=self.nsmap).text
