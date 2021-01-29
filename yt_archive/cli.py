import os
import re
import json
from copy import deepcopy
import urllib.request
from functools import partial
from pathlib import Path
from multiprocessing import Pool
from .extractor import ChannelInfoExtractor

import youtube_dl
import click

REGEX_CHANNEL_ID = re.compile(
    r'.+.com/(c|channel)/(?P<channel_id>[a-z0-9_-]+).*', re.IGNORECASE
)

YDL_OPTS = {
    'format': 'bestvideo+bestaudio',
    'retries': 10,
    'continue': True,
    'writeinfojson': True,
    'writedescription': True,
    'writethumbnail': True,
    'writeannotations': True,
    'allsubs': True,
    'ignoreerrors': True,
    'addmetadata': True,
    'outtmpl': '%(title)s.%(ext)s',
}

CHANNEL_INFO_OPTS = {
    'banner_out': '{}/banner.jpg',
    'avatar_out': '{}/avatar.jpg',
    'description': '{}/description.txt',
    'info': '{}/info.json'
}


def _download_channel_info(channel_url, out_dir):
    channel_info = ChannelInfoExtractor.for_url(channel_url)._extract()
    channel_id = channel_info['channel_id']
    out_path_map = {
        key: value.format(out_dir)
        for key, value in CHANNEL_INFO_OPTS.items()
    }
    # save banner image to disk
    urllib.request.urlretrieve(channel_info['banner_image'],
                               out_path_map['banner_out'])
    # save avatar image to disk
    urllib.request.urlretrieve(channel_info['avatar_image'],
                               out_path_map['avatar_out'])
    # save description to disk
    with open(out_path_map['description'], 'w') as fs:
        fs.write(channel_info['description'])
    # save description to disk
    with open(out_path_map['info'], 'w') as fs:
        fs.write(json.dumps(channel_info, indent=4))


def make_dir(_dir):
    try:
        os.mkdir(_dir)
    except FileExistsError:
        pass


def _download_channel(channel_url, output_dir):
    opts = deepcopy(YDL_OPTS)
    opts['download_archive'] = str(Path(output_dir) / 'download_archive.txt')
    folder_name = (
        REGEX_CHANNEL_ID.search(channel_url).groupdict()['channel_id']
    )
    opts['outtmpl'] = f'{output_dir}/{folder_name}/{opts["outtmpl"]}'
    out_dir = f'{output_dir}/{folder_name}'
    # download channel info using web scrapper
    make_dir(out_dir)
    _download_channel_info(channel_url, out_dir)
    with youtube_dl.YoutubeDL(opts) as ydl:
        ydl.download([channel_url])


@click.command()
@click.option('--output-dir')
@click.argument('channel_urls', nargs=-1)
def main(output_dir, channel_urls):
    try:
        os.mkdir(output_dir)
    except FileExistsError:
        pass
    num_proc = min(2, len(channel_urls))
    pool = Pool(num_proc)
    download = partial(_download_channel, output_dir=output_dir)
    for _ in pool.map(download, channel_urls):
        pass


if __name__ == '__main__':
    main()
