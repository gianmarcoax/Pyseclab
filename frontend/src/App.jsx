import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { useState, useEffect, createContext } from 'react'
import Layout from './components/Layout'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import CryptoDemo from './pages/CryptoDemo'
import SendMessage from './pages/SendMessage'
import Messages from './pages/Messages'
import { getToken, removeToken } from './services/auth'

export const AuthContext = createContext(null)

function App() {
    const [user, setUser] = useState(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        const token = getToken()
        if (token) {
            // Decode JWT to get user info
            try {
                const payload = JSON.parse(atob(token.split('.')[1]))
                setUser({ username: payload.username })
            } catch {
                removeToken()
            }
        }
        setLoading(false)
    }, [])

    const login = (userData, token) => {
        localStorage.setItem('token', token)
        setUser(userData)
    }

    const logout = () => {
        removeToken()
        setUser(null)
    }

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="animate-spin w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full"></div>
            </div>
        )
    }

    return (
        <AuthContext.Provider value={{ user, login, logout }}>
            <BrowserRouter>
                <Routes>
                    <Route path="/login" element={user ? <Navigate to="/" /> : <Login />} />
                    <Route path="/register" element={user ? <Navigate to="/" /> : <Register />} />
                    <Route path="/" element={user ? <Layout /> : <Navigate to="/login" />}>
                        <Route index element={<Dashboard />} />
                        <Route path="demo" element={<CryptoDemo />} />
                        <Route path="send" element={<SendMessage />} />
                        <Route path="messages" element={<Messages />} />
                    </Route>
                </Routes>
            </BrowserRouter>
        </AuthContext.Provider>
    )
}

export default App
