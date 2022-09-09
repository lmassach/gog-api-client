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
import requests
from common import *

print("Reading old token...")
with open(AUTH_FILE) as ifs:
    data = json.load(ifs)
cpprint(data)

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
    cpprint(data)
except Exception:
    print(f"{FGR}Error happened, launching debugger...{RST}")
    import traceback; traceback.print_exc()
    import pdb; pdb.set_trace()

try:
    if os.path.isfile(AUTH_FILE):
        if os.path.isfile(AUTH_FILE + ".bak"):
            os.remove(AUTH_FILE + ".bak")
        os.rename(AUTH_FILE, AUTH_FILE + ".bak")
except Exception:
    print(f"{FGY}Could not backup the previous auth.{RST}")

print("Writing data...")
with open(AUTH_FILE, 'w') as ofs:
    json.dump(data, ofs)
print(f"{AUTH_FILE} written.")
