import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

import pickle
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from implicit.als import AlternatingLeastSquares

saved_model_fname = "model/finalized_model.sav"
data_fname = "data/ratings.csv"
item_fname = "data/movies_final.csv"
weight = 10


def model_train():
    ratings_df = pd.read_csv(data_fname)
    ratings_df["userId"] = ratings_df["userId"].astype("category")
    ratings_df["movieId"] = ratings_df["movieId"].astype("category")

    # (사용자, 영화) 순서로 희소 행렬 생성 (User x Item)
    user_codes = ratings_df["userId"].cat.codes
    movie_codes = ratings_df["movieId"].cat.codes
    
    n_users = len(ratings_df["userId"].cat.categories)
    n_movies = len(ratings_df["movieId"].cat.categories)

    rating_matrix = csr_matrix(
        (ratings_df["rating"].astype(np.float32), (user_codes, movie_codes)),
        shape=(n_users, n_movies)
    )

    als_model = AlternatingLeastSquares(
        factors=50, regularization=0.01, dtype=np.float64, iterations=50
    )

    als_model.fit(weight * rating_matrix)

    os.makedirs(os.path.dirname(saved_model_fname), exist_ok=True)
    with open(saved_model_fname, "wb") as f:
        pickle.dump(als_model, f)
    return als_model


def calculate_item_based(item_id, items):
    with open(saved_model_fname, "rb") as f:
        loaded_model = pickle.load(f)

    res = loaded_model.similar_items(itemid=int(item_id), N=11)

    if isinstance(res, tuple):
        rec_ids = res[0]
    elif hasattr(res, "shape") and len(res.shape) == 2:
        rec_ids = res[:, 0]
    elif isinstance(res, list):
        rec_ids = [r[0] if isinstance(r, (tuple, list, np.ndarray)) else r for r in res]
    else:
        rec_ids = res

    return [int(items[int(r)]) for r in rec_ids if int(r) in items]

def item_based_recommendation(item_id):
    ratings_df = pd.read_csv(data_fname)
    ratings_df["userId"] = ratings_df["userId"].astype("category")
    ratings_df["movieId"] = ratings_df["movieId"].astype("category")
    movies_df = pd.read_csv(item_fname)

    categories = ratings_df["movieId"].cat.categories
    items = dict(enumerate(categories))

    try:
        target_id = int(item_id)
        if target_id in categories:
            parsed_id = categories.get_loc(target_id)
        elif str(item_id) in categories:
            parsed_id = categories.get_loc(str(item_id))
        else:
            return []

        result = calculate_item_based(parsed_id, items)
    except (KeyError, ValueError):
        result = []

    result = [int(x) for x in result if int(x) != int(item_id)]
    result_items = movies_df[movies_df["movieId"].isin(result)].fillna("").to_dict("records")
    return result_items


def calculate_user_based(user_items, items):
    with open(saved_model_fname, "rb") as f:
        loaded_model = pickle.load(f)

    recs = loaded_model.recommend(
        userid=0, user_items=user_items, recalculate_user=True, N=10
    )

    if isinstance(recs, tuple):
        rec_ids = recs[0]
    elif hasattr(recs, "shape") and len(recs.shape) == 2:
        rec_ids = recs[:, 0]
    elif isinstance(recs, list):
        rec_ids = [r[0] if isinstance(r, (tuple, list, np.ndarray)) else r for r in recs]
    else:
        rec_ids = recs

    return [int(items[int(r)]) for r in rec_ids if int(r) in items]


def build_matrix_input(input_rating_dict, categories):
    cat_to_code = {cat: code for code, cat in enumerate(categories)}

    mapped_idx = []
    data = []

    for k, v in input_rating_dict.items():
        try:
            m_id = int(k)
            if m_id in cat_to_code:
                mapped_idx.append(cat_to_code[m_id])
                data.append(weight * float(v))
        except (ValueError, TypeError):
            continue

    row = np.zeros(len(mapped_idx), dtype=np.int32)
    col = np.array(mapped_idx, dtype=np.int32)
    val = np.array(data, dtype=np.float32)

    return csr_matrix((val, (row, col)), shape=(1, len(categories)))


def user_based_recommendation(input_ratings):
    ratings_df = pd.read_csv(data_fname)
    ratings_df["userId"] = ratings_df["userId"].astype("category")
    ratings_df["movieId"] = ratings_df["movieId"].astype("category")
    movies_df = pd.read_csv(item_fname)

    categories = ratings_df["movieId"].cat.categories
    items = dict(enumerate(categories))

    if not isinstance(input_ratings, dict):
        input_dict = {}
        if isinstance(input_ratings, (list, tuple)):
            for item in input_ratings:
                if isinstance(item, str) and ":" in item:
                    k, v = item.split(":")
                    input_dict[k.strip()] = float(v.strip())
        input_ratings = input_dict

    input_matrix = build_matrix_input(input_ratings, categories)
    result = calculate_user_based(input_matrix, items)
    result = [int(x) for x in result]
    result_items = movies_df[movies_df["movieId"].isin(result)].fillna("").to_dict("records")
    return result_items


if __name__ == "__main__":
    model = model_train()