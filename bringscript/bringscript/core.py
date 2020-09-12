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


class DestinationPreparableMixin:
    def __init__(self, parent_dir: str, child_dir: str):
        self._parent_dir = parent_dir
        self._child_dir = child_dir

    def prepare(self):
        parent_dir_path = Path(self._parent_dir)
        if parent_dir_path.exists():
            message = (
                f"{self._parent_dir} already exists (stop not to overwrite)"
            )
            raise RuntimeError(message)
        dest_dir_path = parent_dir_path / self._child_dir
        dest_dir_path.mkdir(parents=True)
