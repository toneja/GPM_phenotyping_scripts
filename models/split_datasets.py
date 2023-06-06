#!/usr/bin/env python3

import csv
import random
import shutil

def count_values(csv_file, value_name):
    count_0 = 0
    count_1 = 0

    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row[value_name] == '0':
                count_0 += 1
            elif row[value_name] == '1':
                count_1 += 1

    return count_0, count_1

def create_balanced_copy(source_file, target_file, value_name, balanced_count):
    rows_0 = []
    rows_1 = []

    with open(source_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row[value_name] == '0':
                rows_0.append(row)
            elif row[value_name] == '1':
                rows_1.append(row)

    random.shuffle(rows_0)
    random.shuffle(rows_1)

    balanced_rows = rows_0[:balanced_count] + rows_1[:balanced_count]

    with open(target_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(balanced_rows)

def create_training_testing_sets(source_file, training_file, testing_file, value_name):
    rows_0 = []
    rows_1 = []

    with open(source_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row[value_name] == '0':
                rows_0.append(row)
            elif row[value_name] == '1':
                rows_1.append(row)

    random.shuffle(rows_0)
    random.shuffle(rows_1)

    training_count_0 = int(len(rows_0) * 0.7)
    training_count_1 = int(len(rows_1) * 0.7)

    training_rows = rows_0[:training_count_0] + rows_1[:training_count_1]
    testing_rows = rows_0[training_count_0:] + rows_1[training_count_1:]

    with open(training_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(training_rows)

    with open(testing_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(testing_rows)

def main():
    germination_source_file = 'germination_training_data.csv'
    germination_target_file = 'germination_balanced_data.csv'
    germination_value = 'germination'
    germination_0, germination_1 = count_values(germination_source_file, germination_value)
    balanced_count = min(germination_0, germination_1)

    create_balanced_copy(germination_source_file, germination_target_file, germination_value, balanced_count)
    print(f"Created balanced copy: {germination_target_file}")

    spore_source_file = 'spore_training_data.csv'
    spore_target_file = 'spore_balanced_data.csv'
    spore_value = 'spore'
    spore_0, spore_1 = count_values(spore_source_file, spore_value)
    balanced_count = min(spore_0, spore_1)

    create_balanced_copy(spore_source_file, spore_target_file, spore_value, balanced_count)
    print(f"Created balanced copy: {spore_target_file}")

    germination_training_file = 'germination_training_set.csv'
    germination_testing_file = 'germination_testing_set.csv'
    create_training_testing_sets(germination_target_file, germination_training_file, germination_testing_file, germination_value)
    print(f"Created training set: {germination_training_file}")
    print(f"Created testing set: {germination_testing_file}")

    spore_training_file = 'spore_training_set.csv'
    spore_testing_file = 'spore_testing_set.csv'
    create_training_testing_sets(spore_target_file, spore_training_file, spore_testing_file, spore_value)
    print(f"Created training set: {spore_training_file}")
    print(f"Created testing set: {spore_testing_file}")

if __name__ == '__main__':
    main()
