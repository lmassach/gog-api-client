#!/usr/bin/env python3
"""Product data download (interactive)."""
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
from collections import namedtuple
import hashlib
import os
import traceback
from urllib.parse import urlparse, unquote
from xml.etree import ElementTree
from tqdm import tqdm
from common import *

GOGFile = namedtuple('GOGFile', 'id size downlink')
GOGDownload = namedtuple('GOGDownload', 'id name total_size files')
GOGCategory = namedtuple('GOGCategory', 'name downloads')
GOGProduct = namedtuple('GOGProduct', 'id name type categories')


def read_files(data):
    for f in data:
        yield GOGFile(f['id'], f['size'], f['downlink'])


def read_downloads(data):
    for d in data:
        files = list(read_files(d['files']))
        if files:
            yield GOGDownload(d['id'], d['name'], d['total_size'], files)


def read_categories(data):
    for k, v in data.items():
        dls = list(read_downloads(v))
        if dls:
            yield GOGCategory(k, dls)


def read_product(data):
    return GOGProduct(data['id'], data.get('name', data.get('title')),
                      data['game_type'],
                      list(read_categories(data['downloads'])))


def human_readable_size(sz):
    sz = float(sz)
    for u in ['B', 'KiB', 'MiB', 'GiB', 'TiB']:
        if sz >= 1e3:
            sz /= 1e3
        else:
            break
    return f"{sz:.3g} {u}"


def md5sum(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("id", type=int, help="Product numeric ID, given by list.")
parser.add_argument("-d", default="downloads", help="Output directory, default %(default)s.")
args = parser.parse_args()

s = get_session()

print("Retrieving product information...")
r = s.get(f'https://api.gog.com/products/{args.id}', params={
    'expand': 'downloads,expanded_dlcs'})
r.raise_for_status()
data = r.json()

products = []
products.append(read_product(data))  # Main game
for dlc in data['expanded_dlcs']:  # DLCs
    products.append(read_product(dlc))

downloads = []
dirs = []
for p in products:
    print(f"{p.name} ({p.type}, {p.id})")
    for c in p.categories:
        print(f"    {c.name}")
        for d in c.downloads:
            print(f"        {FGY}{len(downloads)}{RST} {d.name}"
                  f" ({human_readable_size(d.total_size)}, {d.id})")
            downloads.append(d)
            dirs.append(os.path.join(args.d, str(p.id), c.name, str(d.id)))

while True:
    to_download = input("What should I download (yellow indices, comma separated)? ")
    try:
        to_download = [int(x.strip()) for x in to_download.split(',')]
        break
    except Exception:
        print("Invalid input.")
total_size = sum(downloads[i].total_size for i in to_download)

with tqdm(total=total_size, unit='B', unit_scale=True) as bar:
    for n, i in enumerate(to_download):
        d = downloads[i]
        p = dirs[i]
        print(f"{FGY}{n}. {d.name}{RST} in {p}")
        try:
            os.makedirs(p, exist_ok=True)
        except Exception:
            print(f"{FGR}Error: could not create directory.{RST}")
            traceback.print_exc()
            continue
        for f in d.files:
            print(f"    {f.id}")
            try:
                # Get the actual link and the link to the checksum
                r = s.get(f.downlink)
                r.raise_for_status()
                links = r.json()
                # Download the file
                r = s.get(links['downlink'], stream=True)
                r.raise_for_status()
                fn = os.path.basename(unquote(urlparse(r.url).path)) or str(f.id)
                fp = os.path.join(p, fn)
                if fn != str(f.id):
                    print(f"        {fn}")
                with open(fp, 'wb') as ofs:
                    for chunk in r.iter_content(chunk_size=1024):
                        ofs.write(chunk)
                        bar.update(len(chunk))
                # Check the checksum
                try:
                    r = s.get(links['checksum'])
                    r.raise_for_status()
                    x_root = ElementTree.fromstring(r.text)
                    fsz = int(x_root.attrib['total_size'])
                    fsz_real = os.path.getsize(fp)
                    if fsz_real != fsz:
                        print(f"{FGY}File has wrong size {fsz_real} != {fsz} (expected).{RST}")
                    else:
                        md5 = x_root.attrib["md5"].lower()
                        md5_real = md5sum(fp).lower()
                        if md5_real != md5:
                            print(f"{FGY}File has wrong MD5 {md5_real} != {md5} (expected).{RST}")
                except Exception:
                    print(f"{FGY}Warning: could not check {fn} integrity.{RST}")
                    traceback.print_exc()
            except Exception:
                print(f"{FGR}Error: could not download {f.id}.{RST}")
                traceback.print_exc()
