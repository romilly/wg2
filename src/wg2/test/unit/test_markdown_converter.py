import unittest
from typing import List

from hamcrest import assert_that, equal_to

from wg2.transformers import Formatter, MarkdownConverter
from wg2.pages import MarkdownPage, SkeletonPage


class MockFormatter(Formatter):
    def __init__(self):
        self.skeleton_pages: List[SkeletonPage] = []

    def format(self, skeleton_page: SkeletonPage):
        self.skeleton_pages.append(skeleton_page)


class MarkdownConverterTestCase(unittest.TestCase):
    def test_creates_skeleton_html_page(self):
        markdown_page = MarkdownPage('dont_care','source.md', 'does not matter')
        formatter = MockFormatter()
        converter = MarkdownConverter('wherever', formatter)
        converter.convert(markdown_page)
        assert_that(len(formatter.skeleton_pages), equal_to(1))

        page = formatter.skeleton_pages[0]
        assert_that(page.directory, equal_to('wherever/dont_care'))

