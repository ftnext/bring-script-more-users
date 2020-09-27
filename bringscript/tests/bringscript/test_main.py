from unittest import TestCase
from unittest.mock import patch

from bringscript import main


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
        components_generator = flask_generator_create.return_value

        main.main()

        parse_args.assert_called_once_with()
        flask_generator_create.assert_called_once_with(
            args.dest_dir, args.app_name, child_dir_name="templates"
        )
        components_generator.generate.assert_called_once_with()
