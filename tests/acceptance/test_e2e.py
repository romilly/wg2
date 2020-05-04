import unittest

from bs4 import BeautifulSoup
from hamcrest import assert_that, string_contains_in_order, equal_to

from hamcrest_helpers.files import contains_files, file_content, read
from wg2.builder import SiteBuilder
from wg2.pages import ImageFileCopier
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
        mdc = MarkdownPageProcessor('generated')
        copier = ImageFileCopier('content', 'generated')
        image_localiser = MarkdownImageLocaliser(copier)
        converter = PageProcessorPipeline(image_localiser, mdc, html_formatter, page_writer)
        self.site_builder = SiteBuilder(converter, 'content')
        self.site_builder.build_site()

    def test_html_pages_are_generated_from_markdown(self):
        assert_that('generated', contains_files('index.html','img/romilly.jpg','about/about.html', 'contact/contact.html'))
        assert_that('generated/index.html', file_content(string_contains_in_order('<html lang="en">','</html>')))
        assert_that('generated/index.html', file_content(string_contains_in_order('<meta name="description" content="Tips, tools and resources for Digital Makers">')))
        assert_that('generated/index.html', file_content(string_contains_in_order('<head>','<title>RARESchool</title>')))
        assert_that('generated/index.html', file_content(string_contains_in_order('<body>','<h1>RARESchool</h1>')))
        assert_that('generated/about/about.html', file_content(string_contains_in_order('<meta name="description" content="Romilly Cocking\'s short biography">')))

    def test_images_are_included(self):
        assert_that('generated/about/about.html', file_content(string_contains_in_order('<img alt="Romilly Cocking" src="img/romilly.jpg" />')))

    def test_menu_items_are_on_home_page(self):
        menu_items = self.find_elements_in('generated/index.html').matching('a', class_='nav-link')
        assert_that(len(menu_items), equal_to(4))
        urls = [menu_item['href'] for menu_item in menu_items]
        assert_that(urls, equal_to(['index.html','about/about.html','contact/contact.html','https://blog.rareschool.com']))

    def find_elements_in(self, filename):
        html = read(filename)
        soup = BeautifulSoup(html, 'html5lib')
        return ElementFinder(soup)



