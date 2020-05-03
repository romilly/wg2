from wg2.pages import MarkdownPage
from wg2.transformers import PageProcessor


class PageProcessorPipeline(PageProcessor):

    def __init__(self, *transformers):
        self.transformers = transformers

    def convert(self, page: MarkdownPage):
        for transformer in self.transformers:
            page = transformer.convert(page)
        return page

