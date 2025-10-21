import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Mail, Lock, User,  ArrowRight, Shield, Zap } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { API_BASE_URL } from '../utils/constants';

// Define API URL constant
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const Auth: React.FC = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [newsletter, setNewsletter] = useState(false);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleGoogleSignIn = () => {
    setLoading(true);
    // Redirect to Google OAuth
    window.location.href = `${API_URL}/auth/google`;
  };

  useEffect(() => {
  const params = new URLSearchParams(window.location.search);
  const token = params.get('token');
  const error = params.get('error');
  
  if (token) {
    localStorage.setItem('auth_token', token);
    navigate('/dashboard');
  }
  
  if (error) {
    alert('Google OAuth failed. Please try again.');
  }
}, [navigate]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const endpoint = isLogin ? '/auth/login' : '/auth/signup';
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email,
          password,
          name: !isLogin ? name : undefined,
          newsletter: !isLogin ? newsletter : undefined,
        }),
      });

      const data = await response.json();

      if (data.success) {
        localStorage.setItem('auth_token', data.token);
        localStorage.setItem('user', JSON.stringify(data.user));
        navigate('/dashboard');
      } else {
        alert(data.message || 'Authentication failed');
      }
    } catch (error) {
      console.error('Auth error:', error);
      alert('Authentication failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };


  return (
    <div className="min-h-screen bg-white dark:bg-black text-black dark:text-white py-20 px-4">
      <div className="container mx-auto max-w-md">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-8"
        >
          <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-cyan-700 to-purple-700 dark:from-cyan-500 dark:to-purple-500 bg-clip-text text-transparent">
            {isLogin ? 'Welcome Back' : 'Get Started'}
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            {isLogin ? 'Sign in to your Keginator account' : 'Create your Keginator account'}
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="bg-white/80 dark:bg-black/40 backdrop-blur-sm rounded-2xl border border-gray-300/50 dark:border-gray-800/50 p-8 shadow-xl"
        >
        {/* Google Sign In */}
        <motion.button
        onClick={handleGoogleSignIn}
        disabled={loading}
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
        className="w-full py-3 px-4 bg-white dark:bg-gray-800 border-2 border-gray-300 dark:border-gray-700 rounded-lg font-semibold flex items-center justify-center space-x-3 hover:bg-gray-50 dark:hover:bg-gray-700 transition-all mb-6"
        >
        <img src="/G.png" alt="Google Logo" className="w-5 h-5" />
        <span>Continue with Google</span>
        </motion.button>


          <div className="relative mb-6">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-gray-300 dark:border-gray-700" />
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-4 bg-white dark:bg-black text-gray-500">Or continue with email</span>
            </div>
          </div>

          {/* Email/Password Form */}
          <form onSubmit={handleSubmit} className="space-y-4">
            <AnimatePresence mode="wait">
              {!isLogin && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                >
                  <label className="block text-sm font-medium mb-2">Full Name</label>
                  <div className="relative">
                    <User className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                    <input
                      type="text"
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                      required={!isLogin}
                      className="w-full pl-10 pr-4 py-3 bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent"
                      placeholder="John Doe"
                    />
                  </div>
                </motion.div>
              )}
            </AnimatePresence>

            <div>
              <label className="block text-sm font-medium mb-2">Email Address</label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  className="w-full pl-10 pr-4 py-3 bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent"
                  placeholder="you@example.com"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Password</label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  className="w-full pl-10 pr-4 py-3 bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent"
                  placeholder="••••••••"
                />
              </div>
            </div>

            <AnimatePresence mode="wait">
              {!isLogin && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                  className="flex items-center space-x-2"
                >
                  <input
                    type="checkbox"
                    id="newsletter"
                    checked={newsletter}
                    onChange={(e) => setNewsletter(e.target.checked)}
                    className="w-4 h-4 text-cyan-600 border-gray-300 rounded focus:ring-cyan-500"
                  />
                  <label htmlFor="newsletter" className="text-sm text-gray-600 dark:text-gray-400">
                    Subscribe to our newsletter for updates
                  </label>
                </motion.div>
              )}
            </AnimatePresence>

            <motion.button
              type="submit"
              disabled={loading}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="w-full py-3 px-4 bg-cyan-300 border-cyan-600 dark:bg-[#FFFFff] dark:text-[#000000] dark:border-blue-400  text-[#000000] shadow-lg rounded-lg font-bold flex items-center justify-center space-x-2 hover:bg-cyan-600 dark:hover:bg-cyan-700 transition-all disabled:opacity-50"
            >
              {loading ? (
                <motion.div
                  animate={{ rotate: 360 }}
                  transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
                  className="w-5 h-5 border-2 border-white border-t-transparent rounded-full"
                />
              ) : (
                <>
                  <span className="!text-[#000000]">{isLogin ? 'Sign In' : 'Create Account'}</span>
                  <ArrowRight className="w-5 h-5" />
                </>
              )}
            </motion.button>
          </form>

        <div className="mt-6 text-center">
  <button
    onClick={() => setIsLogin(!isLogin)}
    className="text-sm text-gray-700 dark:text-gray-300"
  >
    {isLogin ? (
      <>
        Don't have an account?{' '}
        <span className="text-purple-600 underline cursor-pointer">
          Sign up
        </span>
      </>
    ) : (
      <>
        Already have an account?{' '}
        <span className="text-purple-600 underline cursor-pointer">
          Sign in
        </span>
      </>
    )}
  </button>
</div>


          {!isLogin && (
            <div className="mt-6 p-4 bg-cyan-500/10 border border-cyan-500/30 rounded-lg">
              <div className="flex items-start space-x-3">
                <Shield className="w-5 h-5 text-cyan-600 dark:text-cyan-400 mt-0.5" />
                <div className="text-xs text-gray-600 dark:text-gray-400">
                  <p className="font-semibold mb-1">Why sign up?</p>
                  <ul className="space-y-1">
                    <li className="flex items-center space-x-1">
                      <Zap className="w-3 h-3" />
                      <span>Access premium features</span>
                    </li>
                    <li className="flex items-center space-x-1">
                      <Zap className="w-3 h-3" />
                      <span>Track dataset history</span>
                    </li>
                    <li className="flex items-center space-x-1">
                      <Zap className="w-3 h-3" />
                      <span>Get blockchain verification</span>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          )}
        </motion.div>
      </div>
    </div>
  );
};

export default Auth;