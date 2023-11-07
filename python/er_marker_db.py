import copy
import re
import json

# DEFAULT QUESTION WEIGHTS
maximum_grade = 10
marking_criteria = {
    "correct_entity_name": 0.2,
    "correct_attributes": 0.1,
    "correct_primary_keys": 0.2,
    "extra_entity": 0.25,
    "correct_weak_entity": 0.5,
    "correct_relationship_entity": 0.5,
    "correct_cardinality": 0.25,
    "extra_relationship": 0.25
}
# TODO: decide if the relationship is attached to a weak entity, should the relationship should be worth half?


def convert(text):
    er_dict = {
        "entities": [],
        "relationships": []
    }

    def parse_relationship(r_line):
        entities = re.findall('\[(.*?)\]', r_line)
        rel = re.search('\](.*?)\[', r_line)
        cardinalities = [x.strip() for x in rel.group(1).split('-')]
        entities_sorted = entities.copy()
        entities_sorted.sort()
        if (entities_sorted[0]!=entities_sorted[1]):
            relationship = {
                "entities": entities_sorted,
                entities[0]: cardinalities[0],
                entities[1]: cardinalities[1]
            }
        else:
             relationship = {
                "entities": entities_sorted,
                entities[0]: [cardinalities[0],cardinalities[1]]
            }
        er_dict["relationships"].append(relationship)

    def parse_entity(e_line):
        attributes = []
        primary_key = []
        partial_primary_keys = []
        e_line = re.search('\[(.*?)\]', e_line)
        split_line = e_line.group(1).split('|')
        entity_name = split_line[0]
        if len(split_line) > 1:
            attributes = [x.strip() for x in split_line[1].split(';')]
            for i, att in enumerate(attributes):
                if '{PK}' in att:
                    attributes[i] = att.strip(' {PK}')
                    primary_key.append(attributes[i])
                if '{PPK}' in att:
                    attributes[i] = att.strip(' {PPK}')
                    partial_primary_keys.append(attributes[i])
        # sorting of the lists here to avoid doing it during marking but could move
            attributes.sort()
            primary_key.sort()
            partial_primary_keys.sort()
        entity = {
            "entity_name": entity_name,
            "primary_key": primary_key,
            "partial_primary_key": partial_primary_keys,
            "attributes": attributes
        }
        er_dict["entities"].append(entity)

    def parse_line(t_line):
        index = t_line.find('-')
        if index == -1:
            parse_entity(t_line)
        else:
            parse_relationship(t_line)

    for line in text.splitlines():
        if line != "":
            parse_line(line)

    def sort_on_entities(e):
        return e["entities"][0]

    er_dict["relationships"].sort(key=sort_on_entities)
    return er_dict


def mark_answer(question, answers, stu_answer):
    student_answer = convert(stu_answer)
    global maximum_grade, marking_criteria
    maximum_grade = question["maximum_grade"]
    try:
        question["other_marking_criteria"] = question["other_marking_criteria"].strip()
        if question["other_marking_criteria"][0] != '{' and question["other_marking_criteria"][-1] != '}':
            question["other_marking_criteria"] = '{ ' + \
                question["other_marking_criteria"] + ' }'
        other_marking_criteria = json.loads(question["other_marking_criteria"])
        for key in other_marking_criteria:
            if key in marking_criteria:
                marking_criteria[key] = other_marking_criteria[key]
    except Exception as inst:
        print(inst)
    top_mark = -1
    top_result = dict()
    for nomnoml_answer in answers:
        answer = convert(nomnoml_answer["answer"])
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
    correct_answer_copy = copy.deepcopy(correct_answer)

    marker_feedback = ""

    # calculate the total marks for the question
    for answer_entity in correct_answer['entities']:
        entity_name_marks += marking_criteria["correct_entity_name"]
        entity_attribute_marks += marking_criteria["correct_attributes"]
        entity_primary_key_marks += marking_criteria["correct_primary_keys"]
        if not answer_entity['primary_key']:
            weak_entity_key_marks += marking_criteria["correct_weak_entity"]
    for relationship in correct_answer['relationships']:
        relationship_entity_marks += marking_criteria["correct_relationship_entity"]
        relationship_cardinality_marks += (
            marking_criteria["correct_cardinality"] * 2)
    entity_marks = entity_name_marks + entity_attribute_marks + \
        entity_primary_key_marks + weak_entity_key_marks
    relationship_marks = relationship_entity_marks + relationship_cardinality_marks
    total_marks = entity_marks + relationship_marks

    # marking entities
    for answer_entity in correct_answer['entities']:
        for i, stu_entity in enumerate(student_answer_copy['entities']):
            if stu_entity['entity_name'] == answer_entity['entity_name']:
                correct_answer_copy['entities'].remove(answer_entity)
                student_entity_names_mark += marking_criteria["correct_entity_name"]
                if stu_entity['attributes'] == answer_entity['attributes']:
                    student_attributes_mark += marking_criteria["correct_attributes"]
                else:
                    marker_feedback += "Incorrect attributes on the " + stu_entity['entity_name'] + " entity\n"
                    marker_feedback += "Student: " + ', '.join(stu_entity['attributes']) + "\n"
                    marker_feedback += "Correct: " + ', '.join(answer_entity['attributes']) + "\n\n"
                if stu_entity['primary_key'] == answer_entity['primary_key']:
                    student_primary_keys_mark += marking_criteria["correct_primary_keys"]
                else:
                    marker_feedback += "Incorrect primary key on the " + stu_entity['entity_name'] + " entity\n"
                    marker_feedback += "Student: " + ', '.join(stu_entity['primary_key']) + "\n"
                    marker_feedback += "Correct: " + ', '.join(answer_entity['primary_key']) + "\n\n"
                if not answer_entity['primary_key']:
                    if (not stu_entity['primary_key'] and
                            stu_entity['partial_primary_key'] == answer_entity['partial_primary_key']):
                        student_weak_entities_mark += marking_criteria["correct_weak_entity"]
                    else:
                        marker_feedback += "Incorrect partial primary key on the " + stu_entity['entity_name'] + " entity\n"
                        marker_feedback += "Student: " + ', '.join(stu_entity['partial_primary_key']) + "\n"
                        marker_feedback += "Correct: " + ', '.join(answer_entity['partial_primary_key']) + "\n\n"
                # Probably not a good idea
                del student_answer_copy['entities'][i]


    # Dock marks for extra entities
    student_extra_entities_mark = 0 - \
        (marking_criteria["extra_entity"] *
         len(student_answer_copy['entities']))

    if len(student_answer_copy['entities']) > 0:
        s = ", ".join([str(item['entity_name']) for item in student_answer_copy['entities']])
        marker_feedback += "Extra entities: " + s + "\n\n"
    if len(correct_answer_copy['entities']) > 0:
        s = ", ".join([str(item['entity_name']) for item in correct_answer_copy['entities']])
        marker_feedback += "Missed entities: " + s + "\n\n"

    student_entities_mark = (student_entity_names_mark
                             + student_attributes_mark
                             + student_primary_keys_mark
                             + student_weak_entities_mark
                             + student_extra_entities_mark)

    
    # marking relationships
    # if the entire relationship is correct
    correct_answer_ = copy.deepcopy(correct_answer_copy)
    for answer_rel in correct_answer_['relationships']:
        for i, stu_rel in enumerate(student_answer_copy['relationships']):
            if stu_rel['entities'] == answer_rel['entities']:
                if answer_rel['entities'][0] == answer_rel['entities'][1]:
                    ans_cardinality_a = answer_rel[stu_rel['entities'][0]][0]
                    stu_cardinality_a = check_sp_char(
                    stu_rel[stu_rel['entities'][0]][0], ans_cardinality_a)
                    ans_cardinality_b = answer_rel[stu_rel['entities'][0]][1]
                    stu_cardinality_b = check_sp_char(
                        stu_rel[stu_rel['entities'][0]][1], ans_cardinality_b)
                else:
                    ans_cardinality_a = answer_rel[stu_rel['entities'][0]]
                    stu_cardinality_a = check_sp_char(
                        stu_rel[stu_rel['entities'][0]], ans_cardinality_a)
                    ans_cardinality_b = answer_rel[stu_rel['entities'][1]]
                    stu_cardinality_b = check_sp_char(
                        stu_rel[stu_rel['entities'][1]], ans_cardinality_b)
                if ((stu_cardinality_a == ans_cardinality_a and # exact match
                    stu_cardinality_b == ans_cardinality_b) or
                    (answer_rel['entities'][0] == answer_rel['entities'][1] and # self relationship
                    (stu_cardinality_a == ans_cardinality_b and 
                    stu_cardinality_b == ans_cardinality_a))):
                    correct_answer_copy['relationships'].remove(answer_rel)
                    student_relationship_entities_mark += marking_criteria["correct_relationship_entity"]
                    student_relationship_cardinalities_mark += (marking_criteria["correct_cardinality"]*2)
                    # Probably not a good idea
                    del student_answer_copy['relationships'][i]
    
    # if one cardinality of the relationship is correct
    correct_answer_ = copy.deepcopy(correct_answer_copy)
    for answer_rel in correct_answer_['relationships']:
        for i, stu_rel in enumerate(student_answer_copy['relationships']):
            if stu_rel['entities'] == answer_rel['entities']:
                if answer_rel['entities'][0] == answer_rel['entities'][1]:
                    ans_cardinality_a = answer_rel[stu_rel['entities'][0]][0]
                    stu_cardinality_a = check_sp_char(
                    stu_rel[stu_rel['entities'][0]][0], ans_cardinality_a)
                    ans_cardinality_b = answer_rel[stu_rel['entities'][0]][1]
                    stu_cardinality_b = check_sp_char(
                        stu_rel[stu_rel['entities'][0]][1], ans_cardinality_b)
                else:
                    ans_cardinality_a = answer_rel[stu_rel['entities'][0]]
                    stu_cardinality_a = check_sp_char(
                        stu_rel[stu_rel['entities'][0]], ans_cardinality_a)
                    ans_cardinality_b = answer_rel[stu_rel['entities'][1]]
                    stu_cardinality_b = check_sp_char(
                        stu_rel[stu_rel['entities'][1]], ans_cardinality_b)
                if ((stu_cardinality_a == ans_cardinality_a or # one cardinality
                    stu_cardinality_b == ans_cardinality_b) or
                    (answer_rel['entities'][0] == answer_rel['entities'][1] and # self relationship one cardinality
                    (stu_cardinality_a == ans_cardinality_b or 
                    stu_cardinality_b == ans_cardinality_a))):
                    correct_answer_copy['relationships'].remove(answer_rel)
                    student_relationship_entities_mark += marking_criteria["correct_relationship_entity"]
                    student_relationship_cardinalities_mark += marking_criteria["correct_cardinality"]
                    marker_feedback += "Incorrect cardinality on the " + str(stu_rel['entities']) + " relationship\n"
                    marker_feedback += ("Student: [" 
                    + str(stu_rel['entities'][0]) + "] " 
                    + stu_cardinality_a + " - " 
                    + stu_cardinality_b + " [" 
                    + str(stu_rel['entities'][1]) + "]\n")
                    marker_feedback += ("Correct: ["
                    + str(answer_rel['entities'][0]) + "] " 
                    + ans_cardinality_a + " - " 
                    + ans_cardinality_b + " [" 
                    + str(answer_rel['entities'][1]) +"]\n\n")
                    # Probably not a good idea
                    del student_answer_copy['relationships'][i]


    # if just the entities of the relationship is correct
    correct_answer_ = copy.deepcopy(correct_answer_copy)
    for answer_rel in correct_answer_['relationships']:
        for i, stu_rel in enumerate(student_answer_copy['relationships']):
           if stu_rel['entities'] == answer_rel['entities']:
                if answer_rel['entities'][0] == answer_rel['entities'][1]:
                    ans_cardinality_a = answer_rel[stu_rel['entities'][0]][0]
                    stu_cardinality_a = check_sp_char(
                    stu_rel[stu_rel['entities'][0]][0], ans_cardinality_a)
                    ans_cardinality_b = answer_rel[stu_rel['entities'][0]][1]
                    stu_cardinality_b = check_sp_char(
                        stu_rel[stu_rel['entities'][0]][1], ans_cardinality_b)
                else:
                    ans_cardinality_a = answer_rel[stu_rel['entities'][0]]
                    stu_cardinality_a = check_sp_char(
                        stu_rel[stu_rel['entities'][0]], ans_cardinality_a)
                    ans_cardinality_b = answer_rel[stu_rel['entities'][1]]
                    stu_cardinality_b = check_sp_char(
                        stu_rel[stu_rel['entities'][1]], ans_cardinality_b)
                correct_answer_copy['relationships'].remove(answer_rel)
                student_relationship_entities_mark += marking_criteria["correct_relationship_entity"]
                marker_feedback += "Incorrect cardinalities on the " + str(stu_rel['entities']) + " relationship\n"
                marker_feedback += ("Student: [" 
                + str(stu_rel['entities'][0]) + "] " 
                + stu_cardinality_a + " - " 
                + stu_cardinality_b + " [" 
                + str(stu_rel['entities'][1]) 
                + "]\n")
                marker_feedback += ("Correct: ["
                + str(answer_rel['entities'][0]) + "] " 
                + ans_cardinality_a + " - " 
                + ans_cardinality_b + " [" 
                + str(answer_rel['entities'][1]) +"]\n\n")
                # Probably not a good idea
                del student_answer_copy['relationships'][i]

    # Dock marks for extra relationships
    student_extra_relationships_mark = 0 - \
        (marking_criteria["extra_relationship"] *
         len(student_answer_copy['relationships']))

    if len(student_answer_copy['relationships']) > 0:
        s = ", ".join([str(item['entities']) for item in student_answer_copy['relationships']])
        marker_feedback += "Extra relationships: " + s + "\n\n"
    if len(correct_answer_copy['relationships']) > 0:
        s = ", ".join([str(item['entities']) for item in correct_answer_copy['relationships']])
        marker_feedback += "Missed relationships: " + s + "\n\n"

    student_relationships_mark = (student_relationship_entities_mark
                                  + student_relationship_cardinalities_mark
                                  + student_extra_relationships_mark)

    student_total_marks = student_entities_mark + student_relationships_mark

    if student_total_marks < 0:
        student_total_marks = 0

    # scale marks with question maximum grade
    scaled_student_total_marks = (
        student_total_marks / total_marks) * maximum_grade

    feedback = ("Entity name marks: "
                + str(round(student_entity_names_mark, 2)) +
                "/" + str(round(entity_name_marks, 2)) + "\n"
                + "Entity attribute marks: "
                + str(round(student_attributes_mark, 2)) + "/" +
                str(round(entity_attribute_marks, 2)) + "\n"
                + "Entity primary key marks: "
                + str(round(student_primary_keys_mark, 2)) + "/" +
                str(round(entity_primary_key_marks, 2)) + "\n"
                + "Weak entity key marks: "
                + str(round(student_weak_entities_mark, 2)) + "/" +
                str(round(weak_entity_key_marks, 2)) + "\n"
                + "Extra entities: "
                + str(round(student_extra_entities_mark, 2)) + "\n"
                + "Total entity marks: "
                + str(round(student_entities_mark, 2)) +
                "/" + str(round(entity_marks, 2)) + "\n"
                + "Relationship entity marks: "
                + str(round(student_relationship_entities_mark, 2)) + "/"
                + str(round(relationship_entity_marks, 2)) + "\n"
                + "Relationship cardinalities marks: "
                + str(round(student_relationship_cardinalities_mark, 2)) + "/"
                + str(round(relationship_cardinality_marks, 2)) + "\n"
                + "Extra relationships: "
                + str(student_extra_relationships_mark) + "\n"
                + "Total relationship marks: "
                + str(round(student_relationships_mark, 2)) +
                "/" + str(round(relationship_marks, 2)) + "\n"
                + "Total marks: " +
                str(round(student_total_marks, 2)) +
                "/" + str(round(total_marks, 2)) + "\n"
                + "Total scaled marks: "
                + str(round(scaled_student_total_marks, 2)) + "/" + str(round(maximum_grade, 2)) + "\n")

    result = {
        "mark": round(scaled_student_total_marks, 2),
        "total": maximum_grade,
        "feedback": feedback,
        "marker_feedback": marker_feedback
    }
    return result


___results___ = mark_answer(
    ___question___, ___potential_answers___, ___student_answer___)