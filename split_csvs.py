#!/usr/bin/python3

import csv

def split_csvs():
    germinated_training_data = []
    ungerminated_training_data = []
    headers = [
        "ID",
        "Area",
        "Perim.",
        "Major",
        "Minor",
        "Circ.",
        "Feret",
        "MinFeret",
        "AR",
        "germination",
    ]
    with open(
        "germination_training_data.csv", "r"
    ) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=",")
        for row in csv_reader:
            row_data = [
                int(row["ID"]),
                int(row["Area"]),
                float(row["Perim."]),
                float(row["Major"]),
                float(row["Minor"]),
                float(row["Circ."]),
                float(row["Feret"]),
                float(row["MinFeret"]),
                float(row["AR"]),
                int(row["germination"]),
            ]
            if int(row["germination"]) == 1:
                germinated_training_data.append(row_data)
            if int(row["germination"]) == 0:
                ungerminated_training_data.append(row_data)

    with open(
        "ungerminated_training_data.csv",
        "w",
        newline="",
    ) as csv_outfile:
        csv_writer = csv.writer(csv_outfile)
        csv_writer.writerow(headers)
        for row in ungerminated_training_data:
            csv_writer.writerow(row)

    with open(
        "germinated_training_data.csv",
        "w",
        newline="",
    ) as csv_outfile:
        csv_writer = csv.writer(csv_outfile)
        csv_writer.writerow(headers)
        for row in germinated_training_data:
            csv_writer.writerow(row)


if __name__ == "__main__":
    split_csvs()
