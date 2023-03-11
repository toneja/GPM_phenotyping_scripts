#!/usr/bin/python3

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

# globals
WORKDIR, GERMINATION, SPORE = "", "", ""


def setup_regression(model):
    """docstring goes here"""
    dataset = pandas.read_csv(f"{WORKDIR}/{model}_training_data.csv")
    if model == "germination":
        vals = ["Perim.", "Circ."]
    elif model == "spore":
        vals = [
            "Area",
            "Major",
            "Minor",
            "Circ.",
            "Feret",
            "MinFeret",
            "AR",
        ]
    _x = dataset[vals]
    _y = dataset[model]

    regression = linear_model.LogisticRegression(solver="liblinear", multi_class="ovr")
    regression.fit(_x.values, _y)

    return regression


def is_germinated(row):
    """docstring goes here"""
    prediction = GERMINATION.predict(
        [
            [
                float(row["Perim."]),
                float(row["Circ."]),
            ]
        ]
    )
    return float(prediction) >= 0.85


def is_spore(row):
    """docstring goes here"""
    prediction = SPORE.predict(
        [
            [
                int(row["Area"]),
                float(row["Major"]),
                float(row["Minor"]),
                float(row["Circ."]),
                float(row["Feret"]),
                float(row["MinFeret"]),
                float(row["AR"]),
            ]
        ]
    )
    return float(prediction) >= 0.85


def analyze_results(plate, isolate, size):
    """docstring goes here"""
    _0hr_results = csv_handler(plate, isolate, 0)
    _48hr_results = csv_handler(plate, isolate, 48)

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
        "Debris",
    ]
    for block in range(size):
        if block > 9:
            img_name = f"Image_00{block}.jpg"
        else:
            img_name = f"Image_000{block}.jpg"

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
                img_name,
                int(_48hr_results[block][6]),
            ]
        )

    # Sort the data by treatment with the controls at the top
    germination_data.sort()
    i = 0
    for item in germination_data:
        if item[0] == "Control":
            germination_data.insert(0, germination_data.pop(i))
        i += 1

    # Write the results to the output file
    with open(
        f"{WORKDIR}/FinalResults_{plate}_{isolate}.csv",
        "w",
        newline="",
    ) as csv_outfile:
        csv_writer = csv.writer(csv_outfile)
        csv_writer.writerow(headers)
        for row in germination_data:
            csv_writer.writerow(row)

    # Print a table of the results for the user
    print(tabulate(germination_data, headers=headers))
    print(f"* Calculated results for isolate {isolate.upper()} from {plate.upper()}")


# handle csv datasets
def csv_handler(plate, isolate, time):
    """docstring goes here"""
    # open csv file
    with open(f"{WORKDIR}/Results_{plate}_{isolate}_{time}hr.csv", "r") as csv_file:
        # read csv as a dict so header is skipped and value lookup is simpler
        csv_reader = csv.DictReader(csv_file, delimiter=",")
        slice_data = []
        roi_count, roi_germinated, debris_rois = 0, 0, 0
        area_total, perim_total, feret_total = 0, 0, 0
        slice_count = 1
        for row in csv_reader:
            # new debris filter
            if not is_spore(row) and not is_germinated(row):
                debris_rois += 1
                continue
            # calculate totals for each slice
            if int(row["Slice"]) == slice_count:
                roi_count += 1
                if is_germinated(row):
                    roi_germinated += 1
                area_total += int(row["Area"])
                perim_total += float(row["Perim."])
                feret_total += float(row["Feret"])
            else:
                # once we've hit the next slice, calculate percentage and store the data
                slice_data.append(
                    [
                        roi_germinated,
                        roi_count,
                        roi_germinated / roi_count * 100,
                        round(area_total / roi_count, 1),
                        round(perim_total / roi_count, 1),
                        round(feret_total / roi_count, 1),
                        debris_rois,
                    ]
                )
                slice_count += 1
                roi_count = 1
                area_total = int(row["Area"])
                perim_total = float(row["Perim."])
                feret_total = float(row["Feret"])
                if is_germinated(row):
                    roi_germinated = 1
                else:
                    roi_germinated = 0
                debris_rois = 0
        # outside of the loop, calculate and store value for the last slice
        slice_data.append(
            [
                roi_germinated,
                roi_count,
                roi_germinated / roi_count * 100,
                round(area_total / roi_count, 1),
                round(perim_total / roi_count, 1),
                round(feret_total / roi_count, 1),
                debris_rois,
            ]
        )
        return slice_data


def main(filename):
    """docstring goes here"""
    global WORKDIR, GERMINATION, SPORE
    args = os.path.splitext(os.path.basename(filename))[0].split("_")
    plate = args[1]
    isolate = args[2]
    # Default is 96 wells
    size = 8 * 12

    WORKDIR = os.path.dirname(filename)
    if not WORKDIR:
        WORKDIR = "."
    GERMINATION = setup_regression("germination")
    SPORE = setup_regression("spore")
    analyze_results(plate, isolate, size)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        sys.exit(f"Usage: {sys.argv[0]} [FILE]")
