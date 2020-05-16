import os
import shutil

from wg2.files import read, empty_directory
from wg2.pages import MarkdownPage
from wg2.transformers import PageProcessor

BOOTSTRAP_LOCATION = 'bootstrap'
IMAGE_DIRECTORY = 'img'


class SiteBuilder:
    def __init__(self, converter: PageProcessor, content_directory, target_directory):
        self.converter = converter
        self.content_directory = content_directory
        self.target_directory = target_directory

    def build_site(self):
        empty_directory(self.target_directory)
        shutil.copytree(BOOTSTRAP_LOCATION, self.target_directory)
        shutil.copytree(os.path.join(self.content_directory, IMAGE_DIRECTORY),
                        os.path.join(self.target_directory, IMAGE_DIRECTORY))
        # for root, directories, files in os.walk(self.content_directory):
        #     self.convert_markdown_files(files, root)
        self.convert_markdown_files(os.listdir(self.content_directory), self.content_directory)

    # TODO: get rid of root; it should be self.content.directory
    def convert_markdown_files(self, files, root):
        for f in files:
            path = os.path.join(root, f)
            if os.path.isfile(path) and f.endswith('.md'):
                contents = read(path)
                relative_path = os.path.relpath(root, self.content_directory)
                if relative_path == '.':
                    relative_path = ''
                markdown_page = MarkdownPage(relative_path, f, contents)
                self.converter.convert(markdown_page)



