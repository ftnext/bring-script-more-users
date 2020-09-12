from argparse import ArgumentParser, ArgumentTypeError
from pathlib import Path


def existing_dir_path(path_str: str) -> Path:
    dir_path = Path(path_str)
    if not dir_path.is_dir():
        message = f"{path_str}: No such directory"
        raise ArgumentTypeError(message)
    return dir_path


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("mode", choices=["gui", "web"])
    parser.add_argument("app_name")
    parser.add_argument("dest_dir", type=existing_dir_path)
    return parser.parse_args()
