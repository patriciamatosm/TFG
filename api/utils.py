import sys 
sys.path.append(r'C:\\Users\\pmato\\OneDrive\\Desktop\\TFG')
from modules.functions import *
from modules.recommendation import *
from sklearn.model_selection import train_test_split
import pickle

def read_predictions_cache():
    predictions_cache = {}
    with open("../file/resnet.pickle", "rb") as f:
        predictions_cache['resnet'] = pickle.load(f)
    
    with open("../file/vgg.pickle", "rb") as f:
        predictions_cache['vgg'] = pickle.load(f)
    
    with open("../file/incpt.pickle", "rb") as f:
        predictions_cache['incpt'] = pickle.load(f)

    with open("../file/cf.pickle", "rb") as f:
        predictions_cache['cf'] = pickle.load(f)

    with open("../file/random.pickle", "rb") as f:
        predictions_cache['random'] = pickle.load(f)

    with open("../file/popularity.pickle", "rb") as f:
        predictions_cache['popularity'] = pickle.load(f)

    return predictions_cache

def write_predictions_cache(predictions_cache):

    with open("../file/resnet.pickle", "wb") as f:
        pickle.dump(predictions_cache['resnet'], f)
    
    with open("../file/vgg.pickle", "wb") as f:
        pickle.dump(predictions_cache['vgg'], f)
    
    with open("../file/incpt.pickle", "wb") as f:
        pickle.dump(predictions_cache['incpt'], f)

    with open("../file/cf.pickle", "wb") as f:
        pickle.dump(predictions_cache['cf'], f)

    with open("../file/random.pickle", "wb") as f:
        pickle.dump(predictions_cache['random'], f)

    with open("../file/popularity.pickle", "wb") as f:
        pickle.dump(predictions_cache['popularity'], f)

def get_predictions(predictions_cache, recommender, user, reviews):
    
    if user in predictions_cache[recommender]:
        print("Cache")
        return predictions_cache[recommender][user]

    if recommender == 'vgg' or recommender == 'resnet' or recommender == 'incpt':
        ranking = recommedation_DL(recommender, user, reviews, debug=True, n_sample=2000)
    elif recommender == 'cf' or recommender == 'random' or recommender == 'popularity':
        ranking = recommedation_CF(recommender, user, reviews, debug=True, n_sample=2000)
    
    if ranking:
        predictions_cache[recommender][user] = ranking

    return ranking

def recommedation_CF(recommender, user, reviews, cutoff=[5, 10, 20, 50], threshold=0,  decimals=None, n_vectors=5, debug=False, n_sample=0):
    return execute_collaborative(recommender, cutoff, threshold, decimals, n_vectors, debug, reviews, n_sample, [user])

def recommedation_DL(recommender, user, reviews, cutoff=[5, 10, 20, 50], threshold=0, decimals=None, n_neighbors=11, test_size=0.2, random_state=None, comb_weights=[1, 1 ,1], debug=False, n_sample=0):
    return execute_network(recommender, cutoff, threshold, decimals, n_neighbors, test_size, random_state, comb_weights, debug, reviews, n_sample, [user])