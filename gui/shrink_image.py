from pathlib import Path

import eel
from PIL import Image


SHRINK_TARGET_EXTENSION = (".jpg", ".png")


def calculate_shrinked_size(width, height, max_length):
    """Calculate shrinked size in proportion

    The larger of width and height should be equal to max_length.

    For exanple, width=500px, height=400px
    width : height = max_length : new_height
    i.e. new_height = max_length * height / width

    if you swap the width and the height:
    width : height = new_width : max_length
    """
    if width > height:
        new_width = max_length
        new_height = int(max_length * height / width)
    else:
        new_width = int(max_length * width / height)
        new_height = max_length
    return (new_width, new_height)


def resize_image(image_path, save_path, max_length):
    """Resize a given image so that the width and the height
    is equal or less than max_length
    """
    image = Image.open(image_path)
    width, height = image.size
    if width > max_length or height > max_length:
        shrinked_size = calculate_shrinked_size(width, height, max_length)
        resized_image = image.resize(shrinked_size, Image.BICUBIC)
        resized_image.save(save_path)


@eel.expose()
def resize(target_image_path_str):
    target_image_path = Path(target_image_path_str)
    target_paths = target_image_path.iterdir()
    # web directory == localhost:8000/
    shrinked_dir_path = Path("web/images") / target_image_path.name
    shrinked_dir_path.mkdir(exist_ok=True)

    for image_path in target_paths:
        if image_path.suffix not in SHRINK_TARGET_EXTENSION:
            continue
        save_path = shrinked_dir_path / image_path.name
        resize_image(image_path, save_path, 300)
        print(f"{image_path} is shrinked: {save_path}")


eel.init("web")
eel.start("resize.html", size=(600, 400))
