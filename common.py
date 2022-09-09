"""Common data and functions."""
# Copyright 2022 Ludovico Massaccesi
#
# This file is part of gog-api-client.
#
# gog-api-client is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
#
# gog-api-client is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with gog-api-client. If not, see <https://www.gnu.org/licenses/>.
import os
import pprint

__all__ = [
    'FGR', 'FGY', 'FGC', 'RST', 'GCA_DIR', 'AUTH_FILE', 'CLIENT_ID',
    'CLIENT_SECRET', 'REDIRECT_URI', 'cpprint']

FGR = '\x1b[31m'
FGY = '\x1b[33m'
FGC = '\x1b[36m'
RST = '\x1b[0m'

GCA_DIR = os.path.dirname(os.path.abspath(__file__))
AUTH_FILE = os.path.join(GCA_DIR, 'auth.json')

# From the docs
CLIENT_ID = 46899977096215655
CLIENT_SECRET = '9d85c43b1482497dbbce61f6e4aa173a433796eeae2ca8c5f6129f2dc4de46d9'
REDIRECT_URI = 'https://embed.gog.com/on_login_success?origin=client'


def cpprint(*args, color=FGC, **kwargs):
    print(color, end='')
    pprint.pprint(*args, **kwargs)
    print(RST, end='')
