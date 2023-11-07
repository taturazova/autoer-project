import copy

# DEFAULT QUESTION WEIGHTS
maximum_grade = 10
correct_entity_name = 0.2
marking_entity_correct_attributes = 0.1
marking_entity_correct_primary_keys = 0.2
marking_entity_extra_entity = 0.25
marking_entity_correct_weak_entity = 0.5
marking_entity_correct_relationship_entity = 0.5
marking_entity_correct_cardinality = 0.25
marking_entity_extra_relationship = 0.25
# TODO: decide if the relationship is attached to a weak entity, should the relationship should be worth half?


def mark_answer(question, student_answer):
    print(question["title"])
    global maximum_grade, correct_entity_name, marking_entity_correct_attributes, marking_entity_correct_primary_keys, marking_entity_extra_entity, marking_entity_correct_weak_entity
    global marking_entity_correct_relationship_entity, marking_entity_correct_cardinality, marking_entity_extra_relationship
    # should these be if statements?
    maximum_grade = question["maximum_grade"]
    correct_entity_name = question["other_marking_criteria"]["correct_entity_name"]
    correct_attributes = question["other_marking_criteria"]["correct_attributes"]
    correct_primary_keys = question["other_marking_criteria"]["correct_primary_keys"]
    extra_entity = question["other_marking_criteria"]["extra_entity"]
    correct_weak_entity = question["other_marking_criteria"]["correct_weak_entity"]
    correct_relationship_entity = question["other_marking_criteria"]["correct_relationship_entity"]
    correct_cardinality = question["other_marking_criteria"]["correct_cardinality"]
    extra_relationship = question["other_marking_criteria"]["extra_relationship"]
    top_mark = -1
    top_result = dict()
    for answer in question["answers"]:
        result = mark(answer, student_answer)
        if top_mark < result["mark"]:
            top_mark = result["mark"]
            top_result = result
    return top_result


def check_sp_char(stu_card, ans_card):
    if ans_card == "*" and (stu_card == "0..*" or stu_card == "1..*"):
        stu_card = "*"
    elif ans_card == "0@1" and (stu_card == "0..1" or stu_card == "1..1"):
        stu_card = "0@1"
    return stu_card


def mark(correct_answer, student_answer):
    # print(student_answer)
    # print(correct_answer)
    # TOTAL MARKS VARIABLES
    entity_name_marks = 0
    entity_attribute_marks = 0
    entity_primary_key_marks = 0
    weak_entity_key_marks = 0
    relationship_entity_marks = 0
    relationship_cardinality_marks = 0

    # STUDENT ANSWER VARIABLES
    student_entity_names_mark = 0
    student_attributes_mark = 0
    student_primary_keys_mark = 0
    student_weak_entities_mark = 0
    student_relationship_entities_mark = 0
    student_relationship_cardinalities_mark = 0

    student_answer_copy = copy.deepcopy(student_answer)

    # calculate the total marks for the question
    for answer_entity in correct_answer['entities']:
        entity_name_marks += correct_entity_name
        entity_attribute_marks += marking_entity_correct_attributes
        entity_primary_key_marks += marking_entity_correct_primary_keys
        if not answer_entity['primary_key']:
            weak_entity_key_marks += marking_entity_correct_weak_entity
    for relationship in correct_answer['relationships']:
        relationship_entity_marks += marking_entity_correct_relationship_entity
        relationship_cardinality_marks += (marking_entity_correct_cardinality * 2)
    entity_marks = entity_name_marks + entity_attribute_marks + entity_primary_key_marks + weak_entity_key_marks
    relationship_marks = relationship_entity_marks + relationship_cardinality_marks
    total_marks = entity_marks + relationship_marks


    # marking entities
    for answer_entity in correct_answer['entities']:
        for i, stu_entity in enumerate(student_answer_copy['entities']):
            if stu_entity['entity_name'] == answer_entity['entity_name']:
                student_entity_names_mark += correct_entity_name
                if stu_entity['attributes'] == answer_entity['attributes']:
                    student_attributes_mark += marking_entity_correct_attributes
                if stu_entity['primary_key'] == answer_entity['primary_key']:
                    student_primary_keys_mark += marking_entity_correct_primary_keys
                if not answer_entity['primary_key']:
                    if (not stu_entity['primary_key'] and
                            stu_entity['partial_primary_key'] == answer_entity['partial_primary_key']):
                        student_weak_entities_mark += marking_entity_correct_weak_entity
                # Probably not a good idea
                del student_answer_copy['entities'][i]

    # Dock marks for extra entities
    student_extra_entities_mark = 0 - (marking_entity_extra_entity * len(student_answer_copy['entities']))
    # print(student_answer_copy['entities'])

    student_entities_mark = (student_entity_names_mark
                             + student_attributes_mark
                             + student_primary_keys_mark
                             + student_weak_entities_mark
                             + student_extra_entities_mark)

    # marking relationships
    for answer_rel in correct_answer['relationships']:
        for i, stu_rel in enumerate(student_answer_copy['relationships']):
            if stu_rel['entities'] == answer_rel['entities']:
                student_relationship_entities_mark += marking_entity_correct_relationship_entity
                ans_cardinality_a = answer_rel[stu_rel['entities'][0]]
                stu_cardinality_a = check_sp_char(stu_rel[stu_rel['entities'][0]], ans_cardinality_a)
                if stu_cardinality_a == ans_cardinality_a:
                    student_relationship_cardinalities_mark += marking_entity_correct_cardinality
                else:
                    print(stu_rel['entities'], stu_cardinality_a, ans_cardinality_a)
                ans_cardinality_b = answer_rel[stu_rel['entities'][1]]
                stu_cardinality_b = check_sp_char(stu_rel[stu_rel['entities'][1]], ans_cardinality_b)
                if stu_cardinality_b == ans_cardinality_b:
                    student_relationship_cardinalities_mark += marking_entity_correct_cardinality
                else:
                    print(stu_rel['entities'], stu_cardinality_b, ans_cardinality_b)
                # Probably not a good idea
                del student_answer_copy['relationships'][i]

    # Dock marks for extra relationships
    student_extra_relationships_mark = 0 - (marking_entity_extra_relationship * len(student_answer_copy['relationships']))
    # print(student_answer_copy['relationships'])

    student_relationships_mark = (student_relationship_entities_mark
                                  + student_relationship_cardinalities_mark
                                  + student_extra_relationships_mark)

    student_total_marks = student_entities_mark + student_relationships_mark

    if student_total_marks < 0:
        student_total_marks = 0

    # scale marks with question point value
    scaled_student_total_marks = (student_total_marks / total_marks) * maximum_grade

    feedback = ("Entity name marks: "
                + str(round(student_entity_names_mark, 2)) + "/" + str(round(entity_name_marks, 2)) + "\n"
                + "Entity attribute marks: "
                + str(round(student_attributes_mark, 2)) + "/" + str(round(entity_attribute_marks, 2)) + "\n"
                + "Entity primary key marks: "
                + str(round(student_primary_keys_mark, 2)) + "/" + str(round(entity_primary_key_marks, 2)) + "\n"
                + "Weak entity key marks: "
                + str(round(student_weak_entities_mark, 2)) + "/" + str(round(weak_entity_key_marks, 2)) + "\n"
                + "Extra entities: "
                + str(round(student_extra_entities_mark, 2)) + "\n"
                + "Total entity marks: "
                + str(round(student_entities_mark, 2)) + "/" + str(round(entity_marks, 2)) + "\n"
                + "Relationship entity marks: "
                + str(round(student_relationship_entities_mark, 2)) + "/"
                + str(round(relationship_entity_marks, 2)) + "\n"
                + "Relationship cardinalities marks: "
                + str(round(student_relationship_cardinalities_mark, 2)) + "/"
                + str(round(relationship_cardinality_marks, 2)) + "\n"
                + "Extra relationships: "
                + str(student_extra_relationships_mark) + "\n"
                + "Total relationship marks: "
                + str(round(student_relationships_mark, 2)) + "/" + str(round(relationship_marks, 2)) + "\n"
                + "Total marks: " + str(round(student_total_marks, 2)) + "/" + str(round(total_marks, 2)) + "\n"
                + "Total scaled marks: "
                + str(round(scaled_student_total_marks, 2)) + "/" + str(round(maximum_grade, 2)) + "\n")
    print(feedback)

    result = {
        "mark": round(scaled_student_total_marks, 2),
        "total": maximum_grade,
        "feedback": ""
    }
    return result

