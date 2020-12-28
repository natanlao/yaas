from typing import Mapping, Sequence

from flask import Flask, jsonify, render_template, redirect, request, url_for
from jinja2 import StrictUndefined
import youtube_dl

__version__ = "0.2.0"


app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined

ydl = youtube_dl.YoutubeDL({
    'logger': app.logger,
    'no_color': True,
    'quiet': True,
    'skip_download': True
})
ydl.add_default_info_extractors()


@app.route('/')
def index():
    return render_template('_base.html')


@app.route('/video', methods=['POST'])
def fetch_redirect():
    if request.form['url']:
        return redirect(url_for('fetch', url=request.form['url']))
    else:
        return redirect(url_for('index'))


@app.route('/fetch')
def fetch():
    try:
        url = request.args['url']
    except KeyError:
        return redirect(url_for('index'))

    try:
        videos = get_video_info(url)
    except youtube_dl.utils.DownloadError as e:
        return render_template('error.html', error=parse_err(e))
    else:
        return render_template('video.html', videos=videos)


def get_video_info(url: str) -> Sequence[Mapping]:
    """
    >>> get_video_info(...)
    {}
    >>> get_video_info(...)
    """
    info = ydl.extract_info(url)
    if info.get('_type') == 'playlist':
        return info['entries']
    else:
        return [info]


def parse_err(err: youtube_dl.utils.DownloadError) -> str:
    msg = err.args[0]
    log_prefix = 'ERROR: '
    invalid_url = [
        'is not a valid URL',
        'Name or service not known',
        'URLError'
    ]
    if any(err in msg for err in invalid_url):
        return 'The provided URL is invalid.'
    elif 'Unsupported URL' in msg:
        return 'The provided URL is not supported by youtube-dl.'
    elif msg.startswith(log_prefix):
        return f'Unknown error: {msg[len(log_prefix):]}'
    else:
        return f'Unknown error: {msg!r}'



# https://stackoverflow.com/a/1094933
def human_filesize(num: int, suffix: str = 'B'):
    for unit in ('', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi'):
        if abs(num) < 1024.0:
            return f'{num:3.1f} {unit}{suffix}'
        num /= 1024.0
    return f'{num:.1f} Yi{suffix}'


app.jinja_env.filters['human_filesize'] = human_filesize


@app.context_processor
def versions() -> Mapping[str, str]:
    return {
        'youtubedl_version': youtube_dl.version.__version__,
        'yaas_version': __version__
    }


# TODO: Error handlers

