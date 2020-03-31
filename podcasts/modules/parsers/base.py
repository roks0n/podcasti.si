from datetime import datetime
from time import mktime

import feedparser

from lxml import etree as ET

from podcasts.models import Episode

import requests


class BasePodcastParser:
    episode_identifier = Episode.identifier.field.name

    def __init__(self, podcast_feed, *args, **kwargs):
        raise NotImplementedError

    def parse(self):
        raise NotImplementedError

    def parse_episode(self, episode_xml):
        episode = {
            "identifier": self.parse_id(episode_xml),
            "title": self.parse_title(episode_xml),
            "description": self.parse_description(episode_xml),
            "published_datetime": self.parse_published_datetime(episode_xml),
            "audio": self.parse_audio(episode_xml),
            "url": self.parse_url(episode_xml),
        }
        return episode

    def parse_id(self, episode_xml):
        raise NotImplementedError

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


class PlainPodcastParser(BasePodcastParser):
    xml_data = None
    nsmap = None

    def __init__(self, podcast_feed, *args, **kwargs):
        response = requests.get(podcast_feed)
        self.xml_data = ET.fromstring(response.content)
        self.nsmap = self.xml_data.nsmap

    def parse(self):
        episodes = []
        for episode in self.xml_data.findall(".//item"):
            parsed_episode = self.parse_episode(episode)
            if parsed_episode:
                episodes.append(parsed_episode)
        return episodes

    def parse_id(self, episode_xml):
        return episode_xml.find("guid", namespaces=self.nsmap).text.strip()


class DefaultPodcastParser(BasePodcastParser):
    feed = None

    def __init__(self, podcast_feed, *args, **kwargs):
        self.feed = feedparser.parse(podcast_feed)

    def parse(self):
        episodes = []
        for episode in self.feed.entries:
            parsed_episode = self.parse_episode(episode)
            if parsed_episode:
                episodes.append(parsed_episode)
        return episodes

    def parse_id(self, episode_xml):
        return episode_xml.id

    def parse_title(self, episode_xml):
        title = episode_xml.title.strip()
        if len(title) >= 256:
            title = f"{title[:256-3]}..."
        return episode_xml.title.strip()

    def parse_description(self, episode_xml):
        if "content" not in episode_xml:
            return ""

        for content in episode_xml.content:
            if content.type != "text/plain":
                continue
            return content.value

        return ""

    def parse_published_datetime(self, episode_xml):
        published = episode_xml.published_parsed
        if published:
            return datetime.fromtimestamp(mktime(published))

    def parse_audio(self, episode_xml):
        for link in episode_xml.links:
            if link.type != "audio/mpeg":
                continue
            return link.href

    def parse_url(self, episode_xml):
        for link in episode_xml.links:
            if link.type != "text/html":
                continue
            return link.href

    def parse_author(self, episode_xml):
        return


class ZakulisjeParser(PlainPodcastParser):
    def parse_title(self, episode_xml):
        return episode_xml.find("title", namespaces=self.nsmap).text.strip()

    def parse_description(self, episode_xml):
        return ""

    def parse_published_datetime(self, episode_xml):
        datetime_string = episode_xml.find("pubDate", namespaces=self.nsmap).text.strip()
        return datetime.strptime(datetime_string, "%a, %d %b %Y %H:%M:%S %z")

    def parse_audio(self, episode_xml):
        html_string = episode_xml.find("description", namespaces=self.nsmap).text
        if not html_string:
            return ""

        dom = ET.HTML(html_string.strip())
        for link in dom.findall(".//a"):
            href = link.attrib.get("href")
            if href and href.endswith(".mp3"):
                return href

    def parse_url(self, episode_xml):
        return episode_xml.find("link").text.strip()


class RadioGaGaParser(DefaultPodcastParser):
    def parse_title(self, episode_xml):
        title = episode_xml.title.strip()
        if title.lower().replace(" ", "").replace("-", "") == "radiogaga":
            # add date to identify episode
            episode_date = self.parse_published_datetime(episode_xml).strftime("%d.%m.%Y")
            return f"{title} {episode_date}"
        else:
            return title
