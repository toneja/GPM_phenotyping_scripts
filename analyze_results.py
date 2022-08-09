#!/usr/bin/python3

"""docstring goes here"""

import sys

from csv_handler import csv_handler
import treatments

plate = sys.argv[1]
isolate = sys.argv[2]
_0hr_results = csv_handler(plate, isolate, 0)
_48hr_results = csv_handler(plate, isolate, 48)

resistant = []
efficacious = []
controls_area = []
controls_perim = []

for i in range(96):
    area_increase = round(_48hr_results[i][1] - _0hr_results[i][1], 3)
    perim_increase = round(_48hr_results[i][2] - _0hr_results[i][2], 3)
    if treatments.get_treatments(plate, i) == treatments.CNTL:
        controls_area.append(area_increase)
        controls_perim.append(perim_increase)
    else:
        if area_increase > 23 and perim_increase > 5:
            if not resistant.count(treatments.get_treatments(plate, i)):
                resistant.append(treatments.get_treatments(plate, i))
        else:
            if not efficacious.count(treatments.get_treatments(plate, i)):
                efficacious.append(treatments.get_treatments(plate, i))

print(f"Results for isolate {isolate.upper()} from {plate.upper()}:")
print()

controls_area.sort()
print("The average area increased in the controls by:")
for x in controls_area:
    print(f"\t{x}")
print()
controls_perim.sort()
print("The average perimeter increased in the controls by:")
for x in controls_perim:
    print(f"\t{x}")
print()

efficacious.sort()
print(f"Isolate {isolate.upper()} is likely NOT resistant the following treatments:\t")
for x in efficacious:
    print(f"\t{x}")
print()
resistant.sort()
print(f"Isolate {isolate.upper()} is likely resistant to the following treatments:\t")
for x in resistant:
    print(f"\t{x}")
