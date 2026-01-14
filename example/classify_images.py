#!/usr/bin/env python3

import os
import subprocess

import pandas as pd
from sklearn import linear_model
from tabulate import tabulate


def setup_regression():
    """Setup the logistic regression used to determine ROI identity."""
    dataset = pd.read_csv("models/model_training_data.csv")
    vals = [
        "Area",
        "Perim.",
        "Major",
        "Minor",
        "Circ.",
        "Feret",
        "AR",
        "Round",
    ]
    _x = dataset[vals]
    _y = dataset["class"]
    regression = linear_model.LogisticRegression(
        solver="newton-cg", max_iter=1000, n_jobs=-1
    )
    regression.fit(_x.values, _y)
    return regression


def identify_roi(row, model):
    """Returns the ROI's predicted identity."""
    prediction = model.predict(
        [
            [
                int(row["Area"]),
                float(row["Perim."]),
                float(row["Major"]),
                float(row["Minor"]),
                float(row["Circ."]),
                float(row["Feret"]),
                float(row["AR"]),
                float(row["Round"]),
            ]
        ]
    )
    return int(prediction[0])


def main():
    # We work out of the main directory
    os.chdir(os.path.dirname(os.path.dirname(__file__)))
    # ImageJ temp folders
    os.makedirs(f"example/ImageJ/images", exist_ok=True)
    os.makedirs(f"example/ImageJ/results", exist_ok=True)
    # Clean out any old ImageJ files
    for folder in "images", "results":
        for file in os.listdir(f"example/ImageJ/{folder}"):
            file = os.path.join(f"example/ImageJ/{folder}", file)
            os.remove(file)
    # Process all of the images with ImageJ
    command = [
        "./ImageJ/ImageJ.exe",
        "-macro",
        "ImageJ/GPM/BatchProcess.ijm",
        "example/images",
    ]
    try:
        subprocess.run(command, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as exception:
        print(f"Error executing the macro: {exception}")
    # Relocate output files into their respective release folders
    for file in os.listdir("ImageJ/GPM/images"):
        if file.endswith(".tif"):
            os.replace(
                f"ImageJ/GPM/images/{file}",
                f"example/ImageJ/images/{file}",
            )
    for file in os.listdir("ImageJ/GPM/results"):
        if file.endswith(".csv"):
            os.replace(
                f"ImageJ/GPM/results/{file}",
                f"example/ImageJ/results/{file}",
            )
    # Setup the logistic model
    model = setup_regression()
    # Apply logistic regression model to csv output tables
    results_df = pd.DataFrame(
        columns=["Germinated", "Total Conidia", "% Germinated", "Image Name"]
    )
    for csv_file in os.listdir("example/ImageJ/results"):
        if csv_file.endswith(".csv"):
            csv_file = os.path.join("example/ImageJ/results", csv_file)
            data = pd.read_csv(csv_file)
            csv_df = pd.DataFrame(data)
            roi_count, roi_germinated = 0, 0
            for _, row in csv_df.iterrows():
                _id = identify_roi(row, model)
                if _id == -1:
                    # skip debris
                    continue
                roi_germinated += _id
                roi_count += 1
            # Handle empty images
            if roi_count == 0:
                image_data = [0] * 3
            else:
                image_data = [
                    roi_germinated,
                    roi_count,
                    round(roi_germinated / roi_count * 100, 2),
                ]
            image_data.extend([os.path.basename(csv_file).replace(".csv", ".jpg")])
            results_df = pd.concat(
                [
                    results_df,
                    pd.Series(image_data, index=results_df.columns).to_frame().T,
                ],
                ignore_index=True,
            )
    # Show the data to the user
    print(tabulate(results_df, headers=results_df.columns, showindex=False))
    # How much inoculum did we classify?
    totals = [
        [int(results_df["Total Conidia"].sum()), "Total Conidia"],
        [int(results_df["Germinated"].sum()), "Total Germinated"],
        [results_df["% Germinated"].mean(), "Mean Germination %"],
    ]
    print(tabulate(totals))
    input("\n")


if __name__ == "__main__":
    main()
