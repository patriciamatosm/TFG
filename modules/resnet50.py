import warnings
warnings.filterwarnings('ignore')

import tensorflow as tf
import pandas as pd
import seaborn as sns
sns.set_color_codes()
sns.set(style="whitegrid")
from sklearn.neighbors import KNeighborsClassifier
import numpy as np # linear algebra
from recommendation import recommend
from functions import read
from networks import Resnet
from metrics import PrecisionAtK, RecallAtK
tf.__version__



if __name__ == '__main__':

    img_width, img_height = 224, 224
    resnet = Resnet(img_width, img_height)

    resnet.create_network()
    resnet.summary()

    df_reviews, x_reviews, y_reviews, users_X, users_y, df_metadata, embeddings, inds_all = read('resnet')
    print('All read.')

    metrics = [PrecisionAtK(cutoff=10, threshold=0), RecallAtK(cutoff=10, threshold=0)]
    knn_resnet = KNeighborsClassifier(n_neighbors=11, weights='distance').fit(embeddings, inds_all)



    # evitar cold start por ahora
    sample = []
    while 1:
        aux = np.random.choice(users_y, 1, replace=False)
        if len(df_reviews[df_reviews['reviewerID'] == aux[0]]) > 3:
            sample.append(aux[0])
        if len(sample) == 5:
            break
    
    for user in sample:
        if len(x_reviews[x_reviews['reviewerID'].str.contains(user)]) > 0:
            print('------ Recommending items for user', user, '------')
            ranking = recommend(user, df_metadata, x_reviews, resnet.red, 'resnet', knn_resnet, None, None)
            # print(len(ranking))
            for metric in metrics:
                metric.score(y_reviews, user, ranking, debug=True)
        else:
            print('Cannot generate recommendation for user', user)


    print()
    for metric in metrics:
        metric.to_string()
    


    