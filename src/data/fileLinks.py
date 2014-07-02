class Links(object):
    """
    Hanldes linking. Has a key word and value eg.
    "term" links to a term, 
    "image" links to name of image file, 
    "file" links to name of file.
    """
    def __init__(self, path):
        self.allowedTypes = ["term", "image", "file"];
        self.types = [];
        self.values = [];
        
    def addLink(self, value, type):
        if type not in self.allowedTypes:
            return False
            
        if value not in self.values:
            self.types.append(type)
            self.value.append(value)
            
        return True

            
    def getLinks(self):
        pass
    
