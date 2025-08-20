import joblib

"""
This model was trained using corpora provided by the Wortschatz Project
(University of Leipzig), licensed under CC BY 4.0.

Source: https://wortschatz.uni-leipzig.de/en/download
License: https://creativecommons.org/licenses/by/4.0/
"""


print("Loading test data")
X_test, y_test = joblib.load("ld_test_data.joblib")

print("Loading ensemble model")
ensemble_model = joblib.load("ld_ensemble_model.joblib")

print("Testing accuracy with unseen test data")
print("Test accuracy:", ensemble_model.score(X_test, y_test))