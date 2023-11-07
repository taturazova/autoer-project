import json
import ermarker
import pytest

cor_answer = "practice_final.json"
stu_answer = "practice-1.json"
mark = 0


def get_data():
    data = []
    answer_dir = '/Users/tatianaurazova/Desktop/Auto ER project/autoer/python/res/questions_formatted/'
    student_dir = '/Users/tatianaurazova/Desktop/Auto ER project/autoer/python/res/json_student_answers/'

    answer_filename = answer_dir + cor_answer
    correct_answer = ""
    try:
        with open(answer_filename, 'r') as answer_json_file:
            correct_answer = json.load(answer_json_file)
    except IOError as e:
        print(e)
        exit(1)
    student_filename = student_dir + stu_answer
    student_answer = ""
    try:
        with open(student_filename, 'r') as stu_json_file:
            student_answer = json.load(stu_json_file)
    except IOError as e:
        print(e)
        exit(1)
    expected_mark = mark
    data.append([correct_answer, student_answer, expected_mark])
    return data


print(ermarker.mark_answer(get_data()[0][0], get_data()[0][1]))


@pytest.mark.parametrize("question, student_answer, expected_mark", get_data())
def test_mark(question, student_answer, expected_mark):
    result = ermarker.mark_answer(question, student_answer)
    assert result["mark"] == expected_mark


# @pytest.mark.parametrize("question, student_answer, expected_mark", get_data())
# def test_answer(question, student_answer, expected_mark):
#     result = ermarker.mark_answer(question, student_answer)
#     assert result["answer"] == result["correct_answer"]
