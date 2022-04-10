from fastapi import FastAPI
import uvicorn
import utils as utils
import pandas as pd
from modules.functions import *
from sklearn.model_selection import train_test_split
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import sys
sys.path.append(r'C:\\Users\\pmato\\OneDrive\\Desktop\\TFG')

# import pickle

# A1UVTDNRML9LEE
app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://localhost:8000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

predictions_cache = utils.read_predictions_cache()

df_reviews, _, _, _, _, _, _, _ = read('', random_state=43)

x_reviews = pd.read_csv('../data/x_reviews_inter.csv', index_col=0)
y_reviews = pd.read_csv('../data/y_reviews_inter.csv', index_col=0)

users_X = x_reviews['reviewerID'].unique()
users_y = y_reviews['reviewerID'].unique()
reviews = [df_reviews, x_reviews, y_reviews, users_X, users_y]

cached_users = list(users_y[:11])
print(cached_users)


df_metadata = pd.read_csv("../data/Z_nodup_aux.csv", index_col=0)

@app.get("/recommendation/{recommender}/{user}")
async def get_recommendation(recommender: str, user: str):
    ranking = utils.get_predictions(
        predictions_cache, recommender, user, reviews)
    keys = list(ranking.keys())[:12]
    print(keys)
    img = []
    for r in keys:
        img.extend(list(df_metadata[df_metadata['asin'] == r]['imageURLHighRes']))
    print(img)
    zip_iterator = zip(keys, img)
    a_dictionary = dict(zip_iterator)
    json_compatible_item_data = jsonable_encoder(a_dictionary)
    return JSONResponse(content=json_compatible_item_data)


@app.on_event("shutdown")
def shutdown_event():
    print("Saving Prediction Cache with Size: ", len(predictions_cache.keys()))
    utils.write_predictions_cache(predictions_cache)


@app.get("/users")
def getUsers():
    object = cached_users
    json_compatible_item_data = jsonable_encoder(object)
    return JSONResponse(content=json_compatible_item_data)

@app.get("/reviewedItems/{user}")
def getReviewedItems(user: str):
    items = list(x_reviews[x_reviews['reviewerID'] == user]['asin'])
    img = []
    for r in items:
        img.extend(list(df_metadata[df_metadata['asin'] == r]['imageURLHighRes']))
    zip_iterator = zip(items, img)
    a_dictionary = dict(zip_iterator)
    json_compatible_item_data = jsonable_encoder(a_dictionary)
    return JSONResponse(content=json_compatible_item_data)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
