import unittest

from hamcrest import assert_that, string_contains_in_order

from wg2.pages import SkeletonPage
from wg2.transformers import HtmlFormatter, Writer


class MockWriter(Writer):
    def write(self, html_page: SkeletonPage):
        pass


class HtmlConverterTestCase(unittest.TestCase):
    def test_creates_html_page_from_markdown(self):
        writer = MockWriter()
        formatter = HtmlFormatter(writer)
        skeleton_page = SkeletonPage('foo','bar.html', '<p>Here is the stuff</p>', {'title': 'Wow!'})
        html_page = formatter.format(skeleton_page)
        assert_that(html_page.contents(), string_contains_in_order('<title>Wow!</title>','<h1>Wow!</h1>','<p>Here is the stuff</p>'))


