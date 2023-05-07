#!/usr/bin/env python3

"""
Evaluate a predictive model using logistic regression with feature selection.

Usage: eval_model.py <csv_filename> [num_runs]

Read a training dataset from a CSV file and perform logistic regression with feature selection.
Evaluate the model's accuracy in predicting the output label and print the evaluation metrics.
"""

import os
import sys
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SequentialFeatureSelector


def evaluate_predictive_model(csv_filename, num_runs=10):
    """Evaluate predictive model using logistic regression with feature selection."""
    # Load dataset from CSV file
    dataset = pd.read_csv(csv_filename)

    # Prepare input features and output label
    filename = os.path.splitext(os.path.basename(csv_filename))[0]
    output_label = filename.split("_")[0]
    _x = dataset.drop(output_label, axis=1)
    _y = dataset[output_label]

    # Create an empty DataFrame to store the results
    results_df = pd.DataFrame(
        columns=["Selected Features", "Accuracy", "Precision", "Recall", "Specificity", "F1-score"]
    )

    for i in range(num_runs):
        # Split dataset into training and testing sets
        _x_train, _x_test, _y_train, _y_test = train_test_split(
            _x, _y, test_size=0.5, random_state=None
        )

        # Use stepwise feature selection to find the best set of features
        logreg = LogisticRegression(solver="liblinear", multi_class="ovr")
        sfs = SequentialFeatureSelector(logreg, n_features_to_select=None)
        sfs.fit(_x_train, _y_train)
        _x_train_sfs = sfs.transform(_x_train)
        _x_test_sfs = sfs.transform(_x_test)

        # Train a logistic regression model with selected features
        logreg.fit(_x_train_sfs, _y_train)

        # Evaluate model's accuracy on the testing set
        accuracy = logreg.score(_x_test_sfs, _y_test)

        # Predict labels for the testing set
        y_pred = logreg.predict(_x_test_sfs)

        # Calculate precision, recall, and F1-score
        precision = precision_score(_y_test, y_pred)
        recall = recall_score(_y_test, y_pred)
        f1 = f1_score(_y_test, y_pred)

        # Calculate confusion matrix
        tn, fp, fn, tp = confusion_matrix(_y_test, y_pred).ravel()

        # Calculate specificity
        specificity = tn / (tn + fp)

        # Store the results in the DataFrame
        selected_features = ", ".join(_x.columns[sfs.get_support()])
        results_df.loc[i] = [selected_features, accuracy, precision, recall, specificity, f1]

    # Print the results
    print(f"Results [{csv_filename}]:")
    print(results_df.to_string())
    print("\nAverage:")
    print(results_df.iloc[:, 1:].mean().to_string())


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if len(sys.argv) > 2:
            evaluate_predictive_model(sys.argv[1], int(sys.argv[2]))
        else:
            evaluate_predictive_model(sys.argv[1])
    else:
        print("Please provide the CSV filename as an argument.")
