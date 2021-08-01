from abc import ABC
import numpy as np

class EvalMesure(ABC):
    
    def __init__(self):
        pass
    
    def evalQuery(self, liste, query):
        pass
    
class Precision(EvalMesure):
    
    def __init__(self, k):
        self.k = k
        
    def evalQuery(self, liste, query):
        rank = liste[:self.k]
        listeP = query.getLDoc()
        s=0
        
        for i in range(len(rank)):
            if i<len(rank):
                doc, _ = rank[i]
                if doc in listeP:
                    s+=1
        
        return s/self.k
    
    def getK(self):
        return self.k
    
class Rappel(EvalMesure):
    
    def __init__(self, k):
        self.k = k
        
    def evalQuery(self, liste, query):
        rank = liste[:self.k]
        listeP = query.getLDoc()
        s=0
        
        if len(listeP) == 0:
            return 1
        
        for i in range(len(rank)):
            if i<len(rank):
                doc, _ = rank[i]
                if doc in listeP:
                    s+=1
        
        return s/len(listeP)
    

class FMesure(EvalMesure):
    
    def __init__(self, k, beta):
        self.k = k
        self.beta = beta
        self.precision = Precision(k)
        self.rappel = Rappel(k)
        
    def evalQuery(self, liste, query):     
        num =  (1+self.beta**2)*self.precision.evalQuery(liste,query)*self.rappel.evalQuery(liste,query)
        denum = ((self.beta**2)*self.precision.evalQuery(liste,query))+self.rappel.evalQuery(liste,query)
        
        if denum == 0:
            return 0
        
        return num/denum
    
    
class AvgP(EvalMesure):
    
    def __init__(self):
        super().__init__()
        
    def evalQuery(self, liste, query):
        avgp = 0
        listeP = query.getLDoc()
        if len(listeP) == 0:
            return 0
        
        for l in range(len(liste)):
            doc, _ = liste[l]
            if doc in listeP:  
                precision = Precision(l+1)
                avgp += precision.evalQuery(liste,query)
        
        return avgp/len(listeP)
        
class MAP(EvalMesure):
    
    def __init__(self):
        self.agvp = AvgP()
        
    def evalQuery(self, liste, query):
        listeP = query.getLDoc()
            
        for l in range(len(liste)):
            doc, _ = liste[l]
            if doc in listeP:
                return 1/(l+1)
        
        return 0        

class ReciprocalRank(EvalMesure):
    
    def __init__(self):
        super().__init__()
        
    def evalQuery(self, liste, query):
        listeP = query.getLDoc()
            
        for l in range(len(liste)):
            doc, _ = liste[l]
            if doc in listeP:
                return 1/(l+1)
        
        return 0
             
    
class NDCG(EvalMesure):
    def __init__(self):
        super().__init__()
        
    def evalQuery(self, liste, query):
        dcg = 0
        idcg = 0
        listeP = query.getLDoc()
        
        if len(listeP) == 0:
            return 0
        
        for i in range(len(liste)):
            doc, r= liste[i]
            if doc in listeP:
                dcg+= 1/np.log2(i+2)

        for i in range(len(listeP)):
            idcg+= 1/np.log2(i+2)
              
        return dcg/idcg
    
    
    
    
    
    
    
    
    
    
    