import time
import Query
import Metriques
import Weighter
import IRModel
import Parsing
import Indexing
import evalIRModel


# nom du fichier
nomFichier= 'cacm'

#parse collection
p = Parsing.Parser()
p.parse(nomFichier+'/'+nomFichier+'.txt')

#index 
i = Indexing.IndexerSimple()
i.indexation(p.getCollection())

#paramètres pour les métriques
k = 100
beta = 1

#dictionnaire des métriques
d_m = {'Precision':Metriques.Precision(k), 'Rappel':Metriques.Rappel(k), 
       'FMesure':Metriques.FMesure(k,beta), 'AvgP':Metriques.AvgP(),
       'ReciprocalRank':Metriques.ReciprocalRank(), 'nDCG':Metriques.NDCG()}

#liste des Weighters
l_w = [Weighter.Weighter1(i), Weighter.Weighter2(i), Weighter.Weighter3(i), 
       Weighter.Weighter4(i), Weighter.Weighter5(i)]

"""
#dictionnaire des modèles
d_modeles = {f'Vectoriel{wi+1}':IRModel.Vectoriel(l_w[wi], False) for wi in range(len(l_w))}

#Ajout de modèles de langue
d_modeles['Langue'] = IRModel.ModeleLangue(i, 0.2)

#Ajout de modèles de Okapi
d_modeles['Okapi'] = IRModel.Okapi(i)

"""
d_m = {'Precision':Metriques.Precision(k)}

d_modeles = {'Langue':IRModel.ModeleLangue(i, 0.2), 'Okapi':IRModel.Okapi(i)}

#parse query
q = Query.QueryParser('../tme1/'+nomFichier+'/'+nomFichier+'.qry',nomFichier+'/'+nomFichier+'.rel')
q.parse()


start_time = time.time()
#Evaluation
evaluateur = evalIRModel.EvalIRModel(d_modeles,d_m,q.getQ())
res = evaluateur.evalu()


print("\nRésultat final :")
for metrique in d_m.keys():
    print(metrique,":\n",res[metrique],'\n')

#print(res)

print("\n --- %s minutes ---" % ((time.time() - start_time)/60))
