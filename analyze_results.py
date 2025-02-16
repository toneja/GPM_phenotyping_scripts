#!/usr/bin/python3
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
    Erysiphe Necator Fungicide Efficacy Assay
    ImageJ results analysis script

"""

import csv
import os
import sys
import pandas
from sklearn import linear_model
from tabulate import tabulate
from treatments import get_treatments


def setup_regression():
    """Setup the logistic regression used to determine ROI identity."""
    dataset = pandas.read_csv("models/model_training_data.csv")
    vals = [
        "Area",
        "Perim.",
        "Major",
        "Minor",
        "Circ.",
        "Feret",
        "MinFeret",
        "AR",
        "Round",
        "Solidity",
    ]
    _x = dataset[vals]
    _y = dataset["class"]

    regression = linear_model.LogisticRegression(solver="newton-cg", max_iter=1000)
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
                float(row["MinFeret"]),
                float(row["AR"]),
                float(row["Round"]),
                float(row["Solidity"]),
            ]
        ]
    )
    return float(prediction)


def analyze_results(plate, isolate):
    """Compare 0hr and 48hr results and calculate full results for the plate."""
    # load the logistic model used for image classification
    model = setup_regression()
    results_path = f"ImageJ/GPM/results/{plate}_{isolate}_"
    images_path = f"ImageJ/GPM/images/{plate}_{isolate}_"
    _48hr_results = [
        csv_handler(os.path.join(f"{results_path}48hr", csv_file), model)
        for csv_file in os.listdir(f"{results_path}48hr")
    ]
    i = 0
    for file in os.listdir(f"{images_path}48hr"):
        if not os.path.exists(f"{results_path}48hr/{file.replace('.tif', '.csv')}"):
            _48hr_results.insert(
                i, [0, 0, 0, 0, 0, 0, f"{file.replace('.tif', '.jpg')} - BAD IMAGE"]
            )
        i += 1
    _48hr_size = len(_48hr_results)
    if os.path.exists(f"{results_path}0hr"):
        _0hr_results = [
            csv_handler(os.path.join(f"{results_path}0hr", csv_file), model)
            for csv_file in os.listdir(f"{results_path}0hr")
        ]
        i = 0
        for file in os.listdir(f"{images_path}0hr"):
            if not os.path.exists(f"{results_path}0hr/{file.replace('.tif', '.csv')}"):
                _0hr_results.insert(i, [0, 0, 0, 0, 0, 0, file.replace(".tif", ".jpg")])
            i += 1
    else:
        _0hr_results = [[0, 0, 0, 0, 0, 0, "NA"]] * _48hr_size
    # Output data and file headers
    germination_data = []
    headers = [
        "Treatment",
        "0hr %",
        "48hr %",
        "Germinated",
        "Total",
        "Area change",
        "Perimeter change",
        "Feret change",
        "Image",
    ]
    for block in range(_48hr_size):
        germination_data.append(
            [
                get_treatments(plate, block),
                round(_0hr_results[block][2], 1),
                round(_48hr_results[block][2], 1),
                int(_48hr_results[block][0]),
                int(_48hr_results[block][1]),
                round(_48hr_results[block][3] - _0hr_results[block][3], 1),
                round(_48hr_results[block][4] - _0hr_results[block][4], 1),
                round(_48hr_results[block][5] - _0hr_results[block][5], 1),
                _48hr_results[block][6],
            ]
        )

    # 24-well UV-C assay does not require as much information
    if _48hr_size < 96:
        locs = [7, 6, 5, 1]
        for loc in locs:
            headers.remove(headers[loc])
            for data in germination_data:
                data.remove(data[loc])

    # Sort the data by treatment with the controls and SHAM at the top
    germination_data.sort()
    i = 0
    for item in germination_data:
        if item[0] == "Control":
            germination_data.insert(0, germination_data.pop(i))
        elif item[0] == "SHAM 100 μg/mL":
            germination_data.insert(8, germination_data.pop(i))
        elif item[0] == "Trifloxystrobin 10 μg/mL":
            germination_data.insert(40, germination_data.pop(i))
        i += 1

    # Write the results to the output file
    with open(
        f"results/FinalResults_{plate}_{isolate}.csv",
        "w",
        encoding="utf-8",
        newline="",
    ) as csv_outfile:
        csv_writer = csv.writer(csv_outfile)
        csv_writer.writerow(headers)
        for row in germination_data:
            csv_writer.writerow(row)

    # Print a table of the results for the user
    print(f"* Results for isolate {isolate.upper()} from {plate.upper()}")
    print(tabulate(germination_data, headers=headers))


# handle csv datasets
def csv_handler(input_file, model):
    """Read CSV file produced by ImageJ and analyze each ROI using logistic regression."""
    # open csv file
    with open(
        input_file,
        "r",
        encoding="utf-8",
    ) as csv_file:
        # read csv as a dict so header is skipped and value lookup is simpler
        csv_reader = csv.DictReader(csv_file, delimiter=",")
        roi_count, roi_germinated = 0, 0
        area_total, perim_total, feret_total = 0, 0, 0
        for row in csv_reader:
            # new debris filter
            _id = identify_roi(row, model)
            if _id == -1:
                # skip bad ROIs
                continue
            roi_germinated += _id
            roi_count += 1
            area_total += int(row["Area"])
            perim_total += float(row["Perim."])
            feret_total += float(row["Feret"])
        # Handle empty images
        if roi_count == 0:
            image_data = [0] * 6
        else:
            image_data = [
                roi_germinated,
                roi_count,
                roi_germinated / roi_count * 100,
                round(area_total / roi_count, 1),
                round(perim_total / roi_count, 1),
                round(feret_total / roi_count, 1),
            ]
        image_data.extend([os.path.basename(input_file).replace(".csv", ".jpg")])
    return image_data


def main(filename):
    """Execute the main objective."""
    args = os.path.basename(filename).split("_")
    plate = args[0]
    isolate = args[1]

    os.chdir(os.path.dirname(__file__))
    analyze_results(plate, isolate)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        sys.exit(f"Usage: {sys.argv[0]} [FOLDER]")
