from flask import Flask, render_template, request
from PIL import Image
from werkzeug.utils import secure_filename


app = Flask(__name__, static_folder="images")


@app.route("/resize", methods=["GET", "POST"])
def resize():
    if request.method == "GET":
        return render_template("resize.html")

    image_file = request.files["image_file"]
    secure_name = secure_filename(image_file.filename)
    image = Image.open(image_file)
    resized_image = image.resize((300, 200))
    resized_image_path = f"images/{secure_name}"
    resized_image.save(resized_image_path)
    return render_template("resize.html", image_path=resized_image_path)


if __name__ == "__main__":
    app.run(debug=True)
