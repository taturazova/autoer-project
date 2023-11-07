from django.forms.models import construct_instance, model_to_dict
import sys
import random
from auto_marking_api.questions.models import (
    Question,
    QuestionTemplate,
    PotentialAnswer,
    GeneratedQuestionType,
)

def add_question(qtype, data, seed, user):
    try:
        template_id = str(qtype.question_template).split(" ")[0]
        template = QuestionTemplate.objects.get(pk=template_id)
        q = Question(title = str(seed), maximum_grade = qtype.maximum_grade, question = data['question'], question_template = template, created_by = user, maximum_attempts = data['maximum_attempts'], penalty_type = data['penalty_type'] )
        q.save()
        a = PotentialAnswer(question = q, answer = data['answer'], is_correct = True)
        a.save()
        return q
    except Exception as e:
        print(e)

def get_question_generation_type(id):
    try:
        type = GeneratedQuestionType.objects.get(pk=id)
        return type
    except Exception as e:
        print(e)

def generate_seed():
    return random.randrange(sys.maxsize)

def generate_question(seed_value, question_type, user):
    generated_question_type = get_question_generation_type(question_type)
    result = compile(generated_question_type.generation_code, 'generate', 'exec')
    args = {
        "___seed_value___": seed_value,
        "___results___": ""
    }
    exec(result, args)
    question_data = args["___results___"]
    question = add_question(generated_question_type, question_data, seed_value, user )
    return question


