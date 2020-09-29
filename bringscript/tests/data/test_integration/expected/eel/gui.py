import eel


@eel.expose
def integration():
    pass


if __name__ == "__main__":
    eel.init("web")
    eel.start("integration.html", size=(600, 400))
