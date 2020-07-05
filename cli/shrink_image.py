"""Shrink images in `../target_images/img_pyconjp`

- Images with a width or height greater than 300px are to be resized
- Shrinked images are placed in directory `images/img_pyconjp`
"""

from argparse import ArgumentParser, ArgumentTypeError
from pathlib import Path

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


def existing_path(path_str):
    path = Path(path_str)
    if not path.exists():
        message = f"{path_str}: No such file or directory"
        raise ArgumentTypeError(message)
    return path


if __name__ == "__main__":
    # code for CLI
    parser = ArgumentParser()
    parser.add_argument("image_dir_path", type=existing_path)
    parser.add_argument("--max_length", default=300, type=int)
    args = parser.parse_args()

    image_dir_path = args.image_dir_path
    shrinked_dir_path = Path("images") / image_dir_path.name
    shrinked_dir_path.mkdir(exist_ok=True)
    for image_path in image_dir_path.iterdir():
        if image_path.suffix not in SHRINK_TARGET_EXTENSION:
            continue
        save_path = shrinked_dir_path / image_path.name
        resize_image(image_path, save_path, args.max_length)
        print(f"{image_path} is shrinked: {save_path}")
