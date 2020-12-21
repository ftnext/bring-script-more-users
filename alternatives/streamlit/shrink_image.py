import uuid
from pathlib import Path

from PIL import Image

import streamlit as st


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


@st.cache
def resize_uploaded_image(image_file_object, max_length):
    """Return resized image path to make use of cache of streamlit

    When image_file_object and max_length are the same,
    there is no need to resize them again
    """
    random_id = uuid.uuid4()
    shrinked_dir_path = Path(f"images/{random_id}")
    shrinked_dir_path.mkdir(parents=True, exist_ok=True)

    resized_image_path = shrinked_dir_path / image_file_object.name
    has_resized = resize_image(
        image_file_object, resized_image_path, max_length
    )
    if has_resized:
        return resized_image_path


st.title("Resize image")

uploaded_files = st.file_uploader(
    "Specify image(s) to be resized in your computer",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True,
)
max_length = st.slider("Specify max length", 100, 500, 300, 50)
if uploaded_files:
    for uploaded_file in uploaded_files:
        resized_image_path = resize_uploaded_image(uploaded_file, max_length)
        if resized_image_path:
            st.image(str(resized_image_path))
