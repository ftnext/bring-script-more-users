from pathlib import Path

from bringscript.components_generator import (
    EelComponentsGenerator,
    FlaskComponentsGenerator,
)
from bringscript.data import TemplateRenderArgument
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
        generator_args = [
            TemplateRenderArgument(
                Path("webapp/webapp.py.jinja"),
                Path(f"{dest_dir}/webapp/webapp.py"),
                {"app_name": app_name},
            ),
            TemplateRenderArgument(
                Path("webapp/webapp.html.jinja"),
                Path(f"{dest_dir}/webapp/templates/{app_name}.html"),
                {},
            ),
        ]
        components_generator = FlaskComponentsGenerator.create(
            generator_args,
            parent_dir=f"{dest_dir}/webapp",
            child_dir="templates",
        )
        components_generator.generate()
