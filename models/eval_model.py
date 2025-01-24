#!/usr/bin/env python3
#
# This file is part of the GPM phenotyping scripts.
#
# Copyright (c) 2025 Jason Toney
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""
Evaluate a predictive model using logistic regression.

Usage: eval_model.py <csv_filename>

Read a multiclass training dataset from a CSV file and perform logistic regression.
Evaluate the model's accuracy in predicting the output label and print the evaluation metrics.
"""

import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    log_loss,
    confusion_matrix,
)


def preprocess_data(df, target_column):
    """docstring goes here."""
    X = df.drop(columns=[target_column])
    y = df[target_column]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )

    return X_train, X_test, y_train, y_test


def evaluate_predictive_model(X_train, X_test, y_train, y_test):
    """docstring goes here."""
    model = LogisticRegression(solver="newton-cg", max_iter=1000)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)

    print("Accuracy:", accuracy_score(y_test, y_pred))
    print(
        "Precision:",
        precision_score(y_test, y_pred, average="weighted", labels=np.unique(y_pred)),
    )
    print(
        "Recall:",
        recall_score(y_test, y_pred, average="weighted", labels=np.unique(y_pred)),
    )
    print(
        "F1 Score:",
        f1_score(y_test, y_pred, average="weighted", labels=np.unique(y_pred)),
    )
    print("ROC AUC Score:", roc_auc_score(y_test, y_pred_proba, multi_class="ovr"))
    print("Log Loss:", log_loss(y_test, y_pred_proba))
    print(
        "Confusion Matrix:\n",
        confusion_matrix(y_test, y_pred, labels=np.unique(y_pred)),
    )
    print("Classification Report:")
    print(classification_report(y_test, y_pred, labels=np.unique(y_pred)))


def main(file):
    df = pd.read_csv(file)
    X_train, X_test, y_train, y_test = preprocess_data(df, "class")
    evaluate_predictive_model(X_train, X_test, y_train, y_test)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        sys.exit(f"Usage: {sys.argv[0]} [FILE]")
