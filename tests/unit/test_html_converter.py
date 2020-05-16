import unittest

from hamcrest import assert_that, string_contains_in_order, equal_to

from wg2.pages import SkeletonPage
from wg2.transformers import HtmlFormatter, PageProcessor


class MockWriter(PageProcessor):
    def convert(self, html_page: SkeletonPage):
        pass


class HtmlConverterTestCase(unittest.TestCase):
    def test_creates_html_page_from_markdown(self):
        formatter = HtmlFormatter('tests/content/templates') # TODO: smell?
        skeleton_page = SkeletonPage('foo/','bar.html', '<p>Here is the stuff</p>', {'title': 'Wow!'})
        html_page = formatter.convert(skeleton_page)
        assert_that(html_page.contents(), string_contains_in_order('<title>Wow!</title>','<h1>Wow!</h1>','<p>Here is the stuff</p>'))
        assert_that(html_page.depth(), equal_to(0))


