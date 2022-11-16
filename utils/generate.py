import io
import os
import random
import textwrap
import unicodedata
from io import BytesIO

import requests
from PIL import Image, ImageDraw, ImageFont

path = os.getcwd()

background_colors = {
  1: (255, 175, 0),
  2: (255, 94, 157),
  3: (118, 118, 254),
  4: (0, 215, 106),
  5: (221, 82, 82)
}

positions = {
    1: [(290, 20)],
    2: [(170, 20), (410, 20)],
    3: [(130, 20), (290, 20), (450, 20)],
    4: [(80, 20), (225, 20), (365, 20), (500, 20)],
    5: [(30, 20), (160, 20), (290, 20), (420, 20), (550, 20)],
    6: [(40, 20), (145, 20), (250, 20), (355, 20), (460, 20), (565, 20)]
}

position_rezise = {
    1: (120, 120),
    2: (120, 120),
    3: (120, 120),
    4: (120, 120),
    5: (120, 120),
    6: (100, 100)
}

def get_event_image(event, brothers_avatar):
    font = ImageFont.truetype(f'{path}/assets/fonts/natwooddraws.ttf', size=25)

    background = Image.new('RGB', (700, 320), background_colors[random.randint(1,5)])

    for i in range(len(brothers_avatar)):
        if brothers_avatar[i].startswith('http'):
            response = requests.get(brothers_avatar[i])

            img = Image.open(BytesIO(response.content)).convert("RGBA")
            img = img.resize(position_rezise[len(brothers_avatar)])

            background.paste(img, positions[len(brothers_avatar)][i], mask=img)

    W, H = background.size
    y_texto = 160

    draw = ImageDraw.Draw(background)

    lines = textwrap.wrap(event, width=40)

    for line in lines:
        w, h = font.getsize(line)
        draw.text(((W-w)/2, y_texto), line, font=font, fill="#000")
        y_texto += h + 2

    arr = io.BytesIO()
    background.save(arr, format='PNG')
    arr.seek(0)

    return arr
