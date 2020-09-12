from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict

from jinja2 import Environment, FileSystemLoader


class TemplateRenderer:
    def __init__(self, environment):
        self._environment = environment

    def render_in_file(self, src: Path, dest: Path, context: Dict) -> None:
        # deal with the following error
        # AttributeError: 'PosixPath' object has no attribute 'split'
        template = self._environment.get_template(str(src))
        output = template.render(**context)
        with open(dest, "w") as fout:
            fout.write(output)

    @classmethod
    def create(cls) -> "TemplateRenderer":
        parent_dir = Path(__file__).resolve(strict=True).parent
        file_loader = FileSystemLoader(parent_dir / "templates")
        environment = Environment(loader=file_loader)
        return cls(environment)


class ComponentsGenerator(ABC):
    def __init__(self, renderer, generator_args):
        self._renderer = renderer
        self._args = generator_args

    def generate(self):
        self._preprocess()
        for argument in self._args:
            self._renderer.render_in_file(*argument.as_tuple())
        self._postprocess()

    @abstractmethod
    def _preprocess(self):
        pass

    @abstractmethod
    def _postprocess(self):
        pass

    @classmethod
    def create(cls, template_dir, generator_args):
        renderer = TemplateRenderer.create(template_dir)
        return cls(renderer, generator_args)
