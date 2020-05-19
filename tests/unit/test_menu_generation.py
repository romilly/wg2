import unittest

from hamcrest import assert_that, string_contains_in_order
from jinja2 import Environment, DictLoader

from wg2.pages import SkeletonPage
from wg2.transformers import HtmlFormatter

MENU_TEMPLATE= """
<nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
    <div class="container">
      <a class="navbar-brand" href="index.html">RARESchool</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarResponsive">
        <ul class="navbar-nav ml-auto">
        {% for item in items %}
          <li class="nav-item active">
            <a class="nav-link" href="{{item[1]}}">{{ item[0] }}
              {% if item[1] is eq '#' %}<span class="sr-only">(current)</span>{% endif %}
            </a>
          </li>
        {% endfor %} 
          <li class="nav-item">
            <a class="nav-link" href="https://blog.rareschool.com">Blog</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
"""


class MenuGenerationTestCase(unittest.TestCase):
    def test_generates_home_page_menu(self):
        loader = DictLoader({'navigation-template.html': MENU_TEMPLATE})
        formatter = HtmlFormatter(Environment(loader=loader))
        meta = {
            'items': [
                ('Home', '#'),
                ('About', 'about.html'),
                ('Contact', 'contact.html'),
                ('Resources', 'resources.html')
            ]
        }
        page = SkeletonPage('','navigation.html','nuffin', meta)
        menu = formatter.convert(page)
        assert_that(menu.contents(), string_contains_in_order('<a class="nav-link" href="#">Home',
                                                              '<span class="sr-only">(current)</span>',
                                                              '<a class="nav-link" href="about.html">About'
                                                              ))


if __name__ == '__main__':
    unittest.main()
