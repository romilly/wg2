import os
import re
from abc import ABC, abstractmethod

import markdown
from jinja2 import Template

from wg2.files import read
from wg2.pages import SkeletonPage, MarkdownPage, HtmlPage, ImageCopier, Page


class PageProcessor(ABC):
    @abstractmethod
    def convert(self, page: Page) -> Page:
        pass


class PageWriter(PageProcessor):
    def convert(self, html_page: SkeletonPage):
        os.makedirs(html_page.directory, exist_ok=True)
        with open(html_page.path(),'w') as html_file:
            html_file.write(html_page.contents())


class HtmlFormatter(PageProcessor):

    def convert(self, skeleton_page: SkeletonPage) -> HtmlPage:
        template = self.template_for(skeleton_page)
        skeleton_page.metadata['script_prefix'] = skeleton_page.depth()*'../'
        html = template.render(contents=skeleton_page.contents(), **skeleton_page.metadata)
        html_page = skeleton_page.html_page(html)
        return html_page

    def template_for(self, page):
        t = read('templates/index.html')
        return Template(t)


class MarkdownImageLocaliser(PageProcessor):
    IMAGE_LINE_RE = re.compile('^!\[([^]]*)\]\(([^)]*)\)')
    IMAGE_DIRECTORY = 'img'

    def __init__(self, image_copier: ImageCopier):
        self.image_copier = image_copier

    def convert(self, markdown_page: MarkdownPage):
        contents = self.make_images_local(markdown_page.contents())
        localised_page = markdown_page.with_contents(contents)
        return localised_page

    def make_image_local(self, line):
        def localise_image(match):
            image_path = match.group(2)
            new_path = self.copy_image(image_path)
            return '![%s](%s)' % (match.group(1), new_path)
        return re.sub(self.IMAGE_LINE_RE, localise_image, line)

    def copy_image(self, image_path: str):
        return self.image_copier.copy(image_path)

    def make_images_local(self, body_text):
        lines = body_text.split('\n')
        return '\n'.join(self.make_image_local(line) for line in lines)


class MarkdownPageProcessor(PageProcessor):
    HTML_RE = re.compile("\.md$")

    def __init__(self, target_directory):
        self.target_directory = target_directory
        self.md = markdown.Markdown(extensions = ['meta'])

    def convert(self, markdown_page: MarkdownPage):
        html_filename = self.HTML_RE.sub('.html', markdown_page.filename)
        html_path = os.path.join(self.target_directory, markdown_page.directory)
        html, metadata = self.convert_content(markdown_page)
        skeleton_page = SkeletonPage(html_path, html_filename, html, metadata)
        return skeleton_page

    def convert_content(self, markdown_page):
        self.md.reset()
        html = self.md.convert(markdown_page.contents())
        metadata = self.md.Meta
        for key in metadata:
            if len(metadata[key]) == 1:
                metadata[key] = metadata[key][0]  # meta should contain values, not singleton lists of values!
        return html, metadata

