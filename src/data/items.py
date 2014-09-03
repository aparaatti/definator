import os
import re
import html
from pathlib import Path


class AttachedImage(object):
    match_attribute = re.compile('"[^"]*"')

    def __init__(self, path: Path=None, title: str=None):
        self._path = path
        self._title = title

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        if type(value) is Path:
            self._path = value
    @property
    def image_tag(self):
        if self._title:
            return '#img("' + str(self._path) + ',"' + self._title + '")'
        return '#img"' + str(self.path) + '")'

    def parse(self, string: str):
        """
        Initializes the object from a string of form
        #img("path/string"[,"image title text"])

        :param string: string representation of object
        """
        print("parsing image from string: " + string)
        matches = self.match_attribute.findall(string)
        if not matches[0]:
            return None

        self._path = Path(matches[0].strip('"'))

        if len(matches) > 1:
            self._title = matches[1].strip('"')

        return self

    def __str__(self):
        if self._title:
            title = self._title
        else:
            title = str(self._path)

        #TODO: translation
        return "Image: " + title



class Paragraph(object):
    def __init__(self, text: str=""):
        self._text = html.escape(text)

    def __str__(self):
        return self._text + os.linesep + os.linesep

    @property
    def text(self):
        return html.unescape(self._text)

    @text.setter
    def text(self, value: str):
        self._text = html.escape(value)


class Title(object):
    def __init__(self, title: str=""):
        self._title = html.escape(title)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = html.escape(value)

    @property
    def title_tag(self):
        return "##" + self._title + "##" + os.linesep + os.linesep

    def __str__(self):
        return self._title
