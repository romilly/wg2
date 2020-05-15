import os
import unittest

from bs4 import BeautifulSoup
from hamcrest import assert_that, string_contains_in_order, equal_to

from hamcrest_helpers.files import contains_files, file_content, read
from wg2.builder import SiteBuilder
# from wg2.pages import ImageFileCopier
from wg2.pipeline import PageProcessorPipeline
from wg2.transformers import PageWriter, HtmlFormatter, MarkdownPageProcessor, MarkdownImageLocaliser


class ElementFinder:
    def __init__(self, soup: BeautifulSoup):
        self.soup = soup

    def matching(self, tag, **kwargs):
        return self.soup.find_all(tag, **kwargs)


class EndToEndTestCase(unittest.TestCase):
    def setUp(self):
        page_writer = PageWriter()
        html_formatter = HtmlFormatter()
        self.target_directory = 'tests/generated'
        mdc = MarkdownPageProcessor(self.target_directory)
        # lines below will be needed when I convert the blog
        # copier = ImageFileCopier('content', 'tests/generated')
        # image_localiser = MarkdownImageLocaliser(copier)
        #converter = PageProcessorPipeline(image_localiser, mdc, html_formatter, page_writer)
        converter = PageProcessorPipeline(mdc, html_formatter, page_writer)
        self.site_builder = SiteBuilder(converter, 'content', self.target_directory)
        self.site_builder.build_site()

    def test_html_pages_are_generated_from_markdown(self):
        self.check_directory_contents(self.target_directory, 'index.html', 'about.html', 'contact.html')
        self.check_file_contents('index.html', '<html lang="en">', '</html>')
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
        assert_that('tests/generated/about.html', file_content(string_contains_in_order('<img alt="Romilly Cocking" src="resources/images/romilly.jpg" />')))

    def test_menu_items_are_on_home_page(self):
        menu_items = elements_in('tests/generated/index.html').matching('a', class_='nav-link')
        assert_that(len(menu_items), equal_to(4))
        links = [(menu_item['href'], menu_item.text) for menu_item in menu_items]
        assert_that(links, equal_to([('index.html','Home'),('about.html','About'),('contact.html','Contact'),('https://blog.rareschool.com','Blog')]))


def elements_in(filename):
    html = read(filename)
    soup = BeautifulSoup(html, 'html5lib')
    return ElementFinder(soup)



