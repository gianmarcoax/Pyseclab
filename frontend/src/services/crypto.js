import api from './api'

export const generateKeys = async (algorithm, keySize) => {
    const response = await api.post('/crypto/keys/generate/', { algorithm, key_size: keySize })
    return response.data
}

export const aesEncrypt = async (plaintext, keySize = 256, key = null) => {
    const data = { plaintext, key_size: keySize }
    if (key) data.key = key
    const response = await api.post('/crypto/aes/encrypt/', data)
    return response.data
}

export const aesDecrypt = async (ciphertext, iv, key) => {
    const response = await api.post('/crypto/aes/decrypt/', { ciphertext, iv, key })
    return response.data
}

export const rsaEncrypt = async (plaintext, publicKey) => {
    const response = await api.post('/crypto/rsa/encrypt/', { plaintext, public_key: publicKey })
    return response.data
}

export const rsaDecrypt = async (ciphertext, privateKey) => {
    const response = await api.post('/crypto/rsa/decrypt/', { ciphertext, private_key: privateKey })
    return response.data
}

export const rsaSign = async (message, privateKey) => {
    const response = await api.post('/crypto/rsa/sign/', { message, private_key: privateKey })
    return response.data
}

export const rsaVerify = async (message, signature, publicKey) => {
    const response = await api.post('/crypto/rsa/verify/', { message, signature, public_key: publicKey })
    return response.data
}
