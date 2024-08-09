from sklearn.pipeline import Pipeline
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

def create_model(data):
    preproc = ColumnTransformer(
        transformers= [
            ("one-hot", OneHotEncoder(drop = "first"), ["direction"])
        ],
        remainder= "passthrough"
    )
    pl = Pipeline([
        ("preproc", preproc),
        ("scaler", StandardScaler()),
        ("MLP", MLPClassifier())
    ])
    try:
        data = data[["direction", "bounce_dist", "hang_time", "was_caught"]]
    except:
        raise ValueError("Input data has incorrect format")
    pl.fit(data[["direction", "bounce_dist", "hang_time"]], data["was_caught"])
    return pl

def create_cont_model(data):
    preproc = ColumnTransformer(
        transformers = [
            ("one-hot", OneHotEncoder(drop = "first"), ["updated_direction"])
        ],
        remainder= "passthrough"
    )
    pl = Pipeline([
        ("preproc", preproc),
        ("scaler", StandardScaler()),
        ("MLP", MLPClassifier())
    ])
    try:
        data = data[["updated_direction", "distance_remaining", "hang_time_remaining", "quarter_sec_velo", "was_caught"]]
    except:
        raise ValueError("Input data has incorrect format")
    pl.fit(data[["updated_direction", "distance_remaining", "hang_time_remaining", "quarter_sec_velo"]], data["was_caught"])
    return pl
