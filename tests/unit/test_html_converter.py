import unittest

from hamcrest import assert_that, string_contains_in_order, equal_to
from jinja2 import Environment, DictLoader

from wg2.pages import SkeletonPage
from wg2.transformers import HtmlFormatter, PageProcessor


class MockWriter(PageProcessor):
    def convert(self, html_page: SkeletonPage):
        pass

BAR_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>
</head>
<body>
<h1>{{ title }}</h1>
{{ contents }}
</body>
</html>
"""


class HtmlConverterTestCase(unittest.TestCase):
    def test_creates_html_page_from_markdown(self):
        formatter = HtmlFormatter(Environment(loader=DictLoader({'bar-template.html': BAR_TEMPLATE})))
        skeleton_page = SkeletonPage('foo/','bar.html', '<p>Here is the stuff</p>', {'title': 'Wow!'})
        html_page = formatter.convert(skeleton_page)
        assert_that(html_page.contents(), string_contains_in_order('<title>Wow!</title>','<h1>Wow!</h1>','<p>Here is the stuff</p>'))
        assert_that(html_page.depth(), equal_to(0))


