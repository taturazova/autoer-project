import axios from 'axios'
import { toast } from 'react-toastify'

export const setAxiosAuthToken = (token) => {
    if (typeof token !== 'undefined' && token) {
        // Apply for every request
        axios.defaults.headers.common['Authorization'] = 'Token ' + token
    } else {
        // Delete auth header
        delete axios.defaults.headers.common['Authorization']
    }
}

export const isEmpty = (value) => {
    if (value === null || value === undefined) return true
    if (typeof value === 'object' && Object.keys(value).length === 0) return true
    if (typeof value === 'string' && value.trim().length === 0) return true
    return false
}

export const toastOnError = (error) => {
    if (error.response) {
        // known error
        toast.error(JSON.stringify(error.response.data))
    } else if (error.message) {
        toast.error(JSON.stringify(error.message))
    } else {
        toast.error(JSON.stringify(error))
    }
}
