import os
import re

import markdown
from jinja2 import Template

from wg2.pages import MarkdownPage, SkeletonPage


class PageWriter:
    def write(self, html_page: SkeletonPage):
        os.makedirs(html_page.directory, exist_ok=True)
        with open(html_page.path(),'w') as html_file:
            html_file.write(html_page.contents())


class HtmlFormatter:
    def __init__(self, page_writer: PageWriter):
        self.page_writer = page_writer

    def format(self, skeleton_page: SkeletonPage):
        self.page_writer.write(skeleton_page)


class MarkdownConverter:
    HTML_RE = re.compile("\.md$")

    def __init__(self, target_directory, content_directory, html_formatter: HtmlFormatter):
        self.html_formatter = html_formatter
        self.content_directory = content_directory
        self.target_directory = target_directory
        self.md = markdown.Markdown(extensions = ['meta'])

    def convert(self, markdown_page: MarkdownPage):
        html_filename = self.HTML_RE.sub('.html', markdown_page.filename)
        relative_path = os.path.relpath(markdown_page.directory, self.content_directory)
        html_path = os.path.join(self.target_directory, relative_path)
        html = self.md.convert(markdown_page.contents())
        template =  Template('<html>{{ body }}</html>')
        html = template.render(body=html)
        skeleton_page = SkeletonPage(html_path, html_filename, html)
        self.html_formatter.format(skeleton_page)


class SiteBuilder:
    def build(self, content_directory, target_directory):
        page_writer=PageWriter()
        html_formatter = HtmlFormatter(page_writer)
        converter = MarkdownConverter(target_directory, content_directory, html_formatter)
        for root, directories, files in os.walk(content_directory):
            for f in files:
                if f.endswith('.md'):
                    markdown_page = MarkdownPage(root, f)
                    converter.convert(markdown_page)
                    