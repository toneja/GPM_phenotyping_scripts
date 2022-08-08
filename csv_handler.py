#!/usr/bin/python3

"""docstring goes here"""

import csv

# handle csv datasets
def csv_handler(time):
    """docstring goes here"""
    # open csv file; hardcoded file name for now
    with open("Results_plate6a_napa05-pb_" + str(time) + "hr.csv", "r") as csv_file:
        # read csv as a dict so header is skipped and value lookup is simpler
        csv_reader = csv.DictReader(csv_file, delimiter=",")
        # slice data list => [[slice_count, area_avg, perim_avg], [...]]
        slice_data = []
        # set counts and totals to zero
        roi_count = 0
        area_total = 0
        perim_total = 0
        # start with Slice 1
        slice_count = 1
        # iterate over the csv values row by row
        for row in csv_reader:
            # calculate totals for each slice
            if int(row["Slice"]) == slice_count:
                roi_count += 1
                area_total += int(row["Area"])
                perim_total += float(row["Perim."])
            else:
                # once we've hit the next slice, calculate averages and store the data
                area_avg = round(area_total / roi_count, 3)
                perim_avg = round(perim_total / roi_count, 3)
                slice_data.append([slice_count, area_avg, perim_avg])
                # move to the next slice
                slice_count += 1
                # start counts and totals with current values since we're on the first of new slice
                roi_count = 1
                area_total = int(row["Area"])
                perim_total = float(row["Perim."])
        # outside of the loop, calculate and store values for the last slice
        area_avg = round(area_total / roi_count, 3)
        perim_avg = round(perim_total / roi_count, 3)
        slice_data.append([slice_count, area_avg, perim_avg])
        # return Slice data
        return slice_data
