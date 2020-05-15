import unittest
from hamcrest import assert_that, equal_to

from helpers.mocks import MockPageProcessor
from wg2.builder import SiteBuilder


class SiteBuilderTestCase(unittest.TestCase):
    def test_builder_forwards_each_markdown_page(self):
        converter = MockPageProcessor()
        # TODO: something else should create the target directory
        builder = SiteBuilder(converter, 'content','tests/generated')
        builder.build_site()
        pages = converter.pages
        homepage = pages[0]
        assert_that(len(pages), equal_to(3))
        assert_that(homepage.directory, equal_to(''))
