from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from bringscript import main
from bringscript.data import TemplateRenderArgument


class MainTestCase(TestCase):
    @patch("bringscript.main.EelComponentsGenerator.create")
    @patch("bringscript.main.parse_args")
    def test_when_gui_is_specified(self, parse_args, eel_generator_create):
        args = parse_args.return_value
        args.mode = "gui"
        generator_args = [
            TemplateRenderArgument(
                Path("gui/gui.py.jinja"),
                Path(f"{args.dest_dir}/gui/gui.py"),
                {"app_name": args.app_name},
            ),
            TemplateRenderArgument(
                Path("gui/gui.html.jinja"),
                Path(f"{args.dest_dir}/gui/web/{args.app_name}.html"),
                {},
            ),
        ]
        components_generator = eel_generator_create.return_value

        main.main()

        parse_args.assert_called_once_with()
        eel_generator_create.assert_called_once_with(
            generator_args, parent_dir=f"{args.dest_dir}/gui", child_dir="web"
        )
        components_generator.generate.assert_called_once_with()
