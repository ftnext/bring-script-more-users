import random

import eel


NUMBERS = list(range(10))


@eel.expose
def say_hello():
    return f"Hello World {random.choice(NUMBERS)}"


@eel.expose
class Helloest:
    @staticmethod
    def say():
        return "Hello World from Helloest class"


eel.init("hello")
eel.start("hello.html", size=(300, 200))
