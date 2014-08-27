import os
from .json_helpers import *
from pathlib import Path


class Links(object):
    """
    Handles linked terms and files.
    """

    def __init__(self, links: list=[]):
        self._links = links

    def add_term_link(self, term_str):
        self._links.append({"term": term_str})

    def add_image(self, path):
        # TODO kopioi oikeaan paikkaan
        # self.__links.add({"image": str(path)})
        raise NotImplementedException("Adding an image not implemented yet.")

    def add_images(self, path: Path):
        if path.exists():
            self._links.add(Image)

    def add_file(self, path):
        # TODO lisää tiedosto
        # self.__links.rem({"file": filename})
        raise NotImplementedException("Adding a file not implemented yet.")

    def rem_term_link(self, term_str):
        self._links.rem({"term": term_str})

    def rem_image(self, name):
        # TODO poista kuva projektikansiosta
        # self.__links.rem({"image": str(path)})
        raise NotImplementedException("Removing an image not implemented yet.")

    def rem_file(self, name):
        # TODO poista muu liite
        raise NotImplementedException("Removing files not implemented")

    def _get_linked_type(self, type_of_link):
        linked = []
        for value in self._links:
            if self._links[value] == type_of_link:
                linked.append(value)
        return linked

    def get_linked_terms(self):
        return self._get_linked_type("term")

    def get_linked_images(self):
        return self._get_linked_type("image")

    def get_linked_files(self):
        return self._get_linked_type("file")

    def save(self, path: Path):
        save_json(path / "links.json", self, LinksEncoder())

    def load(self, path: Path):
        self._links = list(load_json(path / "links.json", LinksDecoder()))

    def delete(self, path: Path):
        os.remove(str(path / "links.json"))

    @property
    def has_changed(self):
        False

    def __str__(self):
        return str(self._links) + " Type: " + str(type(self._links))


class LinksEncoder(json.JSONEncoder):
    """ Encodes a Terms object to JSON eg. saves Term self.__term str
    attributes as JSON array """

    def default(self, obj):
        if isinstance(obj, Links):
            return obj._links
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


class LinksDecoder(json.JSONDecoder):
    """ Decodes a Terms object from JSON. """

    def decode(self, string):
        return set(json.JSONDecoder.decode(self, string))
