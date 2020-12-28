from typing import Mapping, Sequence, Union

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


@app.route('/details')
def fetch():
    try:
        url = request.args['url']
    except KeyError:
        return redirect(url_for('index'))
    else:
        if not url:
            return redirect(url_for('index'))

    try:
        videos = get_video_info(url)
    except youtube_dl.utils.DownloadError as e:
        return render_template('error.html', error=parse_err(e))
    else:
        return render_template('video.html', videos=videos)


@app.route('/details.json')
def fetch_json():
    url = request.args['url']
    return jsonify(get_video_info(url))


# TODO: More playlist details
def get_video_info(url: str) -> Sequence[Mapping]:
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
def human_filesize(num: Union[float, int], suffix: str = 'B'):
    num = float(num)
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


@app.errorhandler(404)
def handle_404(error):
    return render_template('error.html', error=error.description), 404


@app.errorhandler(500)
def handle_500(error):
    return render_template('error.html', error=error.description), 500


@app.errorhandler(502)
def handle_502(error):
    return redirect(url_for('index'))
