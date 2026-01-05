import api from './api'

export const getToken = () => localStorage.getItem('token')
export const removeToken = () => localStorage.removeItem('token')

export const login = async (username, password) => {
    const response = await api.post('/auth/login/', { username, password })
    return response.data
}

export const register = async (data) => {
    const response = await api.post('/auth/register/', data)
    return response.data
}

export const getMe = async () => {
    const response = await api.get('/auth/me/')
    return response.data
}

export const getMyKeys = async () => {
    const response = await api.get('/auth/me/keys/')
    return response.data
}

export const generateMyKeys = async (keySize = 2048) => {
    const response = await api.post('/auth/me/keys/generate/', { key_size: keySize })
    return response.data
}

export const getUsers = async () => {
    const response = await api.get('/auth/users/')
    return response.data
}

export const getPublicKey = async (username) => {
    const response = await api.post('/auth/users/public-key/', { username })
    return response.data
}
