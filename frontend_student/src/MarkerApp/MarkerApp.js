import React from 'react'
import { useState, useEffect } from 'react'
import './MarkerApp.css'
import axios from 'axios'
import { useParams } from 'react-router-dom'

let firstRender = true
const MarkerApp = () => {
    const [markerPage, setMarkerPage] = useState('')
    const token = localStorage.getItem('token')
    let { answerId } = useParams()

    useEffect(() => {
        firstRender = false
    }, [])

    const getQuestion = async () => {
        window.questionToken = token
        try {
            const response = await axios.get(
                `${process.env.REACT_APP_BASE_URL}/api/marks/${answerId}/`,
                {
                    headers: { Authorization: `Token ${token}` }
                }
            )
            let qid = response.data.question.toString()

            const qResponse = await axios.get(
                `${process.env.REACT_APP_BASE_URL}/api/questions/${qid}/`,
                {
                    headers: { Authorization: `Token ${token}` }
                }
            )

            setMarkerPage(qResponse.data.question_template.marker_page)

            let answerData = {
                answer_id: answerId,
                qid: qid,
                question_name: qResponse.data.title,
                answer: response.data.answer,
                date: response.data.created,
                ip_address: response.data.ip_address,
                mark: response.data.mark,
                total: response.data.total,
                feedback: response.data.feedback,
                marker_feedback: response.data.marker_feedback
            }
            setTimeout(() => {
                document.getElementById('marker-page-iframe').contentWindow.acceptData(answerData)
            }, 1000)
        } catch (err) {
            console.log(err)
        }
    }

    if (firstRender) {
        const loadData = async () => {
            await getQuestion(token)
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
                height: '95vh'
            }}
            id="marker-page-iframe"
            title="marker-page-iframe-title"
            srcDoc={markerPage}
        />
    )
}
export default MarkerApp
