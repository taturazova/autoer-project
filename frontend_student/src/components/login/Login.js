import React, { Component } from 'react'
import { withRouter } from 'react-router-dom'
import { connect } from 'react-redux'
import PropTypes from 'prop-types'
import { Link } from 'react-router-dom'
import { Container, Button, Row, Col, Form } from 'react-bootstrap'

import { login } from './LoginActions'

class Login extends Component {
    constructor(props) {
        super(props)
        this.state = {
            username: '',
            password: ''
        }
    }

    onChange = (e) => {
        this.setState({ [e.target.name]: e.target.value })
    }

    onLoginClick = () => {
        const userData = {
            username: this.state.username,
            password: this.state.password
        }
        const query = new URLSearchParams(this.props.location.search)
        const next = query.get('next')
        console.log(next)
        this.props.login(userData, next) // <--- login request
    }
    render() {
        return (
            <Container>
                <Row>
                    <Col md="4">
                        <h1>Login</h1>
                        <Form>
                            <Form.Group controlId="usernameId">
                                <Form.Label>User name</Form.Label>
                                <Form.Control
                                    type="text"
                                    name="username"
                                    placeholder="Enter user name"
                                    value={this.state.username}
                                    onChange={this.onChange}
                                />
                            </Form.Group>

                            <Form.Group controlId="passwordId">
                                <Form.Label>Your password</Form.Label>
                                <Form.Control
                                    type="password"
                                    name="password"
                                    placeholder="Enter password"
                                    value={this.state.password}
                                    onChange={this.onChange}
                                />
                            </Form.Group>
                        </Form>
                        <Button color="primary" onClick={this.onLoginClick}>
                            Login
                        </Button>
                    </Col>
                </Row>
            </Container>
        )
    }
}

// connect action and store and component
Login.propTypes = {
    login: PropTypes.func.isRequired,
    auth: PropTypes.object.isRequired
}

const mapStateToProps = (state) => ({
    auth: state.auth
})

export default connect(mapStateToProps, {
    login
})(withRouter(Login))
