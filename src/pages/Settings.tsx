import React from 'react';
import { motion } from 'framer-motion';
import { Sun, Moon, Shield, LogOut, Bell, UserCog } from 'lucide-react';
import { useTheme } from '../hooks/useTheme';
import { useNavigate } from 'react-router-dom';

const Settings: React.FC = () => {
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user');
    navigate('/');
  };

  const settingsOptions = [
    {
      icon: theme === 'light' ? Moon : Sun,
      label: theme === 'light' ? 'Enable Dark Mode' : 'Enable Light Mode',
      onClick: toggleTheme,
    },
    {
      icon: Bell,
      label: 'Notifications',
      onClick: () => alert('Notification settings coming soon.'),
    },
    {
      icon: UserCog,
      label: 'Account',
      onClick: () => alert('Account settings coming soon.'),
    },
    {
      icon: Shield,
      label: 'Privacy & Security',
      onClick: () => alert('Privacy options coming soon.'),
    },
    {
      icon: LogOut,
      label: 'Logout',
      onClick: handleLogout,
    },
  ];

  return (
    <div className="min-h-screen bg-white dark:bg-black text-black dark:text-white pb-20 pt-12">
      <div className="container mx-auto px-4">
        <motion.h1
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-3xl font-black text-center mb-10 bg-gradient-to-r from-cyan-600 to-purple-600 bg-clip-text text-transparent"
        >
          Settings
        </motion.h1>

        <div className="max-w-lg mx-auto space-y-4">
          {settingsOptions.map((item, index) => (
            <motion.button
              key={index}
              onClick={item.onClick}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.97 }}
              className="w-full flex items-center justify-between px-5 py-4 rounded-xl border border-cyan-500/30 dark:border-cyan-500/20 hover:bg-cyan-500/10 dark:hover:bg-cyan-500/20 transition-all duration-200"
            >
              <div className="flex items-center space-x-4">
                <item.icon className="w-6 h-6 text-cyan-600 dark:text-cyan-300" />
                <span className="font-medium">{item.label}</span>
              </div>
              <motion.span
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="text-sm text-cyan-700 dark:text-cyan-400"
              >
                {item.label === 'Logout' ? '→' : ''}
              </motion.span>
            </motion.button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Settings;
