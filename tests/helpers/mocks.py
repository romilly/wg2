from typing import List

from wg2.pages import MarkdownPage
from wg2.transformers import PageProcessor


class MockPageProcessor(PageProcessor):
    def __init__(self):
        self.pages: List[MarkdownPage] = []

    def convert(self, markdown_page: MarkdownPage):
        self.pages.append(markdown_page)