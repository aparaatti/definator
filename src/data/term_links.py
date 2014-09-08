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
        self._linked_files = dict()
        self._linked_images = dict()

    def __str__(self):
        return str(self._linked_terms) + " Type: " + str(type(self._linked_terms))

    def link_term(self, term_str):
        if term_str not in self._linked_terms:
            self._linked_terms.append(term_str)

    def _link_image(self, path):
        if issubclass(type(path), Path) and path not in self._linked_images.values():
            self._linked_images[path.name] = path
            return True
        else:
            return False

    def _link_file(self, path):
        if issubclass(type(path), Path) and path not in self._linked_files.values():
            self._linked_files[path.name] = path
            return True
        else:
            return False

    def unlink_term(self, term_str):
        self._linked_terms.remove(term_str)

    def unlink_image(self, path: Path):
        if self._linked_images.pop(path.name):
            return True
        return False

    def unlink_file(self, path: Path):
        if self._linked_files.pop(path.name):
            return True
        return False

    def save(self, path: Path, added_images: list()):
        self._save_files_to_term_path(path, added_images)
        save_json(path / "links.json", self, LinksEncoder())

    def _save_files_to_term_path(self, path: Path, added_images):
        """
        Saving of external files happens because their path is different than "". It also
        means that, one  can't add stuff from root folder (maybe).

        The files that are in external paths are copied to term folder, from which they
        are read on load.

        :param path:
        :param added_images:
        :return:
        """
        for file_path in self._linked_files.values():
            if len(file_path.parent.parts) > 0:
                self._copy_file_to(file_path, path)
                self._linked_files[file_path.name] = Path(file_path.name)

        for img_path in added_images:
            if len(img_path.parent.parts) > 0:
                self._copy_file_to(img_path, Path(path))
                self._linked_images[img_path.name] = Path(img_path.name)

    def _copy_file_to(self, src: Path, target: Path):
        shutil.copy2(str(src), str(target / src.name))

    def load(self, path: Path):
        dictionary = load_json(path / "links.json", LinksDecoder())
        if type(dictionary) is dict:
            self._linked_terms = dictionary.get("terms")

        if path.is_dir():
            for files in path.iterdir():
                if files.is_file and files.name not in ["links.json", "description.json"]:
                    self.link_file_on_mime(files)

        print("links after load: " + str(self.linked_images) + " " + str(self.linked_files) + " " + str(self.linked_terms))

    def link_file_on_mime(self, path: Path):
        type_tuple = mimetypes.guess_type(str(path))
        if type_tuple[0] is not None and type_tuple[0].startswith('image'):
            return self._link_image(Path(path.name))
        else:
            return self._link_file(Path(path.name))

    def delete(self, path: Path):
        os.remove(str(path / "links.json"))

    @property
    def linked_terms(self):
        return copy.copy(self._linked_terms)

    @property
    def linked_images(self):
        return list(self._linked_images.values())

    @property
    def linked_files(self):
        return list(self._linked_files.values())


class LinksEncoder(json.JSONEncoder):
    """ Encodes a Terms object to JSON eg. saves Term self.__term str
    attributes as JSON array """

    def default(self, obj):
        if isinstance(obj, Links):
            links = dict()
            images = []
            files = []
            [images.append(path.name) for path in obj.linked_images]
            [files.append(path.name) for path in obj.linked_files]
            links["terms"] = obj.linked_terms
            links["files"] = files
            links["images"] = images

            return links
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


class LinksDecoder(json.JSONDecoder):
    """ Decodes a Terms object from JSON. """

    def decode(self, string):
        return json.JSONDecoder.decode(self, string)
