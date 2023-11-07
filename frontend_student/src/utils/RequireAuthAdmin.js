import React from 'react'
import { connect } from 'react-redux'
import { push } from 'connected-react-router'
import PropTypes from 'prop-types'
import { getStaff } from './../components/login/LoginActions'

export default function requireAuthAdmin(Component) {
    class AuthenticatedComponent extends React.Component {
        constructor(props) {
            super(props)
            this.checkAuth()
        }

        componentDidUpdate(prevProps, prevState) {
            this.checkAuth()
        }

        async checkAuth() {
            if (!this.props.isAuthenticated) {
                const redirectAfterLogin = this.props.location.pathname
                this.props.dispatch(push(`/login?next=${redirectAfterLogin}`))
            } else if (!this.props.isStaff) {
                this.props.dispatch(getStaff())
            }
        }

        render() {
            return (
                <div>
                    {this.props.isAuthenticated && this.props.isStaff ? (
                        <Component {...this.props} />
                    ) : null}
                </div>
            )
        }
    }
    AuthenticatedComponent.propTypes = {
        isAuthenticated: PropTypes.bool.isRequired,
        isStaff: PropTypes.bool.isRequired,
        location: PropTypes.shape({
            pathname: PropTypes.string.isRequired
        }).isRequired,
        dispatch: PropTypes.func.isRequired
    }

    const mapStateToProps = (state) => {
        return {
            isAuthenticated: state.auth.isAuthenticated,
            isStaff: state.auth.isStaff,
            token: state.auth.token
        }
    }

    return connect(mapStateToProps)(AuthenticatedComponent)
}
