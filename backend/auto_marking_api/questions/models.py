"""Models for the answer feature"""
from uuid import uuid4
from django.db import models


class QuestionType(models.Model):
    """Model representing a question Type"""

    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey("users.User", on_delete=models.PROTECT)
    question_type = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        default=None,
    )
    description = models.CharField(max_length=100, blank=True, null=True, default=None)

    def __str__(self):
        return self.question_type


class QuestionTemplate(models.Model):
    """Model representing an question template of html"""

    body = models.TextField(max_length=300000, blank=True)
    marking_code = models.TextField(max_length=300000, blank=True)
    marker_page = models.TextField(max_length=300000, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey("users.User", on_delete=models.PROTECT)
    question_type = models.ForeignKey(
        QuestionType, on_delete=models.PROTECT, null=False
    )

    def __str__(self):
        return str(self.id) + " " + self.question_type.question_type


class Question(models.Model):
    """Model representing an question"""

    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey("users.User", on_delete=models.PROTECT)
    question = models.TextField(
        max_length=10000,
        blank=True,
        null=True,
        default=None,
    )

    title = models.CharField(max_length=100, blank=True, null=True, default=None)
    maximum_grade = models.DecimalField(decimal_places=2,max_digits=5, default=10.00)
    
    # SELECT PENALTY TYPE
    # 0 - restricting number of attempts
    # 1 - regression
    # 2 - give student a choice
    # 3 - random assign
    penalty_type=models.IntegerField(blank=False,default=0)

    # Restricting number of attempts
    maximum_attempts=models.IntegerField(blank=True,default=-1)

    other_marking_criteria = models.TextField(max_length=1000, blank=True)
    custom_css = models.TextField(max_length=1000, blank=True)

    question_template = models.ForeignKey(
        QuestionTemplate, on_delete=models.PROTECT, null=False, default="8"
    )

    def __str__(self):
        if self.title:
            return str(self.id) + " " + self.title
        return str(self.id)


class PotentialAnswer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="potential_answers",
    )
    answer = models.TextField(max_length=1000, blank=True)
    is_correct = models.BooleanField(default=False)


class StudentAnswer(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey("users.User", on_delete=models.PROTECT)
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="student_answers",
    )
    answer = models.TextField(max_length=1000, blank=True)
    ip_address = models.GenericIPAddressField(null=True)
    mark = models.CharField(max_length=100, null=True, blank=True, default=None)
    total = models.CharField(max_length=100, null=True, blank=True, default=None)

    # Penalty type

    # 0 - restricting number of attempts
    # 1 - regression
    penalty_type=models.IntegerField(blank=False,default=0)
    # Restricting number of attempts
    attempt_number=models.IntegerField(blank=False, default=None)

    # Accumulated regression penalty
    regression_penalty=models.CharField(max_length=100, null=True, blank=True, default=None)
    previous_mark=models.CharField(max_length=100, null=True, blank=True, default=None)
    
    feedback = models.TextField(max_length=1000, null=True, blank=True, default=None)
    marker_feedback = models.TextField(max_length=1000, null=True, blank=True, default=None)

class GeneratedQuestionType(models.Model):
    """Model representing a generated question Type"""
    description = models.CharField(max_length=100, blank=True, null=True, default=None)
    question_template = models.ForeignKey(
        QuestionTemplate, on_delete=models.PROTECT, null=False
    )
    maximum_grade = models.DecimalField(decimal_places=2,max_digits=5, default=10.00)
    generation_code = models.TextField(max_length=300000, blank=True)

    def __str__(self):
        if self.description:
            return str(self.id) + " " + self.description
        return str(self.id)

class GeneratedQuestionDetail(models.Model):
    """Model representing the details of a generated question"""
    date_created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey("users.User", on_delete=models.PROTECT)
    question_type = models.ForeignKey(
        GeneratedQuestionType, on_delete=models.PROTECT, null=False
    )
    question_seed = models.CharField(max_length=100, blank=False, null=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=False)




