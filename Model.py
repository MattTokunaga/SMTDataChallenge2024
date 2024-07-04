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
        data = data[["direction", "ideal_length", "hang_time", "was_caught"]]
    except:
        print("ERROR: data format incorrect")
        return False
    pl.fit(data[["direction", "ideal_length", "hang_time"]], data["was_caught"])
    return pl
