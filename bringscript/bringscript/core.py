from abc import ABC, abstractmethod


class TemplateRenderer:
    pass


class ComponentsGenerator(ABC):
    def __init__(self, renderer, generator_args):
        self._renderer = renderer
        self._args = generator_args

    @abstractmethod
    def _preprocess(self):
        pass

    @abstractmethod
    def _postprocess(self):
        pass
