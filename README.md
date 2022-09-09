# GOG API Client
These scripts interface with [GOG](https://www.gog.com/)'s
[APIs](https://gogapidocs.readthedocs.io/).
They are not meant to be user-friendly, I am just writing this because Lutris
seems to be unable to download some extra contents of
[Hollow Knight](https://www.gog.com/game/hollow_knight) that I just bought.

## Requirements
Python 3 (probably 3.6+) with [requests](https://requests.readthedocs.io/).

## Usage
See [here](https://gogapidocs.readthedocs.io/).
 - Authenticate with `./authenticate.py`. Will save credentials in plain text in `auth.json`.
    - Use `./refresh.py` if the token has elapsed to renew it without re-authenticating.

## License
Copyright 2022 Ludovico Massaccesi.
Distributed under the
[GNU General Public License, version 3](https://www.gnu.org/licenses/gpl-3.0.html)
or later (see `LICENSE` file).
