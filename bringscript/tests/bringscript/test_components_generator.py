from unittest import TestCase
from unittest.mock import MagicMock, patch

from bringscript import components_generator
from bringscript.core import TemplateRenderer


class EelComponentsGeneratorTestCase(TestCase):
    def setUp(self):
        self.renderer = MagicMock(spec=TemplateRenderer)
        self.generator_args = MagicMock(spec=list)
        self.parent_dir = MagicMock(spec=str)
        self.child_dir = MagicMock(spec=str)

    def test_init(self):
        from bringscript.core import (
            ComponentsGenerator,
            DestinationPreparableMixin,
        )

        actual = components_generator.EelComponentsGenerator(
            self.renderer, self.generator_args, self.parent_dir, self.child_dir
        )

        self.assertIsInstance(actual, ComponentsGenerator)
        self.assertIsInstance(actual, DestinationPreparableMixin)
        self.assertEqual(actual._renderer, self.renderer)
        self.assertEqual(actual._args, self.generator_args)
        self.assertEqual(actual._parent_dir, self.parent_dir)
        self.assertEqual(actual._child_dir, self.child_dir)

    @patch("bringscript.core.TemplateRenderer.create")
    def test_create(self, renderer_create):
        actual = components_generator.EelComponentsGenerator.create(
            self.generator_args,
            parent_dir=self.parent_dir,
            child_dir=self.child_dir,
        )

        self.assertIsInstance(
            actual, components_generator.EelComponentsGenerator
        )
        self.assertEqual(actual._renderer, renderer_create.return_value)
        self.assertEqual(actual._args, self.generator_args)
        self.assertEqual(actual._parent_dir, self.parent_dir)
        self.assertEqual(actual._child_dir, self.child_dir)
        renderer_create.assert_called_once_with()

    @patch("bringscript.components_generator.EelComponentsGenerator.prepare")
    def test_preprocess(self, prepare):
        sut = components_generator.EelComponentsGenerator(
            self.renderer, self.generator_args, self.parent_dir, self.child_dir
        )

        sut._preprocess()

        prepare.assert_called_once_with()
