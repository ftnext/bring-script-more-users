from unittest import TestCase
from unittest.mock import call, MagicMock, patch

from bringscript import parser


@patch("bringscript.parser.Path")
class ExistingDirPathTestCase(TestCase):
    def test_when_path_dir_exists(self, pathlib_path):
        path_str = MagicMock(spec=str)
        pathlib_path.return_value.is_dir.return_value = True

        actual = parser.existing_dir_path(path_str)

        self.assertEqual(actual, pathlib_path.return_value)
        pathlib_path.assert_called_once_with(path_str)

    def test_when_path_dir_does_not_exist(self, pathlib_path):
        from argparse import ArgumentTypeError

        path_str = MagicMock(spec=str)
        pathlib_path.return_value.is_dir.return_value = False

        with self.assertRaises(ArgumentTypeError) as cm:
            parser.existing_dir_path(path_str)
        self.assertEqual(
            cm.exception.args[0], f"{path_str}: No such directory"
        )


class ParseArgsTestCase(TestCase):
    @patch("bringscript.parser.ArgumentParser")
    def test_when_specified_gui(self, argument_parser):
        mock_parser = argument_parser.return_value

        actual = parser.parse_args()

        self.assertEqual(actual, mock_parser.parse_args.return_value)
        argument_parser.assert_called_once_with()
        mock_parser.add_argument.assert_has_calls(
            [
                call("mode", choices=["gui", "web"]),
                call("app_name"),
                call("dest_dir", type=parser.existing_dir_path),
            ]
        )
        mock_parser.parse_args.assert_called_once_with()
