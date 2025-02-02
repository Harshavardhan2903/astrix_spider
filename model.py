
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import pickle


#ml model
# Sample training data (latency, bandwidth, packet_loss, best_protocol)
data = [
    [10, 100, 0, "QUIC"],
    [50, 10, 5, "TCP"],
    [5, 50, 2, "UDP"],
    [20, 5, 10, "TCP"],
    [8, 200, 0, "QUIC"]
]
#have to further develop and get more datapoints for the dataset .

df = pd.DataFrame(data, columns=["latency", "bandwidth", "packet_loss", "best_protocol"])

# Train Decision Tree Model
X = df[["latency", "bandwidth", "packet_loss"]]
y = df["best_protocol"]
model = DecisionTreeClassifier()
model.fit(X, y)

# Save Model
with open("protocol_selector.pkl", "wb") as f:
    pickle.dump(model, f)

print("AI Model Trained and Saved.")


