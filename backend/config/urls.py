from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include, reverse_lazy
from django.views import defaults as default_views
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from rest_framework.authtoken import views


print(settings.ADMIN_URL, admin.site.urls)
urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path(
        "api/about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    ),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("api/users/", include("auto_marking_api.users.urls", namespace="users")),
    path("api/accounts/", include("allauth.urls")),
    path("api/", include("auto_marking_api.questions.urls", namespace="questions")),
    path("api/rest-auth/", include('rest_auth.urls')),
    path("api/api-token-auth/", views.obtain_auth_token),
    path("api/api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    # Your stuff: custom urls includes go here
    re_path(r"^$", RedirectView.as_view(url=reverse_lazy("api-root"), permanent=False)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns