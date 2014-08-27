import os
from .json_helpers import *
from .items import Title, ImagePath, Paragraph


class Description(object):

    """
    Contains description of the term as a tuple containing different types of
    content in chronological order.

    Description can have Titles, Paragraphs and ImagePaths.
    """
    def __init__(self):
        self._content = list()
        self._old_content = tuple()

    def load(self, path: Path):
        content = load_json(path / "description.json", DescriptionDecoder())
        self._content = content
        self._old_content = tuple(content)

    def save(self, path: Path):
        save_json(path / "description.json", self, DescriptionEncoder())

    def delete(self, path: Path):
        os.remove(str(path / "description.json"))

    @property
    def has_changed(self):
        if len(self._content) != len(self._old_content):
            return True

        for item in self._content:
            if item not in self._old_content:
                return True

        return False

    @property
    def content_html(self):
        content = list()
        for item in self._content:
            if type(item) is Paragraph:
                content.append("<p>" + str(item) + "</p>")
            elif type(item) is Title:
                content.append("<h2>" + str(item) + "</h2>")
            elif type(item) is ImagePath:
                content.append('<img src="' + str(item) + '"/>')
            else:
                print("Could not find type, where are the types?")
                print("Type: " + str(type(item)))
                print("Item: " + str(item))

        return "".join(content)

    @property
    def content_text(self):
        content_text = list()

        for item in self._content:
            if type(item) is Paragraph:
                content_text.append(str(item))
            elif type(item) is Title:
                content_text.append(str(item))
            elif type(item) is ImagePath:
                content_text.append(str(item))
            else:
                print("Could not find type, where are the types?")
                print("Type: " + str(type(item)))
                print("Item: " + str(item))
        return "".join(content_text)

    @content_text.setter
    def content_text(self, text: str):
        """
        This resets the content. Object remebers the content from last time
        the load() method was used to set content.

        :param text: Str containing text annotated with tags.
        """
        self._content = list()
        if len(text):
            self._content.append(Paragraph(text))
            #self.__content.append(Title(text))
            #self.__content.append(ImagePath(path))

    def __str__(self):
        return str(self._content)


class DescriptionEncoder(json.JSONEncoder):
    """ Encodes a Description object to JSON eg. saves Description self.content
    str attributes as JSON array """
    def default(self, obj):
        if isinstance(obj, Description):
            print(obj.content_text)
            strlist = list()
            for item in obj._content:
                if type(item) is Paragraph:
                    strlist.append("Paragraph:" + str(item))
                elif type(item) is Title:
                    strlist.append("Title:" + str(item))
                elif type(item) is ImagePath:
                    strlist.append("ImagePath:" + str(item))
            return strlist
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


class DescriptionDecoder(json.JSONDecoder):
    """ Decodes an Terms object from JSON. """
    def decode(self, string):
        data = list(json.JSONDecoder.decode(self, string))
        content = list()
        for string in data:
            if string.startswith("Paragraph:"):
                content.append(Paragraph(string[10:]))
            if string.startswith("Title:"):
                content.append(Title(string[6:]))
            if string.startswith("ImagePath:"):
                content.append(ImagePath(Path(string[10:])))
        return content
