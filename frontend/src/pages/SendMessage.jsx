import { useState, useEffect } from 'react'
import { getUsers } from '../services/auth'
import { sendMessage } from '../services/messages'

export default function SendMessage() {
    const [users, setUsers] = useState([])
    const [formData, setFormData] = useState({
        recipient: '',
        message: '',
        encryptionType: 'AES'
    })
    const [result, setResult] = useState(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState('')

    useEffect(() => {
        getUsers().then(data => setUsers(data.users)).catch(() => { })
    }, [])

    const handleSubmit = async (e) => {
        e.preventDefault()
        setLoading(true)
        setError('')
        setResult(null)

        try {
            const data = await sendMessage(formData.recipient, formData.message, formData.encryptionType)
            setResult(data)
        } catch (err) {
            setError(err.response?.data?.error || 'Error al enviar mensaje')
        } finally {
            setLoading(false)
        }
    }

    const encryptionTypes = [
        { id: 'AES', name: 'AES-256-CBC', desc: 'Simétrico' },
        { id: 'RSA', name: 'RSA-2048', desc: 'Asimétrico' },
        { id: 'HYBRID', name: 'Híbrido', desc: 'RSA + AES' }
    ]

    return (
        <div className="p-8 max-w-3xl mx-auto space-y-6">
            {/* Header */}
            <div>
                <h1 className="text-2xl font-semibold text-text-primary">Nuevo Mensaje</h1>
                <p className="text-text-secondary text-sm mt-1">Envía un mensaje cifrado</p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
                {/* Recipient */}
                <div className="card p-5">
                    <label className="block text-text-primary font-medium text-sm mb-3">Destinatario</label>
                    <select
                        value={formData.recipient}
                        onChange={e => setFormData(p => ({ ...p, recipient: e.target.value }))}
                        className="input-field w-full"
                        required
                    >
                        <option value="">Selecciona un usuario</option>
                        {users.map(u => (
                            <option key={u.id} value={u.username}>
                                {u.username} {u.has_keys ? '(tiene claves)' : ''}
                            </option>
                        ))}
                    </select>
                </div>

                {/* Encryption Type */}
                <div className="card p-5">
                    <label className="block text-text-primary font-medium text-sm mb-3">Tipo de Cifrado</label>
                    <div className="grid grid-cols-3 gap-2">
                        {encryptionTypes.map(type => {
                            const isSelected = formData.encryptionType === type.id
                            return (
                                <button
                                    key={type.id}
                                    type="button"
                                    onClick={() => setFormData(p => ({ ...p, encryptionType: type.id }))}
                                    style={{
                                        backgroundColor: isSelected ? 'rgba(124, 179, 66, 0.25)' : '#0b141a',
                                        borderColor: isSelected ? '#7cb342' : '#2a3942',
                                        color: isSelected ? '#7cb342' : '#8696a0'
                                    }}
                                    className="p-3 rounded-lg text-left transition text-sm border-2"
                                >
                                    <div className="font-medium">{type.name}</div>
                                    <div className="text-xs opacity-70">{type.desc}</div>
                                </button>
                            )
                        })}
                    </div>
                </div>

                {/* Message */}
                <div className="card p-5">
                    <label className="block text-text-primary font-medium text-sm mb-3">Mensaje</label>
                    <textarea
                        value={formData.message}
                        onChange={e => setFormData(p => ({ ...p, message: e.target.value }))}
                        rows={5}
                        className="input-field w-full resize-none"
                        placeholder="Escribe tu mensaje..."
                        required
                    />
                </div>

                {error && (
                    <div className="bg-red-500/10 border border-red-500/50 text-red-400 px-4 py-3 rounded-lg text-sm">
                        {error}
                    </div>
                )}

                <button
                    type="submit"
                    disabled={loading}
                    className="btn-primary w-full py-3 rounded-lg font-medium disabled:opacity-50"
                >
                    {loading ? 'Enviando...' : 'Enviar Mensaje Cifrado'}
                </button>
            </form>

            {/* Result */}
            {result && (
                <div className="card p-5 border-accent/30">
                    <div className="flex items-center gap-2 mb-4">
                        <svg className="w-5 h-5 text-accent" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                        <h2 className="font-semibold text-accent">Mensaje Enviado</h2>
                    </div>

                    {result.encryption_steps && (
                        <div className="mb-4">
                            <h3 className="text-text-secondary text-sm mb-2">Pasos del cifrado:</h3>
                            <div className="space-y-1">
                                {result.encryption_steps.map((step, i) => (
                                    <div key={i} className="flex items-center gap-2 text-xs text-text-secondary">
                                        <span className="w-4 h-4 bg-accent/20 rounded-full flex items-center justify-center text-accent">
                                            {step.step}
                                        </span>
                                        <span>{step.name}</span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {result.shared_key && (
                        <div className="bg-yellow-500/10 border border-yellow-500/30 p-4 rounded-lg">
                            <div className="text-yellow-500 font-medium text-sm mb-2">Clave Compartida</div>
                            <div className="code-block text-yellow-200 text-xs break-all">{result.shared_key}</div>
                            <p className="text-yellow-500/70 text-xs mt-2">
                                Comparte esta clave de forma segura con el destinatario
                            </p>
                        </div>
                    )}
                </div>
            )}
        </div>
    )
}
