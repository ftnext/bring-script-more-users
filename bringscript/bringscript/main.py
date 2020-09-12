from pathlib import Path

from bringscript.components_generator import EelComponentsGenerator
from bringscript.data import TemplateRenderArgument
from bringscript.parser import parse_args


def main():
    args = parse_args()
    app_name = args.app_name
    dest_dir = args.dest_dir

    if args.mode == "gui":
        generator_args = [
            TemplateRenderArgument(
                Path("gui/gui.py.jinja"),
                Path(f"{dest_dir}/gui/gui.py"),
                {"app_name": app_name},
            ),
            TemplateRenderArgument(
                Path("gui/gui.html.jinja"),
                Path(f"{dest_dir}/gui/web/{app_name}.html"),
                {},
            ),
        ]
        components_generator = EelComponentsGenerator.create(
            generator_args, parent_dir=f"{dest_dir}/gui", child_dir="web"
        )
        components_generator.generate()
