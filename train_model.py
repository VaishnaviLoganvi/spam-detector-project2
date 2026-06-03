import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

url = "https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv"

df = pd.read_csv(url, sep="\t", names=["label", "text"])

df["label"] = df["label"].map({
    "ham":0,
    "spam":1
})

X = df["text"]
y = df["label"]

vectorizer = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1,2),
    max_features=5000
)

X = vectorizer.fit_transform(X)

model = LogisticRegression(max_iter=1000)
model.fit(X,y)

pickle.dump(model, open("model.pkl","wb"))
pickle.dump(vectorizer, open("vectorizer.pkl","wb"))

print("Model Trained Successfully")