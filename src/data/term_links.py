import os
import copy
import shutil
import mimetypes
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

    def link_term(self, term_str):
        if term_str not in self._linked_terms:
            self._linked_terms.append(term_str)

    def link_image(self, path: Path):
        if type(path) is Path and path not in self._linked_images:
            self._linked_images.append(path)
        #elif type(path) is str:
        #    self._linked_images.append(Path(str))
        else:
            print(str(type(self)) + ": could not link image " + str(path))

    def link_file(self, path):
        self._linked_files.append(path)

    def unlink_term(self, term_str):
        self._linked_terms.remove(term_str)

    def unlink_image(self, name):
        self._linked_images.remove(name)

    def unlink_file(self, name):
        self._linked_images.remove(name)

    def save(self, path: Path, added_images: list()):
        self._save_files_to_term_path(path, added_images)
        save_json(path / "links.json", self, LinksEncoder())

    def _save_files_to_term_path(self, path: Path, added_images):
        for file_path in self._linked_files:
            if file_path.parent != path:
                self._copy_file_to(file_path, path)

        for img_path in added_images:
            if img_path.parent != path:
                print("Image path on save: " + str(img_path) + " \n target on save " + str(path))
                self._copy_file_to(img_path, path)
                self._linked_images.append(img_path.name)

    def _copy_file_to(self, src: Path, target: Path):
        shutil.copy2(str(src), str(target / src.name))

    def load(self, path: Path):
        dictionary = load_json(path / "links.json", LinksDecoder())
        if type(dictionary) is dict:
            self._linked_terms = dictionary.get("terms")

        if path.is_dir():
            for x in path.iterdir():
                if x.is_file and x.name not in ["links.json", "description.json"]:
                    type_tuple = mimetypes.guess_type(str(x))
                    self._link_file_on_mime(type_tuple, x)

        print("links after load: " + str(self._linked_images) + " " + str(self._linked_files))

    def _link_file_on_mime(self, type_tuple: tuple, x: Path):
        print("FILE TYPE: " + str(type_tuple) + "\ntype(tuble[0]): " + str(type(type_tuple[0])))
        if type_tuple[0].startswith('image'):
            self.link_image(Path(x.name))
            #self._linked_images.append(x.name)
            print("added image: " + x.name)
        else:
            self.link_file.append(Path(x.name))
            print("added file: " + x.name)

    def delete(self, path: Path):
        os.remove(str(path / "links.json"))

    @property
    def linked_terms(self):
        return copy.copy(self._linked_terms)

    @property
    def linked_images(self):
        return copy.copy(self._linked_images)

    @property
    def linked_files(self):
        return copy.copy(self._linked_files)

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
        return json.JSONDecoder.decode(self, string)
