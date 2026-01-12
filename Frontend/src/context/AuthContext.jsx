import { createContext, useContext, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        // Check if user is logged in
        const token = localStorage.getItem('access_token');
        const userEmail = localStorage.getItem('user_email');
        if (token) {
            try {
                // Decode the JWT to get user info (the token contains the sub which is the user_id)
                const decoded = JSON.parse(atob(token.split('.')[1]));
                setUser({ isAuthenticated: true, id: decoded.sub, email: userEmail });
            } catch (error) {
                // If decode fails, just mark as authenticated
                setUser({ isAuthenticated: true });
            }
        }
        setLoading(false);
    }, []);

    const login = async (email, password) => {
        const response = await api.post('/auth/login', { username: email, password });
        const { access_token, refresh_token } = response.data;

        localStorage.setItem('access_token', access_token);
        localStorage.setItem('refresh_token', refresh_token);
        localStorage.setItem('user_email', email);

        // Decode the JWT to get user info (the token contains the sub which is the user_id)
        const decoded = JSON.parse(atob(access_token.split('.')[1]));
        setUser({ isAuthenticated: true, id: decoded.sub, email: email });
        return response.data;
    };

    const signup = async (name, email, password) => {
        const response = await api.post('/auth/signup', { name, email, password });
        return response.data;
    };

    const logout = () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        setUser(null);
        navigate('/login', { replace: true });
    };

    const value = {
        user,
        login,
        signup,
        logout,
        loading
    };

    return (
        <AuthContext.Provider value={value}>
            {!loading && children}
        </AuthContext.Provider>
    );
};
