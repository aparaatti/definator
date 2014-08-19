import html
from pathlib import Path


class ImagePath(object):
    def __init__(self, path: Path=Path('')):
        self._path = path

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        if type(value) is Path:
            self._path = value

    def __str__(self):
        return str(self._path)


class Paragraph(object):
    def __init__(self, text: str=""):
        self._text = html.escape(text)

    def __str__(self):
        return self._text

    @property
    def text(self):
        return self._text

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

    def __str__(self):
        return self._title
