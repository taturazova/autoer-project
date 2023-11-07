import json
import ermarker
import pytest
from csv import reader


def get_data():
    data = []
    testcases = 'res/testcases.csv'
    answer_dir = 'res/questions_formatted/'
    student_dir = 'res/json_student_answers/'

    with open(testcases, 'r') as read_obj:
        csv_reader = reader(read_obj)
        next(csv_reader)
        print(next(csv_reader))
        for row in csv_reader:
            print(row)
            answer_filename = answer_dir + row[0]
            correct_answer = ""
            try:
                with open(answer_filename, 'r') as answer_json_file:
                    correct_answer = json.load(answer_json_file)
            except IOError as e:
                print(e)
                exit(1)
            student_filename = student_dir + row[1]
            student_answer = ""
            try:
                with open(student_filename, 'r') as stu_json_file:
                    student_answer = json.load(stu_json_file)
            except IOError as e:
                print(e)
                exit(1)
            expected_mark = float(row[2])
            data.append([correct_answer, student_answer, expected_mark])
    return data


@pytest.mark.parametrize("question, student_answer, expected_mark", get_data())
def test_mark(question, student_answer, expected_mark):
    result = ermarker.mark_answer(question, student_answer)
    assert result["mark"] == expected_mark
