from abc import ABC, abstractmethod

from jinja2 import Environment, FileSystemLoader


class TemplateRenderer:
    def __init__(self, environment):
        self._environment = environment

    def render_in_file(self):
        raise NotImplementedError

    @classmethod
    def create(cls, template_dir_name: str) -> "TemplateRenderer":
        file_loader = FileSystemLoader(template_dir_name)
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
