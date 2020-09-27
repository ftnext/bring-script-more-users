from pathlib import Path

from bringscript.components_generator import (
    EelComponentsGenerator,
    FlaskComponentsGenerator,
)
from bringscript.parser import parse_args


def main():
    args = parse_args()
    app_name: str = args.app_name
    dest_dir: Path = args.dest_dir

    if args.mode == "gui":
        components_generator = EelComponentsGenerator.create(
            dest_dir, app_name, child_dir_name="web"
        )
        components_generator.generate()

    if args.mode == "web":
        components_generator = FlaskComponentsGenerator.create(
            dest_dir, app_name, child_dir_name="templates"
        )
        components_generator.generate()
