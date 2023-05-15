from sklearn.ensemble import RandomForestClassifier
import db
from fire import Cause
import random
import argparse
from datetime import datetime
from joblib import dump 

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help = "Print verbose", action="store_true", dest = "verbose")
parser.add_argument("-n", "--nsamples", help = "Number of training samples", default = 5000, type = int, dest = "nsamples")
parser.add_argument("-r", "--rounds", help = "Number of training rounds", default = 1, dest = "rounds", type = int)
parser.add_argument("-o", "--output-file", help = "Name of file to save model to", default = "model.joblib", dest = "filename", type = str)
parser.add_argument("-a", "--all", help = "Train over the entire database", default = False, dest = "all", action = "store_true")
parser.add_argument("-e", "--estimators", help = "Number of estimators", default = 100, type = int, dest = "estimators")
parser.add_argument("-s", "--split", help = "Fraction split for training and testing sets", default = 2, type = int, dest = "split")
args = parser.parse_args()

def timestamp(message: str) -> None:
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("{} {}".format(stamp, message))

def run(rounds: int):

    timestamp("Training {} round(s) with {} estimators".format(args.rounds, args.estimators))

    clf = RandomForestClassifier(n_estimators = args.estimators)

    database = db.Database()

    for i in range(rounds):

        fires = database.get_training_testing_set(args.nsamples)
        if args.all:
            fires = database.get_all_clean_fires()
        random.shuffle(fires)
        pivot = int(len(fires) / args.split)
        training_fires = fires[pivot:]
        testing_fires = fires[:pivot]
        timestamp("Training on {} fires (round {})".format(len(training_fires), i + 1))
        sample_matrix = list()
        labels = list()

        for fire in training_fires:
            sample_matrix.append(fire.get_independent_attributes())
            labels.append(fire.cause.value)

        clf.fit(sample_matrix, labels)

        testing_matrix = list()
        predictions = list()

        for fire in testing_fires:
            testing_matrix.append(fire.get_independent_attributes())

        for prediction in clf.predict(testing_matrix):
            predictions.append(prediction)

        predictions.reverse()

        accuracy = 0

        for fire in testing_fires:
            prediction = predictions.pop()
            if prediction == fire.cause.value:
                accuracy += 1
            if args.verbose:
                fire.pretty_print()
                print("    Predicted {}: {}".format(prediction, Cause(prediction).name))

        timestamp("{} correctly predicted out of {} ({:.2f}%)".format(accuracy, pivot, accuracy / pivot * 100))

    dump(clf, "model.joblib")
    timestamp("Saved model to {}.".format(args.filename))

run(args.rounds)
