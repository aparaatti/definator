# -*- coding: utf-8 -*-
#
# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
__author__ = 'Niko Humalamäki'

import logging
from copy import deepcopy, copy

from .term import *


class TermsController(object):
    """
    Controller class, handles the data object inter operation, term changes and
    their history and loading and saving a project.

    Has a set of Term objects. On initialization reads a list of term
    strings from terms.json file and creates Term objects using the
    string as an initializer and adds related links and description to the term
    from the filesystem.

    Tests:
    >>> tc = TermsController()
    >>> tc.add_term(Term("New"))
    True
    >>> newTerm = tc.get_term("New")
    >>> term_list = tc.load_project(Path("/home/aparaatti/Code/Python/definator/test-project"))
    >>> "html5" in term_list
    True
    >>> "koira" in term_list
    False
    >>> termJSON = tc.get_term("JSON")
    >>> termJSON.term
    'JSON'
    """
    def __init__(self):
        self._project_path = Path('')
        self._terms_list = []
        self._terms = {}
        self._changed_terms = {}
        self._deleted_terms = {}

    def get_term(self, term_str):
        self._lazy_load_term(term_str)
        return deepcopy(self._terms[term_str])

    def remove_term(self, term_str):
        """
        Removes a term given as a string by moving it to deleted terms. The term
        disappears when the project is saved.

        :param term: type Term
        """
        if term_str not in self._terms.keys():
            return False

        if self._deleted_terms.get(term_str) is None:
            self._deleted_terms[term_str] = list()

        self._deleted_terms[term_str].append(self._terms.pop(term_str))
        self._terms_list.remove(term_str)
        #Täällä pitäisi hoittaa viittausten poisto muista termeistä
        return True

    def add_term(self, term: Term):
        """
        Adds a term to the project.

        :param term: type Term
        :return bool: If the term already exist, returns false if term is added
        successfully returns true.
        """
        if term.term not in self._terms_list:
            self._terms[term.term] = term
            if self._changed_terms.get(term.term) is None:
                self._changed_terms[term.term] = list()
            self._changed_terms[term.term].append(term)
            self._terms_list.append(term.term)
            return True
        else:
            #Term already exists
            return False

    def update_term(self, term: Term, skip_name_change_test: bool=False):
        """
        Updates the term. Handles also Term.term changes. For Term.term changes
        to be handled correctly it is assumed that the term will have the
        unmodified version of the term to be updated in the previous_term
        attribute.

        :param term: updated Term object
        :return bool: Returns True if the name of the term has changed.
        """
        if not skip_name_change_test:
            previous_term_str = term.previous_term.term

            #If term has next term the previous name for term
            #is the next term so we change the next term to previous
            #term
            if term.next_term and term.next_term.next_term_str:
                previous_term_str = term.next_term.next_term_str
                term.previous_term = term.next_term

            if term.term not in self._terms_list:
                #We add the term that has changed it's term string as a new Term
                #objet.
                self.add_term(term)
                #And remove the old version if it had one.
                if previous_term_str != term.term:
                    #We remove the old term str from terms_list
                    self._terms_list.remove(previous_term_str)

                    #The original unchanged Term object is removed from self._terms
                    #dictionary and added to a list in delete dictionary:
                    self._deleted_terms[previous_term_str] = self._terms.pop(previous_term_str)
                    self._unlink_terms(term.previous_term, term.previous_term.related_terms)
                    self._link_terms(term, term.related_terms)
                    return True

        self._changed_terms[term.term] = term
        self._terms[term.term] = term
        return False

    def link_terms(self, target1: Term, str_related_terms: list):
        self._link_terms(target1, str_related_terms)
        self.update_term(target1)

    def _link_terms(self, target1: Term, str_related_terms: list):
        for str_related_term in str_related_terms:
            target2 = self.get_term(str_related_term)
            target1.link_term(target2)
            target2.link_term(target1)
            self.update_term(target2, True)
            logging.debug("-------[" + str(target1) + " <==> " + str(target2) + "]-------")

    def unlink_terms(self, target1: Term, str_related_terms: list):
        self._unlink_terms(target1, str_related_terms)
        self.update_term(target1)

    def _unlink_terms(self, target1: Term, str_related_terms: list):
        for str_related_term in str_related_terms:
            target2 = self.get_term(str_related_term)
            target1.unlink_term(target2)
            target2.unlink_term(target1)
            self.update_term(target2, True)
            logging.debug("-------[" + str(target1) + " |   | " + str(target2) + "]-------")



    def _lazy_load_term(self, term_str):
        if term_str not in self._terms.keys() and term_str in self._terms_list:
            logging.debug("loading term " + term_str)
            term_to_load = Term(term_str)
            self._terms[term_str] = term_to_load.load(self._project_path)

    def load_project(self, project_path):
        """
        Build a list of terms in the project.
        Throws FileNotFoundError if can't load the file. The individual terms
        are build lazily when get_term is called.

        :param project_path:
        :return:
        """
        terms_list = load_json(project_path / "terms.json", TermsDecoder())
        if terms_list is not None:
            self._project_path = project_path
            self._terms = {}
            self._terms_list = list(terms_list)
            self._terms_list.sort()
            return self._terms_list.copy()
        else:
            return None

    def save_project(self):
        """
        Saves the project to self._project_path.

        The path has to exists, will not create one.
        """
        path = self._project_path
        if path.exists() and path is not Path(''):
            for term_list in self._deleted_terms.values():
                term_list[0].delete(path)
            for changed_term in self._changed_terms.keys():
                self.get_term(changed_term).save(path)

            self._save_terms()
            self._changed_terms = {}
            self._deleted_terms = {}
            self._terms = {}

    def save_project_as(self, path: Path=None):
        """
        Saves the project to given path.

        The path has to exists, will not create one.
        """
        if path.exists():
            for term in self._terms_list:
                self._lazy_load_term(term)
            for term in self._terms.values():
                term.save(path)

            self._project_path = path
            self._changed_terms = {}
            self._deleted_terms = {}
            self._save_terms()
        else:
            logging.debug("Could not save to: " + str(path))
            raise Exception

    def _save_terms(self):
        """
        Saves list of terms as json to the project root "terms.json".
        """
        save_json(self._project_path / "terms.json", self, TermsEncoder())

    @property
    def unsaved_changes(self):
        return len(self._changed_terms)

    @property
    def project_path(self):
        return copy.copy(self._project_path)

    @property
    def project_name(self):
        if len(self._project_path.parts) is 0:
            return "Untitled"

        return self.project_path.parts[-1]


class TermsEncoder(json.JSONEncoder):
    """ Encodes a Terms object to JSON eg. saves Term self.__term str
    attributes as JSON array """

    def default(self, obj):
        if isinstance(obj, TermsController):
            return obj._terms_list
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


class TermsDecoder(json.JSONDecoder):
    """ Decodes an TermsController object from JSON. """

    def decode(self, term_str):
        return set(json.JSONDecoder.decode(self, term_str))
