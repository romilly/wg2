import os
import re


def read(f):
    with open(f) as input_file:
        return input_file.read()


class MarkdownPage:
    def __init__(self, root, filename):
        self.root = root
        self.filename = filename

    def contents(self):
        return read(self.path())

    def path(self):
        return os.path.join(self.root, self.filename)


class HtmlPage:
    def __init__(self, directory, filename, contents):
        self._contents = contents
        self.filename = filename
        self.directory = directory

    def path(self):
        return os.path.join(self.directory, self.filename)

    def contents(self):
        return self._contents


class PageWriter:
    def write(self, html_page: HtmlPage):
        os.makedirs(html_page.directory, exist_ok=True)
        with open(html_page.path(),'w') as html_file:
            html_file.write(html_page.contents())


class MarkdownConverter:
    HTML_RE = re.compile("\.md$")

    def __init__(self, target_directory, page_writer: PageWriter, content_directory):
        self.content_directory = content_directory
        self.page_writer = page_writer
        self.target_directory = target_directory

    def convert(self, markdown_page: MarkdownPage):
        html_filename = self.HTML_RE.sub('.html', markdown_page.filename)
        relative_path = os.path.relpath(markdown_page.root, self.content_directory )
        html_path = os.path.join(self.target_directory, relative_path)
        html_page = HtmlPage(html_path, html_filename, markdown_page.contents())
        self.page_writer.write(html_page)



class SiteBuilder:
    def build(self, content_directory, target_directory):
        page_writer=PageWriter()
        converter = MarkdownConverter(target_directory, page_writer, content_directory)
        for root, directories, files in os.walk(content_directory):
            for f in files:
                if f.endswith('.md'):
                    markdown_page = MarkdownPage(root, f)
                    converter.convert(markdown_page)
                    