import os
from pathlib import Path

from term import *

class TermsController(object):
    """ 
    Controller class, handles the data objects interoperation and
    loading and saving a project.
    
    Has a set of Term objects. On initialization reads a list of term
    strings from terms.json file and creates Term objects using the
    string as an initializer and adds related links and description to the term.
    """
    def __init__(self, projectPath=None):
        self.projectPath = Path(projectPath)
        self.terms = {};
        
        self.addedTerms = {};
        self.deletedTerms = {};
        self.changedTerms = {};
        
        if os.path.exists(self.projectPath):
            return buildTerms()
        else:
            return initializeNewProject()
            
    def __iter__(self): return self.terms.__iter__()
             
    def buildTerms(self):
        terms = {str(x) for x in p.iterdir() if x.is_dir()}
        for termstr in terms:
            tp = p / termstr
            description = readDescriptionJSON(tp)
            links = readLinksJSON(tp)
            
            term = Term(termstr, description, links)
            self.terms.add(term)
            
    def initializeNewProject(self): self.terms.add(Term())
    
    def getTerms(self): return self.terms.copy()
        
    def addTerm(self, term):
        self.terms.add(term)
        self.addedTerms.add(term)
    
    def remTerm(self, term): self.deletedTerms.add(self.terms.pop(term))
        
    def linkTerms(self, term, relatedTerms):
        for rlTerm in relatedTerms:
            term.linkTerm(rlTerm)
            rlTerm.linkTerm(term)
    
    def saveProject(self):
        if os.path.exists(self.projectPath):
            for term in self.changedTerms: term.save(self.projectPath)
            for term in self.addedTerms: term.save(self.projectPath)
            for term in self.deletedTerms: term.delete(self.projectPath)
        
            self.addedTerms = {}
            self.deletedTerms = {}
        else:
            for term in self.terms: saveTerm(term)

    def __saveTerms(self):
        file = open(projectPath / "terms.json","w")
        file.truncate()
        
        for str in termCodecs.TermsEncoder(self).encode(): file.write(str)
        
        file.close()


class TermsEncoder(json.JSONEncoder):
    """ Encodes a Terms object to JSON eg. saves Term self.__term str 
    attributes as JSON array """
    def default(self,obj):
        if isinstance(obj, Terms):
            terms = []
            for term in obj:
                terms.append(term.term)
            return terms
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)
