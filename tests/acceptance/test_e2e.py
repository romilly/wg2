import os
import unittest

from bs4 import BeautifulSoup
from hamcrest import assert_that, string_contains_in_order, equal_to
from jinja2 import Environment, FileSystemLoader

from hamcrest_helpers.files import contains_files, file_content, read
from wg2.builder import SiteBuilder
# from wg2.pages import ImageFileCopier
from wg2.pipeline import PageProcessorPipeline
from wg2.transformers import PageWriter, HtmlFormatter, MarkdownPageProcessor, MarkdownImageLocaliser


def first_word(text):
    return text if '\n ' not in text else text[:text.index('\n')]

class ElementFinder:
    def __init__(self, soup: BeautifulSoup):
        self.soup = soup

    def matching(self, tag, **kwargs):
        return self.soup.find_all(tag, **kwargs)


class EndToEndTestCase(unittest.TestCase):
    def setUp(self):
        page_writer = PageWriter()
        environment = Environment(loader=FileSystemLoader('templates'))
        html_formatter = HtmlFormatter(environment)
        self.target_directory = 'tests/generated'
        mdc = MarkdownPageProcessor(self.target_directory)
        # lines below will be needed when I convert the blog
        # copier = ImageFileCopier('content', 'tests/generated')
        # image_localiser = MarkdownImageLocaliser(copier)
        #converter = PageProcessorPipeline(image_localiser, mdc, html_formatter, page_writer)
        converter = PageProcessorPipeline(mdc, html_formatter, page_writer)
        self.site_builder = SiteBuilder(converter, 'tests/content', self.target_directory)
        self.site_builder.build_site()

    def test_html_pages_are_generated_from_markdown(self):
        self.check_directory_contents(self.target_directory, 'index.html', 'about.html', 'contact.html')
        self.check_directory_contents( os.path.join(self.target_directory, 'resources'),
                                      'index.html')
        self.check_file_contents('index.html', '<html', '</html>')
        self.check_file_contents('index.html',
                                 '<meta name="description" content="Tips, tools and resources for Digital Makers">')
        self.check_file_contents('index.html', '<head>', '<title>RARESchool</title>')
        self.check_file_contents('index.html', '<body>', '<h1', 'RARESchool</h1>')
        self.check_file_contents('about.html', '<meta name="description" content="Romilly Cocking\'s short biography">')

    def check_file_contents(self, file_to_check, *expected_strings):
        path = os.path.join(self.target_directory, file_to_check)
        assert_that(path, file_content(string_contains_in_order(*expected_strings)))

    def check_directory_contents(self, target_directory, *file_list):
        assert_that(target_directory, contains_files(*file_list))

    def test_images_are_included(self):
        assert_that('%s/about.html' % self.target_directory, file_content(string_contains_in_order('<img alt="Romilly Cocking" src="img/romilly.jpg" />')))

    def test_only_home_is_current_on_home_page(self):
        menu_links = {'Home'      : 'index.html',
                      'About'     : 'about.html',
                      'Contact'   : 'contact.html',
                      'Resources' : 'resources/index.html',
                      'Blog'      : 'https://blog.rareschool.com'
                        }
        parts = self.page_menu_parts('index.html')
        assert_that(parts, equal_to([('Home', '#', True),
                                     ('About', 'about.html', False),
                                     ('Contact', 'contact.html', False),
                                     ('Resources', 'resources/index.html',  False),
                                     ('Blog', 'https://blog.rareschool.com', False)]))
        parts = self.page_menu_parts('about.html')
        assert_that(parts, equal_to([('Home', 'index.html', False),
                                     ('About', '#', True),
                                     ('Contact', 'contact.html', False),
                                     ('Resources', 'resources/index.html', False),
                                     ('Blog', 'https://blog.rareschool.com', False)]))

    def page_menu_parts(self, page):
        menu_items = elements_in('%s/%s' % (self.target_directory, page)).matching('li', class_='nav-item')
        parts = [menu_item_parts(menu_item) for menu_item in menu_items]
        return parts


def menu_item_parts(menu_item):
    anchor = menu_item.find('a')
    # TODO: add test for 'current' span
    result = first_word(anchor.text), anchor['href'], 'active' in menu_item['class']
    return result


def elements_in(filename):
    html = read(filename)
    soup = BeautifulSoup(html, 'html5lib')
    return ElementFinder(soup)



