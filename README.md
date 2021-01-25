# yaas

"youtube-dl as a service". Lightweight wrapper around
[rg3/youtube-dl](https://github.com/rg3/youtube-dl) written in Flask.
Check out the [Live demo](https://yaas.natan.la).

I wrote this around 2014 for one of my HS teachers who wanted a better,
less-sketchy way to download YouTube videos. Some of my friends and family have
ended up using it with some regularity over the years, so I keep it up-to-date.

## Parity with youtube-dl

This repository is configured with Dependabot to streamline the process of
keeping up with youtube-dl's release cycle, which evolves rapidly. Dependabot
PRs for youtube-dl are merged automatically once tests pass.


## Usage

### Development

```console
$ pip install -r requirements.txt
$ FLASK_ENV=development FLASK_APP=yaas.py flask run
```

```console
$ make test
```

### Production

```console
$ docker build . -t yaas
$ docker run -p 80:80 yaas
```

