import csv
import os

# use only "correct" or "student" as values for t
test_directory = 'res/json_student_answers'
output_file = 'res/testcases.csv'

data = [['Correct Answer', 'Test Answer', 'Expected Grade']]
for entry in os.scandir(test_directory):
    if entry.path.endswith(".json") and entry.is_file():
        test_name = entry.name.split(".")[0].split("-")[0]
        test_name += ".json"
        row = [test_name, entry.name, 0]
        data.append(row)

with open(output_file, mode='w', newline='') as out:
    test_csv_writer = csv.writer(out)
    test_csv_writer.writerows(data)
