import pandas as pd

item_fname = "data/movies_final.csv"


def random_items():
    movies_df = pd.read_csv(item_fname)
    # 결측치 방지 및 dict 변환
    movies_df = movies_df.fillna("")
    result = movies_df.sample(n=10).to_dict("records")
    return result


def random_genres_items(genre: str):
    movies_df = pd.read_csv(item_fname)
    movies_df = movies_df.fillna("")

    # 1. genres 컬럼을 문자열로 변환
    movies_df["genres"] = movies_df["genres"].astype(str)

    # 2. 대소문자 구분 없이 장르 검색 (comedy, Comedy 모두 인식)
    genre_df = movies_df[
        movies_df["genres"].str.contains(genre, case=False, na=False)
    ]

    # 해당 장르가 없으면 빈 리스트, 있으면 최대 10개 랜덤 추출
    if genre_df.empty:
        return []

    sample_size = min(10, len(genre_df))
    result = genre_df.sample(n=sample_size).to_dict("records")
    return result