import time
from functions import read
import sys
import argparse
from sklearn.model_selection import train_test_split
from recommendation import execute_network, execute_collaborative
import numpy as np  # linear algebra
import seaborn as sns
import warnings
from xmlrpc.client import boolean
warnings.filterwarnings('ignore')

sns.set_color_codes()
sns.set(style="whitegrid")

img_width, img_height = 224, 224

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Opciones")
    parser.add_argument('--recommender', metavar=('recomendador'), nargs=1, type=str,
                        help='Recomendador que se quiere ejecutar (resnet, incpt, vgg, random, popularity, cf).')
    parser.add_argument('--cutoff', metavar=('cutoff'), nargs=1, default=[5, 10, 20, 50], type=int,
                        help='Valor o valores del cutoff para las métricas (default [5, 10, 20, 50]).')
    parser.add_argument('--threshold', metavar=('umbral'), nargs=1, default=[1.5], type=int,
                        help='Valor del umbral aplicado a los ratings para las métricas (default 1.5).')
    parser.add_argument('--decimals', metavar=('decimales'), nargs=1, default=[None], type=int,
                        help='Numero de decimales a enseñar para los resultados numéricos (default todos los decimales).')
    parser.add_argument('--n_neighbors', metavar=('k'), nargs=1, default=[11], type=int,
                        help='Numero de vecinos a generar para las recomendaciones de aprendizaje profundo (default 11).')
    parser.add_argument('--test_size', metavar=('test_size'), nargs=1, default=[0.2], type=float,
                        help='Tamaño del conjunto de test (default 0.2).')
    parser.add_argument('--random_state', metavar=('random_state'), nargs=1, default=[None],  type=int,
                        help='Random state para la división de los conjuntos de train y test (default 42).')
    parser.add_argument('--n_vectors', metavar=('n_vectors'), nargs=1, default=[5], type=int,
                        help='Numero de vectores a generar para SVD en el filtrado colaborativo (default 5).')
    parser.add_argument('--comb_weights', metavar=('distancia', 'rating', 'tiempo'), nargs=3, type=int, default=[1, 1, 1],
                        help='Pesos otorgados a los valores de distancia, rating del producto y tiempo de valoración a la hora de'
                        + ' generar recomendaciones con aprendizaje profundo (default 1 para las tres).')
    parser.add_argument('--debug', metavar=('debug'), nargs=1, default=[False], type=boolean,
                        help='Modo debug (default False).')
    parser.add_argument('--n_sample', metavar=('sample'), nargs=1, default=[0], type=int,
                        help='Numero de usuarios en la sample para los reviews (default sin sample).')

    args = parser.parse_args()
    if len(sys.argv) < 2 or not args.recommender:
        parser.print_usage()
        sys.exit(1)

    df_reviews, _, _, _, _, _, _, _ = read(
        '', test_size=args.test_size[0], random_state=args.random_state[0])
    x_reviews, y_reviews = train_test_split(
        df_reviews, test_size=args.test_size[0], random_state=args.random_state[0])

    users_X = x_reviews['reviewerID'].unique()
    users_y = y_reviews['reviewerID'].unique()
    reviews = [df_reviews, x_reviews, y_reviews, users_X, users_y]

    init = time.time()
    if args.recommender[0] == 'vgg' or args.recommender[0] == 'resnet' or args.recommender[0] == 'incpt':
        execute_network(args.recommender[0], args.cutoff, args.threshold[0], args.decimals[0], args.n_neighbors[0],
                        args.test_size[0], args.random_state[0], args.comb_weights, args.debug[0], reviews, args.n_sample[0])
    elif args.recommender[0] == 'cf' or args.recommender[0] == 'random' or args.recommender[0] == 'popularity':
        execute_collaborative(args.recommender[0], args.cutoff, args.threshold[0],
                              args.decimals[0], args.n_vectors[0], args.debug[0], reviews, args.n_sample[0])

    else:
        print('------ RESNET ------')
        execute_network('resnet', args.cutoff, args.threshold[0], args.decimals[0], args.n_neighbors[0],
                        args.test_size[0], args.random_state[0], args.comb_weights, args.debug[0], reviews, args.n_sample[0])
        print()
        print('------ INCPT ------')
        execute_network('incpt', args.cutoff, args.threshold[0], args.decimals[0], args.n_neighbors[0],
                        args.test_size[0], args.random_state[0], args.comb_weights, args.debug[0], reviews, args.n_sample[0])
        print()
        print('------ VGG ------')
        execute_network('vgg', args.cutoff, args.threshold[0], args.decimals[0], args.n_neighbors[0],
                        args.test_size[0], args.random_state[0], args.comb_weights, args.debug[0], reviews, args.n_sample[0])
        print()
        print('------ CF - SVD ------')
        execute_collaborative(
            'cf', args.cutoff, args.threshold[0], args.decimals[0], args.n_vectors[0], args.debug[0], reviews, args.n_sample[0])
        print('------ BASELINE RANDOM ------')
        execute_collaborative(
            'random', args.cutoff, args.threshold[0], args.decimals[0], args.n_vectors[0], args.debug[0], reviews, args.n_sample[0])
        print('------ BASELINE POPULARITY ------')
        execute_collaborative('popularity', args.cutoff,
                              args.threshold[0], args.decimals[0], args.n_vectors[0], args.debug[0], reviews, args.n_sample[0])

    end = time.time()
    print("Exec time:", (end-init)//60)
