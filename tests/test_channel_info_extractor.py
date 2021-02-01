from yt_archive.extractor import ChannelInfoExtractor

TEST_YT_URL = [
    "https://www.youtube.com/channel/UCJ04m06GHw3DUDQG6chCAUA"
]

# flake8: noqa: E501
EXPECTED_CHANNEL_INFO = [{
    "banner_image": "https://yt3.ggpht.com/8KAWGmJW1qnYHs9H3fbC1VBNjPo8iIw8WMzDd4vp49zEfmjNf7f_OayTR5CcDbT1t6ZM8NuHYKY=w2560-fcrop64=1,00005a57ffffa5a8-k-c0xffffffff-no-nd-rj",
    "avatar_image": "https://yt3.ggpht.com/ytc/AAUvwnglfb37hW7zsrx1CtBXfFnPWyWTbxYXpBCWZ5EO=s176-c-k-c0x00ffffff-no-rj",
    "description": "If you are looking for fun content as we go exploring the nooks and crannies of the automotive world, welcome aboard the official home of Times Drive on YouTube! Here you will find the performance review series - The Kranti Sambhav Review as well as DIYs, maintenance tips, car and bike buying tips, in-depth comparisons, etc. No matter if you are a motoring enthusiast or a buyer, we have something for everyone.\n\nThis is a channel from Timesnownews.com\n\nGet the latest from the world of Auto - https://t.me/timesdriveofficial",
    "title": "TIMES DRIVE",
    "channel_url": "https://www.youtube.com/channel/UCJ04m06GHw3DUDQG6chCAUA",
    "fb_profile_id": "",
    "channel_id": "UCJ04m06GHw3DUDQG6chCAUA"
}]


def test_channel_info_cli():
    """Unit test of ChannelInfoExtractor"""
    for i in range(0, len(TEST_YT_URL)):
        actual_data = ChannelInfoExtractor.for_url(TEST_YT_URL[i])._extract()
        assert actual_data == EXPECTED_CHANNEL_INFO[i]
