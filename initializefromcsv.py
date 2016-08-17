"""
Copyright Thomas Woodside 2016
All rights resevered.
Reads the all_loans.csv file from kivatools.org to extract features helpful for
analysis.
"""

import csv
from datetime import datetime
import pickle

all_loans = csv.DictReader(open("all_loans.csv"))
features = []
labels = []
startdate = datetime.strptime("01-01-2015 00:00:00", "%d-%m-%Y %H:%M:%S")
for loan in all_loans:
    try:
        date = datetime.strptime(loan["posted_date"], "%d-%m-%Y %H:%M:%S")
    except:
        continue
    if date < startdate:
        continue
    if loan["status"] in ["expired", "funded"]:
        result = {}
        for item in ["partner", "sector", "activity", "loan_amount",
                     "country"]:
            result[item] = loan[item]
        features.append(result)
        labels.append(loan["status"])
pickle.dump(features, open("features.pkl", "wb+"))
pickle.dump(labels, open("labels.pkl", "wb+"))