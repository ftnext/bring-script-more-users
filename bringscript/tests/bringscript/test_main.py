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
        components_generator = eel_generator_create.return_value

        main.main()

        parse_args.assert_called_once_with()
        eel_generator_create.assert_called_once_with(
            args.dest_dir, args.app_name, child_dir_name="web"
        )
        components_generator.generate.assert_called_once_with()

    @patch("bringscript.main.FlaskComponentsGenerator.create")
    @patch("bringscript.main.parse_args")
    def test_when_web_is_specified(self, parse_args, flask_generator_create):
        args = parse_args.return_value
        args.mode = "web"
        generator_args = [
            TemplateRenderArgument(
                Path("webapp/webapp.py.jinja"),
                Path(f"{args.dest_dir}/webapp/webapp.py"),
                {"app_name": args.app_name},
            ),
            TemplateRenderArgument(
                Path("webapp/webapp.html.jinja"),
                Path(f"{args.dest_dir}/webapp/templates/{args.app_name}.html"),
                {},
            ),
        ]
        components_generator = flask_generator_create.return_value

        main.main()

        parse_args.assert_called_once_with()
        flask_generator_create.assert_called_once_with(
            generator_args,
            parent_dir=f"{args.dest_dir}/webapp",
            child_dir="templates",
        )
        components_generator.generate.assert_called_once_with()
