#!/usr/bin/env python3
"""Refresh token after authenticating."""
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
import json
import os
from pprint import pprint
import requests

FGR = '\x1b[31m'
FGY = '\x1b[33m'
RST = '\x1b[0m'

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_FILE = os.path.join(SCRIPT_DIR, 'auth.json')

# From the docs
CLIENT_ID = 46899977096215655
CLIENT_SECRET = '9d85c43b1482497dbbce61f6e4aa173a433796eeae2ca8c5f6129f2dc4de46d9'

print("Reading old token...")
with open(OUT_FILE) as ifs:
    data = json.load(ifs)
pprint(data)

print("Renewing token...")
s = requests.Session()
try:
    r = s.get('https://auth.gog.com/token', params={
        'client_id': str(CLIENT_ID),
        'client_secret': CLIENT_SECRET,
        'grant_type': 'refresh_token',
        'refresh_token': data['refresh_token']})
    r.raise_for_status()
    data = r.json()
    pprint(data)
except Exception:
    print(f"{FGR}Error happened, launching debugger...{RST}")
    import traceback; traceback.print_exc()
    import pdb; pdb.set_trace()

try:
    if os.path.isfile(OUT_FILE):
        if os.path.isfile(OUT_FILE + ".bak"):
            os.remove(OUT_FILE + ".bak")
        os.rename(OUT_FILE, OUT_FILE + ".bak")
except Exception:
    print(f"{FGY}Could not backup the previous auth.{RST}")

print("Writing data...")
with open(OUT_FILE, 'w') as ofs:
    json.dump(data, ofs)
print(f"{OUT_FILE} written.")
