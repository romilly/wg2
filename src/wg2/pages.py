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


class MarkdownPage(Page):
    pass


class SkeletonPage(Page):
    pass


