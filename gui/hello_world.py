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


class Helloer:
    class_var = "BLOND"

    def __init__(self, name):
        self.name = name

    @eel.expose("Helloer_say_instance_method")
    def say_instance(self):
        return f"Hello World from instance method / {self.name}"

    @classmethod
    @eel.expose("Helloer_say_class_method")
    def say_class(cls):
        return f"Hello World from class method / {cls.class_var}"

    @staticmethod
    @eel.expose("Helloer_say_static_method")
    def say_static():
        return "Hello World from static method"

    @staticmethod
    @eel.expose("Helloer.another_say_static_method")
    def say_another_static():
        return "Hellooooooo World from another one"


eel.init("hello")
eel.start("hello.html", size=(300, 200))
