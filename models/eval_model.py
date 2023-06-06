#!/usr/bin/env python3
#
# This file is part of the GPM phenotyping scripts.
#
# Copyright (c) 2023 Jason Toney
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""
Evaluate a predictive model using logistic regression with feature selection.

Usage: eval_model.py <train_csv_filename> <test_csv_filename>

Read a training dataset from a CSV file and perform logistic regression with feature selection.
Evaluate the model's accuracy in predicting the output label and print the evaluation metrics.
"""

import os
import sys
import pandas as pd
import warnings
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix
from sklearn.feature_selection import SequentialFeatureSelector


def evaluate_predictive_model(train_csv_filename, test_csv_filename):
    """Evaluate predictive model using logistic regression with feature selection."""
    # Load training dataset from CSV file
    train_dataset = pd.read_csv(train_csv_filename)

    # Load testing dataset from CSV file
    test_dataset = pd.read_csv(test_csv_filename)

    # Prepare input features and output label for training set
    train_filename = os.path.splitext(os.path.basename(train_csv_filename))[0]
    train_output_label = train_filename.split("_")[0]
    train_x = train_dataset.drop(train_output_label, axis=1)
    train_y = train_dataset[train_output_label]

    # Prepare input features and output label for testing set
    test_filename = os.path.splitext(os.path.basename(test_csv_filename))[0]
    test_output_label = test_filename.split("_")[0]
    test_x = test_dataset.drop(test_output_label, axis=1)
    test_y = test_dataset[test_output_label]

    # Create an empty DataFrame to store the results
    results_df = pd.DataFrame(
        columns=[
            "Selected Features",
            "Accuracy",
            "Precision",
            "Recall",
            "Specificity",
            "F1-score",
        ]
    )

    # ignore some annoying warnings from the code below
    warnings.filterwarnings(
        "ignore", category=FutureWarning, module="sklearn.feature_selection"
    )

    # Use stepwise feature selection to find the best set of features
    logreg = LogisticRegression(solver="liblinear", multi_class="ovr")
    sfs = SequentialFeatureSelector(logreg, n_features_to_select=None)
    sfs.fit(train_x, train_y)
    train_x_sfs = sfs.transform(train_x)
    test_x_sfs = sfs.transform(test_x)

    # Train a logistic regression model with selected features
    logreg.fit(train_x_sfs, train_y)

    # Evaluate model's accuracy on the testing set
    accuracy = logreg.score(test_x_sfs, test_y)

    # Predict labels for the testing set
    y_pred = logreg.predict(test_x_sfs)

    # Calculate precision, recall, and F1-score
    precision = precision_score(test_y, y_pred)
    recall = recall_score(test_y, y_pred)
    f1 = f1_score(test_y, y_pred)

    # Calculate confusion matrix
    tn, fp, fn, tp = confusion_matrix(test_y, y_pred).ravel()

    # Calculate specificity
    specificity = tn / (tn + fp)

    # Store the results in the DataFrame
    selected_features = ", ".join(train_x.columns[sfs.get_support()])
    results_df.loc[0] = [
        selected_features,
        accuracy,
        precision,
        recall,
        specificity,
        f1,
    ]

    # Print the results
    print(f"Results [{train_csv_filename} - {test_csv_filename}]:")
    print(results_df.to_string(index=False))


if __name__ == "__main__":
    if len(sys.argv) > 2:
        evaluate_predictive_model(sys.argv[1], sys.argv[2])
    else:
        print("Please provide the training and testing CSV filenames as arguments.")
