from argparse import ArgumentParser


def existing_path(path_str):
    raise NotImplementedError


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("mode", choices=["gui"])
    parser.add_argument("app_name")
    parser.add_argument("dest_dir", type=existing_path)
    return parser.parse_args()
