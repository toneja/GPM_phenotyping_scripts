#!/usr/bin/python3

"""docstring goes here"""

import os
import sys
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix
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
        _x, _y, test_size=0.5, random_state=42
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

    # Predict labels for the testing set
    y_pred = logreg.predict(_x_test_sfs)

    # Calculate precision, recall, and F1-score
    precision = precision_score(_y_test, y_pred)
    recall = recall_score(_y_test, y_pred)
    f1 = f1_score(_y_test, y_pred)

    # Calculate the confusion matrix
    tn, fp, fn, tp = confusion_matrix(_y_test, y_pred).ravel()

    # Calculate specificity
    specificity = tn / (tn + fp)

    # Print the results
    print("Accuracy:", accuracy)
    print("Selected features:", _x.columns[sfs.get_support()])
    print("Precision:", precision)
    print("Recall:", recall)
    print("Specificity:", specificity)
    print("F1-score:", f1)


evaluate_predictive_model(sys.argv[1])
