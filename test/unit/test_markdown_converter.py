import unittest
from typing import List

from hamcrest import assert_that, equal_to, string_contains_in_order

from wg2.transformers import MarkdownPageProcessor, PageProcessor
from wg2.pages import MarkdownPage, SkeletonPage


class MockFormatter(PageProcessor):
    def __init__(self):
        self.skeleton_pages: List[SkeletonPage] = []

    def convert(self, skeleton_page: SkeletonPage):
        self.skeleton_pages.append(skeleton_page)


class MarkdownConverterTestCase(unittest.TestCase):
    def test_creates_skeleton_html_page(self):
        markdown_page = MarkdownPage('dont_care','source.md', '##does not matter\n\nFoo *bar*')
        converter = MarkdownPageProcessor('wherever')
        page = converter.convert(markdown_page)
        assert_that(page.directory, equal_to('wherever/dont_care'))
        assert_that(page.filename, equal_to('source.html'))
        assert_that(page.contents(), string_contains_in_order('<h2>does not matter</h2>', '<em>bar</em>'))

