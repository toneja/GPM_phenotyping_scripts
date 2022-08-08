#!/usr/bin/python3

"""docstring goes here"""

from csv_handler import csv_handler
import treatments

_0hr_results = csv_handler(0)
_48hr_results = csv_handler(48)
resistant = []
efficacious = []
controls_area = []
controls_perim = []

for i in range(96):
    area_increase = 0
    perim_increase = 0
    # if _0hr_results[i][1] < _48hr_results[i][1]:
    area_increase = round(_48hr_results[i][1] - _0hr_results[i][1], 3)
    # if _0hr_results[i][2] < _48hr_results[i][2]:
    perim_increase = round(_48hr_results[i][2] - _0hr_results[i][2], 3)
    if treatments.PLATE6A_TREATMENT_MAP[i] == treatments.CNTL:
        controls_area.append(area_increase)
        controls_perim.append(perim_increase)
    else:
        if area_increase > 20 and perim_increase > 10:
            if not resistant.count(treatments.PLATE6A_TREATMENT_MAP[i]):
                resistant.append(treatments.PLATE6A_TREATMENT_MAP[i])
        else:
            if not efficacious.count(treatments.PLATE6A_TREATMENT_MAP[i]):
                efficacious.append(treatments.PLATE6A_TREATMENT_MAP[i])

print("The average area increased in the controls by:")
print(*controls_area, sep="\n")
print()
print("The average perimeter increased in the controls by:")
print(*controls_perim, sep="\n")

quit()
print(f"Isolate napa05-pb is likely NOT resistant the following treatments:")
print(*efficacious, sep="\n")
print()
print(f"Isolate napa05-pb is likely resistant to the following treatments:")
print(*resistant, sep="\n")
