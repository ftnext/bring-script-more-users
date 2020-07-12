from flask import Flask, render_template, request
from PIL import Image
from werkzeug.utils import secure_filename


SHRINK_TARGET_EXTENSION = (".jpg", ".png")

app = Flask(__name__, static_folder="images")


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
        return True
    return False


@app.route("/resize", methods=["GET", "POST"])
def resize():
    if request.method == "GET":
        return render_template("resize.html")

    image_files = request.files.getlist("image_file")
    max_length = int(request.form["max_length"])
    image_paths = []
    for image_file in image_files:
        secure_name = secure_filename(image_file.filename)
        resized_image_path = f"images/{secure_name}"
        has_resized = resize_image(image_file, resized_image_path, max_length)
        if has_resized:
            image_paths.append(resized_image_path)
    return render_template("resize.html", image_paths=image_paths)


if __name__ == "__main__":
    app.run(debug=True)
