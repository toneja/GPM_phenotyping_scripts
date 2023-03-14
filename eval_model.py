#!/usr/bin/python3

import os
import sys
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SequentialFeatureSelector


def evaluate_predictive_model(csv_filename):
    # Load the dataset from CSV file
    dataset = pd.read_csv(csv_filename)

    # Prepare input features and output label
    filename = os.path.splitext(os.path.basename(csv_filename))[0]
    output_label = filename.split("_")[0]
    X = dataset.drop(output_label, axis=1)
    y = dataset[output_label]

    # Split dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Use stepwise feature selection to find the best set of features
    logreg = LogisticRegression(solver="liblinear", multi_class="ovr")
    sfs = SequentialFeatureSelector(logreg, n_features_to_select=None)
    sfs.fit(X_train, y_train)
    X_train_sfs = sfs.transform(X_train)
    X_test_sfs = sfs.transform(X_test)

    # Train a logistic regression model with the selected features
    logreg.fit(X_train_sfs, y_train)

    # Evaluate the model's accuracy on the testing set
    accuracy = logreg.score(X_test_sfs, y_test)

    # Print the results
    print("Accuracy:", accuracy)
    print("Selected features:", X.columns[sfs.get_support()])


evaluate_predictive_model(sys.argv[1])
