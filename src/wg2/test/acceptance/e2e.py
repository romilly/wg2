import os
import shutil
import unittest

from hamcrest import assert_that

from hamcrest_helpers.files import is_empty_directory, contains_files
from wg2.builder import SiteBuilder


def empty_directory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.mkdir(directory)


class EndToEndTestCase(unittest.TestCase):
    def setUp(self):
        self.site_builder = SiteBuilder()
        empty_directory('generated')

    def test_html_pages_are_generated_from_markdown(self):
        assert_that('generated', is_empty_directory())
        self.site_builder.build('content','generated')
        assert_that('generated', contains_files('index.html','about/about.html', 'contact/contact.html'))

