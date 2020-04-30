import os


class Page:
    def __init__(self, directory, filename, contents):
        self.directory = directory
        self.filename = filename
        self._contents = contents

    def path(self):
        return os.path.join(self.directory, self.filename)

    def contents(self):
        return self._contents


class HtmlPage(Page):
    pass

class MarkdownPage(Page):
    pass


class SkeletonPage(Page):
    def __init__(self, directory, filename, contents, metadata):
        Page.__init__(self, directory, filename, contents)
        self.metadata = metadata

    def html_page(self, contents):
        return HtmlPage(self.directory, self.filename, contents)



