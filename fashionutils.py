from urllib.parse import urlparse
import os
from os.path import splitext
from PIL import Image

def to_file_path(url, href, folder):

    os.makedirs(folder, exist_ok=True)

    ext = splitext(urlparse(url).path)[1]
    file_path = folder+href.replace('/', ' ').strip().replace(' ', '-')+ext

    return file_path

def resize(image, size):
    image.thumbnail(size, Image.ANTIALIAS)
    image = image.resize(size, Image.ANTIALIAS)
    # print(image.size)

    background = Image.new('RGB', size, (255, 255, 255, 0))
    background.paste(
        image, (int((size[0] - image.size[0]) / 2), int((size[1] - image.size[1]) / 2))
    )

    return background