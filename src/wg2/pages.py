import os


class Page:
    def __init__(self, directory, filename):
        self.directory = directory
        self.filename = filename

    def path(self):
        return os.path.join(self.directory, self.filename)


class MarkdownPage(Page):
    def contents(self):
        return read(self.path())


class HtmlPage(Page):
    def __init__(self, directory, filename, contents):
        Page.__init__(self, directory, filename)
        self._contents = contents

    def contents(self):
        return self._contents


def read(f):
    with open(f) as input_file:
        return input_file.read()