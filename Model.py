from sklearn.pipeline import Pipeline
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler

def create_model(data):
    pl = Pipeline([
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
