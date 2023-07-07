
from io import BytesIO
from random import choices
import string
import qrcode
from PIL import Image, ImageDraw, ImageFont
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask
from qrcode.image.styledpil import StyledPilImage
import qrcode.image.svg
from qrcode.image.styles.moduledrawers.svg import SvgCircleDrawer


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


def generate_styled_qrcode(data):
    # Создаем QR-код
    qr = qrcode.QRCode(
        #version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        #box_size=3,
        #border=0,
    )
    qr.add_data(data)
    qr.make(fit=True)


    qr_img = qr.make_image(image_factory=StyledPilImage,
                           module_drawer=RoundedModuleDrawer(),
                            color_mask = RadialGradiantColorMask(),
                             embeded_image_path = "logo.jpg"
                           )



    # Настраиваем стилизацию QR-кода
    # Примеры настроек:
    #qr_img = qr_img.convert("RGB")  # Конвертируем в RGB, чтобы иметь возможность менять цвета
    #qr_img = qr_img.resize((300, 300))  # Изменяем размер QR-кода по необходимости
    # qr_img = apply_custom_colors(qr_img, fill_color=(0, 0, 255), back_color=(255, 255, 255))  # Настраиваем цвета

    return qr_img

def apply_custom_colors(image, fill_color, back_color):
    # Применяем настраиваемые цвета для QR-кода
    img_data = image.getdata()
    new_img_data = []
    for item in img_data:
        if item == (0, 0, 0):  # Черные элементы QR-кода
            new_img_data.append(fill_color)
        else:  # Белые элементы QR-кода
            new_img_data.append(back_color)
    image.putdata(new_img_data)
    return image

def make_info_qr(qr_img,cap1,text1,cap2,text2):
    background_color = (255, 255, 255)
    cap_color = (140, 140, 140)
    text_color = (0, 0, 0)
    width, height = 450, 600
    image = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(image)
    font_title = ImageFont.truetype('arial.ttf', size=11)
    font_text = ImageFont.truetype('arial.ttf', size=18)

    # Позиция и отступы текста
    text_x = 50
    text_y = 50
    line_spacing = 10

    # Заголовок 1
    title1 = cap1
    draw.text((text_x, text_y), title1, font=font_title, fill=cap_color)
    text_y += font_title.getsize(title1)[1] + line_spacing

    # Текст 1
    text1 = text1
    draw.text((text_x, text_y), text1, font=font_text, fill=text_color)
    text_y += font_text.getsize(text1)[1] + line_spacing * 2

    # Заголовок 2
    title2 = cap2
    draw.text((text_x, text_y), title2, font=font_title, fill=cap_color)
    text_y += font_title.getsize(title2)[1] + line_spacing

    # Текст 2
    text2 = text2
    draw.text((text_x, text_y), text2, font=font_text, fill=text_color)

    # Наложение QR-кода на изображение с текстом
    #qr_img = qr_img.resize((300, 300))  # Изменяем размер QR-кода по необходимости
    qr_position = (0 , (height - qr_img.height) )
    image.paste(qr_img, qr_position)

    return image
