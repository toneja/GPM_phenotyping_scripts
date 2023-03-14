#!/usr/bin/python3

"""docstring goes here"""

import os
import sys
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SequentialFeatureSelector


def evaluate_predictive_model(csv_filename):
    """docstring goes here"""
    # Load the dataset from CSV file
    dataset = pd.read_csv(csv_filename)

    # Prepare input features and output label
    filename = os.path.splitext(os.path.basename(csv_filename))[0]
    output_label = filename.split("_")[0]
    _x = dataset.drop(output_label, axis=1)
    _y = dataset[output_label]

    # Split dataset into training and testing sets
    _x_train, _x_test, _y_train, _y_test = train_test_split(
        _x, _y, test_size=0.2, random_state=42
    )

    # Use stepwise feature selection to find the best set of features
    logreg = LogisticRegression(solver="liblinear", multi_class="ovr")
    sfs = SequentialFeatureSelector(logreg, n_features_to_select=None)
    sfs.fit(_x_train, _y_train)
    _x_train_sfs = sfs.transform(_x_train)
    _x_test_sfs = sfs.transform(_x_test)

    # Train a logistic regression model with the selected features
    logreg.fit(_x_train_sfs, _y_train)

    # Evaluate the model's accuracy on the testing set
    accuracy = logreg.score(_x_test_sfs, _y_test)

    # Print the results
    print("Accuracy:", accuracy)
    print("Selected features:", _x.columns[sfs.get_support()])


evaluate_predictive_model(sys.argv[1])
