import pytest
from yt_archive.extractor import ChannelInfoExtractor


# flake8: noqa: E501
TEST_DATA = [
    ("https://www.youtube.com/channel/UCJ04m06GHw3DUDQG6chCAUA", {
        "banner_image": "https://yt3.ggpht.com/8KAWGmJW1qnYHs9H3fbC1VBNjPo8iIw8WMzDd4vp49zEfmjNf7f_OayTR5CcDbT1t6ZM8NuHYKY=w2560-fcrop64=1,00005a57ffffa5a8-k-c0xffffffff-no-nd-rj",
        "avatar_image": "https://yt3.ggpht.com/ytc/AAUvwnglfb37hW7zsrx1CtBXfFnPWyWTbxYXpBCWZ5EO=s176-c-k-c0x00ffffff-no-rj",
        "description": "If you are looking for fun content as we go exploring the nooks and crannies of the automotive world, welcome aboard the official home of Times Drive on YouTube! Here you will find the performance review series - The Kranti Sambhav Review as well as DIYs, maintenance tips, car and bike buying tips, in-depth comparisons, etc. No matter if you are a motoring enthusiast or a buyer, we have something for everyone.\n\nThis is a channel from Timesnownews.com\n\nGet the latest from the world of Auto - https://t.me/timesdriveofficial",
        "title": "TIMES DRIVE",
        "channel_url": "https://www.youtube.com/channel/UCJ04m06GHw3DUDQG6chCAUA",
        "fb_profile_id": "",
        "channel_id": "UCJ04m06GHw3DUDQG6chCAUA"
    }),
    ("https://youtube.com/c/NehaChhajalane/videos", {
        'banner_image': 'https://yt3.ggpht.com/3Yv7cJYkdTdc3TDW-92241I__XlGjl8KdgfiGJJ6SELQmdI5cVYbiH8y81-lfCiJThxEsT-GKA=w2560-fcrop64=1,00005a57ffffa5a8-k-c0xffffffff-no-nd-rj',
        'avatar_image': 'https://yt3.ggpht.com/ytc/AAUvwng0m5N0BBByyPg-L3MLWz2tXqVDGzAo8Y9GkTj_=s176-c-k-c0x00ffffff-no-rj',
        'description': '',
        'title': 'Neha Chhajalane',
        'channel_url': 'https://www.youtube.com/channel/UCeE-dVXV2DL31ZYMI-GjH4w',
        'fb_profile_id': '',
        'channel_id': 'UCeE-dVXV2DL31ZYMI-GjH4w'
    })
]


@pytest.mark.parametrize("url,expected", TEST_DATA)
def test_channel_info_cli(url, expected):
    """Unit test of ChannelInfoExtractor"""
    assert ChannelInfoExtractor.for_url(
           url)._extract() == expected
