import React from 'react'
import { useState, useEffect } from 'react'
import './UserLastAnswerApp.css'
import axios from 'axios'
import { useParams } from 'react-router-dom'

let firstRender = true
const UserLastAnswerApp = () => {
    let msg = 'Retrieving, please wait.  This can take up to 60 seconds.'
    const [items, setItems] = useState(new Array(msg))
    const token = localStorage.getItem('token')
    let { user } = useParams()

    useEffect(() => {
        firstRender = false
    }, [])

    const getAnswer = async () => {
        let answers = {}
        try {
            answers = await axios.get(
                `${process.env.REACT_APP_BASE_URL}/api/user-answers/${user}/`,
                {
                    headers: { Authorization: `Token ${token}` }
                }
            )
        } catch (err) {
            console.log('answers')
            console.log(err)
        }
        //console.log(answers)
        //console.log(user)
        let userAnswers = answers.data
        // let userAnswers = answers.data.filter((data) => {
        //     return data.user.username == user
        // })
        //console.log(userAnswers)
        let uniqueQuestionIdsSet = new Set()
        userAnswers.forEach((data) => {
            uniqueQuestionIdsSet.add(data.question.toString())
        })
        let uniqueQuestionIds = Array.from(uniqueQuestionIdsSet)
        uniqueQuestionIds.sort()
        //console.log(uniqueQuestionIds)
        let lastAnswers = []
        uniqueQuestionIds.forEach((id) => {
            //console.log(id)
            let questionArray = userAnswers.filter((data) => {
                return data.question == id
            })
            //console.log(questionArray)
            let mostRecentObject = questionArray.reduce((a, b) => {
                return a.created > b.created ? a : b
            })
            //console.log(mostRecentObject)
            lastAnswers.push(mostRecentObject)
        })
        //console.log(lastAnswers)
        let questionDetails = {}
        try {
            questionDetails = await axios.get(
                `${process.env.REACT_APP_BASE_URL}/api/allgeneratedquestiondetails/`,
                {
                    headers: { Authorization: `Token ${token}` }
                }
            )
        } catch (err) {
            onsole.log('details')
            console.log(err)
        }
        //console.log(questionDetails)
        let generatedQuestionList = []
        let generatedQuestionArray = questionDetails.data.filter((data) => {
            if (uniqueQuestionIds.includes(data.question.toString())) {
                generatedQuestionList.push(data.question.toString())
            }
            return uniqueQuestionIds.includes(data.question.toString())
        })
        //console.log(generatedQuestionArray)
        //console.log(generatedQuestionList)
        let questions = {}
        try {
            questions = await axios.get(`${process.env.REACT_APP_BASE_URL}/api/questions/`, {
                headers: { Authorization: `Token ${token}` }
            })
        } catch (err) {
            console.log('questions')
            console.log(err)
        }
        //console.log(questions.data)
        let generatedQuestionType = {}
        try {
            generatedQuestionType = await axios.get(
                `${process.env.REACT_APP_BASE_URL}/api/generatedquestiontype/`,
                {
                    headers: { Authorization: `Token ${token}` }
                }
            )
        } catch (err) {
            console.log('types')
            console.log(err)
        }
        //console.log(generatedQuestionType)
        lastAnswers.forEach((ans) => {
            ans['title'] = ''
            if (generatedQuestionList.includes(ans.question.toString())) {
                const detail = generatedQuestionArray.find((q) => {
                    return q.question.toString() == ans.question
                })
                //console.log(detail)
                if (detail !== 'undefined') {
                    const type = generatedQuestionType.data.find((t) => {
                        return t.id.toString() == detail.question_type.toString()
                    })
                    //console.log(type)
                    if (type !== 'undefined') {
                        ans['title'] = type.description
                    }
                }
            } else {
                const found = questions.data.find((q) => {
                    return q.id.toString() == ans.question
                })
                if (found !== 'undefined') {
                    ans['title'] = found.title
                }
            }
        })
        //console.log(lastAnswers)
        setItems(lastAnswers)
        return ''
    }

    if (firstRender) {
        const loadData = async () => {
            await getAnswer(token)
        }
        loadData()
    }

    return (
        <div>
            Last answers for user: {user}
            <ul>
                {items.length > 0 ? (
                    items[0] != msg ? (
                        items.map(function (value, key) {
                            return (
                                <li key={key}>
                                    Question {value.question} {value.title}; Mark: {value.mark}/
                                    {value.total}; Details:&nbsp;
                                    <a
                                        target="_blank"
                                        rel="noreferrer"
                                        href={value.url.replace('/api', '')}>
                                        {value.url.replace('/api', '')}
                                    </a>
                                </li>
                            )
                        })
                    ) : (
                        <li> {msg} </li>
                    )
                ) : (
                    <li>No Results</li>
                )}
            </ul>
        </div>
    )
}

export default UserLastAnswerApp
