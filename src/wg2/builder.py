import os
import re
from abc import ABC, abstractmethod

import markdown
from jinja2 import Template

from wg2.helpers import read
from wg2.pages import MarkdownPage, SkeletonPage


class PageWriter:
    def write(self, html_page: SkeletonPage):
        os.makedirs(html_page.directory, exist_ok=True)
        with open(html_page.path(),'w') as html_file:
            html_file.write(html_page.contents())


class Formatter(ABC):
    @abstractmethod
    def format(self, skeleton_page: SkeletonPage):
        pass


class HtmlFormatter(Formatter):
    def __init__(self, page_writer: PageWriter):
        self.page_writer = page_writer

    def format(self, skeleton_page: SkeletonPage):
        template = self.template_for(skeleton_page)
        html = template.render(body=skeleton_page.contents(), **skeleton_page.metadata)
        html_page = skeleton_page.html_page(html)
        self.page_writer.write(html_page)

    def template_for(self, page):
        t = read('templates/index.html')
        return Template(t)


class Converter(ABC):
    @abstractmethod
    def convert(self, markdown_page: MarkdownPage):
        pass


class MarkdownConverter(Converter):
    HTML_RE = re.compile("\.md$")

    def __init__(self, target_directory, content_directory, html_formatter: Formatter):
        self.html_formatter = html_formatter
        self.content_directory = content_directory
        self.target_directory = target_directory
        self.md = markdown.Markdown(extensions = ['meta'])

    def convert(self, markdown_page: MarkdownPage):
        html_filename = self.HTML_RE.sub('.html', markdown_page.filename)
        html_path = os.path.join(self.target_directory, markdown_page.directory)
        html, metadata = self.convert_content(markdown_page)
        skeleton_page = SkeletonPage(html_path, html_filename, html, metadata)
        self.html_formatter.format(skeleton_page)

    def convert_content(self, markdown_page):
        self.md.reset()
        html = self.md.convert(markdown_page.contents())
        metadata = self.md.Meta
        for key in metadata:
            if len(metadata[key]) == 1:
                metadata[key] = metadata[key][0]  # meta contains lists of values, not values!
        return html, metadata


class SiteBuilder:
    def __init__(self, converter: Converter, content_directory):
        self.content_directory = content_directory
        self.converter = converter

    def build_site(self):
        for root, directories, files in os.walk(self.content_directory):
            for f in files:
                if f.endswith('.md'):
                    contents = read(os.path.join(root, f))
                    relative_path = os.path.relpath(root, self.content_directory)
                    if relative_path == '.':
                        relative_path = ''
                    markdown_page = MarkdownPage(relative_path, f, contents)
                    self.converter.convert(markdown_page)


