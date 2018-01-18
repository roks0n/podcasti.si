# -*- coding: utf-8 -*-
from datetime import datetime

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

    def parse_author(self):
        raise NotImplementedError


class DefaultPodcastParser(BasePodcastParser):

    def parse_title(self, episode_xml):
        return episode_xml.find('title', namespaces=self.nsmap).text.strip()

    def parse_description(self, episode_xml):
        return episode_xml.find('description', namespaces=self.nsmap).text.strip()

    def parse_published_date(self, episode_xml):
        datetime_string = episode_xml.find('pubDate', namespaces=self.nsmap).text.strip()
        return datetime.strptime(datetime_string, '%a, %d %b %Y %H:%M:%S %z')

    def parse_audio(self, episode_xml):
        return episode_xml.find('enclosure').get('url')

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

    def parse_author(self, episode_xml):
        return episode_xml.find('dc:creator', namespaces=self.nsmap).text.strip()
