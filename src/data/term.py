# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
# html template idea from:
# http://stackoverflow.com/questions/6748559/generating-html-documents-in-python
__author__ = 'Niko Humalamäki'

import os
from pathlib import Path

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

    template = Template("""
    <html>
    <head>
    <title>{{ term }}</title>
    </head>
    <body>
    <h1>{{ term }}</h1>
    {{ description|safe }}
    </body>
    </html>
    """)

    def __init__(self, term=""):
        self.__termId = 0
        self.__term = None
        self.term = term
        self.__term_on_init = term
        self.__description = Description()
        self.__links = Links()
        self.__has_changed = False

    def __contains__(self, related_term):
        return related_term in self.__relatedTerms

    @property
    def has_changed(self):
        if self.__description.has_changed or self.__links.has_changed or self.term != self.__term_on_init:
            return True
        return False

    @property
    def term_on_init(self):
        return self.__term_on_init

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
        if term != self.__term:
            self.__has_changed = True
            self.__term = term

    @description.setter
    def description(self, description_text: str):
        """
        :param description_text: text version of the description. Description
            object has to be able to parse this.

        :return:
        """
        self.__description.content_text = description_text

    def link_term(self, term):
        """
        :param term: Term object
        """
        self.__links.add_term_link(term.term)

    def link_file(self, path: Path):
        self.__links.add_file(path)

    def load(self, path):
        self.__links = Links()
        self.__description = Description()
        self.__links.load(path / self.term)
        print(str(self) + "links: " + str(self.__links))
        self.__description.load(path / self.term)
        print(str(self) + "description: " + str(self.__description))
        print(self.__description.content_html)
        self.__term_on_init = self.term
        return self

    def save(self, path: Path):
        path = path / self.term
        if not path.exists():
            path.mkdir()

        self.__description.save(path)
        self.__links.save(path)

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
