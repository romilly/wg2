import unittest

from hamcrest import string_contains_in_order, assert_that

from wg2.pages import MarkdownPage, ImageCopier
from wg2.test.integration.test_site_builder import MockConverter
from wg2.transformers import MarkdownImageLocaliser

PAGE_WITH_IMAGE="""
# Hello

![xxx](path_to_image/test.jpg)

Stuff
"""


class MockImageCopier(ImageCopier):
    def __init__(self):
        self.paths = []

    def copy(self, image_path):
        self.paths.append(image_path)
        return 'img/%s' % image_path


class MarkdownImageLocaliserTestCase(unittest.TestCase):
    def setUp(self) -> None:
        copier = MockImageCopier()
        self.localiser = MarkdownImageLocaliser(MockConverter(), copier)
        self.markdown_page = MarkdownPage('foo','bar.html',PAGE_WITH_IMAGE)

    def test_images_are_localised(self):
        processed_page = self.localiser.convert(self.markdown_page)
        assert_that(processed_page.contents(), string_contains_in_order('# Hello\n', '![xxx](img/path_to_image/test.jpg)'))


if __name__ == '__main__':
    unittest.main()
