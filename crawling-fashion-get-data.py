import os
from bs4 import BeautifulSoup
import time
import requests
import pickle
import random


def get_brand(item):
    a = item.select('div.main p.brand a')
    if len(a)>0:
        item_brand_href = a[0].attrs['href']
        item_brand = a[0].text
    else:
        item_brand_href = None
        b = item.select('div.main p.brand')
        if len(b)>0:
            item_brand = b[0].text
        else:
            item_brand = None

    return item_brand_href, item_brand


def read_coordinate(link):
    res = requests.get("http://wear.jp" + link);
    soup = BeautifulSoup(res.content, 'html.parser')
    img = soup.select('#coordinate_img p.img img')[0]
    img_src = img.attrs['src']

    items = soup.select('#item li')
    item_list = []
    for item in items:
        item_href = item.select('div.sub a')[0].attrs['href']

        snap = item_href.startswith('/snapitem')

        item_img_src = item.select('div.sub a p.img img')[0].attrs['src']
        item_price = None if snap else item.select('div.sub a p.price')[0].text

        item_brand_href, item_brand = get_brand(item)

        item_category_href = item.select('div.main p.txt a')[0].attrs['href']
        item_category = item.select('div.main p.txt a')[0].text

        item_list.append(
            { 'item_href': item_href,
              'item_img_src': item_img_src,
              'item_price': item_price,
              'item_brand_href': item_brand_href,
              'item_brand': item_brand,
              'item_category_href': item_category_href,
              'item_category': item_category
              }
        )

    tags = soup.select('#tag li')
    tag_list=[]
    for tag in tags:
        tag_href = tag.select('a')[0].attrs['href']
        tag_text = tag.select('a')[0].text
        tag_list.append({
            'tag_href':tag_href,
            'tag':tag_text
        })

    # brands = soup.select('#use_brand li')
    brand_list = []
    # for brand in brands:
    #     brand_href = brand.select('a')[0].attrs['href']
    #     brand_text = brand.select('a')[0].text
    #     brand_list.append({
    #         'brand_href': brand_href,
    #         'brand': brand_text
    #     })

    return {
        'link': link,
        'img_src': img_src,
        'items': item_list,
        'tags' : tag_list,
        'brands' : brand_list
    }



data_file = 'data.pickle'
img_folder= 'images'

data = {}
if os.path.exists(data_file):
    with open(data_file, mode='rb') as f:
        data = pickle.load(f)

print(len(data))


page_num = 1
try:
    while True:
        url = 'http://wear.jp/coordinate/?pageno=%d' % page_num
        page_num+=1

        print(url)
        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'html.parser')
        links = soup.select('#main_list div.image a.over')
        if len(links) <= 0:
            break;

        for a in links:
            link = a.attrs['href']
            print(link);
            if link in data:
                print("skipping %s" % link)
                continue

            try:
                coord = read_coordinate(link)
                data[link] = coord

            finally:
                time.sleep(random.randrange(1, 5)*0.1)

        with open(data_file, mode='wb') as f:
            print('writing to %s' % data_file)
            pickle.dump(data, f)
            print(len(data))

except Exception as e:
    print(e)