# =============================================================================
#                   Import de la librairie pour les regex
# =============================================================================

import re

# =============================================================================
#                   Implémentation des classes
# =============================================================================

class Document :

    """ Les documents sont stockés sous forme d’objets Document pour lesquels
        on peut accéder aux valeurs de l’identifiant et du texte. Vous pouvez 
        également stocker les autres métadonnées qui permettront d’avoir un 
        affichage plus complet.
    """
    
    def __init__(self, data):
        """
        Constructeur de la classe Document.
        
        Parameters
        ----------
        data : dict(str, object)

        """
        
        self.identifiant = (data['I'])
        if "T" in data : self.titre = data['T']
        else: self.titre = ''        
        if "B" in data : self.date = data['B']
        else: self.date = '' 
        if "A" in data : self.auteur = data['A']
        else: self.auteur = '' 
        if "K" in data : self.mots = data['K']
        else: self.mots = '' 
        if "W" in data : self.texte = data['W']
        else: self.texte = '' 
        if "X" in data : self.liens = data['X']
        else: self.liens = None 

    #Getters
    def getId(self):
        return self.identifiant
    
    def getTitre(self):
        return self.titre
    
    def getDate(self):
        return self.date
    
    def getAuteur(self):
        return self.auteur
    
    def getMC(self):
        return self.mots
    
    def getTexte(self):
        return self.texte
    
    def getLiens(self):
        return self.liens
    
# =============================================================================
#     
# =============================================================================

class Parser :
    
    """ Classe permettant de parser la collection stockée sous la
        forme d'un dictionnaire de Documents.
    """
    
    def __init__(self):
        """
        Constructeur de la classe Parser.

        Returns
        -------
        None.

        """
        self.collection = {}
    
    
    def parse2(self, corpus):
        for i in range(len(corpus)):
            self.collection[i]=Document(corpus[i], i+1)
    
    def parse(self, fic):
        """
        Parameters
        ----------
        fic : str
            Nom du fichier à parser

        Returns
        -------
        None.

        """
        data = {}
        #ouverture du fichier fic en mode lecture
        with open(fic,"r") as f:
            #parcours ligne par ligne du fichier
            lines = f.readlines()
            balise = ''
            cpt = 0
            for line in lines:
                #identifiant du document
                if re.search(r"\.I \w+",line):
                    cpt += 1
                    data[cpt] = {'I':(line[3:-1])}
                #autres balises
                elif re.search(r"^\.\w",line):
                    balise = line[1]
                    if balise == 'X':
                        data[cpt]['X'] = []
                    else:
                        data[cpt][balise] = ''
                #contenu des balises
                else:
                    if balise =='X':
                        if line.split():
                            data[cpt]['X'].append(line.split()[0])
                    else:
                        data[cpt][balise] += line[:-1] + ' '
        
        #ajout de documents dans la collection
        #poser la question propreté ou efficacité
        for k, v in data.items():
            self.collection[k] = Document(v)
            
                        
         
    def getCollection(self):
        return self.collection       

    def getDoc(self, iddoc):
        for k,d in self.collection.items():
            if d.getId()==iddoc :
                return d
        return None
    
    
    


    
    
    
