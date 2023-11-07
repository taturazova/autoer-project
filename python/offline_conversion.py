import json
import nomnomltojson
import os

# use only "correct" or "student" as values for t
t = "student"
directory_to_process = '/Users/tatianaurazova/Desktop/Auto ER project/autoer/python/res/text_' + t + '_answers'
output_directory = '/Users/tatianaurazova/Desktop/Auto ER project/autoer/python/res/json_' + t + '_answers'

def process_directory(directory):
    for entry in os.scandir(directory):
        if entry.path.endswith(".txt") and entry.is_file():
            data = ""
            try:
                with open(entry.path, 'r') as text_file:
                    data = text_file.read()
            except IOError as e:
                print(e)
                exit(1)

            out_filename = entry.path.replace(".txt", ".json")
            out_filename = out_filename.replace(directory_to_process, output_directory)
            print(out_filename)
            try:
                with open(out_filename, 'w') as outfile:
                    json.dump(nomnomltojson.convert(data), outfile, indent=4)
            except IOError as e:
                print(e)
                exit(1)


process_directory(directory_to_process)
