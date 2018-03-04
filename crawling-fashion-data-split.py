import os
import time
import random
import shutil
from urllib.parse import urlparse
import requests
import pickle
from os.path import splitext
from fashionutils import to_file_path

def download_img(url, href, folder):
    file_path = to_file_path(url, href, folder)

    if os.path.exists(file_path):
        print('skipping %s' % file_path)
        return;

    print('download %s' % file_path)
    res = requests.get(url, stream = True)
    if res.status_code == 200:
        with open(file_path, 'wb') as f:
            res.raw.decode_content = True
            shutil.copyfileobj(res.raw, f)

    time.sleep(random.randrange(1, 5) * 0.1)


data_file = 'data.pickle'
img_folder= 'images'

data = {}
if os.path.exists(data_file):
    with open(data_file, mode='rb') as f:
        data = pickle.load(f)

items = {}
snapitems = {}

for k in data:
    its = data[k]['items']
    for i in its:
        href = i['item_href']
        snap = href.startswith('/snapitem')
        dict = snapitems if snap else items
        if href in dict:
            print("skipping %s" % href)
        else:
            dict[href] = i

with open("items.pickle", mode='wb') as f:
    print('writing to %s' % "items.pickle")
    pickle.dump(items, f)
    print(len(items))

with open("snapitems.pickle", mode='wb') as f:
    print('writing to %s' % "snapitems.pickle")
    pickle.dump(snapitems, f)
    print(len(snapitems))



for i in items:
    ii = items[i]
    item_href = ii['item_href']
    item_img_src = ii['item_img_src']

    download_img(item_img_src, item_href, img_folder+"/items/")