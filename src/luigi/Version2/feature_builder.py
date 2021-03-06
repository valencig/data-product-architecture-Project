import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer

class FeatureBuilder():
    def __init__(self):
        pass
    def featurize(self, X):
        X1 = X.copy()
        num_cols = X1.dtypes.pipe(lambda x: x[x != 'object']).index
        for x in num_cols:
            imp = SimpleImputer(missing_values = np.nan, strategy = 'median')
            imp.fit(np.array(X1[x]).reshape(-1, 1))
            X1[x] = imp.transform(np.array(X1[x]).reshape(-1, 1))

        nominal_cols = X1.dtypes.pipe(lambda x: x[x == 'object']).index
        for x in nominal_cols:
            imp = SimpleImputer(missing_values = np.nan, strategy = 'most_frequent')
            imp.fit(np.array(X1[x]).reshape(-1, 1))
            X1[x] = imp.transform(np.array(X1[x]).reshape(-1, 1))
        
        X1['fecha'] = pd.to_datetime(X1['fecha'])
        X1['dia'] = pd.DatetimeIndex(X1['fecha']).day.astype('object')
        X1['mes'] = pd.DatetimeIndex(X1['fecha']).month.astype('object')
        X1['dia_semana'] = (pd.DatetimeIndex(X1['fecha']).weekday + 1).astype('object')
        #X1['fecha'] = pd.to_datetime(X1['fecha']).astype('object')

        variables_categoricas = X1.dtypes.pipe(lambda x: x[x == 'object']).index
        x_mat = pd.get_dummies(X1, columns = variables_categoricas, drop_first = True)
        
        return(x_mat)
        
