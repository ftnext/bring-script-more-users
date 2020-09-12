from unittest import TestCase
from unittest.mock import MagicMock

from bringscript import core


class ComponentsGeneratorTestCase(TestCase):
    def setUp(self):
        class TestSampleComponentsGenerator(core.ComponentsGenerator):
            def _preprocess(self):
                pass

            def _postprocess(self):
                pass

        self.sut = TestSampleComponentsGenerator

    def test_init(self):

        renderer = MagicMock(spec=core.TemplateRenderer)
        args = MagicMock(spec=list)

        actual = self.sut(renderer, args)

        self.assertEqual(actual._renderer, renderer)
        self.assertEqual(actual._args, args)
