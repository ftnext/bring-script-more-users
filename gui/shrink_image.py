from pathlib import Path
import re
import sys

import eel
from PIL import Image


SHRINK_TARGET_EXTENSION = (".jpg", ".jpeg", ".png")


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

    Return a result as bool:
    - When the image need to resize and succeed, return True
    - When the image does not need to resize, return False
    """
    image = Image.open(image_path)
    width, height = image.size
    if width > max_length or height > max_length:
        shrinked_size = calculate_shrinked_size(width, height, max_length)
        resized_image = image.resize(shrinked_size, Image.BICUBIC)
        resized_image.save(save_path)
        return True
    return False


def existing_path(path_str):
    path = Path(path_str)
    if not path.exists():
        print(f"{path_str}: No such file or directory")
        return None
    return path


@eel.expose
def resize(target_image_path_str, max_length):
    target_image_path = existing_path(target_image_path_str)
    if not target_image_path:
        return None

    if target_image_path.is_file():
        target_paths = [target_image_path]
        # web directory == localhost:8000/
        shrinked_dir_path = Path("web/images")
    else:
        target_paths = target_image_path.iterdir()
        shrinked_dir_path = Path("web/images") / target_image_path.name
    # When bundled by PyInstaller
    if getattr(sys, "frozen", False):
        shrinked_dir_path = sys._MEIPASS / shrinked_dir_path
    shrinked_dir_path.mkdir(parents=True, exist_ok=True)

    save_paths = []
    for image_path in target_paths:
        if image_path.suffix not in SHRINK_TARGET_EXTENSION:
            continue
        save_path = shrinked_dir_path / image_path.name
        has_resized = resize_image(image_path, save_path, max_length)
        if has_resized:
            print(f"{image_path} is shrinked: {save_path}")
            # To specify image path under web dir
            # as src attribute of img element
            if getattr(sys, "frozen", False):
                save_paths.append(
                    re.sub(f"^{sys._MEIPASS}/web/", "", str(save_path))
                )
            else:
                save_paths.append(re.sub(r"^web/", "", str(save_path)))
    return save_paths


eel.init("web")
eel.start("resize.html", size=(600, 400))
