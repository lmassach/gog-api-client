# GOG API Client
These scripts interface with [GOG](https://www.gog.com/)'s
[APIs](https://gogapidocs.readthedocs.io/).
They are not meant to be user-friendly, I am just writing this because Lutris
seems to be unable to download some extra contents of
[Hollow Knight](https://www.gog.com/game/hollow_knight) that I just bought.

## Requirements
Python 3 (probably 3.6+) with [requests](https://requests.readthedocs.io/) and
[tqdm](https://tqdm.github.io/).

## Usage
See [here](https://gogapidocs.readthedocs.io/).
 - Authenticate with `./authenticate.py`. Will save credentials in plain text in `auth.json`.
    - Use `./refresh.py` if the token has elapsed to renew it without re-authenticating.
 - Use `./list.py` to find products.
    - This will also retrieve the numeric IDs used by the following scripts.
    - See `--help` for details.
 - Use `./info.py` to get extra product details (mainly for developing).
    - See `--help` for details.
 - Use `./download.py` to download product data.
    - It will query all the available downloads for the product and its extras (DLCs, patches,
      installers, etc), then display a list and ask which you want to download.
    - See `--help` for details.

## License
Copyright 2022 Ludovico Massaccesi.
Distributed under the
[GNU General Public License, version 3](https://www.gnu.org/licenses/gpl-3.0.html)
or later (see `LICENSE` file).
