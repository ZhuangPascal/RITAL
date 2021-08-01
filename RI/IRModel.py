import TextRepresenter
import math
import Parsing
import Indexing
import Weighter

class IRModel:
    def _init_(self,index):
        self.index  = index
        
    def getScores(self, query):
        pass
    
    def getRanking(self, query):
        scores = self.getScores(query)
        return [(cle,val) for cle,val in sorted(scores.items(), key=lambda t: t[1], reverse=True) if val > 0]
    
    
class Vectoriel(IRModel):
    def __init__(self, weighter, normalized):
        """
        Si normalized est à True calcul avec score cosinus, si False produit scalaire
        """
        self.weighter = weighter
        self.normalized = normalized
        self.normeDoc = dict()
        if self.normalized:
            #car calcul score cosinus
            self.calculNormeDoc()
            
            
    def calculNormeDoc(self):
        """
            Calcule la norme de tous les doc
        """
        for doc, index in self.weighter.index.index.items():
            norme=0
            for mot, nb in index.items():
                norme+=nb**2
            self.normeDoc[doc]=math.sqrt(norme)
            
            
    def getScores(self,query):
        """
        Retourne le score pour chaque doc en fonction de normaliazed

        """
        if self.normalized:
            return self.getScoreCosinus(query)
        else:
            return self.getScoreScalaire(query)


    def getScoreScalaire(self,query):
        
        poidsInRequete = self.weighter.getWeightsForQuery(query)
        indexDocs = self.weighter.index.index
        
        poidsInDoc = dict()
        
        for i in poidsInRequete:
            poidsInDoc[i]=self.weighter.getWeightsForStem(i)
            
        s={}
        
        for index in indexDocs:
            somme = sum([poidsInDoc[key][index]*poidsInRequete[key] for key in set(poidsInRequete.keys()) & set(indexDocs[index].keys())])
            s[index]=somme
        
        return s



    def getScoreCosinus(self,query):
        """
            Retourne le score cosinus
        """
    
        scalaire = self.getScoreScalaire(query)
        ps = TextRepresenter.PorterStemmer()
        req = ps.getTextRepresentation(query)
        norme = 0
        for mot, occ in req.items():
            norme+=occ**2
        
        norme = math.sqrt(norme)
        
        for doc, score in scalaire.items():
            scalaire[doc]=score/(norme+self.normeDoc[doc])
        
        return scalaire
            


class ModeleLangue(IRModel):
    def __init__(self, index, lamb=0.8):
        """
        lambda = 0.8 si req courte sinon 0.2

        """
        self.index = index
        self.ind = index.getIndex()
        self.indinv = index.getIndexInv()
        self.lamb=lamb
        self.indkeys = list(self.ind.keys())
        self.nbMotDoc = [sum(list(self.ind[doc].values())) for doc in self.ind]
        self.nbMot = sum(self.nbMotDoc)
    
    def getScores(self, query):
        """
        """
        ps = TextRepresenter.PorterStemmer()
        req = ps.getTextRepresentation(query)
        
        score = dict()
        
        for doc in range(len(self.indkeys)):
            nbMotDoc = self.nbMotDoc[doc]
            s=1
            for mot in req:
                if mot in self.indinv:
                    tfDoc = self.ind[self.indkeys[doc]]
                    
                    ptMc = (1-self.lamb) * sum(self.indinv[mot].values())/self.nbMot
                    
                    if mot in tfDoc:
                        ptMd = self.lamb*(tfDoc[mot]/nbMotDoc)
                        s*=(ptMc + ptMd)
                    else:
                        s*=(ptMc)
                        
            score[self.indkeys[doc]]=s

        return score
                
  
     
class Okapi(IRModel):
    
    def __init__(self,index, k1=1.2, b=0.75):
        self.ind = index.getIndex()
        self.idf = index.getIdf()
        self.avgdl = self.calculAvgdl()
        self.k1 = k1
        self.b = b
        self.indkeys = list(self.ind.keys())
        self.nbMotDoc = [sum(list(self.ind[doc].values())) for doc in self.indkeys]
    
    
    def calculAvgdl(self):
        somme = sum([sum(list(self.ind[doc].values())) for doc in self.ind])
        return somme / len(self.ind)
    
    def getScores(self, query):

        req = TextRepresenter.PorterStemmer().getTextRepresentation(query)
        
        scores = dict()
        
        for doc in range(len(self.indkeys)):
            score = 0
            nbMotDoc = self.nbMotDoc[doc]
            for mot in req:
                indexMot = self.ind[self.indkeys[doc]]
                if (mot in indexMot):
                    idf = self.idf[mot]
                    tf = req[mot]
                    score += idf * (tf/(tf+(self.k1) * (1-self.b+self.b*(nbMotDoc/self.avgdl))))
            scores[self.indkeys[doc]]=score
        return scores

        
# =============================================================================
# Tests
# =============================================================================
"""
#Parser
p = Parsing.Parser()
p.parse('../tme1/cisi/cisi.txt')

#Indexer
i = Indexing.IndexerSimple()
i.indexation(p.getCollection())

#Weighter
w = Weighter.Weighter5(i)

#Modèle vectoriel
v=Vectoriel(w, False)
print('Vectoriel',v.getRanking('reveal  high common hold shown')[:10])

#Modèle de langue
l=ModeleLangue(i)
print('Langue',l.getRanking('reveal  high common hold shown')[:10])

#Modèle Okapi
o=Okapi(i)
print('Okapi',o.getRanking('reveal  high common hold shown')[:10])
"""











            