# ascii_image.py

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ASCII_CHARS = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']

def _map_pixels_to_ascii(image: Image.Image, range_width: int = 25) -> str:
    pixels = np.array(image)
    return "".join(
        ASCII_CHARS[pixel // range_width]
        for row in pixels for pixel in row
    )

def image_to_ascii(input_path: str, width: int = 100) -> str:
    img = Image.open(input_path).convert('L')
    orig_w, orig_h = img.size
    new_h = int((orig_h / orig_w) * width * 0.55)
    img = img.resize((width, new_h))
    ascii_str = _map_pixels_to_ascii(img)
    return "\n".join(
        ascii_str[i:i+width]
        for i in range(0, len(ascii_str), width)
    )

def image_to_ascii_from_pil(image: Image.Image, width: int = 100) -> str:
    img = image.convert('L')
    orig_w, orig_h = img.size
    new_h = int((orig_h / orig_w) * width * 0.55)
    img = img.resize((width, new_h))
    ascii_str = _map_pixels_to_ascii(img)
    return "\n".join(
        ascii_str[i:i+width]
        for i in range(0, len(ascii_str), width)
    )

def ascii_to_image(
    ascii_str: str,
    font_path: str = None,
    font_size: int = 12,
    bg_color: str = "white",
    fg_color: str = "black"
) -> Image.Image:
    lines = ascii_str.splitlines()
    if font_path:
        font = ImageFont.truetype(font_path, font_size)
    else:
        font = ImageFont.load_default()
    dummy = Image.new('RGB', (1, 1))
    draw = ImageDraw.Draw(dummy)
    widths, heights = [], []
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        widths.append(bbox[2] - bbox[0])
        heights.append(bbox[3] - bbox[1])
    max_w = max(widths)
    line_h = max(heights)
    img_h = line_h * len(lines)
    img = Image.new('RGB', (max_w, img_h), color=bg_color)
    draw = ImageDraw.Draw(img)
    y = 0
    for line in lines:
        draw.text((0, y), line, font=font, fill=fg_color)
        y += line_h
    return img

