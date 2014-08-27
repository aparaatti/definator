# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
__author__ = 'Niko Humalamäki'

from copy import deepcopy, copy

from .data.term import *
from .data.term_exceptions import TermAlreadyExists


class TermsController(object):
    """
    Controller class, handles the data object inter operation, term changes and their history and
    loading and saving a project.

    Has a set of Term objects. On initialization reads a list of term
    strings from terms.json file and creates Term objects using the
    string as an initializer and adds related links and description to the term
    from the filesystem.

    Tests:
    >>> tc = TermsController()
    >>> newTerm = tc.get_term("New")
    >>> tc.project_path = "/home/aparaatti/Code/Python/definator/test-project"
    >>> term_list = tc.load_project()
    >>> "html5" in term_list
    True
    >>> "koira" in term_list
    False
    >>> termJSON = tc.get_term("JSON")
    >>> termJSON.term
    'JSON'
    """
    #TODO: Mitä tapahtuu kun string listin termin nimi muuttuu?
    #   -menee has changed listaan
    #   -tallennettaessa kysytään termin nimi ladattaessa (vanha nimi), jos on vaihtunut:
    #       --> kopioidaan vanhat tiedot talteen
    #       --> poistetaan vanha termi
    def __init__(self):
        self._project_path = Path('')
        self._terms_list = []
        self._terms = {}
        self._deleted_terms = {}
        self._changed_terms = {}
        self._has_changed = False

    @property
    def unsaved_changes(self):
        return self._has_changed

    @property
    def list_of_terms(self):
        return self._terms.keys()

    @property
    def project_path(self):
        return copy(self._project_path)

    @property
    def project_name(self):
        if len(self._project_path.parts) is 0:
            return "Untitled"

        return self.project_path.parts[-1]

    def get_term(self, term_str):
        return self._lazy_load_term(term_str)

    def remove_term(self, term: Term):
        """
        Removes a term given as a string by moving it to deleted terms. The term disappears
        when the project is saved.

        :param term: type Term
        """
        if self._deleted_terms.get(term.term) is None:
            self._deleted_terms[term.term] = list()

        self._deleted_terms[term.term].append(self._terms.pop(term.term))
        self._terms_list.remove(term.term)
        self._has_changed = True

    def add_term(self, term: Term):
        """
        Adds a term to the project.

        :param term: type Term
        :return bool: If the term already exist, returns false if term is added successfully
        returns true.
        """
        if term.term not in self._terms_list:
            self._terms[term.term] = term

            if self._changed_terms.get(term.term) is None:
                self._changed_terms[term.term] = list()

            self._changed_terms[term.term].append(term)
            self._has_changed = True
            self._terms_list.append(term.term)
            return True
        else:
            #Term already exists
            return False

    def update_term(self, term: Term):
        """
        Update terms assumes that it is given a copy of the terms object TermsController
        already has.

        :param term:
        """
        if term.term_on_init != term.term and term.term not in self._terms_list:
            #We add the term that has changed it's term string as a new Term
            #objet.
            self.add_term(term)

            #We remove the old term str from terms_list, which contains all terms as str
            self._terms_list.remove(term.term_on_init)
            if self._deleted_terms.get(term.term_on_init) is None:
                self._deleted_terms[term.term_on_init] = list()

            #The original unchanged Term object is removed from self._terms
            #dictionary and added to a list in delete dictionary:
            self._deleted_terms[term.term_on_init].append(self._terms.pop(term.term_on_init))
        else:
            #We put the old version of Term in to a list in changed terms dictionary,
            #and replace the older version in self._terms
            if self._changed_terms.get(term.term) is None:
                self._changed_terms[term.term] = list()

            self._changed_terms[term.term].append(self._terms.pop(term.term))
            self._terms[term.term] = term

    def link_terms(self, term, related_terms):
        for rlTerm in related_terms:
            term.link_term(rlTerm)
            rlTerm.link_term(term)

        self._has_changed = True

    def _lazy_load_term(self, term_str):
        if term_str not in self._terms.keys() and term_str in self._terms_list:
            term_to_load = Term(term_str)
            self._terms[term_str] = term_to_load.load(self._project_path)

        return deepcopy(self._terms[term_str])

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
            self._has_changed = False
            return self._terms_list.copy()
        else:
            return None

    def save_project(self, path: Path=None):
        """
        Saves the project to given path, or if it's not
        given to self._project_path.
        """
        if path is None:
            path = self._project_path
        if os.path.exists(str(path)):
            for term_list in self._deleted_terms.values():
                term_list[0].delete(path)
            for term_list in self._changed_terms.values():
                term_list[-1].save(path)

            self._save_terms()
            self._changed_terms = {}
            self._deleted_terms = {}
            self._has_changed = False

    def _save_terms(self):
        """
        Saves list of terms as json to the project root "terms.json".
        """
        save_json(self._project_path / "terms.json", self, TermsEncoder())


class TermsEncoder(json.JSONEncoder):
    """ Encodes a Terms object to JSON eg. saves Term self.__term str
    attributes as JSON array """

    def default(self, obj):
        if isinstance(obj, TermsController):
            terms = []
            for term in obj._terms.values():
                terms.append(term.term)
            return terms
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


class TermsDecoder(json.JSONDecoder):
    """ Decodes an TermsController object from JSON. """

    def decode(self, term_str):
        print(term_str)
        return set(json.JSONDecoder.decode(self, term_str))

