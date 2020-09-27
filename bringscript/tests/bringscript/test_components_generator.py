from pathlib import Path
from unittest import TestCase
from unittest.mock import MagicMock, patch

from bringscript import components_generator
from bringscript.core import PreparableComponentsGenerator, TemplateRenderer
from bringscript.data import TemplateRenderArgument


class EelComponentsGeneratorTestCase(TestCase):
    def setUp(self):
        self.renderer = MagicMock(spec=TemplateRenderer)
        self.generator_args = MagicMock(spec=list)
        self.parent_dir = MagicMock(spec=str)
        self.child_dir = MagicMock(spec=str)

    def test_init(self):
        actual = components_generator.EelComponentsGenerator(
            self.renderer, self.generator_args, self.parent_dir, self.child_dir
        )

        self.assertIsInstance(actual, PreparableComponentsGenerator)
        self.assertEqual(actual._renderer, self.renderer)
        self.assertEqual(actual._args, self.generator_args)
        self.assertEqual(actual._parent_dir, self.parent_dir)
        self.assertEqual(actual._child_dir, self.child_dir)

    @patch("bringscript.core.TemplateRenderer.create")
    def test_create(self, renderer_create):
        dest_dir = Path("test_gui")
        app_name = MagicMock(spec=str)

        actual = components_generator.EelComponentsGenerator.create(
            dest_dir,
            app_name,
            child_dir_name=self.child_dir,
        )

        expected_args = [
            TemplateRenderArgument(
                Path("gui/gui.py.jinja"),
                Path("test_gui/gui/gui.py"),
                {"app_name": app_name},
            ),
            TemplateRenderArgument(
                Path("gui/gui.html.jinja"),
                Path(f"test_gui/gui/web/{app_name}.html"),
                {},
            ),
        ]

        self.assertIsInstance(
            actual, components_generator.EelComponentsGenerator
        )
        self.assertEqual(actual._renderer, renderer_create.return_value)
        self.assertEqual(actual._args, expected_args)
        self.assertEqual(actual._parent_dir, dest_dir / "gui")
        self.assertEqual(actual._child_dir, self.child_dir)
        renderer_create.assert_called_once_with()


class FlaskComponentsGeneratorTestCase(TestCase):
    def setUp(self):
        self.renderer = MagicMock(spec=TemplateRenderer)
        self.generator_args = MagicMock(spec=list)
        self.parent_dir = MagicMock(spec=str)
        self.child_dir = MagicMock(spec=str)

    def test_init(self):
        actual = components_generator.FlaskComponentsGenerator(
            self.renderer, self.generator_args, self.parent_dir, self.child_dir
        )

        self.assertIsInstance(actual, PreparableComponentsGenerator)
        self.assertEqual(actual._renderer, self.renderer)
        self.assertEqual(actual._args, self.generator_args)
        self.assertEqual(actual._parent_dir, self.parent_dir)
        self.assertEqual(actual._child_dir, self.child_dir)

    @patch("bringscript.core.TemplateRenderer.create")
    def test_create(self, renderer_create):
        dest_dir = Path("test_webapp")
        app_name = MagicMock(spec=str)

        actual = components_generator.FlaskComponentsGenerator.create(
            dest_dir,
            app_name,
            child_dir_name=self.child_dir,
        )

        expected_args = [
            TemplateRenderArgument(
                Path("webapp/webapp.py.jinja"),
                Path("test_webapp/webapp/webapp.py"),
                {"app_name": app_name},
            ),
            TemplateRenderArgument(
                Path("webapp/webapp.html.jinja"),
                Path(f"test_webapp/webapp/templates/{app_name}.html"),
                {},
            ),
        ]

        self.assertIsInstance(
            actual, components_generator.FlaskComponentsGenerator
        )
        self.assertEqual(actual._renderer, renderer_create.return_value)
        self.assertEqual(actual._args, expected_args)
        self.assertEqual(actual._parent_dir, dest_dir / "webapp")
        self.assertEqual(actual._child_dir, self.child_dir)
        renderer_create.assert_called_once_with()
