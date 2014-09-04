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
        return related_term in self._links.get_linked_terms()

    @property
    def term_on_init(self):
        return self._term_on_init

    @property
    def term_as_html(self):
        return "<html><head>" +\
            '<meta charset="UTF-8">' +\
            "<title>" + self.term + "</title>" +\
            "</head>" +\
            "<body>" +\
            "<h1>" + self.term + "</h1>" +\
            self._description.content_html + \
            "</body>" + \
            "</html>"

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
        return self._links.get_linked_terms()

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
        self._links.add_term_link(term.term)

    def unlink_term(self, term):
        self._links.rem_term_link(term.term)

    def link_file(self, path: Path):
        self._links.add_file(path)

    def load(self, path):
        self._links = Links()
        self._description = Description()
        self._links.load(path / self.term)
        self._description.load(path / self.term)
        self._term_on_init = self.term
        return self

    def save(self, path: Path):
        path /= self.term
        if not path.exists():
            path.mkdir()

        self._description.save(path)
        self._links.save(path)

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
