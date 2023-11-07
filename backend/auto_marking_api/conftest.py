import pytest
from django.conf import settings
from django.test import RequestFactory
from model_bakery import baker


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> settings.AUTH_USER_MODEL:
    return baker.make(settings.AUTH_USER_MODEL)


@pytest.fixture
def request_factory() -> RequestFactory:
    return RequestFactory()
