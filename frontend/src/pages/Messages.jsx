import { useState, useEffect } from 'react'
import { getInbox, getSent, decryptMessage } from '../services/messages'

export default function Messages() {
    const [tab, setTab] = useState('inbox')
    const [messages, setMessages] = useState([])
    const [loading, setLoading] = useState(true)
    const [decrypting, setDecrypting] = useState(null)
    const [decryptedContent, setDecryptedContent] = useState({})
    // Claves separadas por mensaje
    const [sharedKeys, setSharedKeys] = useState({})

    useEffect(() => {
        loadMessages()
    }, [tab])

    const loadMessages = async () => {
        setLoading(true)
        try {
            const data = tab === 'inbox' ? await getInbox() : await getSent()
            setMessages(data.messages)
        } catch (err) {
            console.error(err)
        } finally {
            setLoading(false)
        }
    }

    const handleDecrypt = async (msgId, encType) => {
        setDecrypting(msgId)
        try {
            const keyForMessage = sharedKeys[msgId] || ''
            const data = await decryptMessage(msgId, encType === 'AES' ? keyForMessage : null)
            setDecryptedContent(prev => ({ ...prev, [msgId]: data }))
        } catch (err) {
            alert('Error al descifrar: ' + (err.response?.data?.error || err.message))
        } finally {
            setDecrypting(null)
        }
    }

    const updateSharedKey = (msgId, value) => {
        setSharedKeys(prev => ({ ...prev, [msgId]: value }))
    }

    return (
        <div className="p-8 space-y-6">
            {/* Header */}
            <div>
                <h1 className="text-2xl font-semibold text-text-primary">Mensajes</h1>
                <p className="text-text-secondary text-sm mt-1">Tus mensajes cifrados</p>
            </div>

            {/* Tabs */}
            <div className="flex gap-2">
                <button
                    onClick={() => setTab('inbox')}
                    style={{
                        backgroundColor: tab === 'inbox' ? '#7cb342' : '#202c33',
                        color: tab === 'inbox' ? 'white' : '#8696a0',
                        borderColor: tab === 'inbox' ? '#7cb342' : '#2a3942'
                    }}
                    className="px-5 py-2.5 rounded-lg font-medium text-sm transition border"
                >
                    Recibidos
                </button>
                <button
                    onClick={() => setTab('sent')}
                    style={{
                        backgroundColor: tab === 'sent' ? '#7cb342' : '#202c33',
                        color: tab === 'sent' ? 'white' : '#8696a0',
                        borderColor: tab === 'sent' ? '#7cb342' : '#2a3942'
                    }}
                    className="px-5 py-2.5 rounded-lg font-medium text-sm transition border"
                >
                    Enviados
                </button>
            </div>

            {/* Messages List */}
            {loading ? (
                <div className="text-center py-8 text-text-secondary text-sm">Cargando...</div>
            ) : messages.length === 0 ? (
                <div className="text-center py-12 card">
                    <svg className="w-12 h-12 mx-auto mb-3 text-text-secondary opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
                    </svg>
                    <p className="text-text-secondary text-sm">No hay mensajes</p>
                </div>
            ) : (
                <div className="space-y-3">
                    {messages.map(msg => (
                        <div key={msg.id} className="card p-5">
                            <div className="flex items-center justify-between mb-3">
                                <div className="flex items-center gap-3">
                                    <div className="w-10 h-10 bg-primary rounded-full flex items-center justify-center text-white font-medium text-sm">
                                        {(tab === 'inbox' ? msg.sender_username : msg.recipient_username)?.[0]?.toUpperCase()}
                                    </div>
                                    <div>
                                        <div className="text-text-primary font-medium text-sm">
                                            {tab === 'inbox' ? msg.sender_username : msg.recipient_username}
                                        </div>
                                        <div className="text-text-secondary text-xs">
                                            {new Date(msg.created_at).toLocaleString()}
                                        </div>
                                    </div>
                                </div>

                                <span
                                    style={{
                                        backgroundColor: msg.encryption_type === 'AES' ? 'rgba(124, 179, 66, 0.2)' :
                                            msg.encryption_type === 'RSA' ? 'rgba(30, 74, 110, 0.3)' :
                                                'rgba(234, 179, 8, 0.2)',
                                        color: msg.encryption_type === 'AES' ? '#7cb342' :
                                            msg.encryption_type === 'RSA' ? '#5a9fd4' :
                                                '#eab308'
                                    }}
                                    className="px-2.5 py-1 rounded text-xs font-medium"
                                >
                                    {msg.encryption_type}
                                </span>
                            </div>

                            <div className="bg-wa-chat p-3 rounded-lg mb-3">
                                <div className="text-text-secondary text-xs mb-1">Contenido cifrado:</div>
                                <div className="text-cyan-400 text-xs font-mono break-all">
                                    {msg.preview}
                                </div>
                            </div>

                            {/* Decrypt Section */}
                            {tab === 'inbox' && !decryptedContent[msg.id] && (
                                <div className="flex items-center gap-2">
                                    {msg.encryption_type === 'AES' && (
                                        <input
                                            type="text"
                                            placeholder="Clave compartida"
                                            value={sharedKeys[msg.id] || ''}
                                            onChange={e => updateSharedKey(msg.id, e.target.value)}
                                            className="input-field flex-1 text-sm py-2"
                                        />
                                    )}
                                    <button
                                        onClick={() => handleDecrypt(msg.id, msg.encryption_type)}
                                        disabled={decrypting === msg.id}
                                        className="btn-primary px-4 py-2 rounded-lg text-sm disabled:opacity-50"
                                    >
                                        {decrypting === msg.id ? 'Descifrando...' : 'Descifrar'}
                                    </button>
                                </div>
                            )}

                            {/* Decrypted Content */}
                            {decryptedContent[msg.id] && (
                                <div style={{ backgroundColor: 'rgba(124, 179, 66, 0.1)', borderColor: 'rgba(124, 179, 66, 0.3)' }} className="border p-4 rounded-lg">
                                    <div className="flex items-center gap-2 mb-2">
                                        <svg className="w-4 h-4 text-accent" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                                        </svg>
                                        <span className="text-accent font-medium text-sm">Descifrado</span>
                                    </div>
                                    <div className="text-text-primary text-sm">{decryptedContent[msg.id].plaintext}</div>
                                    {decryptedContent[msg.id].signature_valid !== null && (
                                        <div className={`mt-2 text-xs ${decryptedContent[msg.id].signature_valid ? 'text-accent' : 'text-red-400'}`}>
                                            {decryptedContent[msg.id].signature_valid ? 'Firma válida' : 'Firma inválida'}
                                        </div>
                                    )}
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            )}
        </div>
    )
}
