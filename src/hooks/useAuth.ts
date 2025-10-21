import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';

interface User {
  id: string;
  name: string;
  email: string;
  plan: 'free' | 'professional' | 'enterprise';
  joined_date: string;
  datasets_processed: number;
  total_storage_used: number;
  newsletter_subscribed: boolean;
}

interface AuthState {
  isAuthenticated: boolean;
  user: User | null;
  logout: () => void;
  refreshUser: () => Promise<void>;
}

export const useAuth = (): AuthState => {
  const [isAuthenticated, setIsAuthenticated] = useState(!!localStorage.getItem('auth_token'));
  const [user, setUser] = useState<User | null>(null);
  const navigate = useNavigate();

  const refreshUser = useCallback(async () => {
    const token = localStorage.getItem('auth_token');
    if (!token) {
      setIsAuthenticated(false);
      setUser(null);
      return;
    }

    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/auth/me`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const data = await response.json();
      if (data.success) {
        setUser(data.user);
        setIsAuthenticated(true);
        localStorage.setItem('user', JSON.stringify(data.user));
      } else {
        setIsAuthenticated(false);
        setUser(null);
        localStorage.removeItem('auth_token');
        localStorage.removeItem('user');
      }
    } catch (error) {
      console.error('Failed to fetch user:', error);
      setIsAuthenticated(false);
      setUser(null);
      localStorage.removeItem('auth_token');
      localStorage.removeItem('user');
    }
  }, []);

  useEffect(() => {
    refreshUser();
  }, [refreshUser]);

  const logout = () => {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user');
    setIsAuthenticated(false);
    setUser(null);
    navigate('/');
  };

  return { isAuthenticated, user, logout, refreshUser };
};