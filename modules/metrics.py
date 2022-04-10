from audioop import avg
import warnings
warnings.filterwarnings('ignore')

from abc import ABC, abstractmethod
import itertools
import numpy as np

class Metric(ABC):
    def __init__(self, cutoff, threshold):
        self.cutoff = cutoff
        self.threshold = threshold
        self.result_values = []
        self.avg = 0.0

    @abstractmethod
    def evaluate(self, y_true, recommendations):
        pass

    @abstractmethod
    def to_string(self, debug=False):
        pass

    def get_metric_average(self):
        return np.average(self.result_values)

    def score(self, df_reviews, user, ranking, debug=False, decimals=None):
        items = df_reviews[df_reviews['reviewerID'] == user]
        
        y_true = {}
        for _, row in items.iterrows():
            y_true[row['asin']] = row['overall']

        self.evaluate(y_true=y_true, recommendations=ranking)
        self.to_string(debug, decimals=decimals)
        
    
    def score_CF(self, user, ranking, pivot, debug=False, decimals=None):
        # Get and sort the user's ratings
        sorted_user_ratings = pivot.loc[user].sort_values(ascending=False)
        rating = sorted_user_ratings.to_frame(name='ratings')

        y_true = {}
        for index, row in rating.iterrows():
            if index in y_true:
                y_true[index] = y_true[index] + row[0]
            else:
                y_true[index] = row[0]
        
        self.evaluate(y_true=y_true, recommendations=ranking)
        self.to_string(debug, decimals=decimals)


class PrecisionAtK(Metric):
    def evaluate(self, y_true, recommendations):
        # Coger solo el topK k -> cutoff
        dict_cutoff = dict(itertools.islice(recommendations.items(), self.cutoff))
        viewed, relevant = 0, 0

        # Por cada recomendacion
        for item in dict_cutoff:
            # Lo visitamos
            viewed += 1
            # Si está en los items que le han gustado al usuario (valorado)
            if item in y_true:
                # Y el rating es mayor al umbral
                if y_true[item] > self.threshold:
                    # Es relevante la recomendación
                    relevant += 1
        
        self.result_values.append(relevant/viewed)
        return self.result_values
    
    def to_string(self, debug=False, decimals=None):
        avg, values = self.get_metric_average(), self.result_values
        if decimals:
            avg = round(avg, decimals)
            values = np.round(self.result_values, decimals=decimals)

        print('Average Precision@' + str(self.cutoff), avg)
        if debug:
            print('Values of Precision@' + str(self.cutoff), values)

class RecallAtK(Metric):
        
    def evaluate(self, y_true, recommendations):
        dict_cutoff = dict(itertools.islice(recommendations.items(), self.cutoff))
        relevant, relevantReturned = 0, 0

        # Por cada item que le ha gustado al usuario
        for item in y_true:
            # Contamos cuantos items son relevantes
            if y_true[item] > self.threshold:
                relevant += 1
        
        value = 0.0
        # Si hay items relevantes
        if relevant > 0:
            # Por cada item recomendado
            for element in dict_cutoff:
                # Si está en los items que le han gustado al usuario (valorado)
                if element in y_true:
                    # Y el rating es mayor al umbral
                    if y_true[element] > self.threshold:
                        # Es relevante la recomendación
                        relevantReturned +=1 

            value = relevantReturned/relevant
        
        self.result_values.append(value)
        return self.result_values
    
    def to_string(self, debug=False, decimals=None):
        avg, values = self.get_metric_average(), self.result_values
        if decimals:
            avg = round(avg, decimals)
            values = np.round(self.result_values, decimals=decimals)

        print('Average Recall@' + str(self.cutoff), avg)
        if debug:
            print('Values of Recall@' + str(self.cutoff), values)
        

