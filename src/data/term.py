# -*- coding: utf-8 -*-
#
# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
__author__ = 'Niko Humalamäki'

from .description import *
from .term_links import *


class Term(object):
    termId = 0
    """
    Term object. Is given a term string on initialization and tells
    its attributes self._description and self.__links to initialize.

    The description and links JSON files are assumed to be located under
    the project folder in a folder named as self.__term string.

    Term it self is saved, when it creates self named folder for
    description and links.

    Todo:
        handle missing folder and missing or empty files.

    Tests:
    >>> term = Term("doctest")
    >>> term.add_paragraph("doctest is a python testing helper utility.")
    >>> term.add_image_to_text("/usr/share/wv/patterns/battributes.jpg")
    >>> term.add_paragraph("it is straight forward")
    >>> term.add_sub_section("end")
    >>> term.add_paragraph("Paragraph under 'end' -subtitle.")
    >>> term2 = Term("another")
    >>> term.link_term(term2)
    """

    def __init__(self, term: str=None):
        self._termId = 0
        self._term = term
        self._term_on_init = term
        self._description = Description()
        self._links = Links()

    def __contains__(self, related_term):
        return related_term in self._links.linked_terms()

    @property
    def term_on_init(self):
        return self._term_on_init

    @property
    def term_as_html(self):
        html = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" ' +\
            '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">' +\
            '<html xmlns="http://www.w3.org/1999/xhtml">' +\
            "<head>" +\
            '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />' +\
            "<title>" + self.term + "</title>" +\
            "</head>" +\
            "<body>" +\
            "<code>" +\
            "<h1>" + self.term + "</h1>" +\
            self._description.content_html +\
            self._make_html_list_of_images() +\
            self._make_html_list_of_files() +\
            "</code>" +\
            "</body>" +\
            "</html>"
        return html

    def _make_html_list_of_images(self):
        image_names = list()
        added_names = set()
        for path in self._description.added_image_paths:
            image_names.append('<a href="' + str(path) + '" target="_blank">' + path.name + '</a>')
            added_names.add(path.name)

        for name in self._links.linked_images:
            if name not in added_names:
                image_names.append('<a href="' + name + '" target="_blank">' + name + '</a>')

        if len(image_names) > 0:
            return "<h2>Attached images: </h2><ul>" + "<br/>".join(image_names) + "</ul>"
        return ""

    def _make_html_list_of_files(self):
        file_names = list()
        for name in self._links.linked_files:
            file_names.append('<a href="' + name + '" target="_blank">' + name + '</a>')

        if len(file_names) > 0:
            return "<h2>Attached files: </h2><ul>" + "<br/>".join(file_names) + "</ul>"
        return ""


    @property
    def term(self):
        return self._term

    @property
    def description(self):
        return self._description.content_text

    @property
    def links(self):
        return self._links

    @property
    def related_terms(self):
        return self._links.linked_terms

    @term.setter
    def term(self, term: str):
        if term == "":
            self.term = None
        elif term != self._term:
            self._term = term

    @description.setter
    def description(self, description_text: str):
        """
        :param description_text: text version of the description. Description
            object has to be able to parse this.

        :return:
        """
        self._description.content_text = description_text

    def link_term(self, term):
        """
        :param term: Term object
        """
        self._links.link_term(term.term)

    def unlink_term(self, term):
        self._links.unlink_term(term.term)

    def link_file(self, path: Path):
        self._links.link_file(path)

    def load(self, path):
        self._links = Links()
        self._links.load(path / self.term)
        self._description = Description()
        self._description.load(path / self.term)
        self._term_on_init = self.term
        return self

    def save(self, path: Path):
        path /= self.term
        if not path.exists():
            path.mkdir()
        self._links.save(path, self._description.added_image_paths)
        self._description.save(path)

    def delete(self, path):
        self._links.delete(path / self.term)
        self._description.delete(path / self.term)

    def __str__(self):
        return "Term object: " + self.term + " " + str(id(self))

    def __lt__(self, other):
        """
        >>> term = Term("abc")
        >>> term2 = Term("xyz")
        >>> term < term2
        True
        >>> term > term2
        False
        >>> term.term = None
        >>> term > term2
        False

        :param other:
        """
        if self.term is None:
            return True
        if other.term is None:
            return False
        return self.term.capitalize() < other.term.capitalize()

    def __gt__(self, other):
        return not self.__lt__(other)

    def __hash__(self):
        return self.term.__hash__()

    def __eq__(self, other):
        """
        Terms are thought as being immutable so if two
        Term objects have same term string they represent the same
        term, although the content may be different.

        >>> term1 = Term("ABC")
        >>> term2 = Term("ABC")
        >>> term1 == term2
        True
        >>> term1.term = "DBC"
        >>> term1 == term2
        False
        >>> term1.term = ""
        >>> print(term1.term)
        None
        >>> term1 == term2
        False

        :param other:
        :return:
        """
        return self.term == other.term
