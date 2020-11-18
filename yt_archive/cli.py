import os
import re
from copy import deepcopy

import youtube_dl
import click

REGEX_CHANNEL_ID = re.compile(
    r'.+.com/(c|channel)/(?P<channel_id>[a-z0-9_-]+).*', re.IGNORECASE
)

YDL_OPTS = {
    'format': 'best',
    'retries': 4,
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


@click.command()
@click.option('--output-dir')
@click.argument('channel_urls', nargs=-1)
def main(output_dir, channel_urls):
    try:
        os.mkdir(output_dir)
    except FileExistsError:
        pass

    for channel_url in channel_urls:
        opts = deepcopy(YDL_OPTS)
        folder_name = (
            REGEX_CHANNEL_ID.search(channel_url).groupdict()['channel_id']
        )
        opts['outtmpl'] = f'{output_dir}/{folder_name}/{opts["outtmpl"]}'
        with youtube_dl.YoutubeDL(opts) as ydl:
            ydl.download([channel_url])


if __name__ == '__main__':
    main()
