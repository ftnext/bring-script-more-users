from pathlib import Path

from bringscript.core import PreparableComponentsGenerator, TemplateRenderer
from bringscript.data import TemplateRenderArgument


class EelComponentsGenerator(PreparableComponentsGenerator):
    @classmethod
    def create(
        cls, dest_dir: Path, app_name: str, child_dir_name: str
    ) -> "EelComponentsGenerator":
        parent_dir = dest_dir / "gui"
        generator_args = [
            TemplateRenderArgument(
                Path("gui/gui.py.jinja"),
                Path(f"{parent_dir}/gui.py"),
                {"app_name": app_name},
            ),
            TemplateRenderArgument(
                Path("gui/gui.html.jinja"),
                Path(f"{parent_dir}/web/{app_name}.html"),
                {},
            ),
        ]
        renderer = TemplateRenderer.create()
        return cls(renderer, generator_args, parent_dir, child_dir_name)


class FlaskComponentsGenerator(PreparableComponentsGenerator):
    @classmethod
    def create(cls, generator_args, parent_dir, child_dir):
        renderer = TemplateRenderer.create()
        return cls(renderer, generator_args, parent_dir, child_dir)
