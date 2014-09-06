import os
import re
from .json_helpers import *
from .items import Title, AttachedImage, Paragraph

#TODO: ensimmäisen latauksen ohjaus tagifiltterin läpi.
class Description(object):
    _img_tag_pattern = re.compile('#img\([^)]*\)')

    """
    Contains description of the term as a tuple containing different types of
    content in chronological order.

    Description can have Titles, Paragraphs and ImagePaths.
    """
    def __init__(self):
        self._path = None
        self._content = list()
        self._attached_images = dict()
        self._old_content = tuple()

    def load(self, path: Path):
        content = load_json(path / "description.json", DescriptionDecoder())
        self._path = path
        self._content = content
        self._old_content = tuple(content)
        #Generate ImagePath objects from tags in text:
        self.content_text = self.content_text

    def save(self, path: Path):
        save_json(path / "description.json", self, DescriptionEncoder())

    def delete(self, path: Path):
        os.remove(str(path / "description.json"))

    def _parse_image_tags(self, text: str):
        image_count = 0
        new_part = None
        match_iterator = self._img_tag_pattern.finditer(text)

        for match in match_iterator:
            ip = AttachedImage().parse(match.group())
            if ip:
                if str(ip.path) in self._attached_images.keys():
                    self._attached_images[str(ip.path)] = ip
                self._attached_images[str(ip.path)] = ip
                self._content.append(ip)
                new_part = text.replace(match.group(), str(ip))
                image_count += 1

            if image_count > 0:
                text = new_part
        return text

    @property
    def added_image_paths(self):
        image_paths = list()
        [image_paths.append(ip.path) for ip in self._attached_images.values()]
        return image_paths

    @property
    def content_html(self):
        content = list()
        for item in self._content:
            if type(item) is Paragraph:
                content.append("<p>" + str(item) + "</p>")
            elif type(item) is Title:
                content.append("<h2>" + str(item) + "</h2>")
            elif type(item) is AttachedImage:
                if len(item.path.parts) > 1:
                    img_path = item.path
                else:
                    img_path = self._path / item.path

                content.append(
                    '<center><img src="' + str(img_path) +
                    '" alt="' + str(item) + '"/><br/>' +
                    '<b>' + str(item.title) + '</b></center>')
            else:
                print("Could not find type, where are the types?")
                print("Type: " + str(type(item)))
                print("Item: " + str(item))

        content_html = "".join(content)
        for ip in self._attached_images.values():
            content_html = content_html.replace(ip.image_tag, str(ip))

        return content_html

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

        for ai in self._attached_images.values():
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

        Text that starts with '#img(' and ends with ')' is an AttachedImage.
        AttachedImage tag can be inside a paragraph, but not in a title. Between image
        tags is path to image and optionally a title for image '"/path/to/image","Image title"'.
        If title is not given, the file name stem is used as reference in paragraph.

        :param text: Str containing text annotated with tags.
        """
        self._content.clear()
        split_text = text.split(os.linesep + os.linesep)

        for part in split_text:
            part = part.strip(os.linesep + " ")
            if part.startswith("##") and part.endswith("##"):
                self._content.append(Title(part[2:-2]))
            else:
                paragraph_index = len(self._content)
                self._content.append(self._parse_image_tags(part))
                self._content.insert(paragraph_index, Paragraph(part))

    def __str__(self):
        return str(self._content)


class DescriptionEncoder(json.JSONEncoder):
    """ Encodes a Description object to JSON eg. saves Description self.content
    str attributes as JSON array """
    def default(self, obj):
        if isinstance(obj, Description):
            str_list = list()
            for item in obj._content:
                if type(item) is Paragraph:
                    paragraph = item.text
                    for ai in obj._attached_images.values():
                        paragraph = paragraph.replace(ai.image_tag, ai.image_tag_name_only)
                    str_list.append("Paragraph:" + paragraph)
                    print(paragraph)
                elif type(item) is Title:
                    str_list.append("Title:" + str(item))
                #No need to save images, since they are instantiated from paragraphs on load.
                #elif type(item) is AttachedImage:
                    #We save only the stem, since Links moves files to term root on save.
                #    str_list.append("ImagePath:" + item.path.name + ":" + item.image_tag)
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

        return content
