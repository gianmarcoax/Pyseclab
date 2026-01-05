import { Outlet, Link, useLocation } from 'react-router-dom'
import { useContext } from 'react'
import { AuthContext } from '../App'

export default function Layout() {
    const { user, logout } = useContext(AuthContext)
    const location = useLocation()

    const navItems = [
        { path: '/', label: 'Inicio', icon: 'home' },
        { path: '/demo', label: 'Demo Cifrado', icon: 'lock' },
        { path: '/send', label: 'Nuevo Mensaje', icon: 'send' },
        { path: '/messages', label: 'Mensajes', icon: 'inbox' },
    ]

    const getIcon = (name) => {
        const icons = {
            home: (
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                </svg>
            ),
            lock: (
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
            ),
            send: (
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
            ),
            inbox: (
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
                </svg>
            ),
            logout: (
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
            )
        }
        return icons[name]
    }

    return (
        <div className="min-h-screen flex bg-wa-dark">
            {/* Sidebar */}
            <aside className="w-64 bg-wa-panel border-r border-wa-border flex flex-col">
                {/* Logo */}
                <div className="p-5 border-b border-wa-border">
                    <div className="flex items-center gap-3">
                        <img src="/logo.png" alt="PySec Lab" className="w-10 h-10" />
                        <div>
                            <h1 className="text-lg font-semibold text-text-primary">PySec Lab</h1>
                            <p className="text-xs text-text-secondary">Laboratorio de Seguridad</p>
                        </div>
                    </div>
                </div>

                {/* Navigation */}
                <nav className="flex-1 p-3">
                    {navItems.map(item => (
                        <Link
                            key={item.path}
                            to={item.path}
                            className={`flex items-center gap-3 px-4 py-3 rounded-lg mb-1 transition-all ${location.pathname === item.path
                                ? 'bg-accent text-white'
                                : 'text-text-secondary hover:bg-wa-hover hover:text-text-primary'
                                }`}
                        >
                            {getIcon(item.icon)}
                            <span className="text-sm">{item.label}</span>
                        </Link>
                    ))}
                </nav>

                {/* User */}
                <div className="p-4 border-t border-wa-border">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                            <div className="w-9 h-9 bg-primary rounded-full flex items-center justify-center text-white font-medium text-sm">
                                {user?.username?.[0]?.toUpperCase() || 'U'}
                            </div>
                            <span className="text-text-primary text-sm">{user?.username}</span>
                        </div>
                        <button
                            onClick={logout}
                            className="text-text-secondary hover:text-red-400 transition p-2"
                            title="Cerrar sesión"
                        >
                            {getIcon('logout')}
                        </button>
                    </div>
                </div>
            </aside>

            {/* Main content */}
            <main className="flex-1 overflow-auto">
                <Outlet />
            </main>
        </div>
    )
}
