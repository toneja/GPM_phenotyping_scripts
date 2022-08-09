#!/usr/bin/python3

"""docstring goes here"""

import sys

from csv_handler import csv_handler
import treatments

def analyze_results(plate, isolate):
    """docstring goes here"""
    debug = True

    _0hr_results = csv_handler(plate, isolate, 0)
    _48hr_results = csv_handler(plate, isolate, 48)

    resistant, efficacious, controls_area, controls_perim, controls_roundness = [], [], [], [], []

    for i in range(96):
        area_increase = round(_48hr_results[i][0] - _0hr_results[i][0], 3)
        perim_increase = round(_48hr_results[i][1] - _0hr_results[i][1], 3)
        roundness_decrease = round(_0hr_results[i][2] - _48hr_results[i][2], 3)
        if treatments.get_treatments(plate, i) == treatments.CNTL:
            controls_area.append(area_increase)
            controls_perim.append(perim_increase)
            controls_roundness.append(roundness_decrease)
        else:
            if area_increase > 23 and perim_increase > 5 and roundness_decrease > 0.1:
                if not resistant.count(treatments.get_treatments(plate, i)):
                    resistant.append(treatments.get_treatments(plate, i))
            else:
                if not efficacious.count(treatments.get_treatments(plate, i)):
                    efficacious.append(treatments.get_treatments(plate, i))

    print(f"Results for isolate {isolate.upper()} from {plate.upper()}:")
    print()

    if debug:
        controls_area.sort()
        print("The average area increased in the controls by:")
        for item in controls_area:
            print(f"\t{item}")
        print()
        controls_perim.sort()
        print("The average perimeter increased in the controls by:")
        for item in controls_perim:
            print(f"\t{item}")
        print()
        controls_roundness.sort()
        print("The average roundness decreased in the controls by:")
        for item in controls_roundness:
            print(f"\t{item}")
        print()

    efficacious.sort()
    print(f"Isolate {isolate.upper()} is likely NOT resistant to the following treatments:\t")
    for item in efficacious:
        print(f"\t{item}")
    print()
    resistant.sort()
    print(f"Isolate {isolate.upper()} is likely resistant to the following treatments:\t")
    for item in resistant:
        print(f"\t{item}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} [PLATE] [ISOLATE]")
    else:
        analyze_results(sys.argv[1], sys.argv[2])
