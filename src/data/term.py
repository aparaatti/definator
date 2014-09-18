# -*- coding: utf-8 -*-
#
# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
__author__ = 'Niko Humalamäki'

import logging

from .description import *
from .term_links import *


class Term(object):
    """
    Term object. Is given a term string on initialization and tells
    its attributes self._description and self.__links to initialize.

    The description and links JSON files are assumed to be located under
    the project folder in a folder named as self.__term string.

    Term it self is saved, when it creates self named folder for
    description and links.

    Todo:
        handle missing folder and missing or empty files.
    """

    def __init__(self, term: str=None):
        self._term = ""
        self.term = term
        self._description = Description()
        self._links = Links()
        self._previous_term = None
        self._next_term = None

    def __contains__(self, related_term):
        return related_term in self._links.linked_terms()

    @property
    def can_undo(self):
        return self.previous_term is not None

    @property
    def can_redo(self):
        return self.next_term is not None

    @property
    def next_term(self):
        return self._next_term

    @next_term.setter
    def next_term(self, term):
        self._next_term = term
        term._previous_term = self

    @property
    def previous_term(self):
        return self._previous_term

    @previous_term.setter
    def previous_term(self, term):
        self._previous_term = term
        term.next_term = self._previous_term

    @property
    def term_as_html(self):
        html = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
            "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
            <html xmlns="http://www.w3.org/1999/xhtml">
            <head>
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />''' +\
            "<title>" + self.term + "</title>" +\
            "</head><body><code>" +\
            "<h1>" + self.term + "</h1>" +\
            self._description.content_html +\
            self._make_html_list_of_files() +\
            "</code></body></html>"
        return html

    @property
    def term(self):
        return self._term

    @term.setter
    def term(self, term: str):
        """
        Sets the term string for this Term object. IF "" is given, the Term.term is set
        to None.

        :param term: The term as a string.
        """
        if term is None:
            return
        elif term != self._term:
            self._term = term

    @property
    def description(self):
        return self._description.content_text

    @description.setter
    def description(self, description_text: str):
        """
        New Description object is created. The previous version of the term
        will reference the previous version of _description.

        :param description_text: text version of the description. Description
            object has to be able to parse this.

        :return:
        """
        self._description = Description()
        self._description.content_text = description_text

    @property
    def linked_images(self):
        return self._links.linked_images

    @property
    def linked_files(self):
        return self._links.linked_files

    @property
    def related_terms(self):
        return self._links.linked_terms

    @property
    def related_terms_as_html(self):
        html = list()
        html.append('''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
            "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
            <html xmlns="http://www.w3.org/1999/xhtml">
            <head>
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
            <title>Related terms</title>
            </head><body><code>''')

        for term in self._links.linked_terms:
            html.append('<a href="' + term + '" target="_blank">' + term + '</a> ')

        html.append("</code></body></html>")

        return "".join(html)

    @property
    def links(self):
        return copy.deepcopy(self._links)

    def get_file_path(self, file_name: str):
        return self._links.get_file_path(file_name)

    def deepcopy_links_from_previous(self):
        if self._previous_term:
            self._links = self._previous_term.links

    def _make_html_list_of_files(self):
        file_names = list()
        added_names = set()
        for path in self._description.added_image_paths:
            file_names.append(
                '<a href="' + str(path) + '" target="_blank" class="image">'
                + path.name + '</a>')
            added_names.add(path.name)

        for path in self._links.linked_images:
            if path.name not in added_names:
                file_names.append(
                    '<a href="' + path.name + '" target="_blank" class="image">'
                    + path.name + '</a>')

        for path in self._links.linked_files:
            file_names.append(
                '<a href="' + path.name + '" target="_blank" class="file">'
                + path.name + '</a>')

        if len(file_names) > 0:
            return "<br/><br/><h3>Attached files: </h3><ul>" + "<br/>".join(file_names) + "</ul>"
        return ""

    def link_term(self, term):
        """
        Links a term to this term with Links object.

        :param term: Term object
        """
        self._links.link_term(term.term)

    def unlink_term(self, term):
        self._links.unlink_term(term.term)

    def link_file(self, path: Path):
        return self._links.link_file_on_mime(path)

    def unlink_file(self, path: Path):
        return self._links.unlink_file(path)

    def load(self, path):
        self._links = Links()
        self._links.load(path / self.term)
        self._description = Description()
        self._description.load(path / self.term)
        return self

    def save(self, path: Path):
        """
        Saves the current term into given path.
        Set _previous_term and _next_term to None, eg. forgets undo/redo
        history.

        :param path: path to project folder
        :return: None
        """
        path /= self.term
        if not path.exists():
            path.mkdir()
        self._links.save(path, self._description.added_image_paths)
        self._description.save(path)
        self._previous_term = None
        self._next_term = None

    def delete(self, path):
        self._links.delete(path / self.term)
        self._description.delete(path / self.term)
        try:
            os.removedirs(str(path / self.term))
        except OSError as e:
            logging.info(
                "The term " + self.term + " was removed, referenced files where not removed. "
                + os.linesep + str(e))

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
