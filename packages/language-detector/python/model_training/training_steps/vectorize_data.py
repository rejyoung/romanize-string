import pandas as pd
import joblib
from sklearn.feature_extraction.text import CountVectorizer


"""
This model was trained using corpora provided by the Wortschatz Project
(University of Leipzig), licensed under CC BY 4.0.

Source: https://wortschatz.uni-leipzig.de/en/download
License: https://creativecommons.org/licenses/by/4.0/
"""

print("Reading data")
df = pd.read_csv("ld_balanced_data.csv")
cv = CountVectorizer(analyzer="char", ngram_range=(2, 4))


print("Count-vectorizing")
X = cv.fit_transform(df["text"])
y = df["label"].values

print("Writing vectorized data to disk")
joblib.dump((X, y), "ld_vectorized_data.joblib")

print("Writing vectorizer to disk")
joblib.dump(cv, "ld_vectorizer.joblib")
print("Write complete")