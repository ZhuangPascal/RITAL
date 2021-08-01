#Fichier pour le bonus du TME2

# =============================================================================
# Importation de fichiers et de librairies
# =============================================================================

import numpy as np
import time
import Query
import Metriques
import IRModel
import Parsing
import Indexing
import evalIRModel

# =============================================================================
# Fonctions
# =============================================================================

def trainSplit(q, pourcent):    
    n = len(q.q)
    idQ = list(q.getQ().keys())
    train = {}
    test = {}   
    idTrain = np.random.choice(idQ, int(pourcent*n), replace=False)
            
    for i in idQ:
        if i in idTrain:
            train[i]=q.getQ()[i]
        else:
            test[i]=q.getQ()[i]
    return train, test

# =============================================================================
# Initialisation de variables   
# =============================================================================

nomFichier= 'cacm'

#parse collection
p = Parsing.Parser()
p.parse('../tme1/'+nomFichier+'/'+nomFichier+'.txt')

#index 
i = Indexing.IndexerSimple()
i.indexation(p.getCollection())

#paramètres pour les métriques
k = 20
beta = 1

#dictionnaire des métriques
d_m = {'Precision':Metriques.Precision(k), 'Rappel':Metriques.Rappel(k), 
       'FMesure':Metriques.FMesure(k,beta), 'AvgP':Metriques.AvgP(),
       'ReciprocalRank':Metriques.ReciprocalRank(), 'nDCG':Metriques.NDCG()}

#parse query
q = Query.QueryParser(nomFichier+'/'+nomFichier+'.qry',nomFichier+'/'+nomFichier+'.rel')
q.parse()

# =============================================================================
# Grid-Search  
# =============================================================================
start_time = time.time()

#paramètre modèles
b = np.arange(0.1,1,0.2)
k1 = np.arange(0.7,1.5,0.2)
lamb = np.arange(0.1,1,0.2)

# --------------------------------- Okapi -------------------------------------

train, test = trainSplit(q, 0.8)

res_okapi = []

for ki in k1:
    l = []
    for bi in b:    
        ev = evalIRModel.EvalIRModel({'Okapi':IRModel.Okapi(i,ki,bi)}, d_m,train)
        l.append(ev.evalu())
    res_okapi.append(l)
        
s = np.zeros((len(k1),len(b)))

for ki in range(len(res_okapi)):
    for bi in range(len(res_okapi[ki])):
        # Pour chaque métrique, on calcule la moyenne des moyennes de chaque modèle
        # Pour chaque paramètre, on calcule la moyenne des moyennes de chaque métrique
        s[ki][bi] = np.mean([np.mean([v2[0] for k2,v2 in v.items()]) for k,v in res_okapi[ki][bi].items()])

# On prend l'indice des paramètres ayant le meilleur résultat
kbest, bbest = np.unravel_index(np.argmax(s),s.shape) 


#VALEUR OPTIMALE pour k1 et b trouvées: (2,4)


# -------------------------------- Langue -------------------------------------

# res_langue : [{Métrique : {Modèle : (mean,std)}} for l in lambda]
res_langue = []

for l in lamb:
    ev = evalIRModel.EvalIRModel({'Langue':IRModel.ModeleLangue(i, l)}, d_m, train)
    res_langue.append(ev.evalu())


# 1) Pour chaque métrique, on calcule la moyenne des moyennes de chaque modèle
# 2) Pour chaque lambda, on calcule la moyenne des moyennes de chaque métriques
# 3) On prend le lambda correspondant à la meilleur moyenne

s = [np.mean([np.mean([v2[0] for k2,v2 in v.items()]) for k,v in ri.items()]) for ri in res_langue] 
best2 = lamb[np.argmax(s)]   


#VALEUR OPTIMALE pour lambda trouvée : 0.1 


print("\n --- %s minutes ---" % ((time.time() - start_time)/60)) # --- 9.304767839113872 minutes ---

# =============================================================================
# Sur les données de tests
# =============================================================================

"""
start_time = time.time()

best_k1, best_b = k1[kbest], b[bbest]

best_models = {'Okapi':IRModel.Okapi(i,best_k1,best_b),'Langue':IRModel.ModeleLangue(i,best2)}

evaluateur = evalIRModel.EvalIRModel(best_models, d_m, test)
res_test = evaluateur.evalu()

print("\n --- %s minutes ---" % ((time.time() - start_time)/60))
"""











