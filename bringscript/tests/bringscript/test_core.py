from unittest import TestCase
from unittest.mock import call, MagicMock

from bringscript import core


class ComponentsGeneratorTestCase(TestCase):
    def setUp(self):
        class TestSampleComponentsGenerator(core.ComponentsGenerator):
            def _preprocess(self):
                pass

            def _postprocess(self):
                pass

        self.sut_class = TestSampleComponentsGenerator
        self.renderer = MagicMock(spec=core.TemplateRenderer)

    def test_init(self):
        args = MagicMock(spec=list)

        actual = self.sut_class(self.renderer, args)

        self.assertEqual(actual._renderer, self.renderer)
        self.assertEqual(actual._args, args)

    def test_generate(self):
        from bringscript.data import TemplateRenderArgument

        args1 = MagicMock(spec=TemplateRenderArgument)
        args2 = MagicMock(spec=TemplateRenderArgument)
        args = [args1, args2]
        sut = self.sut_class(self.renderer, args)

        sut.generate()

        self.renderer.render_in_file.assert_has_calls(
            [
                call(*args1.as_tuple.return_value),
                call(*args2.as_tuple.return_value),
            ]
        )
