from io import BytesIO

from PIL import ExifTags, Image, ImageDraw, ImageFont


def watermark(image_bytes):
    image_in_memory = BytesIO(initial_bytes=image_bytes)
    output_img_in_memory = BytesIO()
    img = Image.open(image_in_memory).convert('RGBA')
    rotated_img = rotate_image(img)
    txt_layer = Image.new('RGBA', rotated_img.size, (255, 255, 255, 0))

    text = 'Dating App'
    font = ImageFont.truetype('arial.ttf', 27)
    draw = ImageDraw.Draw(txt_layer)

    draw = place_text(draw, rotated_img.size, text, font, 3, 10)
    draw = place_text(draw, rotated_img.size, text, font, 2, 3)

    watermarked = Image.alpha_composite(rotated_img, txt_layer)
    watermarked.save(output_img_in_memory, format='png')
    return output_img_in_memory


def rotate_image(image):
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = image.getexif()
        if exif[orientation] == 3:
            rotated = image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            rotated = image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            rotated = image.rotate(90, expand=True)
        return rotated
    except (AttributeError, KeyError, IndexError):
        return image


def place_text(draw, img_size, text, font, row_column_num, divider):
    width, height = img_size
    left_lim = width // divider
    right_lim = width - width // divider
    bottom_lim = height // divider
    top_lim = height - height // divider
    text_width, text_height = draw.textsize(text, font)
    step_horizontal = (right_lim - left_lim) // (row_column_num - 1)
    step_vertical = (top_lim - bottom_lim) // (row_column_num - 1)
    for coord_x in range(left_lim, right_lim + 1, step_horizontal):
        for coord_y in range(bottom_lim, top_lim + 1, step_vertical):
            corrected_x = coord_x - text_width // 2
            corrected_y = coord_y - text_height // 2
            draw.text(
                (corrected_x, corrected_y),
                text,
                fill=(255, 255, 255, 100),
                font=font)
    return draw
