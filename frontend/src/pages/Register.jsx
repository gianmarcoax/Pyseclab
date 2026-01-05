import { useState, useContext } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { AuthContext } from '../App'
import { register as registerService } from '../services/auth'

export default function Register() {
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        password_confirm: '',
        generate_keys: true,
        key_size: 2048
    })
    const [error, setError] = useState('')
    const [loading, setLoading] = useState(false)
    const navigate = useNavigate()

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target
        setFormData(prev => ({
            ...prev,
            [name]: type === 'checkbox' ? checked : value
        }))
    }

    const handleSubmit = async (e) => {
        e.preventDefault()
        setError('')
        setLoading(true)

        try {
            await registerService(formData)
            navigate('/login')
        } catch (err) {
            const errors = err.response?.data
            if (errors) {
                const firstError = Object.values(errors)[0]
                setError(Array.isArray(firstError) ? firstError[0] : firstError)
            } else {
                setError('Error al registrar')
            }
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
                    <p className="text-text-secondary text-sm mt-1">Crea tu cuenta</p>
                </div>

                {/* Form Card */}
                <div className="card p-8">
                    <h2 className="text-xl font-semibold text-text-primary mb-6">Registro</h2>

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
                                name="username"
                                value={formData.username}
                                onChange={handleChange}
                                className="input-field w-full"
                                required
                            />
                        </div>

                        <div>
                            <label className="block text-text-secondary text-sm mb-2">Email</label>
                            <input
                                type="email"
                                name="email"
                                value={formData.email}
                                onChange={handleChange}
                                className="input-field w-full"
                            />
                        </div>

                        <div>
                            <label className="block text-text-secondary text-sm mb-2">Contraseña (mín. 12 caracteres)</label>
                            <input
                                type="password"
                                name="password"
                                value={formData.password}
                                onChange={handleChange}
                                className="input-field w-full"
                                minLength={12}
                                required
                            />
                        </div>

                        <div>
                            <label className="block text-text-secondary text-sm mb-2">Confirmar Contraseña</label>
                            <input
                                type="password"
                                name="password_confirm"
                                value={formData.password_confirm}
                                onChange={handleChange}
                                className="input-field w-full"
                                required
                            />
                        </div>

                        <div className="bg-wa-chat p-4 rounded-lg border border-wa-border">
                            <label className="flex items-center gap-3 text-text-primary cursor-pointer">
                                <input
                                    type="checkbox"
                                    name="generate_keys"
                                    checked={formData.generate_keys}
                                    onChange={handleChange}
                                    className="w-4 h-4 accent-accent"
                                />
                                <span className="text-sm">Generar par de claves RSA</span>
                            </label>

                            {formData.generate_keys && (
                                <div className="mt-3">
                                    <label className="block text-text-secondary text-xs mb-1">Tamaño de clave</label>
                                    <select
                                        name="key_size"
                                        value={formData.key_size}
                                        onChange={handleChange}
                                        className="input-field w-full text-sm"
                                    >
                                        <option value={2048}>RSA-2048 (Recomendado)</option>
                                        <option value={3072}>RSA-3072</option>
                                        <option value={4096}>RSA-4096</option>
                                    </select>
                                </div>
                            )}
                        </div>

                        <button
                            type="submit"
                            disabled={loading}
                            className="btn-primary w-full py-3 rounded-lg font-medium disabled:opacity-50"
                        >
                            {loading ? 'Registrando...' : 'Crear Cuenta'}
                        </button>
                    </form>

                    <p className="text-center text-text-secondary text-sm mt-6">
                        ¿Ya tienes cuenta?{' '}
                        <Link to="/login" className="text-accent hover:underline">
                            Inicia sesión
                        </Link>
                    </p>
                </div>
            </div>
        </div>
    )
}
