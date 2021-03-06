from pathlib import Path
from unittest import TestCase
from unittest.mock import call, MagicMock, mock_open, patch

from jinja2 import Environment

from bringscript import core


class TemplateRendererTestCase(TestCase):
    def test_init(self):
        environment = MagicMock(spec=Environment)

        actual = core.TemplateRenderer(environment)

        self.assertEqual(actual._environment, environment)

    def test_render_in_file(self):
        environment = MagicMock(spec=Environment)
        sut = core.TemplateRenderer(environment)

        template = environment.get_template.return_value
        output = template.render.return_value

        src, dest = MagicMock(spec=Path), MagicMock(spec=Path)
        context = MagicMock(spec=dict)

        with patch("bringscript.core.open", mock_open()) as m:
            sut.render_in_file(src, dest, context)

        environment.get_template.assert_called_once_with(str(src))
        template.render.assert_called_once_with(**context)
        m.assert_called_once_with(dest, "w")
        handle = m()
        handle.write.assert_called_once_with(output)

    @patch("bringscript.core.Environment")
    @patch("bringscript.core.FileSystemLoader")
    @patch("bringscript.core.Path")
    def test_create(self, pathlib_path, file_system_loader, environment):
        parent_dir = MagicMock(spec=Path)
        pathlib_path.return_value.resolve.return_value.parent = parent_dir

        actual = core.TemplateRenderer.create()

        self.assertIsInstance(actual, core.TemplateRenderer)
        self.assertEqual(actual._environment, environment.return_value)
        file_system_loader.assert_called_once_with(parent_dir / "templates")
        environment.assert_called_once_with(
            loader=file_system_loader.return_value
        )


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


class DestinationPreparableMixinTestCase(TestCase):
    def setUp(self):
        self.parent_dir = MagicMock(spec=str)
        self.child_dir = MagicMock(spec=str)

    def test_init(self):
        actual = core.DestinationPreparableMixin(
            self.parent_dir, self.child_dir
        )

        self.assertEqual(actual._parent_dir, self.parent_dir)
        self.assertEqual(actual._child_dir, self.child_dir)

    @patch("bringscript.core.Path")
    def test_prepare_when_directory_not_exists(self, pathlib_path):
        sut = core.DestinationPreparableMixin(self.parent_dir, self.child_dir)
        parent_dir_path = MagicMock(spec=Path)
        parent_dir_path.exists.return_value = False
        pathlib_path.return_value = parent_dir_path
        dest_dir = parent_dir_path / self.child_dir

        sut.prepare()

        pathlib_path.assert_called_once_with(self.parent_dir)
        dest_dir.mkdir.assert_called_once_with(parents=True)

    @patch("bringscript.core.Path")
    def test_prepare_raises_error_when_directory_exists(self, pathlib_path):
        sut = core.DestinationPreparableMixin(self.parent_dir, self.child_dir)
        parent_dir_path = MagicMock(spec=Path)
        parent_dir_path.exists.return_value = True

        with self.assertRaises(RuntimeError) as cm:
            sut.prepare()
        self.assertEqual(
            cm.exception.args[0],
            f"{self.parent_dir} already exists (stop not to overwrite)",
        )


class PreparableComponentsGeneratorTestCase(TestCase):
    def setUp(self):
        self.renderer = MagicMock(spec=core.TemplateRenderer)
        self.generator_args = MagicMock(spec=list)
        self.parent_dir = MagicMock(spec=str)
        self.child_dir = MagicMock(spec=str)

    def test_init(self):
        from bringscript.core import (
            ComponentsGenerator,
            DestinationPreparableMixin,
        )

        actual = core.PreparableComponentsGenerator(
            self.renderer, self.generator_args, self.parent_dir, self.child_dir
        )

        self.assertIsInstance(actual, ComponentsGenerator)
        self.assertIsInstance(actual, DestinationPreparableMixin)
        self.assertEqual(actual._renderer, self.renderer)
        self.assertEqual(actual._args, self.generator_args)
        self.assertEqual(actual._parent_dir, self.parent_dir)
        self.assertEqual(actual._child_dir, self.child_dir)

    @patch("bringscript.core.PreparableComponentsGenerator.prepare")
    def test_preprocess(self, prepare):
        sut = core.PreparableComponentsGenerator(
            self.renderer, self.generator_args, self.parent_dir, self.child_dir
        )

        sut._preprocess()

        prepare.assert_called_once_with()
