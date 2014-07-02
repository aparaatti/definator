import json
class Description(object):

    def __init__(self): self.__content = [{}]
        
    def addParagraph(self, text): self.content.append({"paragraph": text})
    def addImage(self, path): self.content.append({"image": str(path)})
    def addSubtitle(self, text): self.content.append({"subtitle": text})
    def load(self, path):
        file = open(path / "description.json", "r")
        self.content = DescriptionDecoder().decode(file.read())
        file.close()
        
    def save(self, path):
        file = open(path / "description.json", "w")
        file.write(DescriptionEncoder().encode(self))
        file.close()
        
    @property
    def content(self): return self.__content.copy()
        
class DescriptionEncoder(json.JSONEncoder):
    """ Encodes a Description object to JSON eg. saves Description self.content str 
    attributes as JSON array """
    def default(self,obj):
        if isinstance(obj, Description):
            return obj.content
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)
    
class DescriptionDecoder(json.JSONDecoder):
    """ Decodes an Terms object from JSON. """
    def decode(self,str):
        return set(json.JSONDecoder.decode(self,str))
