import os
import re
import logging
from .json_helpers import *
from .items import Title, AttachedImage, Paragraph, ASCII, BulletList


class Description(object):
    """
    Contains description of the term as a tuple containing different types of
    content in chronological order.

    Description can have Titles, Paragraphs and ImagePaths.
    """
    def __init__(self):
        self._path = Path()
        self._content = list()
        self._attached_images = dict()
        self._old_content = tuple()

    def __str__(self):
        return str(self._content)

    def load(self, path: Path):
        content = load_json(path / "description.json", DescriptionDecoder())
        self._path = path
        self._content = content
        # Generate ImagePath objects from tags in text:
        self.content_text = self.content_text

    def save(self, path: Path):
        self._path = path
        save_json(path / "description.json", self, DescriptionEncoder())

    def delete(self):
        os.remove(str(self._path / "description.json"))

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path: Path):
        logging.debug("Description path set to: " + str(path))
        self._path = path

    @property
    def content_html(self):
        """
        This makes a html repreasentation of this Description object.
        :return:
        """
        logging.debug("-----------------GETTING DESCRIPTION HTML-------------")
        content = list()
        for item in self._content:
            if type(item) in [Paragraph, Title, AttachedImage, BulletList,
                              ASCII]:
                content.append(item.html)
            else:
                logging.debug('Could not find type ' + str(type(item)) +
                              '. For item "' + str(item) + '".')

        content_html = "".join(content)
        for ip in self._attached_images.values():
            content_html = content_html.replace(
                ip.image_tag, ip.html_reference)
        return content_html

    @property
    def content_text(self):
        logging.debug("-----------------GETTING DESCRIPTION TEXT-------------")
        content_text_list = list()

        for item in self._content:
            if type(item) in [Paragraph, Title, BulletList, ASCII]:
                content_text_list.append(item.text)
            elif type(item) is AttachedImage:
                pass
            else:
                logging.debug('Could not find type ' + str(type(item)) +
                              '. For item "' + str(item) + '".')

        return "".join(content_text_list).strip(os.linesep)

    @content_text.setter
    def content_text(self, text: str):
        """
        This resets the content. Object remembers the content from last time
        the load() method was used to set content.

        Text that ends in two line separators or end of text string and doesn't
        begin with a known tag is a Paragraph.

        Text that starts with ## and ends in ## and two line separators is a
        Title.

        Text that starts with '#img(' and ends with ')' is an AttachedImage.
        Between image tags is path to image and optionally a title for image
        '"/path/to/image","Image title"'.
        If title is not given, the file name stem is used as reference in
        paragraph.

        :param text: Str containing text annotated with tags.
        """
        logging.debug("----------------SETTING DESCRIPTION TEXT--------------")
        self._content.clear()
        self._attached_images.clear()
        split_text = text.split(os.linesep + os.linesep)

        for part in split_text:
            if BulletList.parse_bullet_list_from_text(part):
                self._content.append(BulletList.instance)
            elif ASCII.parse_ascii_from_text(part):
                self._content.append(ASCII.instance)
            elif part.startswith("##") and part.endswith("##"):
                self._content.append(Title(part[2:-2]))
            else:
                paragraph_index = len(self._content)
                self._parse_tags_from_text(part)
                self._content.insert(paragraph_index, Paragraph(part))

    def _parse_tags_from_text(self, text: str):
        for ip in AttachedImage.parse_imgs_from_str(text, self._path):
            self._attached_images[str(ip.path.name)] = ip
            self._content.append(ip)

    @property
    def added_image_paths(self):
        """
        This property returns the paths to images wrapped in AttachedImages of
        this Description.
        """
        image_paths = list()
        for ip in self._attached_images.values():
            image_paths.append(ip.path)

        return image_paths


class DescriptionEncoder(json.JSONEncoder):
    """ Encodes a Description object to JSON eg. saves Description self.content
    str attributes as JSON array

    Only Paragraphs and Titles are saved, since images can be parsed from
    Paragraphs.

    """
    def default(self, obj):
        if isinstance(obj, Description):
            str_list = list()
            for item in obj._content:
                if type(item) is Paragraph:
                    paragraph = str(item)
                    for ai in obj._attached_images.values():
                        paragraph = paragraph.replace(
                            ai.image_tag, ai.image_tag_name_only)
                    str_list.append("Paragraph:" + paragraph)
                elif type(item) is Title:
                    str_list.append("Title:" + item.title)
                elif type(item) is ASCII:
                    str_list.append("ASCII:" + item.lines)
                elif type(item) is BulletList:
                    str_list.append("BulletList:" + "<>".join(item._items))
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
            elif s.startswith("Title:"):
                content.append(Title(s[6:]))
            elif s.startswith("ASCII:"):
                content.append(ASCII(s[6:]))
            elif s.startswith("BulletList:"):
                content.append(BulletList(s[11:].split("<>"), True))
        return content
