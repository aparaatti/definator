# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
# html template idea from:
# http://stackoverflow.com/questions/6748559/generating-html-documents-in-python
__author__ = 'Niko Humalamäki'

import os

from .description import *
from .term_links import *
from .term_exceptions import *

from django.template import Template, Context
from django.conf import settings
settings.configure()

class Term(object):
    termId = 0
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

    template = Template("""
    <html>
    <head>
    <title>{{ term }}</title>
    </head>
    <body>
    <h1>{{ term }}</h1>
    {{ description|safe }}.
    </body>
    </html>
    """)

    def __init__(self, term="New"):
        self.__termId = 0
        self.__term = term
        self.__description = Description()
        self.__links = Links()

    def __contains__(self, related_term):
        return related_term in self.__relatedTerms

    @property
    def term_as_html(self):
        context = Context(
            dict(term=self.__term, description=self.__description.content_html)
        )
        return self.template.render(context)

    @property
    def term(self):
        return self.__term

    @property
    def description(self):
        return self.__description.content_text

    @property
    def links(self):
        return self.__links

    @term.setter
    def term(self, term: str):
        self.__term = term

    @description.setter
    def description(self, description: Description):
        """
        :type description: Descripiton
        :param description: Decription of the term
        """
        if self.__description is None:
            self.__description = description
        else:
            raise DescriptionAlreadySetException(self)

    @links.setter
    def links(self, links: Links):
        """
        :param links: Links object containing links to resource files and linked terms
        :type links: Links
        """
        if self.__links is None:
            self.__links = links
        else:
            raise LinksAlreadySetException(self)

    def link_term(self, term):
        """
        :param term: Term object
        """
        self.__links.add_term_link(term.term)

    def add_paragraph(self, paragraph: str):
        self.__description.add_paragraph(paragraph)

    def rem_paragraph(self, paragraph: str):
        self.__description.rem_paragraph(paragraph)

    def add_image(self, image_path: Path):
        # TODO check that it really is an image.
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
        self.description.add_image_path(image_path)
        raise NotImplementedException("Adding an image not implemented")

    def load(self, path):
        self.__links = Links()
        self.__description = Description()
        self.__links.load(path / self.term)
        print(str(self) + "links: " + str(self.__links))
        self.__description.load(path / self.term)
        print(str(self) + "description: " + str(self.__description))
        print(self.__description.content_html)
        return self

    def save(self, path):
        self.__links.save(path / self.term)
        self.__description.save(path / self.term)

    def delete(self, path):
        self.__links.delete(path / self.term)
        self.__description.delete(path / self.term)

    def __str__(self):
        return self.term + os.linesep + str(self.__description) + os.linesep
        + str(self.__links)

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
