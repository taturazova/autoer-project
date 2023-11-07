import React from 'react'

const QuestionTemplate = () => {
    return (
        <ul>
            {potentialAnswers.potential_answers
                ? potentialAnswers.potential_answers.map((potential_answer, index) => {
                      let correctOne = potential_answer.is_correct ? 'CORRECT' : 'WRONG'

                      return (
                          <li key={index}>
                              {potential_answer.answer} {correctOne}{' '}
                          </li>
                      )
                  })
                : ''}
        </ul>
    )
}
