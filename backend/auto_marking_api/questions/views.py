"""
Views for the answers app.
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics

from auto_marking_api.questions.models import (
    Question, 
    QuestionTemplate, 
    StudentAnswer, 
    GeneratedQuestionType,
    GeneratedQuestionDetail,
)
from auto_marking_api.questions.serializers import (
    QuestionSerializer,
    QuestionTemplateSerializer,
    StudentAnswerSerializer,
    GeneratedQuestionTypeSerializer,
    GeneratedQuestionDetailSerializer,

)


class QuestionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return Question.objects.all().order_by(
            "-created"
        )


class QuestionTemplateViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = QuestionTemplateSerializer

    def get_queryset(self):
        return QuestionTemplate.objects.all().order_by(
            "-created"
        )

class LastAnswerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = StudentAnswerSerializer

    def get_queryset(self):
        return StudentAnswer.objects.filter(created_by=self.request.user).order_by(
            "-created"
        )
class UserAnswers(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudentAnswerSerializer

    def get_queryset(self):
        print(self.kwargs['user'])
        # I can also try pagination
        # I should be able to create another new view that follows foreign key relationships
        # to speed up question retrieval as well
        answers = StudentAnswer.objects.order_by('created_by').distinct('created_by')
        for answer in answers:
            print(answer)
            if str(answer.created_by) == self.kwargs['user']:
                return StudentAnswer.objects.filter(created_by=answer.created_by).order_by(
                    "-created"
                )
        return StudentAnswer.objects.none()
        
        
class StudentAnswerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = StudentAnswerSerializer
    
    def get_queryset(self):
        return StudentAnswer.objects.all()

class GeneratedQuestionTypeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = GeneratedQuestionTypeSerializer

    def get_queryset(self):
        return GeneratedQuestionType.objects.all()

class GeneratedQuestionDetailViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = GeneratedQuestionDetailSerializer

    def get_queryset(self):
        return GeneratedQuestionDetail.objects.filter(created_by=self.request.user).order_by(
        # return GeneratedQuestionDetail.objects.all().order_by(
            "-date_created"
        )

class AllGeneratedQuestionDetailViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = GeneratedQuestionDetailSerializer

    def get_queryset(self):
        # return GeneratedQuestionDetail.objects.filter(created_by=self.request.user).order_by(
        return GeneratedQuestionDetail.objects.all().order_by(
            "-date_created"
        )
