import TextRepresenter
import numpy as np
import math
import Indexing
import Parsing


class Weighter:
    def __init__(self, index):
        """
            index: IndexerSimple
        
        """
        self.index = index
        
        
    def getWeightsForDoc(self,idDoc):
        """
        Parameters
        ----------
        idDoc : String
            le nom du document ex: '1'

        Returns
        -------
        None.

        """
        pass
    
    def getWeightsForStem(self,stem):
        """

        Parameters
        ----------
        stem : string
            C'est un terme.

        Returns
        -------
        None

        """
        pass
    
    
    def  getWeightsForQuery(self, query):
        pass
    
    
    
class Weighter1(Weighter):
    
    def getWeightsForDoc(self, idDoc):
        return self.index.getTfsForDoc(idDoc)
    
    def getWeightsForStem(self,stem): 
        return self.index.getTfsForStem(stem)
        
    def getWeightsForQuery(self, query):
        ps = TextRepresenter.PorterStemmer()
        req = ps.getTextRepresentation(query)
        return {i:1 for i in req}
    
    
class Weighter2(Weighter):
    
    def getWeightsForDoc(self, idDoc):
        return self.index.getTfsForDoc(idDoc)
    
    def getWeightsForStem(self,stem): 
        return self.index.getTfsForStem(stem)
    
    def getWeightsForQuery(self, query):
        ps = TextRepresenter.PorterStemmer()
        return ps.getTextRepresentation(query)
    
class Weighter3(Weighter):
    
    def getWeightsForDoc(self, idDoc):
        return self.index.getTfsForDoc(idDoc)
    
    def getWeightsForStem(self,stem): 
        return self.index.getTfsForStem(stem)
    
    def getWeightsForQuery(self, query):
        idf = self.index.getIdf()
        ps = TextRepresenter.PorterStemmer()
        req = ps.getTextRepresentation(query)
        return {key : idf[key] for key in set(req) & set(idf.keys())}
    
class Weighter4(Weighter):
    
    def getWeightsForDoc(self, idDoc):
        i = self.index.getTfsForDoc(idDoc)
        return {key : 1+np.log(i[key]) for key in i}
    
    def getWeightsForStem(self,stem): 
        i = self.index.getTfsForStem(stem)
        return {key : 1+np.log(i[key]) for key in i}
    
    def getWeightsForQuery(self, query):
        idf = self.index.getIdf()
        ps = TextRepresenter.PorterStemmer()
        req = ps.getTextRepresentation(query)
        return {key : idf[key] for key in set(req) & set(idf.keys())}
    
class Weighter5(Weighter):
    
    def getWeightsForDoc(self, idDoc):
        idf = self.index.getIdf()
        i = self.index.getTfsForDoc(idDoc)
        return {key : (1+math.log(i[key]))*idf[key] for key in i}
    
    def getWeightsForStem(self,stem): 
        idf = self.index.getIdf()
        i = self.index.getTfsForStem(stem)
        return {key : (1+np.log(i[key]))*idf[stem] for key in i}
    
    def getWeightsForQuery(self, query):
        idf = self.index.getIdf()
        ps = TextRepresenter.PorterStemmer()
        req = ps.getTextRepresentation(query)
        return {key : (1+np.log(req[key]))*idf[key] for key in set(req.keys()) & set(idf.keys())}
    
    
    
# =============================================================================
# Tests
# =============================================================================
"""
#Parser
p = Parsing.Parser()
p.parse("cisi/cisi.txt")

#Indexer
i = Indexing.IndexerSimple()
i.indexation(p.getCollection())

#Weighter1
w = Weighter1(i)
print(w.getWeightsForDoc('1'))
print(w.getWeightsForStem('reveal'))
print(w.getWeightsForQuery('reveal cucu ok lol pour voir voir medical identifier reveal'))

#Weighter2
w = Weighter2(i)
print(w.getWeightsForDoc('1'))
print(w.getWeightsForStem('reveal'))
print(w.getWeightsForQuery('reveal cucu ok lol pour voir voir medical identifier reveal'))

#Weighter3
w = Weighter3(i)
print(w.getWeightsForDoc('1'))
print(w.getWeightsForStem('reveal'))
print(w.getWeightsForQuery('reveal cucu ok lol pour voir voir medical identifier reveal'))

#Weighter4
w = Weighter4(i)
print(w.getWeightsForDoc('1'))
print(w.getWeightsForStem('reveal'))
print(w.getWeightsForQuery('reveal cucu ok lol pour voir voir medical identifier reveal'))

#Weighter5
w = Weighter5(i)
print(w.getWeightsForDoc('1'))
print(w.getWeightsForStem('reveal'))
print(w.getWeightsForQuery('reveal cucu ok lol pour voir voir medical identifier reveal'))
"""
    