# yaas

"youtube-dl as a service". Lightweight wrapper around
[rg3/youtube-dl](https://github.com/rg3/youtube-dl) written in Flask.
Check out the [Live demo](https://yaas.natan.la).

I wrote this around 2014 for one of my HS teachers who wanted a better,
less-sketchy way to download YouTube videos. Some of my friends and family have
ended up using it with some regularity over the years, so I keep it up-to-date.

## Parity with youtube-dl

Given the breadth of services it supports, youtube-dl's functionality evolves
rapidly. It doesn't appear to provide any compatibility guarantees for its API,
nor does it use semantic versioning (which makes sense).

This repository is configured with Dependabot and some basic tests. When a new
version of youtube-dl is released, Dependabot opens a pull request which is
automatically merged if tests pass. This minimizes the work I need to do to keep
yaas working.


## Usage

```console
$ pip install -r requirements.txt
$ FLASK_ENV=development FLASK_APP=yaas.py flask run
```

