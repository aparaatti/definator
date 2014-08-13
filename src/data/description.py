from .json_helpers import *


class Description(object):
    def __init__(self):
        self.__content = [{}]

    def add_paragraph(self, text):
        self.content.append({"paragraph": text})

    def add_image(self, path):
        self.content.append({"image": str(path)})

    def add_subtitle(self, text):
        self.content.append({"subtitle": text})

    def load(self, path):
        self.__content = load_json(path / "description.json", DescriptionDecoder())

    def save(self, path):
        save_json(self,  path, DescriptionEncoder())
        
    @property
    def content(self):
        return self.__content


class DescriptionEncoder(json.JSONEncoder):
    """ Encodes a Description object to JSON eg. saves Description self.content str 
    attributes as JSON array """
    def default(self, obj):
        if isinstance(obj, Description):
            return obj.__content
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


class DescriptionDecoder(json.JSONDecoder):
    """ Decodes an Terms object from JSON. """
    def decode(self, string):
        return list(json.JSONDecoder.decode(self, string))
