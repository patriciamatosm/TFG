import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from skimage import io
import matplotlib.pyplot as plt # plotting
import pandas as pd
import requests
import sys
sys.path.append(r'C:\\Users\\pmato\\OneDrive\\Desktop\\TFG')

def plot_figures(figures, nrows = 1, ncols=1,figsize=(8, 8)):
    """Plot a dictionary of figures.

    Parameters
    ----------
    figures : <title, figure> dictionary
    ncols : number of columns of subplots wanted in the display
    nrows : number of rows of subplots wanted in the figure
    """

    fig, axeslist = plt.subplots(ncols=ncols, nrows=nrows,figsize=figsize)
    for ind,title in enumerate(figures):
        image = io.imread(figures[title])
        axeslist.ravel()[ind].imshow(image)
        axeslist.ravel()[ind].set_title(title)
        axeslist.ravel()[ind].set_axis_off()
    plt.tight_layout() # optional

def check_url(img_url):
    response = requests.get(img_url)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        return False
    return True

def read(code='resnet', test_size=0.2, random_state=None):

    # Leemos todos los datasets que neceistamos

    df_reviews = pd.read_csv('../data/df_reviews_38k.csv', index_col=0)
    df_metadata, embeddings, inds_all = None, None, None

    if code == 'resnet':
        df_metadata = pd.read_csv("../data/Z_nodup_aux.csv", index_col=0)
        embeddings = pd.read_csv('../data/embs_Z_resnet.csv', index_col=0)
        inds_all = embeddings.index.values.tolist()
    elif code == 'vgg':
        df_metadata = pd.read_csv("../data/Z_nodup_aux.csv", index_col=0)
        embeddings = pd.read_csv('../data/embs_vgg.csv', index_col=0)
        inds_all = embeddings.index.values.tolist()
    elif code == 'incpt':
        df_metadata = pd.read_csv("../data/Z_nodup_aux.csv", index_col=0)
        embeddings = pd.read_csv('../data/embs_incpt.csv', index_col=0)
        inds_all = embeddings.index.values.tolist()
    elif code == 'cf':
        df_reviews.drop(['image', 'reviewTime', 'unixReviewTime', 'style', 'vote', 'reviewText', 'verified', 'reviewerName', 'summary'], axis=1, inplace=True)
        df_reviews = df_reviews.reindex(['reviewerID', 'asin', 'overall'], axis="columns")


    x_reviews, y_reviews = pd.read_csv('../data/x_reviews_inter.csv', index_col=0), pd.read_csv('../data/y_reviews_inter.csv', index_col=0)

    users_X = x_reviews['reviewerID'].unique()
    users_y = y_reviews['reviewerID'].unique()
    return df_reviews, x_reviews, y_reviews, users_X, users_y, df_metadata, embeddings, inds_all