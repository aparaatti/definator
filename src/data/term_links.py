import os
import copy
from .json_helpers import *
from pathlib import Path


class Links(object):
    """
    Handles linked terms and files.
    """

    def __init__(self, links: list=[]):
        self._linked_terms = []
        self._linked_files = []
        self._linked_images = []

    def add_term_link(self, term_str):
        if term_str not in self._linked_terms:
            self._linked_terms.append(term_str)

    def add_image_link(self, path: Path):
        self._linked_images.append(path)

    def add_file(self, path):
        self._linked_files.append(path)

    def rem_term_link(self, term_str):
        self._linked_terms.remove(term_str)

    def rem_image_link(self, name):
        self._linked_images.remove(name)

    def rem_file_link(self, name):
        self._linked_images.remove(name)

    def get_linked_terms(self):
        return copy.copy(self._linked_terms)

    def get_linked_images(self):
        return copy.copy(self._linked_images)

    def get_linked_files(self):
        return copy.copy(self._linked_files)

    def save(self, path: Path):
        self._save_files_to_term_path(path)
        save_json(path / "links.json", self, LinksEncoder())

    def _save_files_to_term_path(self, path):
        #TODO move all referenced files in to the term's folder
        #for path in self._linked_files:
        #    print(str(path))

        #for path in self._linked_images:
        #    print(str(path))
        pass

    def load(self, path: Path):
        dictionary = load_json(path / "links.json", LinksDecoder())
        if type(dictionary) is dict:
            self._linked_terms = dictionary.get("terms")
            self._linked_files = dictionary.get("files")
            self._linked_images = dictionary.get("images")
        else:
            print("not a dict")
            self._linked_terms = list()
            self._linked_files = list()
            self._linked_images = list()

    def delete(self, path: Path):
        os.remove(str(path / "links.json"))

    @property
    def has_changed(self):
        return copy.copy(self._has_changed)

    def __str__(self):
        return str(self._linked_terms) + " Type: " + str(type(self._linked_terms))


class LinksEncoder(json.JSONEncoder):
    """ Encodes a Terms object to JSON eg. saves Term self.__term str
    attributes as JSON array """

    def default(self, obj):
        if isinstance(obj, Links):
            links = dict()
            links["terms"] = obj._linked_terms
            links["files"] = obj._linked_files
            links["images"] = obj._linked_images
            return links
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


class LinksDecoder(json.JSONDecoder):
    """ Decodes a Terms object from JSON. """

    def decode(self, string):
        print(string)
        return json.JSONDecoder.decode(self, string)
