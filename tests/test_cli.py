from multiprocessing.dummy import Pool

import pytest
from click.testing import CliRunner

from yt_archive.cli import main

MODULE = 'yt_archive.cli'


@pytest.fixture(autouse=True)
def replace_process_pool_with_thread(mocker):
    mocker.patch(f'{MODULE}.Pool', Pool)


@pytest.fixture(autouse=True)
def replace_download_with_mock(mocker):
    mocker.patch(f"{MODULE}._download_channel_info", return_value=None)


def test_cli(mocker, tmpdir):
    mock_youtube_dl = mocker.patch(f'{MODULE}.youtube_dl')
    channel_urls = [
        'https://youtube.com/channel/123',
        'https://youtube.com/c/ABC',
    ]

    result = CliRunner().invoke(main, ['--output-dir', tmpdir] + channel_urls)

    assert result.exit_code == 0
    assert result.output == ''
    assert mock_youtube_dl.YoutubeDL().__enter__().download.call_count == len(
        channel_urls
    )
    assert mock_youtube_dl.YoutubeDL.call_args_list == [
        mocker.call(
            {
                'addmetadata': True,
                'allsubs': True,
                'continue': True,
                'download_archive': f'{tmpdir}/download_archive.txt',
                'format': 'bestvideo+bestaudio',
                'ignoreerrors': True,
                'outtmpl': f'{tmpdir}/123/%(title)s.%(ext)s',
                'retries': 10,
                'writeannotations': True,
                'writedescription': True,
                'writeinfojson': True,
                'writethumbnail': True,
            }
        ),
        mocker.call(
            {
                'addmetadata': True,
                'allsubs': True,
                'continue': True,
                'download_archive': f'{tmpdir}/download_archive.txt',
                'format': 'bestvideo+bestaudio',
                'ignoreerrors': True,
                'outtmpl': f'{tmpdir}/ABC/%(title)s.%(ext)s',
                'retries': 10,
                'writeannotations': True,
                'writedescription': True,
                'writeinfojson': True,
                'writethumbnail': True,
            }
        ),
        mocker.call(),
    ]
