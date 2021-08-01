# =============================================================================
# Importation de fichiers et de librairies
# =============================================================================

import Parsing
import Indexing
import Query
import IRModel
import numpy as np
import CrossValidation as cv
import Metriques
import evalIRModel

# =============================================================================
# Fonctions
# =============================================================================

#Calcule de façon itérative les scores pour chacun des noeuds
def score(P,iteration,d=0.85, aj=1):
    # P : Une matrice de transition
    nbPage= P.shape[1]
    s = np.array([1/nbPage for i in range(nbPage)])
    for it in range(iteration):
        tmp = s.copy()
        for i in range(P.shape[0]):
            tmp[i] = d * np.sum(P[:,i]*s) + ((1-d) * aj)
        s = tmp / np.sum(s)
    return s

#Récupère les documents qui citent le document donné en paramètre
def getHyperlinksTo(parser, doc):
    res = []
    for k,d in parser.getCollection().items():
        if doc in d.getLiens():
            res.append(d.getId())     
    return res

#Récupère les documents cités par le document donné en paramètre
def getHyperlinksFrom(parser, doc):
    return parser.getDoc(doc).getLiens()


#Construit la matrice de transition d'un graphe
def dict_to_mat(g):
    #On récupère les documents présents dans le graphe
    flat_list = set([item for sublist in g.values() for item in sublist])
    docs = sorted(list(set(g.keys()).union(set(flat_list))))
    
    #On construit la matrice de transition résultat
    res = np.zeros((len(docs),len(docs)))
    for k, v in g.items():
        res[docs.index(k)] = [v.count(d)/len(v) for d in docs]
    
    return res, docs

def modele_graph(parser, model,  n, k, dquery):
    """
    Définir des modèles de recherche documentaire basés sur ces algorithmes 
    à base de marche aléatoire sur des graphes.

    Parameters
    ----------
    model : IRModel
       Le modèle de base permettant de récupérer les documents seeds
    n : int
        Le paramètre n déterminant le nombre de documents seeds à considérer
    k : int
        Le paramètre k déterminant le nombre de liens entrants à considérer pour chaque document seed
    dquery : dict(str, Query)
        Le dictionnaire contenant les requêtes
        
    Return
    ------
    res : list(list(str))
        La liste des graphes.
    
    """
    #Liste qui contiendra les graphes des requêtes
    res = []
    
    #Parcours de chaque requête Q
    for idq, query in dquery.items():
        #seeds : liste des n premiers documents du ranking de model sur query
        seeds = np.array(model.getRanking(query.getTexte())[:n])[:,0].tolist()
        
        #Initialisation des VQ dans le graphes
        graphe = {s:[] for s in seeds}
        
        #Parcours sur l'ensemble S des documents seeds
        for seed in seeds:
            #Ajout dans VQ de tous les documents pointés par le document seed
            graphe[seed] += getHyperlinksFrom(parser, seed)
            #Liens pointants vers le document seed
            linksTo = getHyperlinksTo(parser, seed)
            
            #Condition pour vérifier qu'il y a au moins un lien entrant
            if linksTo:
                nb = len(linksTo)
                #On choisi aléatoirement s'il y a plus de k liens entrants
                if nb > k:
                    rand = np.random.choice(linksTo, k, replace=False).tolist()
                #On sélectionne tous les liens si il y a moins de k liens
                else:
                    rand = linksTo 
                    
                #Ajout dans VQ des liens entrants   
                graphe[seed] += rand

        res.append(graphe)
        
    return res



# =============================================================================
# Initialisation des variables de tests  
# =============================================================================

# nom du fichier
nomFichier= 'cacm'

#parse collection
p = Parsing.Parser()
p.parse(nomFichier+'/'+nomFichier+'.txt')

#index 
i = Indexing.IndexerSimple()
i.indexation(p.getCollection())

#parse query
q = Query.QueryParser(nomFichier+'/'+nomFichier+'.qry',nomFichier+'/'+nomFichier+'.rel')
q.parse()
cles = q.q.keys()

#Facteur d'amortissement
d=0.85
#Probabilité a priori
aj=1

#Modèle de base permettant de récupérer les documents seeds
modele = IRModel.Okapi(i)
#Paramètre n déterminant le nombre de documents seeds à considérer 
n = 20
#Paramètre k déterminant le nombre de liens entrants à considérer pour chaque document seed
k = 20
#Itération
iteration = 100

# =============================================================================
# Tests
# =============================================================================
"""
#Liste de graphes correspondant aux requêtes
liste_graph = modele_graph(p,modele,n,k,q.q)
#Matrice de transition associée à un graphe
P, indexP = dict_to_mat(liste_graph[0])

#Scores
print(score(P,iteration,d, aj))
"""


