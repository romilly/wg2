import os

from wg2.helpers import read
from wg2.pages import MarkdownPage
from wg2.transformers import PageProcessor


class SiteBuilder:
    def __init__(self, converter: PageProcessor, content_directory):
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



