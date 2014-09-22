import os
import re
import html
import logging
from pathlib import Path


class AttachedImage(object):
    """
    This class represents an image tag. It provides method
    parse_imgs_from_str to parse image tags from text.
    """

    _img_tag_pattern = re.compile('#img\([^)]*\)')
    _match_attribute = re.compile('"[^"]*"')

    @staticmethod
    def parse_imgs_from_str(text: str, parent_path: Path):
        attached_images = list()

        match_iterator = AttachedImage._img_tag_pattern.finditer(text)
        for match in match_iterator:
            try:
                ip = AttachedImage(match.group(), parent_path)
                if ip and ip not in attached_images:
                    attached_images.append(ip)
            except ValueError as e:
                logging.warning(e.args[0] + str(match))
            except IsADirectoryError:
                logging.warnign("Could not parse tag: " + str(match) +
                                " no file specified.")
        return attached_images

    def _parse(self, string):
        """
        Initializes the object from a string of form
        #img("path/string"[,"image title text"])

        :param string: string representation of object
        :param parent_path: Path object, if only a file name is parsed from the
            string this path is appended to filepath
        """
        matches = self._match_attribute.findall(string)
        logging.debug("matches: " + str(matches) + " len:" + str(len(matches)))
        if len(matches) < 1:
            raise ValueError("Could not parse values from tag")

        self._path = Path(matches[0].strip('"'))

        if len(self._path.parts) == 0:
            raise ValueError("Could not parse filename for image '" +
                             self._path.name + "'.")

        if len(matches) > 1:
            self._title = matches[1].strip('"')
        else:
            self._title = str(self._path.stem)

        self._tag = string
        if not self.path.exists():
            raise ValueError("File does not exist: " + str(self.path))

        logging.debug(
            "Img self._path set to: " + str(self._path) + os.linesep +
            "        self.path set to: " + str(self.path))
        return self

    def __init__(self, title_tag: str, parent_path: Path):
        self._path = Path()
        self._parent_path = parent_path
        self._title = ""
        self._tag = ""
        self._parse(title_tag)

    def __eq__(self, other):
        return self.path.name == other.path.name

    def __str__(self):
        return str(self._path) + " " + self._title

    @property
    def html_reference(self):
        return '(Image: <a href="#' + str(id(self)) +\
            '">' + self._title + '</a>)'

    @property
    def path(self):
        """
        Returns the path to image. If given path has only image name
        and parent path is given on parse, the parent_path + image name
        is returned.
        """
        if len(self._path.parts) == 1 and self._parent_path is not None:
            logging.debug(
                "Returning parent + name as path: " +
                str(self._parent_path / self._path))
            return self._parent_path / self._path
        logging.debug("Returning sole path: " + str(self._path))
        return self._path

    @path.setter
    def path(self, value):
        if type(value) is Path:
            self._path = value
        elif type(value) is str:
            self._path = Path(str)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def image_tag(self):
        return self._tag

    @property
    def image_tag_name_only(self):
        return '#img("' + str(self._path.name) + '","' + self._title + '")'

    @property
    def html(self):
        return '<center><a name="' + str(id(self)) + '">' + '<img src="' +\
            str(self.path) + '" alt="' + self.title + '"/><br/>' +\
            'Image: ' + '<b>' + str(self.title) + '</b></a></center>'


class Paragraph(object):
    def __init__(self, text: str=""):
        self._text = html.escape(text)

    def __str__(self):
        return html.unescape(self._text)

    @property
    def text(self):
        return html.unescape(self._text) + os.linesep + os.linesep

    @text.setter
    def text(self, value: str):
        self._text = html.escape(value)

    @property
    def html(self):
        return '<p>' + html.unescape(self._text) + '</p>'


class Title(object):
    def __init__(self, title: str=""):
        self._title = html.escape(title)

    def __str__(self):
        return html.unescape(self._title)

    @property
    def title(self):
        return html.unescape(self._title)

    @title.setter
    def title(self, value):
        self._title = html.escape(value)

    @property
    def text(self):
        return "##" + html.unescape(self._title) + "##" +\
               os.linesep + os.linesep

    @property
    def html(self):
        return '<h3>' + self._title + '</h3>'


class ASCII(object):
    instance = None

    @staticmethod
    def parse_ascii_from_text(text):
        lines = text.split(os.linesep)
        if lines[0].startswith("##ASCII##") and\
           lines[-1].endswith("##END##"):
                ASCII.instance = ASCII(os.linesep.join(lines[1:-1]))
                return True
        return False

    def __init__(self, lines: str):
        self._lines = lines

    @property
    def lines(self):
        return self._lines

    @property
    def text(self):
        return "##ASCII##" + os.linesep + self._lines + os.linesep + "##END##" \
            + os.linesep + os.linesep

    @property
    def html(self):
        return "<pre>" + self._lines + "</pre>"


class BulletList(object):
    instance = None

    @staticmethod
    def parse_bullet_list_from_text(text: str):
        if text.startswith("##LIST##") and\
           text.endswith("##END##"):
            BulletList.instance = BulletList(text.split(os.linesep)[1:-1])
            return True
        return False

    def __init__(self, str_list: list, escaped: bool=False):
        escaped = list()
        if escaped:
            self._items = str_list
            self._un_escaped_items = list()
            for item in str_list:
                self._un_escaped_items.append(html.unescape(item))

        else:
            self._un_escaped_items = str_list
            self._items = list()
            for item in str_list:
                self._items.append(html.escape(item))

    @property
    def items(self):
        return self._items

    @property
    def text(self):
        return "##LIST##" + os.linesep \
               + os.linesep.join(self._un_escaped_items) + os.linesep + \
               "##END##" + os.linesep + os.linesep

    @property
    def html(self):
        return "<ul><li>" + "</li><li>".join(self._items) + "</li></ul>"
