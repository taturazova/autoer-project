from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.conf import settings
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    """Default user for auto_marking_api."""

    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
