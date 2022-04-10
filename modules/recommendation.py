from itertools import count
import warnings
warnings.filterwarnings('ignore')
import sys 
sys.path.append(r'C:\\Users\\pmato\\OneDrive\\Desktop\\TFG')

import pandas as pd
from PIL import Image
from io import BytesIO
from skimage import io
import requests
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications import resnet50
from tensorflow.keras.applications import vgg16
from tensorflow.keras.applications import inception_v3
import matplotlib.pyplot as plt # plotting
from modules.functions import plot_figures, check_url
from sklearn.neighbors import KNeighborsClassifier
from sklearn.utils import shuffle
from modules.recommender import SVD
from modules.metrics import PrecisionAtK, RecallAtK
from modules.networks import Inception, VGG, Resnet
from modules.functions import read
import calendar
import datetime
import csv

img_width, img_height, _ = 224, 224, 3 


def recommend_item(embedding, knn, n_neighbors=11):
    distances, indices = knn.kneighbors(embedding,  n_neighbors=n_neighbors)   
    indices = indices.reshape(n_neighbors, 1)
    df_indices = pd.DataFrame(indices, columns = ['title'])
    return df_indices, distances

def get_embedding_resnet50(model, img_name):
    if not check_url(img_name):
        return np.empty((2048,))
    response = requests.get(img_name)
    img = Image.open(BytesIO(response.content))
    img = img.convert('RGB')
    img = img.resize((img_width, img_height), Image.NEAREST)        
    # img to Array
    x   = image.img_to_array(img)
    # Expand Dim (1, w, h)
    x   = np.expand_dims(x, axis=0)
    # Pre process Input
    x   = resnet50.preprocess_input(x)
    preds = model.predict(x).reshape(-1)
    # print(preds)
    return preds

def get_embedding_vgg16(model, img_name):
    if not check_url(img_name):
        return np.empty((2048,))
    response = requests.get(img_name)
    img = Image.open(BytesIO(response.content))
    img = img.convert('RGB')
    img = img.resize((img_width, img_height), Image.NEAREST)        
    # img to Array
    x   = image.img_to_array(img)
    # Expand Dim (1, w, h)
    x   = np.expand_dims(x, axis=0)
    # Pre process Input
    x   = vgg16.preprocess_input(x)
    preds = model.predict(x).reshape(-1)
    # print(preds)
    return preds

def get_embedding_incpt(model, img_name):
    if not check_url(img_name):
        return np.empty((2048,))
    response = requests.get(img_name)
    img = Image.open(BytesIO(response.content))
    img = img.convert('RGB')
    img = img.resize((img_width, img_height), Image.NEAREST)        
    # img to Array
    x   = image.img_to_array(img)
    # Expand Dim (1, w, h)
    x   = np.expand_dims(x, axis=0)
    # Pre process Input
    x   = inception_v3.preprocess_input(x)
    preds = model.predict(x).reshape(-1)
    # print(preds)
    return preds

def get_embedding(model, img_name, code):
    if code == 'resnet':
        return get_embedding_resnet50(model, img_name)
    elif code == 'vgg':
        return get_embedding_vgg16(model, img_name)
    else:
        return get_embedding_incpt(model, img_name)

def generate_recommendation(indice, model, data, code, knn):
    # Generate prediction
    preds = get_embedding(model, data.loc[indice]['imageURLHighRes'], code)
    ind, distances = recommend_item(preds.reshape(1, -1), knn)

    # Get result
    df_result = pd.DataFrame()
    for i, val in enumerate(ind.iterrows()):
        k = int(val[1])
        df_result[i] = data.iloc[k]
    df_result = df_result.transpose()
    
    return df_result, distances

def plot_recommendation(indice, data, df_result):
    # Plot initial image
    image_init = io.imread(data.loc[indice]['imageURLHighRes'])
    plt.title(data.loc[indice]['asin'])
    plt.imshow(image_init)
    plt.show()
    
    # Plot recommendations
    figures = {row.asin: row.imageURLHighRes 
               for i, row in df_result.iterrows()}
    plot_figures(figures, 2, 6)

def get_recommendation_weight(dists, item_rating, unix_time_difference, comb_weights):
    w = []
    distances = dists[0]
    for dist in distances:
        eps = 0.0001
        dist_norm = ((dist - min(distances)) / (max(distances)- min(distances))) + eps
        dist_norm = 1/dist_norm #min  0, max  100 -- 100 - 1 - 1, 0 - 0 - 1000, 10 - 0.1 - 10
        max_dist_norm = 1/(eps)

        # Negativo porque a más distancia, menos peso tiene
        rating_norm = (item_rating-1) / 4 #(-rating) * item_rating
        time_norm = 1/unix_time_difference
        
        score = comb_weights[0] * dist_norm/max_dist_norm + comb_weights[1] * rating_norm + comb_weights[2] * time_norm
        w.append(score)
    return np.round(w, decimals=3)

def recommend(user, df_metadata, df_reviews, red, code_red, knn, comb_weights=[1,1,1]):
    user_recommendations = {}
    # Cogemos los items de los usuarios
    items = df_reviews[df_reviews['reviewerID'] == user]
    
    # Ordenamos por pesos
    # Mientras mas alto, mas nuevo
    df = items.sort_values(by=['unixReviewTime'], ascending=False)

    for _, row in df.iterrows():
        # Calculamos pesos
        ind = df_metadata.index[df_metadata['asin'] == row['asin']]

        # Generamos recomendaciones
        df_result, distances = generate_recommendation(ind.values[0], red, df_metadata, code_red, knn)
        
        # plot_recommendation(ind.values[0], df_metadata, df_result)
        # plt.show()

        # Unix time stamp del dia actual
        date = datetime.datetime.utcnow()
        utc_time = calendar.timegm(date.utctimetuple())
        
        # Fechas
        date_time_now = datetime.datetime.fromtimestamp(utc_time)
        date_time = datetime.datetime.fromtimestamp(row['unixReviewTime'])
        
        # Tiempo que ha pasado desde su valoracion (en años)
        diff = ((date_time_now - date_time).days)/365
        
        # Si es nuevo, colocamos 1 para que no afecte a los calculos
        if diff == 0.0:
            diff = 1.0
        
        # Generamos pesos
        weights = get_recommendation_weight(distances, row['overall'], diff, comb_weights)

        # Diccionario
        for i, r in enumerate(df_result.iterrows()):
            row_result = r[1]
            # TODO: If in training, remove
            if len(items[items['asin'].str.contains(row_result['asin'])]) == 0:
                if row_result['asin'] in user_recommendations:
                    user_recommendations[row_result['asin']] = weights[i] + user_recommendations[row_result['asin']]
                else:
                    user_recommendations[row_result['asin']] = weights[i]
    
    # Generar ranking de recomendaciones
    ranking = dict(sorted(user_recommendations.items(), reverse=True, key=lambda item: item[1]))
    
    return ranking

def recommend_collaborative(recommender, user, svd, df_reviews):

    if recommender == 'cf':
        sorted_user_predictions = svd.preds.loc[user].sort_values(ascending=False)
        
        ranking = {}
        preds = sorted_user_predictions.to_frame(name='predictions')
        items = svd.df_reviews_train[svd.df_reviews_train['reviewerID'] == user]
        for index, row in preds.iterrows():
            # TODO: If in training, remove
            if len(items[items['asin'].str.contains(index)]) == 0:
                if recommender == 'cf':
                    if index in ranking:
                        ranking[index] = ranking[index] + row[0]
                    else:
                        ranking[index] = row[0]
    else:
        sorted_user_predictions = svd.df_reviews_train
        
        if recommender == 'random':
            sorted_user_predictions = sorted_user_predictions.sample(frac=1).reset_index(drop=True)
        sorted_user_predictions = sorted_user_predictions.set_index('asin')
        
        counts_by_item = svd.df_reviews_train['asin'].value_counts()
        ranking = {}
        for index, row in sorted_user_predictions.iterrows():
            if recommender == 'random':
                ranking[index] = 0
            elif recommender == 'popularity':
                ranking[index] = counts_by_item[index]

    if recommender == 'cf' or recommender == 'popularity':
        ranking = dict(sorted(ranking.items(), reverse=True, key=lambda item: item[1]))
    
    return ranking

def execute_network(recommender, cutoffs, threshold, decimals, n_neighbors, test_size, random_state, comb_weights, debug, reviews, n_sample, users=None):
    if recommender == 'resnet':
        red = Resnet(img_width, img_height)
    elif recommender == 'vgg':
        red = VGG(img_width, img_height)
    elif recommender == 'incpt':
        red = Inception(img_width, img_height)

    red.create_network()
    if debug:
        red.summary()

    df_reviews, x_reviews, y_reviews, users_x, users_y = reviews[0], reviews[1], reviews[2], reviews[3], reviews[4]
    _, _, _, _, _, df_metadata, embeddings, inds_all = read(recommender, test_size=test_size, random_state=random_state)
    if debug:
        print('All read.')
    metrics = []
    for cutoff in cutoffs:
        metrics.append(PrecisionAtK(cutoff=cutoff, threshold=threshold))
        metrics.append(RecallAtK(cutoff=cutoff, threshold=threshold))
    knn = KNeighborsClassifier(n_neighbors=n_neighbors, weights='distance').fit(embeddings, inds_all)

    if not users:
        users = users_y
        if n_sample != 0:
            inter = list(set(users_y) & set(users_x))
            users = np.random.choice(inter, n_sample, replace=False)

    ranking = {}
    count_no_recom = 0
    for user in users:
        if len(x_reviews[x_reviews['reviewerID'].str.contains(user)]) > 0:
            if debug:
                print('------ Recommending items for user', user, '------')
            ranking = recommend(user, df_metadata, x_reviews, red.red, recommender, knn, comb_weights=comb_weights)
            for metric in metrics:
                metric.score(y_reviews, user, ranking, debug=debug, decimals=decimals)
        else:
            print('Cannot generate recommendation for user', user)
            count_no_recom += 1


    print()
    for metric in metrics:
        metric.to_string(decimals=decimals)

    print("Users with no recommendation:", count_no_recom, "out of", len(users))
    return ranking

def execute_collaborative(recommender, cutoffs, threshold, decimals, n_vectors, debug, reviews, n_sample, users=None):

    df_reviews, x_reviews, y_reviews = reviews[0], reviews[1], reviews[2]
    _, users_y = reviews[3], reviews[4]

    if debug:
        print('All read.')

    metrics = []
    for cutoff in cutoffs:
        metrics.append(PrecisionAtK(cutoff=cutoff, threshold=threshold))
        metrics.append(RecallAtK(cutoff=cutoff, threshold=threshold))
    svd = SVD(n_vectors=n_vectors, index='reviewerID', columns='asin', values='overall', aggfunc=np.sum)
    svd.build_pivot_tables(x_reviews, y_reviews)
    svd.get_predictions()
    

    if not users:
        users = users_y
        if n_sample != 0:
            inter = list(set(users_y) & set(svd.x_pivot.index))
            users = np.random.choice(inter, n_sample, replace=False)

    ranking = {}
    count_no_recom = 0
    for user in users:
        if user in svd.x_pivot.index:
            if debug:
                print('------ Recommending items for user', user, '------')
            ranking = recommend_collaborative(recommender, user, svd, df_reviews)
            for metric in metrics:
                metric.score_CF(user, ranking, svd.y_pivot, debug=debug, decimals=decimals)
        else:
            print('Cannot generate recommendation for user', user)
            count_no_recom += 1


    print()
    for metric in metrics:
        metric.to_string(decimals=decimals)
    print("Users with no recommendation:", count_no_recom, "out of", len(users))
    return ranking