import os
# QUESTION TYPE
populateQuestionsScript=""
populateQuestionsScript+='INSERT INTO \"questions_questiontype\" (\"created\",\"question_type\",\"created_by_id\")\n'
populateQuestionsScript+='VALUES (NOW(),\'autoER\',1);\n'

htmlString=""
with open('./src/inlined.html', 'r') as f:
    htmlString = f.read()

markingString=""
with open('./python/er_marker_db.txt', 'r') as f:
    markingString= f.read()

print(populateQuestionsScript)

# QUESTION TEMPLATE
populateQuestionsScript+="INSERT INTO \"questions_questiontemplate\" (\"body\",\"marking_code\",\"created\",\"created_by_id\",\"question_type_id\")\n"
populateQuestionsScript+=("VALUES (%s, %s, NOW(), 1, 1);\n",htmlString,markingString)



f = open("./python/sqlscripts/populate_questions.sql", "w")
f.write(populateQuestionsScript)
f.close()




