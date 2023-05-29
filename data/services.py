from PIL import Image
from io import BytesIO
from random import choices
import string

def makeThumb(image):
    fill_color = '#fff'
    base_image = Image.open(image)
    blob = BytesIO()
    if base_image.mode in ('RGBA', 'LA'):
        background = Image.new(base_image.mode[:-1], base_image.size, fill_color)
        background.paste(base_image, base_image.split()[-1])
        base_image = background

    width, height = base_image.size
    transparent = Image.new('RGB', (width, height), (0, 0, 0, 0))
    transparent.paste(base_image, (0, 0))
    transparent.thumbnail((150, 300), Image.ANTIALIAS)
    transparent.save(blob, 'png', quality=100, optimize=True)
    return blob

def create_random_string(digits=False, num=4):
    if not digits:
        random_string = ''.join(choices(string.ascii_uppercase + string.digits, k=num))
    else:
        random_string = ''.join(choices(string.digits, k=num))
    return random_string