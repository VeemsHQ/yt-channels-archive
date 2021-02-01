import json
import re
from urllib.parse import urlparse
import attr
import requests
from bs4 import BeautifulSoup


class ChannelInfoExtractorException(Exception):
    def __init__(self, message=None, error=None):
        self.message = message
        self.error = error


@attr.s
class ChannelInfo(object):
    channel_id = attr.ib()
    banner_image = attr.ib()
    avatar_image = attr.ib()
    description = attr.ib()
    title = attr.ib()
    channel_url = attr.ib()
    fb_profile_id = attr.ib()
    channel_id = attr.ib()


@attr.s
class YTExtractor(object):
    """You Tube Channel extractor"""

    yt_url = attr.ib()

    def _fetch_url_content(self):
        response = requests.get(self.yt_url)
        if response.status_code != 200:
            raise(ChannelInfoExtractorException('Requested Url not found'))
        return response.content

    def _get_yt_json(self):
        yt_json = {}
        soup = BeautifulSoup(self._fetch_url_content(), 'html5lib')
        for script in soup.body.find_all('script', recursive=False):
            _text = script.get_text()
            if re.match(r'var\s+ytInitialData\s+=\s+', _text):
                yt_info = re.split(r'var\s+ytInitialData\s+=\s+', _text)[-1]
                yt_info = ((yt_info and len(yt_info) > 1
                           and yt_info[: len(yt_info) - 1]) or '')
                yt_json = json.loads(yt_info)
        return yt_json

    def _parse(self):
        yt_json = self._get_yt_json()
        img_dict = (yt_json.get('header', {})
                    .get('c4TabbedHeaderRenderer', {}))
        avatar_list = img_dict.get('avatar', {}).get('thumbnails', [])
        banner_list = img_dict.get('banner', {}).get('thumbnails', [])
        info_dict = (yt_json.get('metadata', {})
                     .get('channelMetadataRenderer', {}))
        return ChannelInfo(
            avatar_image=((avatar_list[-1] or {}).get('url')
                          if len(avatar_list) > 0 else ''),
            banner_image=((banner_list[-1] or {}).get('url')
                          if len(banner_list) > 0 else ''),
            title=info_dict.get('title', ''),
            description=info_dict.get('description', ''),
            channel_url=info_dict.get('channelUrl', ''),
            fb_profile_id=info_dict.get('facebookProfileId', ''),
            channel_id=img_dict.get('channelId', '')
        )


@attr.s
class ChannelInfoExtractor(object):
    """ChannelInfoExtractor of a channel"""

    url = attr.ib()
    cl_extractor = attr.ib(default=YTExtractor(url))

    @staticmethod
    def _get_extractor(url):
        # TODO Later Added for other social media sites too
        domain_extractor_map = {
            'www.youtube.com': YTExtractor(url)
        }
        return domain_extractor_map.get(urlparse(url).netloc, YTExtractor(url))

    @classmethod
    def for_url(cls, url):
        return cls(
            url=url,
            cl_extractor=ChannelInfoExtractor._get_extractor(url))

    def _extract(self):
        return attr.asdict(self.cl_extractor._parse())
