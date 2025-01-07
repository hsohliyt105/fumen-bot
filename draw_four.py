# -*- coding: utf-8 -*-

from io import BytesIO
from os.path import abspath, dirname
from typing import List, Optional, Tuple

import py_fumen
from PIL import Image, ImageDraw, ImageFont

colours = {
    "light": {
        "I": { "normal": '#41afde', "light": '#43d3ff', "clear": '#3bbcf5' },
        "T": { "normal": '#b451ac', "light": '#e56add', "clear": '#cc5fc4' },
        "S": { "normal": '#66c65c', "light": '#88ee86', "clear": '#72d467' },
        "Z": { "normal": '#ef624d', "light": '#ff9484', "clear": '#f97563' },
        "L": { "normal": '#ef9535', "light": '#ffbf60', "clear": '#f9a54b' },
        "J": { "normal": '#1983bf', "light": '#1ba6f9', "clear": '#1893de' },
        "O": { "normal": '#f7d33e', "light": '#fff952', "clear": '#f9de49' },
        "X": { "normal": '#686868', "light": '#949494', "clear": '#848484' },
        "Empty": { "normal": '#ffffff' },
        "Shadow": { "normal": '#6f6f6f1c' } # original colour is #6f6f6f17, but i changed because PIL gives errorneous results, idk why
    },
      "dark": {
        "I": { "normal": '#42afe1', "light": '#6ceaff', "clear": '#5cc7f9' },
        "T": { "normal": '#9739a2', "light": '#d958e9', "clear": '#b94bc6' },
        "S": { "normal": '#51b84d', "light": '#84f880', "clear": '#70d36d' },
        "Z": { "normal": '#eb4f65', "light": '#ff7f79', "clear": '#f96c67' },
        "L": { "normal": '#f38927', "light": '#ffba59', "clear": '#f99e4c' },
        "J": { "normal": '#1165b5', "light": '#339bff', "clear": '#2c84da' },
        "O": { "normal": '#f6d03c', "light": '#ffff7f', "clear": '#f9df6c' },
        "X": { "normal": '#868686', "light": '#dddddd', "clear": '#bdbdbd' },
        "Empty": { "normal": '#313338' },
        "Shadow": { "normal": '#09090938' }
    }
}

font = ImageFont.truetype("./font/Arial Unicode MS.ttf", 15)
comment_top_margin = 5
comment_bottom_margin = 15
comment_side_margin = 5

def get_op_positions(operation: py_fumen.Operation) -> List[List[int]]:
    piece = py_fumen.parse_piece(operation.piece_type)
    positions = py_fumen.get_pieces(piece)
    if operation.rotation.lower() == "left":
        positions = py_fumen.rotate_left(py_fumen.get_pieces(piece))
    elif operation.rotation.lower() == "right":
        positions = py_fumen.rotate_right(py_fumen.get_pieces(piece))
    elif operation.rotation.lower() == "reverse":
        positions = py_fumen.rotate_reverse(py_fumen.get_pieces(piece))
    
    for i in range(len(positions)):
        positions[i][0] += operation.x
        positions[i][1] += operation.y

    return positions

def get_max_num_rows(field: py_fumen.Field) -> int:
    num_rows = 0
    num_rows = field.string().count("\n") + 1     
    if num_rows == 1:
        for x in range(10):
            if field.at(x, 0) == "_": 
                 continue
    return num_rows

def text_wrap(text, font: ImageFont.FreeTypeFont, max_width):
    lines = []

    if font.getlength(text) <= max_width:
        return text

    for text_line in text.split("\n"):
        if font.getlength(text_line) <= max_width:
            lines.append(text_line)

        else:
            prev_i = 0
            line = ""
            for i in range(len(text_line)):
                line = text_line[prev_i:i+1]
                if font.getlength(line) > max_width:
                    lines.append(text_line[prev_i:i])
                    prev_i = i

                if i == len(text_line) - 1 :
                    lines.append(text_line[prev_i:i+1])

    wrapped_text = "\n".join(lines)

    return wrapped_text

def draw(page: py_fumen.Page, size: Tuple[int, int], tile_size: int = 20, num_rows: Optional[int] = None, transparency: bool = True, theme: str = "dark", background: str = None, display_comment: bool = False, font: ImageFont.FreeTypeFont = None) -> Image.Image:
    theme = theme.lower()
    if theme != "dark" and theme != "light":
        raise ValueError

    field = page.get_field()
    operation = page.operation
    comment = page.comment

    if operation is not None:
        positions = get_op_positions(operation)

        for position in positions:
            field.set(position[0], position[1], operation.piece_type)

    if num_rows is None:
        num_rows = get_max_num_rows(field)

    width = size[0]
    height = size[1]

    if display_comment: 
        comment = text_wrap(comment, font, width - 2 * comment_side_margin)

    if transparency:
        page_img = Image.new("RGBA", (width, height), "#FFFFFF00")
    elif background is None:
        page_img = Image.new("RGBA", (width, height), colours[theme]["Empty"]["normal"])
    else:
        page_img = Image.new("RGBA", (width, height), background)

    overlay = Image.new("RGBA", (width, height), "#FFFFFF00")
    overlay_draw = ImageDraw.Draw(overlay)
    
    for i in range(10):
        for j in range(num_rows):
            if field.at(i, j) != "_":
                overlay_draw.rectangle((
                    i * tile_size + tile_size / 4, 
                    (num_rows - j + 1) * tile_size + tile_size / 5 * 2, 
                    (i + 1) * tile_size + tile_size / 4 - 1, 
                    (num_rows - j + 2) * tile_size + tile_size / 5 * 2 - 1),
                    fill=colours[theme]["Shadow"]["normal"])

    page_img = Image.alpha_composite(page_img, overlay)

    img_draw = ImageDraw.Draw(page_img)

    for i in range(10):
        for j in range(num_rows):
            if field.at(i, j) != "_":
                img_draw.rectangle((
                    i * tile_size, 
                    (num_rows - j + 1) * tile_size - tile_size / 5, 
                    (i + 1) * tile_size - 1, 
                    (num_rows - j + 2) * tile_size - 1),
                    fill=colours[theme][field.at(i, j)]["light"])

    for i in range(10):
        for j in range(num_rows):
            clear = True
            for x in range(10):
                if field.at(x, j) == "_":
                    clear = False

            if field.at(i, j) != "_":
                if clear and (page.flags.lock is not None or page.flags.lock):
                    colour = "clear"

                else:
                    colour = "normal"

                img_draw.rectangle((
                    i * tile_size, 
                    (num_rows - j + 1) * tile_size, 
                    (i + 1) * tile_size - 1, 
                    (num_rows - j + 2) * tile_size - 1),
                    fill=colours[theme][field.at(i, j)][colour])
                
    if display_comment:
        img_draw.rectangle((
                    0, 
                    (num_rows + 3) * tile_size, 
                    width, 
                    height),
                    fill="#FFFFFF")

        img_draw.multiline_text((width / 2, (num_rows + 3) * tile_size + comment_top_margin), comment, fill="#000000", font=font, anchor="ma", align="center")

    return page_img

def draw_fumens(pages: List[py_fumen.Page], tile_size: int = 20, start: int = 0, end: Optional[int] = None, transparency: bool = True, duration: int = 500, theme: str = "dark", background: str = None, is_comment: bool = True):
    if len(pages) > 1:
        transparency = False

    theme = theme.lower()
    if theme != "dark" and theme != "light":
        raise ValueError

    if end is None:
        end = len(pages)
        
    width = 11 * tile_size
    max_num_rows = 0
    max_comment_height = 0
    display_comment = False

    temp_draw = ImageDraw.Draw(Image.new("RGB", (width, 1)))

    for x in range(start, end):
        field = pages[x].get_field()
        operation = pages[x].operation
        comment = pages[x].comment

        if operation is not None:
            positions = get_op_positions(operation)

            for position in positions:
                field.set(position[0], position[1], operation.piece_type)
                    
        max_num_rows = max(get_max_num_rows(field), max_num_rows)

        if comment is not None and comment != "" and is_comment:
            display_comment = True
            comment = text_wrap(comment, font, width - 2 * comment_side_margin)
            textbbox = temp_draw.multiline_textbbox((width / 2, 0), comment, font, anchor="ma", align="center")
            max_comment_height = max(textbbox[3] - textbbox[1], max_comment_height)

    max_num_rows = min(23, max_num_rows)

    height = (max_num_rows + 3) * tile_size

    if display_comment:
        height += max_comment_height + comment_top_margin + comment_bottom_margin

    page_imgs: List[Image.Image] = []

    if background is None:
        for x in range(start, end):
            page_imgs.append(draw(pages[x], (width, height), tile_size, max_num_rows, transparency, theme, display_comment=display_comment, font=font))

    else:
        for x in range(start, end):
            page_imgs.append(draw(pages[x], (width, height), tile_size, max_num_rows, transparency, theme, background, display_comment, font))

    if len(page_imgs) == 1:
        page_gif = BytesIO()
        page_imgs[0].save(page_gif, format="PNG")
        page_gif.seek(0)

    else:  
        page_gif = BytesIO()
        page_imgs[0].save(page_gif, format="GIF", save_all=True, append_images=page_imgs[1:], duration=duration, loop=0, disposal=2)
        page_gif.seek(0)

    return page_gif
