import api from './api'

export const getMessages = async () => {
    const response = await api.get('/messages/')
    return response.data
}

export const getInbox = async () => {
    const response = await api.get('/messages/inbox/')
    return response.data
}

export const getSent = async () => {
    const response = await api.get('/messages/sent/')
    return response.data
}

export const sendMessage = async (recipientUsername, plaintext, encryptionType = 'AES') => {
    const response = await api.post('/messages/send/', {
        recipient_username: recipientUsername,
        plaintext,
        encryption_type: encryptionType
    })
    return response.data
}

export const getMessage = async (id) => {
    const response = await api.get(`/messages/${id}/`)
    return response.data
}

export const decryptMessage = async (id, sharedKey = null) => {
    const data = sharedKey ? { shared_key: sharedKey } : {}
    const response = await api.post(`/messages/${id}/decrypt/`, data)
    return response.data
}
