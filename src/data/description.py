from .json_helpers import *
from .items import Title, ImagePath, Paragraph


class Description(object):

    """
    Contains description of the term as a list containing different types of
    content in chronological order.

    Description can have Titles, Paragraphs and ImagePaths.
    """
    def __init__(self):
        self.__content = list()

    def add_paragraph(self, text):
        print("Adding a paragraph: " + text)
        self.__content.append(Paragraph(text))

    def add_subsection_title(self, text):
        self.__content.append(Title(text))

    def add_image_path(self, path: Path):
        self.__content.append(ImagePath(path))

    def load(self, path):
        self.__content = load_json(path / "description.json", DescriptionDecoder())

    def save(self, path):
        save_json(self,  path, DescriptionEncoder())

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

    def __str__(self):
        return str(self.__content)


class DescriptionEncoder(json.JSONEncoder):
    """ Encodes a Description object to JSON eg. saves Description self.content
    str attributes as JSON array """
    def default(self, obj):
        if isinstance(obj, Description):
            return obj.__content
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
