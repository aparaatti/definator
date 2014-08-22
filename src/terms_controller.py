# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
__author__ = 'Niko Humalamäki'

from copy import deepcopy

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

    def __init__(self):
        self._project_path = Path('')

        self._terms_list = []
        self._terms = {}

        self._added_terms = {}
        self._deleted_terms = {}
        self._changed_terms = {}

        self._has_changed = False

        self.add_term("New")

    @property
    def unsaved_changes(self):
        return self._has_changed

    def get_term(self, term_str):
        self._lazy_load_term(term_str)
        return deepcopy(self._terms[term_str])

    def _lazy_load_term(self, term_str):
        if term_str not in self._terms.keys() and term_str in self._terms_list:
            term_to_load = Term(term_str)
            self._terms[term_str] = term_to_load.load(self._project_path)

        return deepcopy(self._terms[term_str])

    @property
    def list_of_terms(self):
        return self._terms.keys()

    @property
    def project_path(self):
        return self._project_path

    @property
    def project_name(self):
        if len(self._project_path.parts) is 0:
            return "Untitled"

        return self.project_path.parts[-1]

    def remove_term(self, term_str):
        """
        Removes a term given as a string by moving it to deleted terms. The term disappears
        when the project is saved.

        :param term_str:
        """
        self._lazy_load_term(term_str)
        self._deleted_terms.add(self._terms.pop(term_str))
        self._terms_list.remove(term_str)
        self._has_changed = True

    def add_term(self, term_str):
        """
        Adds a term to the project.

        :param term_str: type str
        :return bool: If the term already exist, returns false if term is added successfully
        returns true.
        """
        term = Term(term_str)
        if term_str not in self._terms_list:
            self._terms[term_str] = term
            self._added_terms[term_str] = term
            self._has_changed = True
            return True
        else:
            raise TermAlreadyExists(
                "There already is a term '" + term_str + "'. Update terms using update_term method)")
            return False

    def update_term(self, original: Term, new: Term):
        self._changed_term(self._term[original])
        self._has_changed = True
        return True

    # def change_term_name(self, term):
    #     self._changed_terms(self._terms[term])
    #     raise NotImplemented
    #
    # def change_term_description(self, term, description):
    #     self._changed_terms(self._terms[term])
    #     raise NotImplemented
    #
    # def change_term_images(self, term, paths):
    #     self._changed_terms(self._terms[term])
    #     raise NotImplemented
    #
    # def change_term_attachments(self, term, paths):
    #     self._changed_terms(self._terms[term])
    #     raise NotImplemented

    @staticmethod
    def link_terms(self, term, related_terms):
        for rlTerm in related_terms:
            term.link_term(rlTerm)
            rlTerm.link_term(term)

        self._has_changed = True

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

    def save_project(self):
        """
        Saves the project to project_path

        :return:
        """
        if os.path.exists(self.__project_path):
            raise NotImplemented
        else:
            raise NotImplemented

        for term in self.changed_terms:
            term.save(self.__project_path)
        for term in self._added_terms:
            term.save(self.__project_path)
        for term in self._deleted_terms:
            term.delete(self.__project_path)

        self._added_terms = {}
        self._deleted_terms = {}

        for term in self.terms:
            term.save(self.__project_path / term.term)

        self.__save_terms()
        self._has_changed = False

    def __save_terms(self):
        """
        Saves list of terms as json to the project root "terms.json".
        """
        save_json(self.__project_path / "terms.json", self._terms, TermsEncoder())


class TermsEncoder(json.JSONEncoder):
    """ Encodes a Terms object to JSON eg. saves Term self.__term str
    attributes as JSON array """

    def default(self, obj):
        if isinstance(obj, TermsController):
            terms = []
            for term in obj:
                terms.append(term.term)
            return terms
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


class TermsDecoder(json.JSONDecoder):
    """ Decodes an TermsController object from JSON. """

    def decode(self, term_str):
        print(term_str)
        return set(json.JSONDecoder.decode(self, term_str))

