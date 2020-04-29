import os
import shutil
import unittest

from hamcrest import assert_that,string_contains_in_order
from hamcrest.core.base_matcher import BaseMatcher, T
from hamcrest.core.description import Description

from hamcrest_helpers.files import is_empty_directory, contains_files
from wg2.builder import SiteBuilder
from wg2.pages import read


def empty_directory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.mkdir(directory)


class FileContentMatcher(BaseMatcher):
    def describe_mismatch(self, item: T, mismatch_description: Description) -> None:
        if not os.path.isfile(item):
            mismatch_description.append_text('%s was not a file' % item)
        else:
            mismatch_description.append_text('a file with contents %s' % read(item))

    def _matches(self, item: T) -> bool:
        if not os.path.isfile(item):
            return False
        return self.content_matcher.matches(read(item))

    def describe_to(self, description: Description) -> None:
        description.append_text('a file with contents ')
        self.content_matcher.describe_to(description)

    def __init__(self, matcher: BaseMatcher):
        self.content_matcher = matcher


def file_content(matcher):
    return FileContentMatcher(matcher)


class EndToEndTestCase(unittest.TestCase):
    def setUp(self):
        self.site_builder = SiteBuilder()
        empty_directory('generated')

    def test_html_pages_are_generated_from_markdown(self):
        assert_that('generated', is_empty_directory())
        self.site_builder.build('content','generated')
        assert_that('generated', contains_files('index.html','about/about.html', 'contact/contact.html'))
        assert_that('generated/index.html', file_content(string_contains_in_order('<html>','</html>')))

