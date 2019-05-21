# -*- coding: utf-8 -*-
import functools
import os

from flask import flash, Flask, render_template, redirect, request, url_for
import youtube_dl

__version__ = "0.1.0"

app = Flask(__name__)
app.secret_key = os.urandom(24)  # dirty
app.jinja_env.globals.update({
    'youtubedl_version': youtube_dl.version.__version__,
    'yaas_version': __version__
})
ydl = youtube_dl.YoutubeDL({'skip_download': True})
ydl.add_default_info_extractors()


@app.route('/')
def serve_index():
    return render_template("index.html")


@app.route("/video", methods=['POST'])
def get_video():
    try:
        url = get_video_info(request.form['url'])
        assert url
    except youtube_dl.utils.DownloadError as e:
        if "not a valid URL" in str(e):
            flash("The provided URL is not valid.")
        elif "Unsupported URL" in str(e):
            flash("The provided URL is not supported.")
        return redirect(url_for('serve_index'))
    except:
        flash("There was an error.")
        return redirect(url_for('serve_index'))
    return redirect(url)


@functools.lru_cache(maxsize=None)
def get_video_info(url):
    return ydl.extract_info(url)['url']


if __name__ == "__main__":
    app.run(debug=True)
