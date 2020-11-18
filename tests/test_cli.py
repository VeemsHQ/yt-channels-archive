from click.testing import CliRunner

from yt_archive.cli import main

MODULE = 'yt_archive.cli'


def test_cli(mocker, tmpdir):
    mock_youtube_dl = mocker.patch(f'{MODULE}.youtube_dl')
    channel_urls = [
        'https://youtube.com/channel/123',
        'https://youtube.com/c/ABC',
    ]
    runner = CliRunner()

    result = runner.invoke(main, ['--output-dir', tmpdir] + channel_urls)

    assert result.exit_code == 0
    assert result.output == ''
    assert (
        mock_youtube_dl.YoutubeDL().__enter__().download.call_count ==
        len(channel_urls)
    )
    assert mock_youtube_dl.YoutubeDL.call_args_list == [
        mocker.call(
            {
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
                'outtmpl': f'{tmpdir}/123/%(title)s.%(ext)s'
            }
        ),
        mocker.call(
            {
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
                'outtmpl': f'{tmpdir}/ABC/%(title)s.%(ext)s'
            }
        ),
        mocker.call()
    ]
