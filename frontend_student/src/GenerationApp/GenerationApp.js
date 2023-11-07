import React from 'react'
import { useState, useEffect } from 'react'
import './GenerationApp.css'
import axios from 'axios'
import { useParams } from 'react-router-dom'

let firstRender = true
const GenerationApp = () => {
    const [questionTemplate, setQuestionTemplate] = useState('')
    const token = localStorage.getItem('token')
    let { questionTypeId } = useParams()

    useEffect(() => {
        firstRender = false
    }, [])

    const generateQuestion = async () => {
        try {
            const response = await axios({
                method: 'post',
                url: `${process.env.REACT_APP_BASE_URL}/api/generatedquestiondetails/`,
                data: {
                    question_type: questionTypeId,
                    question_seed: '',
                    question: 2
                },
                headers: { Authorization: `Token ${token}` }
            })
        } catch (err) {
            console.log(err)
        }
        return ''
    }

    const getGeneratedQuestion = async () => {
        try {
            const questionDetails = await axios.get(
                `${process.env.REACT_APP_BASE_URL}/api/generatedquestiondetails/`,
                {
                    headers: { Authorization: `Token ${token}` }
                }
            )
            for (let i = 0; i < questionDetails.data.length; i++) {
                if (questionDetails.data[i].question_type == questionTypeId) {
                    return questionDetails.data[i].question
                }
            }
            await generateQuestion()
            // return await getGeneratedQuestion()
            const questionDetails1 = await axios.get(
                `${process.env.REACT_APP_BASE_URL}/api/generatedquestiondetails/`,
                {
                    headers: { Authorization: `Token ${token}` }
                }
            )
            for (let i = 0; i < questionDetails1.data.length; i++) {
                if (questionDetails1.data[i].question_type == questionTypeId) {
                    return questionDetails1.data[i].question
                }
            }
            return -1
        } catch (err) {
            console.log(err)
        }
    }

    const getAnswer = async (questionId) => {
        try {
            const last_answer = await axios.get(
                `${process.env.REACT_APP_BASE_URL}/api/last-answer/`,
                {
                    headers: { Authorization: `Token ${token}` }
                }
            )
            let questionArray = last_answer.data.filter((data) => {
                return data.question == questionId
            })
            let mostRecentObject = questionArray.reduce((a, b) => (a.created > b.created ? a : b))
            return mostRecentObject
        } catch (err) {
            console.log(err)
        }
        return ''
    }

    const getQuestion = async () => {
        window.questionToken = token
        try {
            const questionId = await getGeneratedQuestion()
            const response = await axios.get(
                `${process.env.REACT_APP_BASE_URL}/api/questions/${questionId}/`,
                {
                    headers: { Authorization: `Token ${token}` }
                }
            )
            setQuestionTemplate(response.data.question_template.body)
            let o_ans = await getAnswer(questionId)
            let questionData = {
                qid: questionId,
                name: response.data.title,
                maximum_attempts: response.data.maximum_attempts,
                penalty_type: response.data.penalty_type,
                markdown: response.data.question,
                old_answer: o_ans
            }

            setTimeout(() => {
                document
                    .getElementById('question-template-iframe')
                    .contentWindow.acceptData(questionData)
            }, 1000)
        } catch (err) {
            console.log(err)
        }
    }

    const submitAnswer = async (answerData) => {
        let markStatus = {
            mark: 'N/A',
            total: 'N/A',
            feedback: 'N/A',
            ip_address: 'Server Error',
            id: ''
        }
        try {
            const response = await axios({
                method: 'post',
                url: `${process.env.REACT_APP_BASE_URL}/api/marks/`,
                data: answerData,
                headers: { Authorization: `Token ${token}` }
            })
            markStatus = response.data
        } catch (err) {
            console.log(err)
        }
        return markStatus
    }
    window.submitAnswer = submitAnswer

    if (firstRender) {
        const loadData = async () => {
            await getQuestion()
        }
        loadData()
    }

    return (
        <iframe
            className="App"
            frameBorder="0"
            style={{
                overflow: 'hidden',
                overflowX: 'hidden',
                overflowY: 'hidden',
                width: '100%',
                top: '0px',
                left: '0px',
                right: '0px',
                height: '92vh'
            }}
            id="question-template-iframe"
            title="question-template-iframe-title"
            srcDoc={questionTemplate}
        />
    )
}
export default GenerationApp
