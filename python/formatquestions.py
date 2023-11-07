import json
import os

# DEFAULTS
question_id = 1
creator_id = 1
template_id = 1
maximum_grade = 10
correct_entity_name = 0.2
marking_entity_correct_attributes = 0.1
marking_entity_correct_primary_keys = 0.2
marking_entity_extra_entity = 0.25
marking_entity_correct_weak_entity = 0.5
marking_entity_correct_relationship_entity = 0.5
marking_entity_correct_cardinality = 0.25
marking_entity_extra_relationship = 0.25
custom_css = ""

directory_to_process = '/Users/tatianaurazova/Desktop/Auto ER project/autoer/python/res/text_correct_answers'
output_directory = '/Users/tatianaurazova/Desktop/Auto ER project/autoer/python/res/questions_formatted'


def create_question(title, ans):
    q = dict()
    q["id"] = question_id
    q["title"] = title
    q["created_by"] = creator_id
    q["question_template"] = template_id
    q["maximum_grade"] = maximum_grade
    q["other_marking_criteria"] = {
        "correct_entity_name": correct_entity_name,
        "correct_attributes": marking_entity_correct_attributes,
        "correct_primary_keys": marking_entity_correct_primary_keys,
        "extra_entity": marking_entity_extra_entity,
        "correct_weak_entity": marking_entity_correct_weak_entity,
        "correct_relationship_entity": marking_entity_correct_relationship_entity,
        "correct_cardinality": marking_entity_correct_cardinality,
        "extra_relationship": marking_entity_extra_relationship
    }
    q["custom_css"] = custom_css
    question_markdown_file = '/Users/tatianaurazova/Desktop/Auto ER project/autoer/python/res/markdown/' + title + '.txt'
    markdown = ""
    try:
        with open(question_markdown_file, 'r') as text_file:
            markdown = text_file.read()
    except IOError as er:
        print(er)
    q["question"] = markdown
    q["answers"] = [{"answer": ans}]
    return q


# clear all files in the directory
for entry in os.scandir(output_directory):
    os.remove(entry)

for entry in os.scandir(directory_to_process):
    # get the answer
    if entry.path.endswith(".txt") and entry.is_file():
        question_name = entry.name.split(".")[0].split("-")[0]
        print(question_name)
        try:
            with open(entry.path, 'r') as text_file:
                answer = text_file.read()
        except IOError as e:
            print(e)
            exit(1)
        # see if the question exist
        question_file = output_directory + "/" + question_name + ".json"
        if not os.path.isfile(question_file):
            question = create_question(question_name, answer)
            question_id += 1
        else:
            question = dict()
            try:
                with open(question_file, 'r') as json_file:
                    question = json.load(json_file)
            except IOError as e:
                print(e)
                exit(1)
            question["answers"].append({"answer": answer})
        try:
            with open(question_file, 'w') as outfile:
                json.dump(question, outfile, indent=4)
        except IOError as e:
            print(e)
            exit(1)
