from jinja2 import StrictUndefined
from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import (
    JSONResponse,
    PlainTextResponse,
    Response,
    RedirectResponse,
)
from starlette.templating import Jinja2Templates
import yt_dlp
import yt_dlp.version

__version__ = "1.1.0"


# https://stackoverflow.com/a/1094933
def human_filesize(num: float | int, suffix: str = "B") -> str:
    num = float(num)
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < 1024.0:
            return f"{num:3.1f} {unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f} Yi{suffix}"


def print_filesize(video: dict) -> str:
    filesize = video.get("filesize", video.get("filesize_approx"))
    return f"({human_filesize(filesize)})" if filesize else ""


def handle_http_exception(request: Request, exc: HTTPException) -> Response:
    context = {"error": f"{exc.detail} (HTTP {exc.status_code})", "request": request}
    return templates.TemplateResponse("error.html", context)


ydl = yt_dlp.YoutubeDL({"no_color": True, "quiet": True, "skip_download": True})
ydl.add_default_info_extractors()

templates = Jinja2Templates(directory="templates")
templates.env.undefined = StrictUndefined
templates.env.filters["print_filesize"] = print_filesize
templates.env.globals.update(
    {
        "youtubedl_version": yt_dlp.version.__version__,
        "yaas_version": __version__,
    }
)
exception_handlers = {HTTPException: handle_http_exception}
app = Starlette(exception_handlers=exception_handlers)  # type: ignore


@app.route("/")
@app.route("/index.html")  # propriety
async def index(request: Request) -> Response:
    return templates.TemplateResponse("_base.html", {"request": request})


@app.route("/details")
async def fetch(request: Request) -> Response:
    try:
        url = request.query_params["url"]
    except KeyError:
        return RedirectResponse(url=request.url_for("index"))
    else:
        if not url:
            return RedirectResponse(url=request.url_for("index"))

    try:
        videos = get_video_info(url)
    except yt_dlp.utils.DownloadError as e:
        # A handled youtube-dl error is still an HTTP 200 from us
        return templates.TemplateResponse(
            "error.html", {"error": parse_err(e), "request": request}
        )
    except NotImplementedError as exc:
        return templates.TemplateResponse(
            "error.html", {"error": str(exc), "request": request}
        )
    else:
        return templates.TemplateResponse(
            "video.html", {"videos": videos, "request": request}
        )


@app.route("/details.json")
def fetch_json(request: Request) -> Response:
    url = request.query_params["url"]
    return JSONResponse(get_video_info(url))


@app.route("/robots.txt")
def robots_txt(request: Request) -> Response:
    # Prevent indexing of any path except index
    robots_txt = (
        "User-Agent: *",
        "Allow: /index.html",
        "Allow: /$",  # nonstandard syntax
        "Disallow: /",
    )
    return PlainTextResponse("\n".join(robots_txt))


# TODO: More playlist details
def get_video_info(url: str) -> list[dict]:
    info = ydl.extract_info(url)
    # yt_dlp.extractors.common.InfoExtractor says we should assume _type
    # is 'video' if it is missing.
    media_type = info.get("_type", "video")
    if media_type == "video":
        return [info]
    elif media_type in ("playlist", "multi_video"):
        return info["entries"]
    else:
        raise NotImplementedError(
            f"Media type {info['_type']} is supported by youtube-dl, but not by yaas."
        )


def parse_err(err: yt_dlp.utils.DownloadError) -> str:
    msg = err.args[0]
    log_prefix = "ERROR: "
    invalid_url = ["is not a valid URL", "Name or service not known", "URLError"]
    if any(err in msg for err in invalid_url):
        return "The provided URL is invalid."
    elif "Unsupported URL" in msg:
        return "The provided URL is not supported by youtube-dl."
    elif msg.startswith(log_prefix):
        return f"Unknown error: {msg[len(log_prefix) :]}"
    else:
        return f"Unknown error: {msg!r}"
