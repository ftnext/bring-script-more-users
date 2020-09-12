from bringscript.core import ComponentsGenerator, TemplateRenderer


class EelComponentsGenerator(ComponentsGenerator):
    def __init__(self, renderer, generator_args, parent_dir, child_dir):
        self._parent_dir = parent_dir
        self._child_dir = child_dir
        super().__init__(renderer, generator_args)

    @classmethod
    def create(cls, generator_args, parent_dir, child_dir):
        renderer = TemplateRenderer.create()
        return cls(renderer, generator_args, parent_dir, child_dir)

    def _preprocess(self):
        pass

    def _postprocess(self):
        pass
