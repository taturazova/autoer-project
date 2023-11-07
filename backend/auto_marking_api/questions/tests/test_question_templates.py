import pytest
from model_bakery import baker
from django.conf import settings
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.forms.models import model_to_dict
import json

from auto_marking_api.questions.models import QuestionTemplate, QuestionType

pytestmark = pytest.mark.django_db


def test_get_question_template():
    """
    Returns a question template when authenticated user requests it
    """
    user = baker.make(settings.AUTH_USER_MODEL, is_active=True, username="joe")
    question_type = baker.make(QuestionType, created_by=user, question_type="MC")
    html_body = "<p>Hello World</p>"

    question_template = baker.make(
        QuestionTemplate,
        created_by=user,
        question_type=question_type,
        body=html_body,
    )

    url = reverse(
        "questions:question-template-detail",
        kwargs={"pk": question_template.pk},
    )

    client = APIClient()
    token = Token.objects.create(user=user)
    client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
    response = client.get(url)
    assert response.status_code == 200

    assert response.json() == {
        "body": html_body,
        "question_type": model_to_dict(question_type),
        "url": f"http://testserver/questions/question-template/{question_template.pk}/",
        "id": question_template.pk,
    }
