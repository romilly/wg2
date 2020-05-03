import os
import shutil
import unittest

from hamcrest import assert_that, string_contains_in_order
from markdown.extensions.tables import PIPE_LEFT

from hamcrest_helpers.files import contains_files, file_content
from wg2.builder import SiteBuilder
from wg2.pages import ImageFileCopier
from wg2.pipeline import PageProcessorPipeline
from wg2.transformers import PageWriter, HtmlFormatter, MarkdownPageProcessor, MarkdownImageLocaliser


def empty_directory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.mkdir(directory)


class EndToEndTestCase(unittest.TestCase):
    def setUp(self):
        empty_directory('generated')
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


