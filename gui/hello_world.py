import random

import eel


NUMBERS = list(range(10))


@eel.expose
def say_hello():
    return f"Hello World {random.choice(NUMBERS)}"


eel.init("hello")
eel.start("hello.html", size=(300, 200))
