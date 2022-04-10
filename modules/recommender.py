import warnings
warnings.filterwarnings('ignore')

import tensorflow as tf
import pandas as pd
import seaborn as sns
sns.set_color_codes()
sns.set(style="whitegrid")
import numpy as np # linear algebra
from scipy.sparse.linalg import svds
from abc import ABC
tf.__version__

class Collaborative(ABC):
    def __init__(self):
        pass

class SVD(Collaborative):
    def __init__(self, n_vectors, index, columns, values, aggfunc):
        self.n_vectors = n_vectors
        self.index = index
        self.columns = columns
        self.values = values
        self.aggfunc = aggfunc
    
    def build_pivot_tables(self, df_reviews_train, df_reviews_test):
        self.df_reviews_train = df_reviews_train
        self.x_pivot = df_reviews_train.pivot_table(index=self.index, columns=self.columns, values=self.values, aggfunc=self.aggfunc).fillna(0)
        self.y_pivot = df_reviews_test.pivot_table(index=self.index, columns=self.columns, values=self.values, aggfunc=self.aggfunc).fillna(0)
        return self.x_pivot, self.y_pivot
    
    def get_predictions(self):
        if self.x_pivot is None:
            print('There is no pivot table to get predictions from.')

        U, sigma, Vt = svds(self.x_pivot, k = self.n_vectors)
        # Construct diagonal array in SVD
        sigma = np.diag(sigma)
        all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) 
        # Predicted ratings TRAIN
        self.preds = pd.DataFrame(all_user_predicted_ratings, columns= self.x_pivot.columns, index=self.x_pivot.index)
        return self.preds