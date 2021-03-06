import os
import re
from abc import ABC, abstractmethod
from collections import namedtuple

import markdown

from wg2.pages import SkeletonPage, MarkdownPage, HtmlPage, ImageCopier, Page


class PageProcessor(ABC):
    @abstractmethod
    def convert(self, page: Page) -> Page:
        pass


class PageWriter(PageProcessor):
    def convert(self, html_page: SkeletonPage):
        os.makedirs(html_page.directory, exist_ok=True)
        with open(html_page.path(),'w') as html_file:
            contents = html_page.contents()
            html_file.write(contents)


menu_item = namedtuple('MenuItem', ['href', 'label'])


class HtmlFormatter(PageProcessor):
    TEMPLATES = {'Home' : 'index-template.html',
                 'Info' : 'info-template.html' ,
                 'Resources': 'resources-template.html'
                }
    def __init__(self, environment):
        self.environment = environment

    def convert(self, skeleton_page: SkeletonPage) -> HtmlPage:
        template = self.template_for(skeleton_page)
        skeleton_page.metadata['menu_items'] = self.menu_items_for(skeleton_page)
        html = template.render(contents=skeleton_page.contents(), **skeleton_page.metadata)
        html_page = skeleton_page.html_page(html)
        return html_page

    def template_for(self, page: SkeletonPage):
        template_name = self.TEMPLATES[page.page_type()]
        return self.environment.get_template(template_name)

    def menu_items_for(self, skeleton_page: SkeletonPage):
        items = {'Home' : '/index.html',
                 'About': '/about.html',
                 'Contact': '/contact.html',
                 'Resources': '/resources/index.html'
        }
        return [menu_item('#' if label == skeleton_page.label() else items[label], label) for label in items.keys()]


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
            metadata[key] = ' '.join(metadata[key]) # meta should contain values, not lists of values!
        return html, metadata

