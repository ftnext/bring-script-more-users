from unittest import TestCase
from unittest.mock import call, MagicMock, patch

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
        self.args = MagicMock(spec=list)

    def test_init(self):
        actual = self.sut_class(self.renderer, self.args)

        self.assertEqual(actual._renderer, self.renderer)
        self.assertEqual(actual._args, self.args)

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

    @patch("bringscript.core.TemplateRenderer.create")
    def test_create(self, template_renderer_create):
        template_dir = MagicMock(spec=str)

        actual = self.sut_class.create(template_dir, self.args)

        self.assertIsInstance(actual, self.sut_class)
        self.assertEqual(
            actual._renderer, template_renderer_create.return_value
        )
        self.assertEqual(actual._args, self.args)
        template_renderer_create.assert_called_once_with(template_dir)
