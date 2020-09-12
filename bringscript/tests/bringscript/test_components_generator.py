from unittest import TestCase
from unittest.mock import MagicMock, patch

from bringscript import components_generator


class EelComponentsGeneratorTestCase(TestCase):
    def test_init(self):
        from bringscript.core import ComponentsGenerator, TemplateRenderer

        renderer = MagicMock(spec=TemplateRenderer)
        generator_args = MagicMock(spec=list)
        parent_dir = MagicMock(spec=str)
        child_dir = MagicMock(spec=str)

        actual = components_generator.EelComponentsGenerator(
            renderer, generator_args, parent_dir, child_dir
        )

        self.assertIsInstance(actual, ComponentsGenerator)
        self.assertEqual(actual._renderer, renderer)
        self.assertEqual(actual._args, generator_args)
        self.assertEqual(actual._parent_dir, parent_dir)
        self.assertEqual(actual._child_dir, child_dir)

    @patch("bringscript.core.TemplateRenderer.create")
    def test_create(self, renderer_create):
        generator_args = MagicMock(spec=list)
        parent_dir = MagicMock(spec=str)
        child_dir = MagicMock(spec=str)

        actual = components_generator.EelComponentsGenerator.create(
            generator_args, parent_dir=parent_dir, child_dir=child_dir
        )

        self.assertIsInstance(
            actual, components_generator.EelComponentsGenerator
        )
        self.assertEqual(actual._renderer, renderer_create.return_value)
        self.assertEqual(actual._args, generator_args)
        self.assertEqual(actual._parent_dir, parent_dir)
        self.assertEqual(actual._child_dir, child_dir)
        renderer_create.assert_called_once_with()
