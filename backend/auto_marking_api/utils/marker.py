from django.forms.models import model_to_dict
from auto_marking_api.questions.models import (
    Question,
    QuestionTemplate,
    PotentialAnswer,
)


# retrieve question from the database
def get_question(qid):
    question_obj = Question.objects.get(pk=qid)
    max_grade = float(str(question_obj.maximum_grade))
    question = model_to_dict(question_obj)
    question["maximum_grade"] = max_grade
    return question

def get_potential_answers(qid):
    answer_set = PotentialAnswer.objects.filter(question=qid)
    potential_answers = []
    for answer in answer_set:
        potential_answers.append(model_to_dict(answer))
    return potential_answers

# retrieve marking code from the database
def get_marking_code(template_id):
    questionTemplate = QuestionTemplate.objects.get(pk=template_id)
    code = questionTemplate.marking_code
    return code


def mark_answer(qid, answer):
    question = get_question(qid)
    potential_answers = get_potential_answers(qid)
    marking_code = get_marking_code(question["question_template"])
    result = compile(marking_code, 'mark_answer', 'exec')
    args = {
        "___question___": question,
        "___potential_answers___": potential_answers,
        "___student_answer___": answer,
        "___results___": ""
    }
    exec(result, args)

    marking_code_results=args["___results___"]
    
    return marking_code_results

