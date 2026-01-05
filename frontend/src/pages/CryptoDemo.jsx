import { useState } from 'react'
import { aesEncrypt, aesDecrypt, generateKeys, rsaEncrypt, rsaSign, rsaVerify } from '../services/crypto'

export default function CryptoDemo() {
    const [tab, setTab] = useState('AES')
    const [message, setMessage] = useState('Hola, este es un mensaje de prueba!')
    const [result, setResult] = useState(null)
    const [loading, setLoading] = useState(false)
    const [keys, setKeys] = useState(null)

    const handleGenerateKeys = async () => {
        setLoading(true)
        try {
            const data = await generateKeys(tab, tab === 'AES' ? 256 : 2048)
            setKeys(data)
            setResult(null)
        } catch (err) {
            console.error(err)
        } finally {
            setLoading(false)
        }
    }

    const handleEncrypt = async () => {
        setLoading(true)
        try {
            if (tab === 'AES') {
                const data = await aesEncrypt(message)
                setResult(data)
                setKeys({ key: data.key })
            } else {
                if (!keys?.public_key) {
                    alert('Primero genera un par de claves RSA')
                    return
                }
                const data = await rsaEncrypt(message, keys.public_key)
                setResult(data)
            }
        } catch (err) {
            console.error(err)
        } finally {
            setLoading(false)
        }
    }

    const handleSign = async () => {
        if (tab !== 'RSA' || !keys?.private_key) return
        setLoading(true)
        try {
            const data = await rsaSign(message, keys.private_key)
            setResult(data)
        } catch (err) {
            console.error(err)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="p-8 space-y-6">
            {/* Header */}
            <div>
                <h1 className="text-2xl font-semibold text-text-primary">Demo de Cifrado</h1>
                <p className="text-text-secondary text-sm mt-1">
                    Visualiza paso a paso cómo funcionan los algoritmos
                </p>
            </div>

            {/* Tab Selector */}
            <div className="flex gap-2">
                {['AES', 'RSA'].map(t => (
                    <button
                        key={t}
                        onClick={() => { setTab(t); setResult(null); setKeys(null) }}
                        style={{
                            backgroundColor: tab === t ? '#7cb342' : '#202c33',
                            color: tab === t ? 'white' : '#8696a0',
                            borderColor: tab === t ? '#7cb342' : '#2a3942'
                        }}
                        className="px-5 py-2.5 rounded-lg font-medium text-sm transition border"
                    >
                        {t === 'AES' ? 'AES-256-CBC' : 'RSA-2048'}
                    </button>
                ))}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Input Panel */}
                <div className="card p-6">
                    <h2 className="font-semibold text-text-primary mb-4">Entrada</h2>

                    <div className="space-y-4">
                        <div>
                            <label className="block text-text-secondary text-sm mb-2">Mensaje a cifrar</label>
                            <textarea
                                value={message}
                                onChange={e => setMessage(e.target.value)}
                                rows={4}
                                className="input-field w-full resize-none"
                            />
                        </div>

                        {tab === 'RSA' && (
                            <button
                                onClick={handleGenerateKeys}
                                disabled={loading}
                                className="btn-secondary w-full py-2.5 rounded-lg text-sm"
                            >
                                {loading ? 'Generando...' : 'Generar Par de Claves RSA'}
                            </button>
                        )}

                        <div className="flex gap-2">
                            <button
                                onClick={handleEncrypt}
                                disabled={loading}
                                className="btn-primary flex-1 py-2.5 rounded-lg text-sm font-medium"
                            >
                                {loading ? 'Cifrando...' : 'Cifrar'}
                            </button>

                            {tab === 'RSA' && keys?.private_key && (
                                <button
                                    onClick={handleSign}
                                    disabled={loading}
                                    className="btn-secondary flex-1 py-2.5 rounded-lg text-sm font-medium"
                                >
                                    Firmar
                                </button>
                            )}
                        </div>
                    </div>

                    {keys && (
                        <div className="mt-4 p-4 bg-wa-chat rounded-lg border border-wa-border">
                            <h3 className="text-xs font-medium text-text-secondary mb-2">
                                {tab === 'AES' ? 'Clave AES' : 'Claves RSA'}
                            </h3>
                            {tab === 'AES' ? (
                                <div className="code-block text-accent text-xs">{keys.key}</div>
                            ) : (
                                <div className="space-y-2">
                                    <details>
                                        <summary className="text-text-secondary cursor-pointer text-xs">Clave Pública</summary>
                                        <pre className="code-block text-accent text-xs mt-2">{keys.public_key?.substring(0, 200)}...</pre>
                                    </details>
                                    <details>
                                        <summary className="text-text-secondary cursor-pointer text-xs">Clave Privada (sensible)</summary>
                                        <pre className="code-block text-red-400 text-xs mt-2">{keys.private_key?.substring(0, 200)}...</pre>
                                    </details>
                                </div>
                            )}
                        </div>
                    )}
                </div>

                {/* Steps Panel */}
                <div className="card p-6">
                    <h2 className="font-semibold text-text-primary mb-4">Pasos del Proceso</h2>

                    {result?.steps ? (
                        <div className="space-y-3">
                            {result.steps.map((step, i) => (
                                <div
                                    key={i}
                                    className="p-3 bg-wa-chat rounded-lg border-l-2 border-accent"
                                >
                                    <div className="flex items-center gap-2 mb-2">
                                        <span className="w-5 h-5 bg-accent rounded-full flex items-center justify-center text-xs font-medium text-white">
                                            {step.step}
                                        </span>
                                        <span className="font-medium text-text-primary text-sm">{step.name}</span>
                                    </div>

                                    <div className="code-block text-xs">
                                        {step.type === 'text' && (
                                            <span className="text-accent">{step.data}</span>
                                        )}
                                        {step.type === 'hex' && (
                                            <span className="text-yellow-400">{step.data}</span>
                                        )}
                                        {step.type === 'hex_partial' && (
                                            <span className="text-orange-400">{step.data}</span>
                                        )}
                                        {step.type === 'base64' && (
                                            <span className="text-cyan-400 break-all">{step.data}</span>
                                        )}
                                        {step.type === 'pem_partial' && (
                                            <span className="text-purple-400">{step.data}</span>
                                        )}
                                        {step.type === 'info' && (
                                            <span className="text-text-secondary">{step.data}</span>
                                        )}
                                    </div>

                                    {step.length && (
                                        <div className="text-text-secondary text-xs mt-1">
                                            Longitud: {step.length} bytes
                                        </div>
                                    )}
                                </div>
                            ))}
                        </div>
                    ) : (
                        <div className="text-center py-12 text-text-secondary">
                            <svg className="w-12 h-12 mx-auto mb-3 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                            </svg>
                            <p className="text-sm">Los pasos aparecerán aquí</p>
                        </div>
                    )}
                </div>
            </div>

            {/* Result */}
            {result?.result && (
                <div className="card p-6 border-accent/30">
                    <h2 className="font-semibold text-text-primary mb-4">Resultado</h2>
                    <div className="code-block">
                        <pre className="text-cyan-400 whitespace-pre-wrap break-all text-xs">
                            {JSON.stringify(result.result, null, 2)}
                        </pre>
                    </div>
                </div>
            )}
        </div>
    )
}
