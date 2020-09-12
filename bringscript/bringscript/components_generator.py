from bringscript.core import PreparableComponentsGenerator, TemplateRenderer


class EelComponentsGenerator(PreparableComponentsGenerator):
    @classmethod
    def create(cls, generator_args, parent_dir, child_dir):
        renderer = TemplateRenderer.create()
        return cls(renderer, generator_args, parent_dir, child_dir)
