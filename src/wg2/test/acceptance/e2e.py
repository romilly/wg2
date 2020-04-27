import unittest

from hamcrest import assert_that

from hamcrest_helpers.files import is_empty_directory, contains_files
from wg2.builder import SiteBuilder


class EndToEndTestCase(unittest.TestCase):
    def test_html_pages_are_generated_from_markdown(self):
        assert_that('generated', is_empty_directory())
        SiteBuilder().build('content','generated')
        assert_that('generated', contains_files('index.html','about/about.html', 'contact/contact.html'))


if __name__ == '__main__':
    unittest.main()
