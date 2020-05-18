import os
import unittest

from hamcrest import assert_that, equal_to, contains_string
from jinja2 import Environment, FileSystemLoader
from selenium.webdriver import Firefox, DesiredCapabilities
from selenium.webdriver.firefox.webdriver import WebDriver

from helpers.ssl_server import start_server
from wg2.builder import SiteBuilder
from wg2.pages import ImageFileCopier
from wg2.pipeline import PageProcessorPipeline
from wg2.transformers import PageWriter, HtmlFormatter, MarkdownPageProcessor, MarkdownImageLocaliser

TARGET_DIRECTORY = 'output'


class TestPage:
    def __init__(self, driver: WebDriver, url):
        self.driver = driver
        self.driver.get(url)

    def title(self):
        return self.driver.title

    def metadata(self, name):
        return self.driver.find_element_by_xpath("//meta[@name='%s']" % name).get_attribute("content")

    # TODO: replace by tests for the cards
    # def main_content(self):
    #     return self.driver.find_element_by_class_name('post-preview').text

    def menu_items(self):
        return self.driver.find_elements_by_class_name()


class IndexPageTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        desired_capabilities = DesiredCapabilities.FIREFOX.copy()
        desired_capabilities['acceptInsecureCerts'] = True
        cls.driver = Firefox(capabilities=desired_capabilities)
        cls.server = start_server('generated')

    def setUp(self) -> None:
        page_writer = PageWriter()
        html_formatter = HtmlFormatter(Environment(loader=FileSystemLoader('content/templates')))
        mdc = MarkdownPageProcessor('generated')
        copier = ImageFileCopier('content', 'generated')
        image_localiser = MarkdownImageLocaliser(copier)
        converter = PageProcessorPipeline(image_localiser, mdc, html_formatter, page_writer)
        self.site_builder = SiteBuilder(converter, 'content', 'generated')
        self.site_builder.build_site()
        self.index_page = TestPage(self.driver, 'https://trefusis:4443/index.html')

    def test_index_page_title(self):
        assert_that(self.index_page.title(), equal_to('RARESchool'))

    def test_index_page_metadata(self):
        assert_that(self.index_page.metadata('description'), equal_to('Tips, tools and resources for Digital Makers'))
        assert_that(self.index_page.metadata('author'), equal_to('Romilly Cocking'))

    # def test_index_page_content(self):
    #     assert_that(self.index_page.main_content(), contains_string('Looking for clear, current, reliable information'))

    def test_css_copied(self):
        self.assertTrue(os.path.exists('generated/css/small-business.css'))

    def tearDown(self) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        cls.driver.quit()
        cls.server.shutdown()

