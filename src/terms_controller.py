# -*- coding: utf-8 -*-
#
# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
__author__ = 'Niko Humalamäki'

from copy import deepcopy
from .data.term import *


class TermsController(object):
    """
    Controller class, handles the data object inter operation, term changes and
    their history and loading and saving a project.

    Has a set of Term objects. On initialization reads a list of term
    strings from terms.json file and creates Term objects using the
    string as an initializer and adds related links and description to the term
    from the file system.

    Tests:
    >>> tc = TermsController()
    >>> tc.add_term(Term("New"))
    True
    >>> newTerm = tc.get_term("New")
    >>> term_list = tc.load_project(Path(
        "/home/aparaatti/Code/Python/definator/test-project"))
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

    def get_term(self, term_str) -> Term:
        if term_str in self._terms_list:
            self._lazy_load_term(term_str)
            return deepcopy(self._terms[term_str])
        else:
            raise NoSuchTermException

    @property
    def count(self):
        return len(self._terms_list)

    def remove_term(self, term_str):
        """
        Removes a term given as a string by moving it to deleted terms. The
        term is deleted from fs when the project is saved.

        :param term_str: term to remove as a str
        """
        if term_str not in self._terms.keys():
            return False

        if self._deleted_terms.get(term_str) is None:
            self._deleted_terms[term_str] = list()

        term_to_be_deleted = self._terms.pop(term_str)
        self._deleted_terms[term_str].append(term_to_be_deleted)
        self._unlink_terms(
            term_to_be_deleted, term_to_be_deleted.related_terms)
        self._terms_list.remove(term_str)
        return True

    def add_term(self, term: Term):
        """
        Adds a term to the project.

        :param term: type Term
        :return bool: If the term already exist, returns false if term is added
        successfully returns true.
        """
        if term.term not in self._terms_list and term.term is not "":
            self._terms[term.term] = term
            self._changed_terms[term.term] = term
            self._terms_list.append(term.term)
            return True
        else:
            # Term already exists
            return False

    def update_term(self, term: Term, skip_name_change_test: bool=False):
        """
        Updates the term. Handles also Term.term changes. For Term.term changes
        to be handled correctly it is assumed that the term will have the
        unmodified version of the term to be updated in the previous_term
        attribute.

        :param term: updated Term object
        :param skip_name_change_test: True/False whether the name change should
                be checked.
        :return bool: Returns True if the name of the term has changed.
        """
        if not skip_name_change_test:
            previous_term_str = term.previous_term.term

            if term.term not in self._terms_list:
                # We add the term that has changed it's term string as a new
                # Term objet.
                self.add_term(term)

                # And remove the old name from term.term list
                if previous_term_str in self._terms_list:
                    self._terms_list.remove(previous_term_str)
                else:
                    raise RuntimeError(
                        "Changing a name of a term that doesn't exist!")
                # The original unchanged Term object is removed from
                # self._terms dictionary
                old_term = self._terms.pop(term.previous_term.term)

                # We link the new term to the original old, not the cloned one
                # that is given for UI.
                old_term.next_term = term

                # We ad old term into the deleted dictionary:
                self._deleted_terms[previous_term_str] = old_term

                # We remove links to old term
                self._unlink_terms(
                    term.previous_term, term.previous_term.related_terms)
                # We add links to new term
                self._link_terms(term, term.related_terms)
                return True

        # term is added to changed terms, to be saved later.
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
            logging.debug("-------[" + str(target1) + " <==> " + str(target2) +
                          "]-------")

    def unlink_terms(self, target1: Term, str_related_terms: list):
        self._unlink_terms(target1, str_related_terms)
        self.update_term(target1)

    def _unlink_terms(self, target1: Term, str_related_terms: list):
        for str_related_term in str_related_terms:
            target2 = self.get_term(str_related_term)
            target1.unlink_term(target2)
            target2.unlink_term(target1)
            self.update_term(target2, True)
            logging.debug("-------[" + str(target1) + " |   | " + str(target2)
                          + "]-------")

    def _lazy_load_term(self, term_str):
        if term_str not in self._terms.keys():
            logging.debug("loading term " + term_str)
            term_to_load = Term(term_str)
            self._terms[term_str] = term_to_load.load(self._project_path)

    def load_project(self, project_path):
        """
        Build a list of terms in the project.
        Throws FileNotFoundError if can't load the file. The individual terms
        are build lazily when get_term is called.

        :param: project_path
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

    def _copy_linked_files_to_new_location(self, deleted_term):
        # If we have a new file, we have to move the files
        # to the new location
        new_term = deleted_term.next_term
        while new_term.next_term:
            new_term = new_term.next_term

        if new_term and new_term.term in self._changed_terms.keys():
            to_copy = list()
            for file in deleted_term.linked_images:
                try:
                    new_term.get_file_path(file.name)
                    to_copy.append(file.name)
                except FileNotFoundError:
                    pass

            for file in deleted_term.linked_files:
                try:
                    new_term.get_file_path(file.name)
                    to_copy.append(file.name)
                except FileNotFoundError:
                    pass

            if len(to_copy) > 0:
                make_dir(new_term.path / new_term.term)

            for file in to_copy:
                copy_file_to(deleted_term.path / deleted_term.term / file,
                             new_term.path / new_term.term)

    def save_project(self):
        """
        Saves the project to self._project_path.

        The path has to exists, will not create one.
        """
        path = self._project_path
        if path.exists() and path is not Path(''):
            for deleted_term in self._deleted_terms.values():
                self._copy_linked_files_to_new_location(deleted_term)
                deleted_term.delete()

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

    def clear(self):
        self._changed_terms = {}
        self._deleted_terms = {}
        self._terms = {}
        self._terms_list = []

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


class NoSuchTermException(Exception):
    pass

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
