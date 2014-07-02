import json

class TermLinks(object):
    """
    Handles linked terms and files.
    """
    def __init__(self): self.__links = []
        
    def addTermLink(self, value,  types): self.__links.add({"term": value})
    def remTermLink(self, value): self.__links.rem({"term": value})
    def addImage(self, path): 
        #kopioi oikeaan paikkaan
        #self.__links.add({"image": str(path)})
        pass
        
    def remImage(self, path): 
        #poista kuva
        #self.__links.rem({"image": str(path)})
        pass
        
    def addFile(self, path):
        #poista tiedosto"
        #self.__links.rem({"file": filename})
        pass
        
    def __getLinkedType(self, type):
        linked = []
        for value in self.__links:
            if self.__links[value] == type:
                linked.append(value)
        return linked
        
    def getLinkedTerms(self): return self.__getLinkedType("term")
    def getLinkedImages(self): return self.__getLinkedType("image")
    def getLinkedFiles(self): return self.__getLinkedType("file")
    
    def save(self, path):
        pass
    
    def load(self, path):
        pass

class LinksEncoder(json.JSONEncoder):
    """ Encodes a Terms object to JSON eg. saves Term self.__term str 
    attributes as JSON array """
    def default(self,obj):
        if isinstance(obj, TermLinks):
            return obj.__links
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)
    
        
class LinksDecoder(json.JSONDecoder):
    """ Decodes an Terms object from JSON. """
    def decode(self,str):
        return set(json.JSONDecoder.decode(self,str))
        
