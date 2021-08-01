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

def k_fold(q, k):
    #nombre d'éléments dans un fold
    taille_k = len(q.q)//k
    
    #on récupère et mélange les clés de la collection de Query
    melange = np.array([i for i in list(q.q.keys())])
    np.random.shuffle(melange)
    
    k_folds = []
    
    for ki in range(k):
        cles = melange[ki*taille_k:(ki+1)*taille_k].tolist()
        k_folds.append({ci:q.getQ()[ci] for ci in cles})
    
    return k_folds
        
# =============================================================================
# Initialisation de variables   
# =============================================================================

nomFichier= 'cacm'

#parse collection
p = Parsing.Parser()
p.parse(nomFichier+'/'+nomFichier+'.txt')

#index 
indexing = Indexing.IndexerSimple()
indexing.indexation(p.getCollection())

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

cles = q.q.keys()

# =============================================================================
# Cross-Validation
# =============================================================================

start_time = time.time()

#paramètre modèles
b = np.arange(0.1,1,0.2)
k1 = np.arange(0.7,1.5,0.2)
lamb = np.arange(0.1,1,0.2)

# --------------------------------- Okapi ------------------------------------- 

k_folds = k_fold(q, k=3)

res_okapi = np.zeros((len(k1),len(b)))

for ki in range(len(k1)):
    for bi in range(len(b)):
        r = []
        for fi in k_folds:
            train = {ci:q.getQ()[ci] for ci in cles if ci not in fi}
            ev = evalIRModel.EvalIRModel({'Okapi':IRModel.Okapi(indexing,k1[ki],b[bi])}, d_m, train)
            r.append(ev.evalu())
            
        res_okapi[ki][bi] = np.mean([np.mean([np.mean([v2[0] for k2,v2 in v.items()]) for k,v in ri.items()]) for ri in r])

#Paramètres optimaux          
kbest, bbest = np.unravel_index(np.argmax(res_okapi),res_okapi.shape) #2,4

#VALEUR OPTIMALE pour k1 et b trouvées: (2,4)


time_okapi = (time.time() - start_time)/60 #7 minutes

# -------------------------------- Langue ------------------------------------- 

res_langue = []

for l in lamb :
    r = []
    for fi in k_folds:
        train = {ci:q.getQ()[ci] for ci in cles if ci not in fi}    
        ev = evalIRModel.EvalIRModel({'Langue':IRModel.ModeleLangue(indexing, l)}, d_m, train)
        r.append(ev.evalu())
    #moyenne de chaque fold  
    f = [np.mean([np.mean([v2[0] for k2,v2 in v.items()]) for k,v in ri.items()]) for ri in r]
    #moyenne des folds
    res_langue.append(np.mean(f))

#Paramètres optimaux  
best = lamb[np.argmax(res_langue)] #0.1

#VALEUR OPTIMALE pour lambda trouvée : 0.1 


time_langue = ((time.time() - start_time)/60) - time_okapi #17 minutes

    
# =============================================================================
# MAP    
# =============================================================================

d_m = { 'AvgP':Metriques.AvgP()}

# --------------------------------- Okapi -------------------------------------

res_okapi = np.zeros((len(k1),len(b)))

for ki in range(len(k1)):
    for bi in range(len(b)):
        r = []
        for fi in k_folds:
            train = {ci:q.getQ()[ci] for ci in cles if ci not in fi}
            ev = evalIRModel.EvalIRModel({'Okapi':IRModel.Okapi(indexing,k1[ki],b[bi])}, d_m, train)
            r.append(ev.evalu())
            
        res_okapi[ki][bi] = np.mean([np.mean([np.mean([v2[0] for k2,v2 in v.items()]) for k,v in ri.items()]) for ri in r])

#Paramètres optimaux        
kbest_map, bbest_map = np.unravel_index(np.argmax(res_okapi),res_okapi.shape) #3,3

#VALEUR OPTIMALE pour k1 et b trouvées: (3,3)


# -------------------------------- Langue -------------------------------------
res_langue = []

for l in lamb :
    r = []
    for fi in k_folds:
        train = {ci:q.getQ()[ci] for ci in cles if ci not in fi}    
        ev = evalIRModel.EvalIRModel({'Langue':IRModel.ModeleLangue(indexing, l)}, d_m, train)
        r.append(ev.evalu())
    #moyenne de chaque fold  
    f = [np.mean([np.mean([v2[0] for k2,v2 in v.items()]) for k,v in ri.items()]) for ri in r]
    #moyenne des folds
    res_langue.append(np.mean(f))

#Paramètres optimaux  
best_map = lamb[np.argmax(res_langue)] #0.1

#VALEUR OPTIMALE pour lambda trouvée : 0.1 


time_map = ((time.time() - start_time)/60) - time_langue - time_okapi #4 minutes


print("\n --- Temps Okapi %s minutes ---" % (time_okapi))
print("\n --- Temps Langue %s minutes ---" % (time_langue))  
print("\n --- Temps MAP %s minutes ---" % (time_map))  

#28 minutes au total




    