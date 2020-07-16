from pathlib import Path

import eel


@eel.expose
def listup(path_str):
    path = Path(path_str)
    if not path.is_dir():
        return []
    return [str(child) for child in path.iterdir()]


eel.init("listup")
eel.start("files.html", size=(600, 400))
