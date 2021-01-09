# yt-channels-archive

A CLI tool to backup multiple YouTube channels along with their associated metadata and thumbnails. In the highest available quality.

## Installation

```bash
pip install yt-channels-archive
```

## Usage

```bash
yt_archive --output-dir ./backup https://www.youtube.com/channel/UC7edjYPNhTm5LYJMT7UMt0Q/videos https://www.youtube.com/channel/UC6cMYsKMx6XicFcFm7mTsmA
```

You may notice this will also place a file in your backup folder called 'download_archive.txt'.

Don't delete that as it's used to ensure videos are only downloaded once (if you remove it and re-run the above command existing videos will be re-downloaded).

## Running the tests

```bash
pip install -r requirements-dev.txt
pytest tests
```

## Running the linter

```bash
pip install -r requirements-dev.txt
flake8
```
