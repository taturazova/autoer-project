"""Serializers for answers app"""
from django.forms.models import model_to_dict
from rest_framework import serializers
from auto_marking_api.questions.models import (
    PotentialAnswer,
    Question,
    QuestionTemplate,
    QuestionType,
    StudentAnswer,
    GeneratedQuestionType,
    GeneratedQuestionDetail,
)
from auto_marking_api.utils.marker import mark_answer
from auto_marking_api.utils.generate import generate_seed, generate_question


class PotentialAnswerSerializer(serializers.ModelSerializer):
    """
    Serializer for Potential answers
    """

    class Meta:
        model = PotentialAnswer
        fields = ("id", "answer", "is_correct", "question")


class QuestionTemplateSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        lookup_field="pk",
        read_only=True,
        view_name="questions:question-templates-detail",
    )

    class Meta:
        model = QuestionTemplate
        fields = ("id", "body", "marking_code", "marker_page", "url")

    def create(self, validated_data):
        return QuestionTemplate.objects.create(
            created_by=self.context["request"].user, **validated_data
        )


class QuestionSerializer(serializers.ModelSerializer):
    """
    Serializer for questions and question templates
    """

    url = serializers.HyperlinkedIdentityField(
        lookup_field="pk",
        read_only=True,
        view_name="questions:questions-detail",
    )

    potential_answers = PotentialAnswerSerializer(many=True, read_only=True)
    question_template = QuestionTemplateSerializer(many=False, read_only=True)

    class Meta:
        model = Question
        fields = (
            "id",
            "title",
            "question",
            "question_template",
            "maximum_grade",
            "penalty_type",
            "maximum_attempts",
            "other_marking_criteria",
            "potential_answers",
            "url",
            "custom_css",
        )

    def create(self, validated_data):
        return Question.objects.create(
            created_by=self.context["request"].user, **validated_data
        )


class StudentAnswerSerializer(serializers.ModelSerializer):
    """
    Serializer for student answers and marking
    """
    user = serializers.SerializerMethodField('get_user')

    def get_user(self, stu):
      user =  model_to_dict(stu.created_by)
      user = {
          'id': user["id"],
          'name': user["name"],
          'username': user["username"]
      }
      return user


    url = serializers.HyperlinkedIdentityField(
        lookup_field="pk",
        read_only=True,
        view_name="questions:marks-detail",
    )

    class Meta:
        model = StudentAnswer
        fields = (
            "id",
            "user",
            "answer",
            "feedback",
            "mark",
            "question",
            "total",
            "penalty_type",
            "attempt_number",
            "regression_penalty",
            "previous_mark",
            "url",
            "ip_address",
            "created",
            "marker_feedback",
        )
    def validate(self, data):
        # here you can access all values
        try:
            print(data)
            answer = data['answer']
            previous_mark=float(data['previous_mark'])
            question = str(data['question']).split(" ")[0]
            result = mark_answer(question, answer)
            print("marked")
            print(result)
            data['total'] = result['total']
            data['feedback'] = result['feedback']
            data['marker_feedback'] = result['marker_feedback']
            data['regression_penalty']=float(data['regression_penalty'])+max(previous_mark-float(result['mark']),0)*0.5
            print("DATA")
            print(data)
            if (data['penalty_type']==1):
                data['mark']=float(result['mark'])-float(data['regression_penalty'])
                data['feedback']=data['feedback']+"Regression Penalty: "+ str(round(float(data['regression_penalty']),2)) + "\n"
            else:
                data['mark']=result['mark']
        except Exception as inst:
        # perform your validation
            raise serializers.ValidationError(inst)
        return data


    def create(self, validated_data):
        x_forwarded_for = self.context.get('request').META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.context.get('request').META.get('REMOTE_ADDR')
        validated_data['ip_address'] = ip
        return StudentAnswer.objects.create(
            created_by=self.context["request"].user, **validated_data
        )

class GeneratedQuestionTypeSerializer(serializers.ModelSerializer):
    """
    Serializer for generated questions types
    """

    question_template = QuestionTemplateSerializer(many=False, read_only=True)

    class Meta:
        model = GeneratedQuestionType
        fields = (
            "id",
            "description",
            "question_template",
            "maximum_grade",
            "generation_code",
        )

    def create(self, validated_data):
        return GeneratedQuestionType.objects.create(
            created_by=self.context["request"].user, **validated_data
        )

class GeneratedQuestionDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for generated question details
    """
    # question = QuestionSerializer(many=False)

    class Meta:
        model = GeneratedQuestionDetail
        fields = (
            "date_created",
            "question_type",
            "question_seed",
            "question"
        )

    # def validate_question_seed(self, value):
    #     print(value)
    #     return value

    def run_validation(self, data):
        try:
            seed = generate_seed()
            data['question_seed'] = seed
            qType = str(data['question_type']).split(" ")[0]
            data['question_type'] = GeneratedQuestionType.objects.get(pk=qType)
            generated_question = generate_question(seed, qType, self.context["request"].user)
            data['question'] = generated_question
        except Exception as inst:
        # perform you validation
            raise serializers.ValidationError(inst)
        return data

    
    def create(self, validated_data):
        try:
            genQuestion = GeneratedQuestionDetail.objects.create(
                created_by=self.context["request"].user, **validated_data
            )
        except Exception as e:
            print("create error")
            print(e)

        return genQuestion