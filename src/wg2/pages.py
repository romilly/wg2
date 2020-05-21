import os
import shutil
from abc import ABC, abstractmethod


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


class ImageCopier(ABC):
    @abstractmethod
    def copy(self, image_path):
        pass


class MarkdownPage(Page):
    def with_contents(self, contents):
        return MarkdownPage(self.directory, self.filename, contents)


class SkeletonPage(Page):
    def __init__(self, directory, filename, contents, metadata):
        Page.__init__(self, directory, filename, contents)
        self.metadata = metadata

    def html_page(self, contents):
        return HtmlPage(self.directory, self.filename, contents)

    def page_type(self):
        return self.metadata['type']


class ImageFileCopier(ImageCopier):
    IMG_DIRECTORY = 'img'

    def __init__(self, content_root, output_directory):
        self.content_root = content_root
        self.target_directory = os.path.join(output_directory, self.IMG_DIRECTORY)

    def copy(self, image_path):
        _, image_file_name = os.path.split(image_path)
        new_location = os.path.join(self.IMG_DIRECTORY, image_file_name)
        from_location = os.path.join(self.content_root, image_path)
        to_location = os.path.join(self.target_directory, image_file_name)
        os.makedirs(self.target_directory, exist_ok=True)
        shutil.copy(from_location, to_location)
        return new_location

