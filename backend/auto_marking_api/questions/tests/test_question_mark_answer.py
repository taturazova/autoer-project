import pytest
from model_bakery import baker
from django.conf import settings
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.forms.models import model_to_dict
from auto_marking_api.utils.ermarker import mark_answer
from auto_marking_api.utils.nomnomltojson import convert_nomnoml_to_json
from auto_marking_api.questions.models import (
    StudentAnswer,
    QuestionType,
    Question,
    QuestionTemplate,
)
import json

with open("auto_marking_api/questions/answers/autoshop.json") as f:
    autoshop_answer_key = json.load(f)

pytestmark = pytest.mark.django_db


def test_question_mark_answer():
    """
    Accepts the student's Answer, Marks it, and returns a result
    """

    user = baker.make(settings.AUTH_USER_MODEL, is_active=True, username="Becca")
    submitted_answer = """[Estimate|id {PK};cost;time]
[Job|num {PK};repairDate]
[Repair|num;partCost;description]
[Mechanic|name {PK};hourlyRate]
[Car|licnum {PK};make;model;year;custName;custAddress]
[WorksOn|time;laborCost]
[Mechanic]1..1 - [Estimate]
[Estimate]1..* - 1..1[Car]
[Estimate]1..1 - 0..1[Job]
[Job]1..* - 1..1[Car]
[Job]1..1 - 1..*[Repair]
[Mechanic]1..1 - 0..*[WorksOn]
[Repair]1..1 - 1..*[WorksOn]"""

    question_type = baker.make(QuestionType, created_by=user, question_type="MC")
    html_body = "<p>Hello World</p>"

    question_template = baker.make(
        QuestionTemplate,
        created_by=user,
        question_type=question_type,
        body=html_body,
    )

    question = baker.make(
        Question,
        created_by=user,
        question="""[Customers](Customer) bring their [cars](Car) to the shop for an estimate of repairs. \nOne [mechanic](Mechanic) looks at the car and estimates the total [cost](cost) and [time](time) required for the job. \nAn [estimate](Estimate) has a unique [id](id). If the [customer](Customer) accepts the [estimate](Estimate), a [job](Job) is created from the estimate. \nA [job](Job) has a unique [number](num) is scheduled for a certain [date](repairDate). \nInformation on the [car](Car) is recorded such as the car's [license plate number](licnum) (unique), [make](make), [model](model), [year](year), and the customer's [name](custName) and [address](custAddress). \nA car may come in for service multiple times (may have multiple jobs). \nA [job](Job) is divided into a list of [repairs](Repair). Each [repair](Repair) has a [number](num), [part cost](partCost) and [description](description). \nA repair may be [done by](WorksOn) one or more mechanics, who can work for different amounts of [time](time). A mechanic has a unique [name](name) and an [hourly rate](hourlyRate). \nThe [labor cost](laborCost) of a mechanic [working on](WorksOn) a repair is calculated using his time and the mechanic's hourly rate.""",
        question_template=question_template,
    )

    answer_to_mark = baker.make(
        StudentAnswer, question=question, answer=submitted_answer, created_by=user
    )

    # print(answer_to_mark.answer)

    json_answer = convert_nomnoml_to_json(answer_to_mark.answer)

    mark_results = mark_answer(autoshop_answer_key, json_answer)

    # print(mark_results)
    # url = reverse("questions:student-answer-detail", kwargs={"pk": answer_to_mark.pk})
    # client = APIClient()
    # token = Token.objects.create(user=user)
    # client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
    # response = client.get(url)
    # assert response.status_code == 200

    # assert response.json() == {
    #     "question": "Who's the best Beatle?",
    #     "question_type": model_to_dict(question_type),
    #     "potential_answers": [george, ringo, paul, john],
    #     "id": question.pk,
    #     "url": f"http://testserver/questions/question/{question.pk}/",
    # }


# def test_check_nomnoml():

#     some_nomnoml = """[Estimate|id {PK};cost;time]
# [Job|num {PK};repairDate]
# [Repair|num;partCost;description]
# [Mechanic|name {PK};hourlyRate]
# [Car|licnum {PK};make;model;year;custName;custAddress]
# [WorksOn|time;laborCost]
# [Mechanic]1..1 - [Estimate]
# [Estimate]1..* - 1..1[Car]
# [Estimate]1..1 - 0..1[Job]
# [Job]1..* - 1..1[Car]
# [Job]1..1 - 1..*[Repair]
# [Mechanic]1..1 - 0..*[WorksOn]
# [Repair]1..1 - 1..*[WorksOn]"""

#     json_nomnoml = convert_nomnoml_to_json(some_nomnoml)
#     mark_answer()
