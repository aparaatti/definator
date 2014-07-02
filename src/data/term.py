# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
# Author Niko Humalamäki
from description import *
from fileLinks import *

class Term(object):
    """
    Term object. Is given a term string on initialization and tells
    its attributes self.__description and self.__links to initialize.
    
    The description and links JSON files are assumed to be located under
    the project folder in a folder named as self.__term string.
    
    Todo:
        save and delete
        handle missing folder and missing or empty files.
    """    
    def __init__(self, term="New"):
        self.__term = term
        self.__description = Description()
        self.__links = Links()
        
    def __cmp__(self,other): QString.localeAwareCompare(self.term.toLower(),other.term.toLower())
    def __hash__(self): return self.__term.__hash__()
    def __eq__(self,other): return self.__term == other.__term
    def __contains__(self, relatedTerm): return relatedTerm in self.__relatedTerms
    
    @property
    def description(self): return self.__description.copy()
        
    @property
    def links(self): return self.__links.copy()
    
    @property
    def term(self): return self.__term.copy()

    @description.setter
    def description(self, description):
        self.hasChanged = True
        self.__description = value    
    
    @links.setter
    def links(self, links):
        self.__hasChanged = True
        self.__links = value
    
    def linkTerm(self, term):
        self.__links.addLink(term.term,  "term")
        
    def save(self, path):
        self.__links.save(path)
        self.__description.save(path)
        
    def delete(self, path):
        self.__links.delete(path)
        self.__description.delete(path)
