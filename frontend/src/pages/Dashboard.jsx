import { useState, useEffect, useContext } from 'react'
import { Link } from 'react-router-dom'
import { AuthContext } from '../App'
import { getMyKeys } from '../services/auth'
import { getInbox } from '../services/messages'

export default function Dashboard() {
    const { user } = useContext(AuthContext)
    const [keys, setKeys] = useState(null)
    const [inbox, setInbox] = useState({ messages: [], unread_count: 0 })
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        const loadData = async () => {
            try {
                const [keysData, inboxData] = await Promise.all([
                    getMyKeys().catch(() => null),
                    getInbox().catch(() => ({ messages: [], unread_count: 0 }))
                ])
                setKeys(keysData)
                setInbox(inboxData)
            } finally {
                setLoading(false)
            }
        }
        loadData()
    }, [])

    if (loading) {
        return (
            <div className="p-8">
                <div className="animate-pulse text-text-secondary">Cargando...</div>
            </div>
        )
    }

    return (
        <div className="p-8 space-y-6">
            {/* Header */}
            <div>
                <h1 className="text-2xl font-semibold text-text-primary">
                    Bienvenido, {user?.username}
                </h1>
                <p className="text-text-secondary text-sm mt-1">
                    Sistema de mensajería con cifrado AES y RSA
                </p>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="card p-5">
                    <div className="flex items-center gap-4">
                        <div className="w-12 h-12 bg-primary/20 rounded-lg flex items-center justify-center">
                            <svg className="w-6 h-6 text-primary-light" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
                            </svg>
                        </div>
                        <div>
                            <div className="text-2xl font-bold text-text-primary">{inbox.unread_count}</div>
                            <div className="text-text-secondary text-sm">Mensajes sin leer</div>
                        </div>
                    </div>
                </div>

                <div className={`card p-5 ${keys ? 'border-accent/30' : 'border-yellow-500/30'}`}>
                    <div className="flex items-center gap-4">
                        <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${keys ? 'bg-accent/20' : 'bg-yellow-500/20'}`}>
                            <svg className={`w-6 h-6 ${keys ? 'text-accent' : 'text-yellow-500'}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
                            </svg>
                        </div>
                        <div>
                            <div className="text-2xl font-bold text-text-primary">
                                {keys ? `RSA-${keys.key_size}` : 'Sin claves'}
                            </div>
                            <div className="text-text-secondary text-sm">
                                {keys ? 'Claves activas' : 'Genera tus claves'}
                            </div>
                        </div>
                    </div>
                </div>

                <div className="card p-5">
                    <div className="flex items-center gap-4">
                        <div className="w-12 h-12 bg-primary/20 rounded-lg flex items-center justify-center">
                            <svg className="w-6 h-6 text-primary-light" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                            </svg>
                        </div>
                        <div>
                            <div className="text-2xl font-bold text-text-primary">3</div>
                            <div className="text-text-secondary text-sm">Modos de cifrado</div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Quick Actions */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Link to="/demo" className="card p-6 hover:border-accent/50 transition group">
                    <div className="flex items-center gap-4">
                        <div className="w-12 h-12 bg-accent/20 rounded-lg flex items-center justify-center group-hover:bg-accent/30 transition">
                            <svg className="w-6 h-6 text-accent" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                            </svg>
                        </div>
                        <div>
                            <h3 className="font-semibold text-text-primary">Demo de Cifrado</h3>
                            <p className="text-text-secondary text-sm">Visualiza el proceso paso a paso</p>
                        </div>
                    </div>
                </Link>

                <Link to="/send" className="card p-6 hover:border-accent/50 transition group">
                    <div className="flex items-center gap-4">
                        <div className="w-12 h-12 bg-accent/20 rounded-lg flex items-center justify-center group-hover:bg-accent/30 transition">
                            <svg className="w-6 h-6 text-accent" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                            </svg>
                        </div>
                        <div>
                            <h3 className="font-semibold text-text-primary">Enviar Mensaje</h3>
                            <p className="text-text-secondary text-sm">Envía un mensaje cifrado</p>
                        </div>
                    </div>
                </Link>
            </div>

            {/* Encryption Types */}
            <div className="card p-6">
                <h2 className="font-semibold text-text-primary mb-4">Tipos de Cifrado</h2>

                <div className="space-y-3">
                    <div className="flex items-start gap-4 p-4 bg-wa-chat rounded-lg">
                        <div className="w-10 h-10 bg-accent/20 rounded-lg flex items-center justify-center flex-shrink-0">
                            <svg className="w-5 h-5 text-accent" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                            </svg>
                        </div>
                        <div>
                            <h3 className="font-medium text-accent">AES-256-CBC (Simétrico)</h3>
                            <p className="text-text-secondary text-sm">Emisor y receptor comparten una clave secreta. Rápido y eficiente.</p>
                        </div>
                    </div>

                    <div className="flex items-start gap-4 p-4 bg-wa-chat rounded-lg">
                        <div className="w-10 h-10 bg-primary/20 rounded-lg flex items-center justify-center flex-shrink-0">
                            <svg className="w-5 h-5 text-primary-light" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
                            </svg>
                        </div>
                        <div>
                            <h3 className="font-medium text-primary-light">RSA-2048 (Asimétrico)</h3>
                            <p className="text-text-secondary text-sm">Usa par de claves pública/privada. Incluye firma digital.</p>
                        </div>
                    </div>

                    <div className="flex items-start gap-4 p-4 bg-wa-chat rounded-lg">
                        <div className="w-10 h-10 bg-yellow-500/20 rounded-lg flex items-center justify-center flex-shrink-0">
                            <svg className="w-5 h-5 text-yellow-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
                            </svg>
                        </div>
                        <div>
                            <h3 className="font-medium text-yellow-500">Híbrido (RSA + AES)</h3>
                            <p className="text-text-secondary text-sm">Combina seguridad de RSA con velocidad de AES.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}
