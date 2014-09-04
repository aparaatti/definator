import os
import re
from .json_helpers import *
from .items import Title, AttachedImage, Paragraph


class Description(object):
    _img_tag_pattern = re.compile('#img\(.*\)')

    """
    Contains description of the term as a tuple containing different types of
    content in chronological order.

    Description can have Titles, Paragraphs and ImagePaths.
    """
    def __init__(self):
        self._content = list()
        self._attached_images = list()
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
    def content_html(self):
        content = list()
        for item in self._content:
            if type(item) is Paragraph:
                content.append("<p>" + str(item) + "</p>")
            elif type(item) is Title:
                content.append("<h2>" + str(item) + "</h2>")
            elif type(item) is AttachedImage:
                content.append('<img src="' + str(item.path) + '"/>')
            else:
                print("Could not find type, where are the types?")
                print("Type: " + str(type(item)))
                print("Item: " + str(item))

        return "".join(content)

    @property
    def content_text(self):
        content_text_list = list()

        for item in self._content:
            if type(item) is Paragraph:
                content_text_list.append(str(item))
            elif type(item) is Title:
                content_text_list.append(item.title_tag)
            else:
                print("Could not find type, where are the types?")
                print("Type: " + str(type(item)))
                print("Item: " + str(item))

        content_text = "".join(content_text_list).strip(os.linesep)

        for ai in self._attached_images:
            content_text = content_text.replace(str(ai), ai.image_tag)

        return content_text

    @content_text.setter
    def content_text(self, text: str):
        """
        This resets the content. Object remembers the content from last time
        the load() method was used to set content.

        Text that ends in two line separators or end of text string and doesn't begin with a known tag
        is a Paragraph.

        Text that starts with ## and ends with ## and two line separators is a Title.

        Text that starts with '#img(' and ends with ')' is a Image.
        Image tag can be inside a paragraph, but not in a title. Between image
        tags is path to image and a title for image '"/path/to/image","Image title"'.

        :param text: Str containing text annotated with tags.
        """
        self._content.clear()
        print(text)
        text.replace(os.linesep + " ", os.linesep)
        split_text = text.split(os.linesep + os.linesep)
        print(split_text)
        new_part = None
        image_count = 0

        for part in split_text:
            part = part.strip(os.linesep + " ")
            if part.startswith("##") and part.endswith("##"):
                self._content.append(Title(part[2:-2]))
                print("Title: " + part[2:-2])
            else:
                match_iterator = self._img_tag_pattern.finditer(part)
                paragraph_index = len(self._content)
                for match in match_iterator:
                    ip = AttachedImage().parse(match.group())
                    if ip:
                        self._content.append(ip)
                        self._attached_images.append(ip)
                        new_part = part.replace(match.group(), str(ip))
                        image_count += 1
                if image_count > 0:
                    part = new_part
                    image_count = 0

                self._content.insert(paragraph_index, Paragraph(part))
                print(self._content)

    def __str__(self):
        return str(self._content)


class DescriptionEncoder(json.JSONEncoder):
    """ Encodes a Description object to JSON eg. saves Description self.content
    str attributes as JSON array """
    def default(self, obj):
        if isinstance(obj, Description):
            print(obj.content_text)
            str_list = list()
            for item in obj._content:
                if type(item) is Paragraph:
                    str_list.append("Paragraph:" + str(item))
                elif type(item) is Title:
                    str_list.append("Title:" + str(item))
                elif type(item) is AttachedImage:
                    str_list.append("ImagePath:" + str(item))
            return str_list
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


class DescriptionDecoder(json.JSONDecoder):
    """ Decodes an Terms object from JSON. """
    def decode(self, s):
        data = list(json.JSONDecoder.decode(self, s))
        content = list()
        for s in data:
            if s.startswith("Paragraph:"):
                content.append(Paragraph(s[10:]))
            if s.startswith("Title:"):
                content.append(Title(s[6:]))
            if s.startswith("ImagePath:"):
                content.append(AttachedImage(Path(s[10:])))
        return content
