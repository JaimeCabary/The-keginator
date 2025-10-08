import React, { useState, useEffect, useCallback } from 'react';
import { motion } from 'framer-motion';
import { 
  User, Mail, Calendar, Shield, Zap, Database, 
  TrendingUp, LogOut, CreditCard, Award, Activity 
} from 'lucide-react';
import { useNavigate, Link } from 'react-router-dom';
import { API_BASE_URL } from '../utils/constants';

// Define API URL constant
// const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

interface UserData {
  id: string;
  name: string;
  email: string;
  plan: 'free' | 'professional' | 'enterprise';
  joined_date: string;
  datasets_processed: number;
  total_storage_used: number;
  newsletter_subscribed: boolean;
}

const Dashboard: React.FC = () => {
  const [userData, setUserData] = useState<UserData | null>(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  const fetchUserData = useCallback(async () => {
    try {
      const token = localStorage.getItem('auth_token');
      if (!token) {
        navigate('/auth');
        return;
      }

      const response = await fetch(`${API_BASE_URL}/auth/me`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      const data = await response.json();
      if (data.success) {
        setUserData(data.user);
      } else {
        navigate('/auth');
      }
    } catch (error) {
      console.error('Failed to fetch user data:', error);
      navigate('/auth');
    } finally {
      setLoading(false);
    }
  }, [navigate]);

  useEffect(() => {
    fetchUserData();
  }, [fetchUserData]);

  const handleLogout = () => {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user');
    navigate('/');
  };

  const handleUpgrade = (plan: string) => {
    navigate(`/pricing?plan=${plan}`);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-white dark:bg-black flex items-center justify-center">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
          className="w-12 h-12 border-4 border-cyan-500 border-t-transparent rounded-full"
        />
      </div>
    );
  }

  if (!userData) return null;

  const planColors = {
    free: 'bg-gray-500',
    professional: 'bg-blue-500',
    enterprise: 'bg-purple-500',
  };

  const planLimits = {
    free: { storage: '1 GB', processing: '10 datasets/month' },
    professional: { storage: '100 GB', processing: '1000 datasets/month' },
    enterprise: { storage: 'Unlimited', processing: 'Unlimited' },
  };



  return (
    <div className="min-h-screen bg-white dark:bg-black text-black dark:text-white py-20 px-4">
      <div className="container mx-auto max-w-6xl">
        {/* Header */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <h1 className="text-4xl font-bold mb-2">Welcome back, {userData.name}!</h1>
            <p className="text-gray-600 dark:text-gray-400">Manage your Keginator account</p>
          </motion.div>

          <motion.button
            onClick={handleLogout}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="mt-4 md:mt-0 px-6 py-2 border border-red-500 text-red-500 rounded-lg hover:bg-red-500/10 flex items-center space-x-2"
          >
            <LogOut className="w-4 h-4" />
            <span>Logout</span>
          </motion.button>
        </div>

        {/* Stats Grid */}
        <div className="grid md:grid-cols-4 gap-6 mb-8">
          {[
            { label: 'Current Plan', value: userData.plan.toUpperCase(), icon: Award, color: 'text-purple-500' },
            { label: 'Datasets Processed', value: userData.datasets_processed, icon: Database, color: 'text-blue-500' },
            { label: 'Storage Used', value: `${userData.total_storage_used} MB`, icon: Activity, color: 'text-green-500' },
            { label: 'Member Since', value: new Date(userData.joined_date).toLocaleDateString('en-US', { month: 'short', year: 'numeric' }), icon: Calendar, color: 'text-cyan-500' },
          ].map((stat, index) => (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="p-6 bg-white/80 dark:bg-black/40 backdrop-blur-sm rounded-xl border border-gray-300/50 dark:border-gray-800/50 shadow-lg"
            >
              <stat.icon className={`w-8 h-8 ${stat.color} mb-3`} />
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">{stat.label}</p>
              <p className="text-2xl font-bold">{stat.value}</p>
            </motion.div>
          ))}
        </div>

        {/* Account Details */}
        <div className="grid md:grid-cols-2 gap-6 mb-8">
          {/* Profile Info */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="p-6 bg-white/80 dark:bg-black/40 backdrop-blur-sm rounded-xl border border-gray-300/50 dark:border-gray-800/50 shadow-lg"
          >
            <h2 className="text-2xl font-bold mb-6 flex items-center space-x-2">
              <User className="w-6 h-6 text-cyan-500" />
              <span>Profile Information</span>
            </h2>

            <div className="space-y-4">
              <div>
                <label className="text-sm text-gray-600 dark:text-gray-400">Full Name</label>
                <p className="text-lg font-semibold">{userData.name}</p>
              </div>

              <div>
                <label className="text-sm text-gray-600 dark:text-gray-400">Email Address</label>
                <p className="text-lg font-semibold flex items-center space-x-2">
                  <Mail className="w-4 h-4 text-gray-400" />
                  <span>{userData.email}</span>
                </p>
              </div>

              <div>
                <label className="text-sm text-gray-600 dark:text-gray-400">User ID</label>
                <p className="text-sm font-mono text-gray-600 dark:text-gray-400">{userData.id}</p>
              </div>

              <div className="flex items-center space-x-2 pt-2">
                <input
                  type="checkbox"
                  checked={userData.newsletter_subscribed}
                  readOnly
                  className="w-4 h-4"
                />
                <span className="text-sm">Subscribed to newsletter</span>
              </div>
            </div>
          </motion.div>

          {/* Current Plan */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="p-6 bg-white/80 dark:bg-black/40 backdrop-blur-sm rounded-xl border border-gray-300/50 dark:border-gray-800/50 shadow-lg"
          >
            <h2 className="text-2xl font-bold mb-6 flex items-center space-x-2">
              <Shield className="w-6 h-6 text-purple-500" />
              <span>Subscription Plan</span>
            </h2>

            <div className={`inline-block px-4 py-2 ${planColors[userData.plan]} text-white rounded-full font-bold mb-4`}>
              {userData.plan.toUpperCase()} PLAN
            </div>

            <div className="space-y-3 mb-6">
              <div className="flex justify-between items-center">
                <span className="text-gray-600 dark:text-gray-400">Storage Limit</span>
                <span className="font-semibold">{planLimits[userData.plan].storage}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600 dark:text-gray-400">Processing Limit</span>
                <span className="font-semibold">{planLimits[userData.plan].processing}</span>
              </div>
            </div>

            {userData.plan !== 'enterprise' && (
              <motion.button
                onClick={() => handleUpgrade(userData.plan === 'free' ? 'professional' : 'enterprise')}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="w-full py-3 bg-gradient-to-r from-cyan-500 to-purple-500 text-white rounded-lg font-bold flex items-center justify-center space-x-2"
              >
                <TrendingUp className="w-5 h-5" />
                <span>Upgrade Plan</span>
              </motion.button>
            )}
          </motion.div>
        </div>

        {/* Quick Actions */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="p-6 bg-white/80 dark:bg-black/40 backdrop-blur-sm rounded-xl border border-gray-300/50 dark:border-gray-800/50 shadow-lg"
        >
          <h2 className="text-2xl font-bold mb-6 flex items-center space-x-2">
            <Zap className="w-6 h-6 text-yellow-500" />
            <span>Quick Actions</span>
          </h2>

          <div className="grid md:grid-cols-3 gap-4">
            <Link to="/upload">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="w-full py-4 px-6 bg-cyan-500 dark:bg-cyan-600 text-white rounded-lg font-semibold hover:bg-cyan-600 dark:hover:bg-cyan-700"
              >
                Upload Dataset
              </motion.button>
            </Link>

            <Link to="/history">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="w-full py-4 px-6 border-2 border-cyan-500 text-cyan-500 rounded-lg font-semibold hover:bg-cyan-500/10"
              >
                View History
              </motion.button>
            </Link>

            <Link to="/verify">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="w-full py-4 px-6 border-2 border-purple-500 text-purple-500 rounded-lg font-semibold hover:bg-purple-500/10"
              >
                Verify Data
              </motion.button>
            </Link>
          </div>
        </motion.div>

        {/* Billing Section */}
        {userData.plan !== 'free' && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="mt-6 p-6 bg-white/80 dark:bg-black/40 backdrop-blur-sm rounded-xl border border-gray-300/50 dark:border-gray-800/50 shadow-lg"
          >
            <h2 className="text-2xl font-bold mb-6 flex items-center space-x-2">
              <CreditCard className="w-6 h-6 text-green-500" />
              <span>Billing & Payments</span>
            </h2>

            <div className="flex justify-between items-center">
              <div>
                <p className="text-gray-600 dark:text-gray-400 mb-1">Next billing date</p>
                <p className="text-lg font-semibold">
                  {new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toLocaleDateString('en-US', { 
                    month: 'long', 
                    day: 'numeric', 
                    year: 'numeric' 
                  })}
                </p>
              </div>

              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="px-6 py-2 border border-gray-300 dark:border-gray-700 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800"
              >
                Manage Billing
              </motion.button>
            </div>
          </motion.div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;