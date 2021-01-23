import os
import re
from copy import deepcopy
from functools import partial
from pathlib import Path
from multiprocessing import Pool

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


def _download_channel(channel_url, output_dir):
    opts = deepcopy(YDL_OPTS)
    opts['download_archive'] = str(Path(output_dir) / 'download_archive.txt')
    folder_name = (
        REGEX_CHANNEL_ID.search(channel_url).groupdict()['channel_id']
    )
    opts['outtmpl'] = f'{output_dir}/{folder_name}/{opts["outtmpl"]}'
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
