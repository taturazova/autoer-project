import axios from 'axios'
import { push } from 'connected-react-router'
import { toast } from 'react-toastify'
import { SET_TOKEN, SET_CURRENT_USER, UNSET_CURRENT_USER, SET_STAFF } from './LoginTypes'
import { setAxiosAuthToken, toastOnError } from '../../utils/Utils'

export const login = (userData, redirectTo) => (dispatch) => {
    axios
        .post(`${process.env.REACT_APP_BASE_URL}/api/rest-auth/login/`, userData)
        .then((response) => {
            const auth_token = response.data.key
            setAxiosAuthToken(auth_token)
            dispatch(setToken(auth_token))
            dispatch(getStaff())
            dispatch(getCurrentUser(redirectTo))
        })
        .catch((error) => {
            dispatch(unsetCurrentUser())
            toastOnError(error)
        })
}

export const getCurrentUser = (redirectTo) => (dispatch) => {
    axios
        .get(`${process.env.REACT_APP_BASE_URL}/api/rest-auth/user/`, {
            headers: { Authorization: 'Token ' + localStorage.getItem('token') }
        })
        .then((response) => {
            const user = {
                username: response.data.username,
                email: response.data.email
            }
            dispatch(setCurrentUser(user, redirectTo))
        })
        .catch((error) => {
            dispatch(unsetCurrentUser())
            toastOnError(error)
        })
}

export const getStaff = () => (dispatch) => {
    axios
        .get(`${process.env.REACT_APP_BASE_URL}/api/users/me/`, {
            headers: { Authorization: 'Token ' + localStorage.getItem('token') }
        })
        .then((response) => {
            const staff = response.data.permissions.is_staff
            dispatch(setStaff(staff))
        })
        .catch((error) => {
            dispatch(unsetCurrentUser())
            toastOnError(error)
        })
}

export const setCurrentUser = (user, redirectTo) => (dispatch) => {
    localStorage.setItem('user', JSON.stringify(user))
    dispatch({
        type: SET_CURRENT_USER,
        payload: user
    })

    if (redirectTo !== '') {
        dispatch(push(redirectTo))
    }
}

export const setToken = (token) => (dispatch) => {
    setAxiosAuthToken(token)
    localStorage.setItem('token', token)
    dispatch({
        type: SET_TOKEN,
        payload: token
    })
}
export const setStaff = (staff) => (dispatch) => {
    dispatch({
        type: SET_STAFF,
        payload: staff
    })
}

export const unsetCurrentUser = () => (dispatch) => {
    setAxiosAuthToken('')
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    dispatch({
        type: UNSET_CURRENT_USER
    })
}

export const logout = () => (dispatch) => {
    axios
        .post(`${process.env.REACT_APP_BASE_URL}/api/rest-auth/logout/`)
        .then((response) => {
            dispatch(unsetCurrentUser())
            dispatch(push('/'))
            toast.success('Logout successful.')
        })
        .catch((error) => {
            dispatch(unsetCurrentUser())
            toastOnError(error)
        })
}
