#!/usr/bin/env python3
"""Product extended info."""
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
import argparse
from pprint import pprint
from common import *

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("id", type=int, help="Product numeric ID, given by list.")
args = parser.parse_args()

s = get_session()
r = s.get(f'https://api.gog.com/products/{args.id}', params={
    'expand': 'downloads,expanded_dlcs'})
r.raise_for_status()
pprint(r.json())
