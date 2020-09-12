from unittest import TestCase
from unittest.mock import call, patch

from bringscript import parser


class ParseArgsTestCase(TestCase):
    @patch("bringscript.parser.ArgumentParser")
    def test_when_specified_gui(self, argument_parser):
        mock_parser = argument_parser.return_value

        actual = parser.parse_args()

        self.assertEqual(actual, mock_parser.parse_args.return_value)
        argument_parser.assert_called_once_with()
        mock_parser.add_argument.assert_has_calls(
            [
                call("mode", choices=["gui"]),
                call("app_name"),
                call("dest_dir", type=parser.existing_path),
            ]
        )
        mock_parser.parse_args.assert_called_once_with()
