from django.urls import path

from auto_marking_api.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
    user_who_am_i_view,
)

app_name = "users"
urlpatterns = [
    path("me/", view=user_who_am_i_view, name="me"),
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
]
