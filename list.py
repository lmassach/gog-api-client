#!/usr/bin/env python3
"""List products."""
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
from common import *
from common import get_session

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("search_query", help="Search string")
parser.add_argument("-u", "--user", action="store_true",
                    help="Search user-owned only.")
parser.add_argument("-a", "--all", action="store_true",
                    help="Prints all available information.")
parser.add_argument("--media-type", default='game', choices=['game', 'movie'])
args = parser.parse_args()
url = 'https://embed.gog.com/' + (
    'account/getFilteredProducts' if args.user else 'games/ajax/filtered')
media_type = int(args.media_type == 'movie') + 1 if args.user else args.media_type

s = get_session()
r = s.get(url, params={'search': args.search_query, 'mediaType': media_type})
r.raise_for_status()
data = r.json()
products = data['products']

print(f"Showing page 1 of {data['totalPages']}, {len(products)} results.")
if args.all:
    cpprint(data)
else:
    for p in products:
        print(f"{p['title']}\n    {p['url']}\n    {p['id']}")
