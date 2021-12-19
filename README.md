# yaas

"youtube-dl as a service". Lightweight wrapper around
[yt-dlp/yt-dlp](https://github.com/yt-dlp/yt-dlp) written using Starlette.
Check out the [live demo](https://yaas.natan.la).

I wrote this around 2014 for one of my HS teachers who wanted a better,
less-sketchy way to download YouTube videos. Some of my friends and family have
ended up using it with some regularity over the years, so I keep it up-to-date.

## Usage

### Development

```
pip install -r requirements.txt
pip install -r requirements.dev.txt
uvicorn yaas:app --reload
```

```
make test
```

### Production

```
docker build . -t yaas
docker run -p 80:80 yaas
```

