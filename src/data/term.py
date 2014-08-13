# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
__author__ = 'Niko Humalamäki'

import os

from .description import *
from .term_links import *


class Term(object):
    """
    Term object. Is given a term string on initialization and tells
    its attributes self.__description and self.__links to initialize.
    
    The description and links JSON files are assumed to be located under
    the project folder in a folder named as self.__term string.
    
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

    def __init__(self, term="New"):
        self.term = term
        self.__description = Description()
        self.__links = Links()

    def __contains__(self, related_term):
        return related_term in self.__relatedTerms

    @property
    def description(self):
        return self.__description

    @property
    def links(self):
        return self.__links

    @description.setter
    def description(self, description: Description):
        """
        :type description: Descripiton
        :param description: Decription of the term
        """
        self.__description = description

    @links.setter
    def links(self, links: Links):
        """
        :param links: Links object containing links to resource files and linked terms
        :type links: Links
        """
        self.__links = links

    def link_term(self, term: Term):
        """
        :param term: Term object
        """
        self.__links.add_term_link(term.term)

    def add_paragraph(self, paragraph: str):
        self.__description.add_paragraph(paragraph)

    def rem_paragraph(self, paragraph: str):
        self.__description.rem_paragraph(paragraph)

    def add_image(self, image_path: Path):
        #TODO check that it really is an image.
        """

        :param image_path: path to image file
        :raise NotImplementedException:
        """
        raise NotImplementedException("Adding an image not implemented")

    def add_image_to_text(self, new_description: Description, image_path: Path):
        """
        Add image to term and tag it to a location in Description text.

        :param new_description: description containing tag for image
        :param image_path: path to image
        :raise NotImplementedException:
        """
        raise NotImplementedException("Adding an image not implemented")

    def load(self, path):
        self.__links = Links()
        self.__description = Description()
        self.__links.load(path / self.term)
        self.__description.load(path / self.term)
        return self

    def save(self, path):
        self.__links.save(path / self.term)
        self.__description.save(path / self.term)

    def delete(self, path):
        self.__links.delete(path / self.term)
        self.__description.delete(path / self.term)

    def __str__(self):
        return self.term + os.linesep + self.__description + os.linesep + self.__links

    def __lt__(self, other):
        """
        >>> term = Term("abc")
        >>> term2 = Term("xyz")
        >>> term < term2
        True
        >>> term > term2
        False

        :param other:
        """
        return self.term.capitalize() < other.term.capitalize()

    def __gt__(self, other):
        return self.term.capitalize() > other.term.capitalize()

    def __hash__(self):
        return self.term.__hash__()

    def __eq__(self, other):
        return self.term == other.term