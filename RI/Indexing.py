# =============================================================================
#                       Import des fichiers
# =============================================================================
import TextRepresenter
import math
import json
import Parsing

# =============================================================================
#                   Implémentation des classes
# =============================================================================

class IndexerSimple:
    
    def __init__(self):
        """
        Constructeur de la classe IndexerSimple.

        Returns
        -------
        None.

        """
        
        self.collection = {}
        self.index = {}
        self.index_inv = {}
        self.df = {}
        self.idf = {}
        
        
    def indexation(self, collection):
        """
        Fonction permettant d'indexer une collection.

        Parameters
        ----------
        collection : dict(int, Document)
            La collection à indexer.

        Returns
        -------
        None.

        """
        self.collection = collection
        ps = TextRepresenter.PorterStemmer()
        nbdoc = len(collection)
        
        #Construction des dict. index, index_inv et df
        for i, d in collection.items():
            tr = ps.getTextRepresentation(d.getTexte())
            docId=d.getId()
            self.index[docId] = tr
            
            for k,v in tr.items():
                if k not in self.index_inv:
                    self.index_inv[k] = {docId:v}
                else : 
                    self.index_inv[k][docId] = v
                   
                if k not in self.df:
                    self.df[k] = 1
                else:
                    self.df[k] += 1
        
        #calcul des idf
        self.idf = {mot:math.log((1+nbdoc)/(1+val)) for mot, val in self.df.items()}
                    
                    
    #Getters 
    
    def getTfsForDoc(self, numDoc):
        """
        Retourne la représentation (stem-tf) d’un document a partir de
        l’index.

        Parameters
        ----------
        numDoc : int
            Numero du document à traiter

        Returns
        -------
        dict(str, int)
            Le dictionnaire tf du document numDoc

        """
        if numDoc in self.index.keys():
            return self.index[numDoc]
        else:
            return {}
    
        
    def getTfIDFsForDoc(self, numDoc):
        """
         Retourne la représentation (stem-TFIDF) d’un document a partir
         de l’index.

        Parameters
        ----------
        numDoc : int
            Numero du document à traiter

        Returns
        -------
        dict(str,float)
            Le dictionnaire tf-idf 

        """
        tf = self.getTfsForDoc(numDoc)
        print(tf)
        print()
        return {mot:tf[mot]*self.idf[mot] for mot, val in tf.items()}
   
    def getTfsForStem(self, stem):
        """
        Retourne la représentation (doc-tf) d’un stem a partir de l’index
        inverse 

        Parameters
        ----------
        stem : str
            Mot à traiter

        Returns
        -------
        dict(int,float)
            Le dictionnaire tf pour le mot stem

        """
        if stem in self.index_inv.keys():
            return self.index_inv[stem]
        else:
            return {}
   
    def getTfIDFsForStem(self, stem):    
        """
        Retourne la représentation (doc-TFIDF) d’un stem a partir de
        l’index inverse.

        Parameters
        ----------
        stem : str
            Mot à traiter

        Returns
        -------
        None.

        """
        tf = self.getTfsForStem(stem)
        return {mot:tf[mot]*self.idf[stem] for mot, val in tf.items()}
        
   
    def getStrDoc(self, numDoc):
        """"""
        for i, document in self.collection.items():
            if document.getId()==numDoc:
                return document.getTexte()[:-1]
                
        
    def getCollection(self):
        return self.collection
    
    def getIndex(self):
        return self.index
    
    def getIndexInv(self):
        return self.index_inv
    
    def getDf(self):
        return self.df
    
    def getIdf(self):  
        return self.idf
    
    
def ecrire(dict,nomFichier="../tme1/cisi/collectionCISI.txt" ):
    with open(nomFichier, 'w', encoding='utf-8') as file:
        json.dump(dict, file)
        
def lire(nomFichier='../tme1/cisi/collectionCISI.txt'):
    with open(nomFichier, 'r',encoding='utf-8' ) as file:
        return json.load(file)
        

# =============================================================================
# Tests
# =============================================================================

"""
#Parser
p = Parsing.Parser()
p.parse("cisi/cisi.txt")

print(p.getCollection()[1].getId())

#Indexer
i = IndexerSimple()
i.indexation(p.getCollection())

print(i.getTfsForDoc('50'))

print(i.getTfIDFsForDoc('60'))

print(i.getTfsForStem('detail'))

print(i.getTfIDFsForStem('detail'))
"""
        
        
        
            