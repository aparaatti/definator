import copy
import mimetypes
from .fs_helpers import *
from .json_helpers import *
from pathlib import Path


class Links(object):
    """
    Handles linked terms and files.
    """
    # TODO: Re factor all path changes through path property, now
    #       path gets set on load and save
    def __init__(self):
        self._linked_terms = []
        self._linked_files = dict()
        self._linked_images = dict()
        self._to_delete = list()
        self._path = None

    def __str__(self):
        return "linked terms: " + str(self._linked_terms) + os.linesep \
            + "linked files: " + str(self._linked_files) + os.linesep \
            + "linked images: " + str(self._linked_images) + os.linesep

    def link_term(self, term_str):
        if term_str not in self._linked_terms:
            self._linked_terms.append(term_str)

    def _link_image(self, path):
        if issubclass(type(path), Path) and\
           path not in self._linked_images.values():
                self._linked_images[path.name] = path
                return True
        else:
            return False

    def _link_file(self, path):
        if issubclass(type(path), Path) and\
           path not in self._linked_files.values():
                self._linked_files[path.name] = path
                return True
        else:
            return False

    def unlink_term(self, term_str):
        self._linked_terms.remove(term_str)

    def unlink_file(self, path: Path):
        if self._linked_files.get(path.name):
            self._to_delete.append(self._linked_files.pop(path.name))
            return True
        elif self._linked_images.get(path.name):
            self._to_delete.append(self._linked_images.pop(path.name))
            return True
        raise FileNotFoundError("Coudn't remove file from term: " + path.name)

    def save(self, path: Path, description_images: list()):
        """
        This saves linked files and deletes unlinked files from the parent
        term. Term object passes description_images list from the description
        object, because links handler doesn't nesesscarily have information of
        all shown images.
        """
        self._path = path
        self._delete_removed_files(description_images)
        self._save_files_to_term_path(description_images)
        save_json(path / "links.json", self, LinksEncoder())

    def _delete_removed_files(self, description_images: list()):
        """
        We delete the files, that are marked for deletion, are not in
        term_files anymore and are in **term folder**.
        """
        term_folder_files = set()
        [term_folder_files.add(path.name) for path in self._path.iterdir()]

        term_files = set()
        [term_files.add(f.name) for f in self._linked_files.values()]
        [term_files.add(f.name) for f in self._linked_images.values()]
        [term_files.add(f.name) for f in description_images]

        logging.debug("Files in term before save/delete: " + str(term_files))

        for path in self._to_delete:
            if path.name not in term_files and\
               path.name in term_folder_files:
                    remove_file(self._path / path.name)

    def _save_files_to_term_path(self, description_images: list):
        """
        Saving of external files happens because their path is different than
        "". It also means that, one  can't add stuff from root folder (maybe).

        The files that are in external paths are copied to term folder, from
        which they are read on load.

        :param path:
        :param added_images:
        :return:
        """
        term_folder_files = set()
        [term_folder_files.add(path.name) for path in self._path.iterdir()]

        for file_path in self._linked_files.values():
            if file_path.name not in term_folder_files:
                copy_file_to(file_path, self._path)
                self._linked_files[file_path.name] = Path(file_path.name)

        for img_path in description_images:
            if img_path.name not in term_folder_files:
                copy_file_to(img_path, Path(self._path))
                self._linked_images[img_path.name] = Path(img_path.name)

    def load(self, path: Path):
        self._path = path
        dictionary = load_json(self._path / "links.json", LinksDecoder())
        if type(dictionary) is dict:
            self._linked_terms = dictionary.get("terms")

        if self._path.is_dir():
            for file in self._path.iterdir():
                if file.is_file and file.name not in ["links.json",
                                                      "description.json"]:
                    self.link_file_on_mime(Path(file.name))

        logging.debug("links after load: " + str(self.linked_images) + " "
                      + str(self.linked_files) + " " + str(self.linked_terms))

    def link_file_on_mime(self, path: Path):
        """
        This links file paths based on its extension. If it is an image
        it is added to image list, otherwise it is added to file list.
        """
        type_tuple = mimetypes.guess_type(str(path))
        if type_tuple[0] is not None and type_tuple[0].startswith('image'):
            return self._link_image(path)
        else:
            return self._link_file(path)

    def delete(self):
        remove_file(self._path / "links.json")
        for file in self._linked_files.values():
            remove_file(self._path / file)

        for file in self._linked_images.values():
            remove_file(self._path / file)

    @property
    def linked_terms(self):
        return copy.copy(self._linked_terms)

    @property
    def linked_images(self):
        return list(self._linked_images.values())

    @property
    def linked_files(self):
        return list(self._linked_files.values())

    def get_file_path(self, file_name: str):
        """
        This returns always the absolute path for the file. It relays on
        self._path being set, which is the case when project is loaded.
        Only when project is loaded there are files without a path
        e.g. files located in the term folder.
        """
        fn = self._linked_files.get(file_name)
        if fn:
            # if the file is in project folder we add project path:
            if len(fn.parents) == 1:
                fn = self._path / fn
            return fn

        fi = self._linked_images.get(file_name)
        if fi:
            # if the image is in project folder we add project path:
            if len(fi.parents) == 1:
                fi = self._path / fi
            return fi

        raise FileNotFoundError

    def get_non_project_file_path(self, file_name: str):
        """
        This returns the file path for given file_name if it's different
        than current project path. When file is in project path, only the
        name of the file is returned.
        """
        fn = self._linked_files.get(file_name)
        if fn:
            return fn

        fi = self._linked_images.get(file_name)
        if fi:
            return fi

        raise FileNotFoundError

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path: Path):
        self._path = path


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
    # def decode(self, string):
    #    return json.JSONDecoder.decode(self, string)
