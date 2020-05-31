import eel
from PIL import Image


eel.init("web")


@eel.expose()
def resize(image_path):
    image_name = image_path.split("/")[-1]
    image = Image.open(image_path)
    resized_image = image.resize((300, 200))
    resized_image_path = f"web/images/{image_name}"
    resized_image.save(resized_image_path)
    # web directory == localhost:8000/
    return f"images/{image_name}"


eel.start("resize.html", size=(600, 400))
