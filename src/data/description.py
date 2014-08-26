from .json_helpers import *
from .items import Title, ImagePath, Paragraph


class Description(object):

    """
    Contains description of the term as a tuple containing different types of
    content in chronological order.

    Description can have Titles, Paragraphs and ImagePaths.
    """
    def __init__(self):
        self.__content = list()
        self.__old_content = tuple()

    def load(self, path):
        content = load_json(path / "description.json", DescriptionDecoder())
        self.__content = content
        self.__old_content = tuple(content)

    def save(self, path):
        save_json(self,  path, DescriptionEncoder())

    @property
    def has_changed(self):
        if len(self.__content) != len(self.__old_content):
            return True

        for item in self.__content:
            if item not in self.__old_content:
                return True

        return False

    @property
    def content_html(self):
        content = list()
        for item in self.__content:
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

        for item in self.__content:
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
        self.__content = list()

        self.__content.append(Paragraph(text))
        #self.__content.append(Title(text))
        #self.__content.append(ImagePath(path))

    def __str__(self):
        return str(self.__content)


class DescriptionEncoder(json.JSONEncoder):
    """ Encodes a Description object to JSON eg. saves Description self.content
    str attributes as JSON array """
    def default(self, obj):
        if isinstance(obj, Description):
            return list(obj.__content)
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
        return tuple(content)
