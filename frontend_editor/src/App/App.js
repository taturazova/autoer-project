import React from 'react';
import { useState } from 'react'
import './App.css';
import Container from '@material-ui/core/Container';
import Typography from '@material-ui/core/Typography';
import { Button, Paper, TextField } from '@material-ui/core';
import axios from 'axios';


function App() {

  const [text, setText] = useState("Login Status")
  const [token, setToken] = useState("")
  const [question, setQuestion] = useState("")
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [potentialAnswers, setPotentialAnswers] = useState({})

  const login = async () => {
    try{

      const response = await axios.post(`http://localhost:8000/api-token-auth/`, { username: username, password: 'password'})
      setToken(response.data.token);
      setText("Authenticated!")
    }catch(err){
      setText("Try again")
    }

  }

  const getData = async () => {
    try{

      const response = await axios.get(`http://localhost:8000/questions/question/1/`, {
        headers: {
          'authorization': `Token ${token}`
        }
      })
      const data = response.data;
      setQuestion(data.question);
      setPotentialAnswers(data)
    }catch(err){
      setQuestion("Please login first")
    }
  }

  const handleChangeUsername = (event)=>{
    setUsername(event.target.value)
  }

  const handleChangePassword = (event)=>{
    setPassword(event.target.value)
  }

  return (
    <Container maxWidth="sm" className="App">
      <Paper>
        <Typography variant="h4" component="h1" gutterBottom>
          Demo
        </Typography>
        <h4>
          {text}
        </h4><br/>
        <TextField label="Username" value={username} onChange={handleChangeUsername}/><br/>
        <TextField label="Password" type="password" value={password} onChange={handleChangePassword}/><br/><br/>
        <Button onClick={login} variant="contained" color="primary">
          Login
        </Button>
        <Button onClick={getData} variant="contained" color="secondary">
          Get Question
        </Button>
    <h2>
      {question}
    </h2>
    <ul>
      {potentialAnswers.potential_answers? potentialAnswers.potential_answers.map((potential_answer, index) => {
        let correctOne = potential_answer.is_correct ? "CORRECT":"WRONG"
          
        return <li key={index}>{potential_answer.answer} -> {correctOne} </li>
      }):''}
    </ul>
  
      </Paper>
    </Container>
  );
}
export default App;