import warnings
warnings.filterwarnings('ignore')

import tensorflow as tf
import seaborn as sns
sns.set_color_codes()
sns.set(style="whitegrid")
import numpy as np # linear algebra
from recommendation import recommend_collaborative
from functions import read
from recommender import SVD

from metrics import PrecisionAtK, RecallAtK
tf.__version__


if __name__ == '__main__':
    df_reviews, x_reviews, y_reviews, users_X, users_y, _, _, _ = read('cf')
    print('All read.')

    metrics = [PrecisionAtK(cutoff=3000, threshold=0), RecallAtK(cutoff=3000, threshold=0)]
    svd = SVD(n_vectors=5, index='reviewerID', columns='asin', values='overall', aggfunc=np.sum)
    svd.build_pivot_tables(x_reviews, y_reviews)
    svd.get_predictions()
    
    sample = []
    while 1:
        aux = np.random.choice(users_y, 1, replace=False)
        if aux[0] in svd.x_pivot.index:
            sample.append(aux[0])
        if len(sample) == 5:
            break
    
    for user in sample:
        if user in svd.x_pivot.index:
            print('------ Recommending items for user', user, '------')
            ranking = recommend_collaborative(user, svd.preds)
            for metric in metrics:
                metric.score_CF(user, ranking, svd.y_pivot, debug=True)
        else:
            print('Cannot generate recommendation for user', user)


    print()
    for metric in metrics:
        metric.to_string()