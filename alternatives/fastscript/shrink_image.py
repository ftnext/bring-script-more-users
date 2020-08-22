from argparse import ArgumentTypeError
from pathlib import Path

from fastscript import call_parse, Param
from PIL import Image


SHRINK_TARGET_EXTENSION = (".jpg", ".jpeg", ".png")


def calculate_shrinked_size(width, height, max_length):
    if width > height:
        new_width = max_length
        new_height = int(max_length * height / width)
    else:
        new_width = int(max_length * width / height)
        new_height = max_length
    return (new_width, new_height)


def resize_image(image_path, save_path, max_length):
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
        message = f"{path_str}: No such file or directory"
        raise ArgumentTypeError(message)
    return path


@call_parse
def main(
    target_image_path: Param("Path of target image", existing_path),
    max_length: Param(
        "Size of square, shrinked image will fit", type=int
    ) = 300,
):
    # Enable to pass not only a directory path but also a file path
    if target_image_path.is_file():
        target_paths = [target_image_path]
        shrinked_dir_path = Path("images")
    else:
        target_paths = target_image_path.iterdir()
        shrinked_dir_path = Path("images") / target_image_path.name
    shrinked_dir_path.mkdir(parents=True, exist_ok=True)

    for image_path in target_paths:
        if image_path.suffix not in SHRINK_TARGET_EXTENSION:
            continue
        save_path = shrinked_dir_path / image_path.name
        resize_image(image_path, save_path, max_length)
        print(f"{image_path} is shrinked: {save_path}")
