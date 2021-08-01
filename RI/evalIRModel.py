import time
import numpy as np
from scipy import stats


class EvalIRModel:
    def __init__(self, dictIRModel, dictMetric, q):
        self.models =  dictIRModel
        self.metrics = dictMetric
        self.q=q
        
    def evalSimple(self, idquery, model, metric):
        rank = self.models[model].getRanking(self.q[idquery].getTexte())
        return self.metrics[metric].evalQuery(rank, self.q[idquery])
        
    
    def evalu(self):
        
        res = {}
        for me in self.metrics.keys():
            res[me]={}
            for mod in self.models.keys():
                print("Evaluation de la métrique",me,"du modèle", mod,"...")
                start_time = time.time()
                eva = np.array([self.evalSimple(i,mod,me) for i in self.q.keys()])
                res[me][mod] = (np.mean(eva),np.std(eva))
                print("\n --- %s secondes ---" % (time.time() - start_time))
            print("\nResultat",me,":\n",res[me],'\n')
        return res
    
    
    def ttest(self, x, y, a=0.05):
        n = len(x)
        moy_x = np.mean(x)
        moy_y = np.mean(y)
        s_x = (1/n-1) * np.sum((x-moy_x)**2)
        s_y = (1/n-1) * np.sum((y-moy_y)**2)
        
        #t-statistic
        t = (moy_x-moy_y)/np.sqrt((s_x+s_y)/n)
        
        #degré de liberté
        ddl = (2*n)-2
        #valeur critique
        vc = stats.t.ppf(1 - a/2, ddl)
        
        return t, vc, np.abs(t) <= vc
    
    
#Tests dans le fichier Test.py