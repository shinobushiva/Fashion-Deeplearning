import os
import time
import random
import shutil
from urllib.parse import urlparse
import requests
import pickle
from os.path import splitext


def download_img(url, href, folder):
    os.makedirs(folder, exist_ok=True)

    ext = splitext(urlparse(url).path)[1]
    file_path = folder+href.replace('/', ' ').strip().replace(' ', '-')+ext

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

for k in data:
    d = data[k]
    img_href = d['link']
    img_src = d['img_src']

    items = d['items']
    for ii in items:
        item_href = ii['item_href']
        item_img_src = ii['item_img_src']

        download_img(item_img_src, item_href, img_folder+"/items/")


    download_img(img_src, img_href, img_folder+"/coordinates/")
