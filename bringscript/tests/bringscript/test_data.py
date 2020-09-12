from pathlib import Path
from unittest import TestCase
from unittest.mock import MagicMock

from bringscript import data


class TemplateRenderArgumentTestCase(TestCase):
    def test_as_tuple(self):
        src, dest = MagicMock(spec=Path), MagicMock(spec=Path)
        context = MagicMock(spec=dict)
        sut = data.TemplateRenderArgument(src, dest, context)

        actual = sut.as_tuple()

        self.assertEqual(actual, (src, dest, context))
