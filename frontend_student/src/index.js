import React from 'react'
import ReactDOM from 'react-dom'
import 'bootstrap/dist/css/bootstrap.css'
import './index.css'
import { ThemeProvider } from '@material-ui/core/styles'
import App from './App/App'
import MarkerApp from './MarkerApp/MarkerApp'
import GenerationApp from './GenerationApp/GenerationApp'
import UserLastAnswerApp from './UserLastAnswerApp/UserLastAnswerApp'
import Home from './Home/Home'
import Login from './components/login/Login'
import theme from './theme'
import Root from './Root'
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom'
import requireAuth from './utils/RequireAuth'
import requireAuthAdmin from './utils/RequireAuthAdmin'
import 'react-toastify/dist/ReactToastify.css'
import { ToastContainer } from 'react-toastify'

ReactDOM.render(
    <ThemeProvider theme={theme}>
        {/* CssBaseline kickstart an elegant, consistent, and simple baseline to build upon. */}
        <Root>
            <ToastContainer hideProgressBar={true} newestOnTop={true} />
            <Switch>
                <Route path="/questions/:questionId" component={requireAuth(App)} />
                <Route
                    path="/generatedQuestion/:questionTypeId"
                    component={requireAuth(GenerationApp)}
                />
                <Route path="/marks/:answerId" component={requireAuthAdmin(MarkerApp)} />
                <Route path="/users/:user" component={requireAuthAdmin(UserLastAnswerApp)} />
                <Route path="/login" component={Login} />
                <Route exact path="/" component={Home} />
            </Switch>
        </Root>
        ,
    </ThemeProvider>,
    document.getElementById('root')
)
