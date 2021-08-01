import Parsing
import Indexing
import Weighter
import IRModel


class Query:
    
    def __init__(self, id, txt):
        self.idreq = id
        self.texte = txt
        self.l_doc = []
    
    def getIdReq(self):
        return self.idreq
    
    def getTexte(self):
        return self.texte
    
    def getLDoc(self):
        return self.l_doc
    
    
class QueryParser:
    
    def __init__(self, fic_req, fic_pert):
        self.f_req = fic_req
        self.f_pert = fic_pert
        self.q = {}
        self.parse()
        
    def parse(self):
        
        parser = Parsing.Parser()
        parser.parse(self.f_req)
        
        collections = parser.getCollection()
        
        for k,v in collections.items():
            self.q[v.getId()] = Query(v.getId(),v.getTexte())
            
        with open(self.f_pert,"r") as f:
           #parcours ligne par ligne du fichier
           lines = f.readlines()
           
           for line in lines:
               l = line.split()
               id_req = ''
               if l[0][0]=='0':
                   id_req = l[0][1]
               else:
                   id_req = l[0]
                                      
               id_doc = l[1]
               
               self.q[id_req].getLDoc().append(id_doc)
               
    
    def getQ(self):
        #Retourne un dictionnaire de Query
        return self.q
               
# =============================================================================
# Tests
# =============================================================================
"""
#Parser
nomFichier= 'cisi'
p = Parsing.Parser()
p.parse(nomFichier+'/'+nomFichier+'.txt')

#Indexer
i = Indexing.IndexerSimple()
i.indexation(p.getCollection())

#Modèle
w = Weighter.Weighter5(i)
v = IRModel.Vectoriel(w, False)

#Query
q = QueryParser(nomFichier+'/'+nomFichier+'.qry',nomFichier+'/'+nomFichier+'.rel')   
print(q.getQ())        
print(q.getQ()['11'].getIdReq())
print(q.getQ()['11'].getTexte())
print(q.getQ()['11'].getLDoc())
"""