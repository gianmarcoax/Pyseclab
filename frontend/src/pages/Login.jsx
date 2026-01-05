import { useState, useContext } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { AuthContext } from '../App'
import { login as loginService } from '../services/auth'

export default function Login() {
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [error, setError] = useState('')
    const [loading, setLoading] = useState(false)
    const { login } = useContext(AuthContext)
    const navigate = useNavigate()

    const handleSubmit = async (e) => {
        e.preventDefault()
        setError('')
        setLoading(true)

        try {
            const data = await loginService(username, password)
            login(data.user, data.access)
            navigate('/')
        } catch (err) {
            setError(err.response?.data?.detail || 'Error al iniciar sesión')
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="min-h-screen flex items-center justify-center p-4 bg-wa-dark">
            <div className="w-full max-w-md">
                {/* Logo */}
                <div className="text-center mb-8">
                    <img src="/logo.png" alt="PySec Lab" className="w-20 h-20 mx-auto mb-4" />
                    <h1 className="text-2xl font-semibold text-text-primary">PySec Lab</h1>
                    <p className="text-text-secondary text-sm mt-1">Laboratorio de Seguridad</p>
                </div>

                {/* Form Card */}
                <div className="card p-8">
                    <h2 className="text-xl font-semibold text-text-primary mb-6">Iniciar Sesión</h2>

                    {error && (
                        <div className="bg-red-500/10 border border-red-500/50 text-red-400 px-4 py-3 rounded-lg mb-4 text-sm">
                            {error}
                        </div>
                    )}

                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div>
                            <label className="block text-text-secondary text-sm mb-2">Usuario</label>
                            <input
                                type="text"
                                value={username}
                                onChange={e => setUsername(e.target.value)}
                                className="input-field w-full"
                                required
                            />
                        </div>

                        <div>
                            <label className="block text-text-secondary text-sm mb-2">Contraseña</label>
                            <input
                                type="password"
                                value={password}
                                onChange={e => setPassword(e.target.value)}
                                className="input-field w-full"
                                required
                            />
                        </div>

                        <button
                            type="submit"
                            disabled={loading}
                            className="btn-primary w-full py-3 rounded-lg font-medium disabled:opacity-50"
                        >
                            {loading ? 'Ingresando...' : 'Ingresar'}
                        </button>
                    </form>

                    <p className="text-center text-text-secondary text-sm mt-6">
                        ¿No tienes cuenta?{' '}
                        <Link to="/register" className="text-accent hover:underline">
                            Regístrate
                        </Link>
                    </p>
                </div>
            </div>
        </div>
    )
}
