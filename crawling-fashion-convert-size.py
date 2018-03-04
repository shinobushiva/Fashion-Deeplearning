import pickle
from fashionutils import to_file_path, resize
from PIL import Image
import os

data_file = 'items.pickle'
img_folder = 'images'
out_folder = 'images-299'

target = '/items/'

attr_src = 'item_img_src'
attr_href = 'item_href'

items = {}
if os.path.exists(data_file):
    with open(data_file, mode='rb') as f:
        items = pickle.load(f)

for k in items:
    item = items[k]
    # print(item)
    path = to_file_path(item[attr_src], item[attr_href], img_folder+target)

    if not os.path.exists(path):
        continue

    fp = to_file_path(item[attr_src], item[attr_href], out_folder + target)
    if os.path.exists(fp):
        continue

    print(fp)

    image = Image.open(path)
    size = (299, 299)
    resized = resize(image, size)

    resized.save(fp)

