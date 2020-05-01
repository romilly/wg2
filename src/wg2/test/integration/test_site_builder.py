import unittest
from typing import List

from hamcrest import assert_that, equal_to

from wg2.builder import SiteBuilder
from wg2.transformers import Converter
from wg2.pages import MarkdownPage


class MockConverter(Converter):
    def __init__(self):
        self.pages: List[MarkdownPage] = []

    def convert(self, markdown_page: MarkdownPage):
        self.pages.append(markdown_page)


class SiteBuilderTestCase(unittest.TestCase):
    def test_builder_forwards_each_markdown_page(self):
        converter = MockConverter()
        builder = SiteBuilder(converter, 'content')
        builder.build_site()
        pages = converter.pages
        homepage = pages[0]
        assert_that(len(pages), equal_to(3))
        assert_that(homepage.directory, equal_to(''))


if __name__ == '__main__':
    unittest.main()
