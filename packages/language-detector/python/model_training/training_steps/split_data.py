
import joblib
from sklearn.model_selection import train_test_split


"""
This model was trained using corpora provided by the Wortschatz Project
(University of Leipzig), licensed under CC BY 4.0.

Source: https://wortschatz.uni-leipzig.de/en/download
License: https://creativecommons.org/licenses/by/4.0/
"""

print("Loading data")
X, y = joblib.load("ld_vectorized_data.joblib")

print("Spliting data")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05, random_state=42)

print("Writing split data to disk")
joblib.dump((X_train, y_train), "ld_train_data.joblib")
joblib.dump((X_test, y_test), "ld_test_data.joblib")
print("Write complete")