import unittest
from hamcrest import assert_that, equal_to

from helpers import MockPageProcessor
from wg2.builder import SiteBuilder


class SiteBuilderTestCase(unittest.TestCase):
    def test_builder_forwards_each_markdown_page(self):
        converter = MockPageProcessor()
        builder = SiteBuilder(converter, 'content')
        builder.build_site()
        pages = converter.pages
        homepage = pages[0]
        assert_that(len(pages), equal_to(3))
        assert_that(homepage.directory, equal_to(''))
