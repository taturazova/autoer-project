import pytest
from model_bakery import baker
from django.conf import settings
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.forms.models import model_to_dict
import json
from auto_marking_api.questions.models import Question, PotentialAnswer, QuestionType, Mark

pytestmark = pytest.mark.django_db

def test_get_question():
    """
    Returns a question when authenticated user requests it
    """
    user = baker.make(settings.AUTH_USER_MODEL, is_active=True, username="joe")

    question_type = baker.make(QuestionType, created_by=user, question_type="MC")

    question = baker.make(
        Question,
        created_by=user,
        question="Who's the best Beatle?",
        question_type=question_type,
    )

    george = model_to_dict(
        baker.make(PotentialAnswer, question=question, is_correct=True, answer="George")
    )
    ringo = model_to_dict(
        baker.make(PotentialAnswer, question=question, is_correct=False, answer="Ringo")
    )
    paul = model_to_dict(
        baker.make(PotentialAnswer, question=question, is_correct=False, answer="Paul")
    )
    john = model_to_dict(
        baker.make(PotentialAnswer, question=question, is_correct=False, answer="John")
    )

    url = reverse("questions:question-detail", kwargs={"pk": question.pk})
    print(url)
    client = APIClient()
    token = Token.objects.create(user=user)
    client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
    response = client.get(url)
    assert response.status_code == 200

    assert response.json() == {
        "question": "Who's the best Beatle?",
        "question_type": model_to_dict(question_type),
        "potential_answers": [george, ringo, paul, john],
        "id": question.pk,
        "url": f"http://testserver/questions/question/{question.pk}/",
    }
