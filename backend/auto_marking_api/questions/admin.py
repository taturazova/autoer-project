from django.contrib import admin
from django import forms
from auto_marking_api.questions import models
from auto_marking_api.questions.models import Question, QuestionTemplate


class PotentialAnswerAdmin(admin.ModelAdmin):
    list_display = ("id", "answer", "is_correct")
    ordering = ("question__question", "id")


class QuestionTypeAdmin(admin.ModelAdmin):
    list_display = ["id", "question_type", "description"]


class QuestionAdminForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["id", "question"]
        widgets = {
            "text": forms.Textarea(attrs={"cols": 80, "rows": 100}),
        }


class QuestionAdmin(admin.ModelAdmin):
    list_display = ["id", "title","penalty_type"]

    def get_form(self, request, obj=None, **kwargs):
        kwargs["widgets"] = {"question": forms.Textarea}
        return super().get_form(request, obj, **kwargs)


class QuestionTemplateAdminForm(forms.ModelForm):
    class Meta:
        model = QuestionTemplate
        fields = ["id", "body"]
        widgets = {
            "text": forms.Textarea(attrs={"cols": 80, "rows": 100}),
        }


class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ["id", "question","penalty_type", "answer","attempt_number", "created", "created_by"]


class QuestionTemplateAdmin(admin.ModelAdmin):
    list_display = ["id","question_type"]

    def get_form(self, request, obj=None, **kwargs):
        kwargs["widgets"] = {"body": forms.Textarea}
        return super().get_form(request, obj, **kwargs)

class GeneratedQuestionTypeAdmin(admin.ModelAdmin):
    list_display = ["id","description", "question_template"]

class GeneratedQuestionDetailAdmin(admin.ModelAdmin):
    list_display = ["id","date_created", "created_by", "question_type"]


admin.site.register(models.Question, QuestionAdmin)
admin.site.register(models.QuestionTemplate, QuestionTemplateAdmin)
admin.site.register(models.QuestionType, QuestionTypeAdmin)
admin.site.register(models.PotentialAnswer, PotentialAnswerAdmin)
admin.site.register(models.StudentAnswer, StudentAnswerAdmin)
admin.site.register(models.GeneratedQuestionType, GeneratedQuestionTypeAdmin)
admin.site.register(models.GeneratedQuestionDetail, GeneratedQuestionDetailAdmin)
