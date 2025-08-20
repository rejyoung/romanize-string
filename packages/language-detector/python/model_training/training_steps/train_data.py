import joblib
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import VotingClassifier



"""
This model was trained using corpora provided by the Wortschatz Project
(University of Leipzig), licensed under CC BY 4.0.

Source: https://wortschatz.uni-leipzig.de/en/download
License: https://creativecommons.org/licenses/by/4.0/
"""

print("Reading prepared training data")
X_train, y_train = joblib.load("ld_train_data.joblib")


ensemble_model = VotingClassifier(
    estimators=[
        ('nb', MultinomialNB()),
        ('sgd', SGDClassifier(loss="log_loss", class_weight="balanced"))
    ],
    voting='soft'
)

print("Fitting ensemble model")
ensemble_model.fit(X_train, y_train)

print("Testing accuracy with train data")
print("Train accuracy:", ensemble_model.score(X_train, y_train))


print("Writing ensemble model to disk")
joblib.dump(ensemble_model, "ld_ensemble_model.joblib")
print("Write complete")
