from rest_framework.routers import DefaultRouter
from django.conf.urls import url, include

from auto_marking_api.questions import views

app_name = "questions"

router = DefaultRouter()
router.register(r"marks", views.StudentAnswerViewSet, basename="marks")
router.register(r"last-answer", views.LastAnswerViewSet, basename="last-answer")
router.register(r"questions", views.QuestionViewSet, basename="questions")
router.register(
    r"question-templates", views.QuestionTemplateViewSet, basename="question-templates"
)
router.register(
    r"generatedquestiontype", views.GeneratedQuestionTypeViewSet, basename="generatedquestiontype"
)
router.register(
    r"generatedquestiondetails", views.GeneratedQuestionDetailViewSet, basename="generatedquestiondetails"
)
router.register(
    r"allgeneratedquestiondetails", views.AllGeneratedQuestionDetailViewSet, basename="allgeneratedquestiondetails"
)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'user-answers/(?P<user>[^/.]+)/$', views.UserAnswers.as_view(), name="user-list"),
]
