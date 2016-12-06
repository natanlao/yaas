# -*- coding: utf-8 -*-
from flask import flash, Flask, render_template, redirect, request, url_for
import os
from werkzeug.contrib.cache import SimpleCache
import youtube_dl

__version__ = "0.1.0"

app = Flask(__name__)
# dirty
app.secret_key = os.urandom(24)
app.jinja_env.globals.update({
    'youtubedl_version': youtube_dl.version.__version__,
    'yaas_version': __version__
})

ydl_options = {
    'skip_download': True,
    'format': 'bestaudio/best'
}

ydl = youtube_dl.YoutubeDL(ydl_options)
ydl.add_default_info_extractors()

cache = SimpleCache()


@app.route('/')
def serve_index():
    return render_template("index.html")


@app.route("/video", methods=['POST'])
def get_video():
    try:
        url = get_video_info(request.form['url'])
    except Exception as e:
        if isinstance(e, youtube_dl.utils.DownloadError):
            if "not a valid URL" in e.message:
                flash("The provided URL is not valid.")
            elif "Unsupported URL" in e.message:
                flash("The provided URL is not supported.")
        else:
            flash("There was an error.")

        return redirect(url_for("serve_index"))

    if not url:
        flash("There was an error.")
        return redirect(url_for("serve_index"))

    return redirect(url)


def get_video_info(url):
    rv = cache.get(url)

    if rv is None:
        rv = ydl.extract_info(url)['url']
        cache.set(url, rv, timeout=60 * 60 * 24)

    return rv


if __name__ == "__main__":
    app.run(debug=True)
