// import { useState, useEffect, useCallback } from 'react';
// import { useNavigate } from 'react-router-dom';

// interface User {
//   id: string;
//   name: string;
//   email: string;
//   plan: 'free' | 'professional' | 'enterprise';
//   joined_date: string;
//   datasets_processed: number;
//   total_storage_used: number;
//   newsletter_subscribed: boolean;
// }

// interface AuthState {
//   isAuthenticated: boolean;
//   user: User | null;
//   logout: () => void;
//   refreshUser: () => Promise<void>;
// }

// export const useAuth = (): AuthState => {
//   const [isAuthenticated, setIsAuthenticated] = useState(!!localStorage.getItem('auth_token'));
//   const [user, setUser] = useState<User | null>(null);
//   const navigate = useNavigate();

//   const refreshUser = useCallback(async () => {
//     const token = localStorage.getItem('auth_token');
//     if (!token) {
//       setIsAuthenticated(false);
//       setUser(null);
//       return;
//     }

//     try {
//       const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/auth/me`, {
//         headers: { Authorization: `Bearer ${token}` },
//       });
//       const data = await response.json();
//       if (data.success) {
//         setUser(data.user);
//         setIsAuthenticated(true);
//         localStorage.setItem('user', JSON.stringify(data.user));
//       } else {
//         setIsAuthenticated(false);
//         setUser(null);
//         localStorage.removeItem('auth_token');
//         localStorage.removeItem('user');
//       }
//     } catch (error) {
//       console.error('Failed to fetch user:', error);
//       setIsAuthenticated(false);
//       setUser(null);
//       localStorage.removeItem('auth_token');
//       localStorage.removeItem('user');
//     }
//   }, []);

//   useEffect(() => {
//     refreshUser();
//   }, [refreshUser]);

//   const logout = () => {
//     localStorage.removeItem('auth_token');
//     localStorage.removeItem('user');
//     setIsAuthenticated(false);
//     setUser(null);
//     navigate('/');
//   };

//   return { isAuthenticated, user, logout, refreshUser };
// };

// useAuth.ts - FIXED VERSION

import { useState, useEffect, useCallback } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

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
  loading: boolean;
}

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const useAuth = (): AuthState => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const location = useLocation();

  const refreshUser = useCallback(async () => {
    console.log('🔄 Refreshing user...');
    const token = localStorage.getItem('auth_token');
    
    if (!token) {
      console.log('❌ No token found');
      setIsAuthenticated(false);
      setUser(null);
      setLoading(false);
      return;
    }

    try {
      console.log('📡 Fetching user info with token:', token.substring(0, 20) + '...');
      
      const response = await fetch(`${API_URL}/auth/me`, {
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
      });

      console.log('📥 Response status:', response.status);

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const data = await response.json();
      console.log('✅ User data received:', data);

      if (data.success && data.user) {
        setUser(data.user);
        setIsAuthenticated(true);
        localStorage.setItem('user', JSON.stringify(data.user));
        console.log('✅ User authenticated:', data.user.email);
      } else {
        throw new Error('Invalid response format');
      }
    } catch (error) {
      console.error('❌ Failed to fetch user:', error);
      setIsAuthenticated(false);
      setUser(null);
      localStorage.removeItem('auth_token');
      localStorage.removeItem('user');
    } finally {
      setLoading(false);
    }
  }, []);

  // Handle token from URL (OAuth callback)
  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const tokenFromUrl = params.get('token');
    
    if (tokenFromUrl) {
      console.log('🔑 Token found in URL, storing...');
      localStorage.setItem('auth_token', tokenFromUrl);
      
      // Clean URL
      window.history.replaceState({}, document.title, location.pathname);
      
      // Trigger refresh
      refreshUser();
    }
  }, [location, refreshUser]);

  // Initial load
  useEffect(() => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      console.log('🔑 Token found in localStorage, refreshing user...');
      refreshUser();
    } else {
      console.log('ℹ️ No token in localStorage');
      setLoading(false);
    }
  }, []);

  const logout = () => {
    console.log('👋 Logging out...');
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user');
    setIsAuthenticated(false);
    setUser(null);
    navigate('/');
  };

  return { isAuthenticated, user, logout, refreshUser, loading };
};