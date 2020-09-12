from abc import ABC, abstractmethod


class TemplateRenderer:
    def render_in_file(self):
        raise NotImplementedError

    @classmethod
    def create(cls):
        raise NotImplementedError


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
