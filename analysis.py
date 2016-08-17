"""
Copyright Thomas Woodside 2016
All rights reserved.
Analyzes the data extracted in initializefromcsv.py and uses a Random Forest
to generate probability estimates for expiration. These estimates are used
to split the loans into categories of chance for expiration. Currently there
are seven categories but there may be more in the future.

"""
import pickle
from sklearn.feature_extraction import DictVectorizer
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import LabelBinarizer
from sklearn.ensemble import RandomForestClassifier
from collections import defaultdict

features = pickle.load(open("features.pkl", "rb"))
labels = pickle.load(open("labels.pkl", "rb"))
vectorizer = DictVectorizer()
features = vectorizer.fit_transform(features)
lb = LabelBinarizer()
labels = lb.fit_transform(labels)

features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels)

forest = RandomForestClassifier(class_weight="balanced", n_estimators=640)
#found using GridSearchCV
fitted = forest.fit(features_train, labels_train[:,0])
predictions = forest.predict_proba(features_test)


results = defaultdict(lambda: defaultdict(int))
for i, prediction in enumerate(predictions):
    if prediction[1] < 0.1:
        if labels_test[i] == 1:
            results["1"]["correct"] += 1
        results["1"]["total"] += 1
    elif prediction[1] < 0.2:
        if labels_test[i] == 1:
            results["2"]["correct"] += 1
        results["2"]["total"] += 1
    elif prediction[1] < 0.3:
        if labels_test[i] == 1:
            results["3"]["correct"] += 1
        results["3"]["total"] += 1
    elif prediction[1] < 0.4:
        if labels_test[i] == 1:
            results["4"]["correct"] += 1
        results["4"]["total"] += 1
    elif prediction[1] < 0.6:
        if labels_test[i] == 1:
            results["5"]["correct"] += 1
        results["5"]["total"] += 1
    elif prediction[1] < 1:
        if labels_test[i] == 1:
            results["6"]["correct"] += 1
        results["6"]["total"] += 1
    else:
        if labels_test[i] == 1:
            results["7"]["correct"] += 1
        results["7"]["total"] += 1

brackets = []
for bracket in results:
    brackets.append(bracket)
    results[bracket]["percentage"] = results[bracket]["correct"]/results[
        bracket]["total"]
for bracket in sorted(brackets):
    print(bracket, results[bracket]["percentage"])