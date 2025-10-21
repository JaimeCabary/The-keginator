import React from 'react';
import { motion } from 'framer-motion';
import { Sun, Moon, Shield, LogOut, Bell, UserCog, ArrowLeft } from 'lucide-react';
import { useTheme } from '../hooks/useTheme';
import { useAuth } from '../hooks/useAuth';
import { useNavigate } from 'react-router-dom';

const Settings: React.FC = () => {
  const { theme, toggleTheme } = useTheme();
  const { isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

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
    ...(isAuthenticated
      ? [
          {
            icon: LogOut,
            label: 'Logout',
            onClick: logout,
          },
        ]
      : []),
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 20 }}
      transition={{ duration: 0.25 }}
      className="fixed inset-0 z-[999] flex flex-col bg-white dark:bg-black text-black dark:text-white"
    >
      {/* Back button */}
      <div className="absolute top-4 left-4 z-50">
        <button
          onClick={() => navigate(-1)}
          className="flex items-center space-x-2 px-4 py-2 rounded-full bg-cyan-500/10 hover:bg-cyan-500/20 border border-cyan-500/30 dark:border-cyan-500/40 transition-all"
        >
          <ArrowLeft className="w-5 h-5 text-cyan-600 dark:text-cyan-300" />
          <span className="font-medium text-cyan-700 dark:text-cyan-300">Back</span>
        </button>
      </div>

      {/* Main content */}
      <div className="flex-1 flex flex-col items-center px-4 pt-[100px] sm:pt-24 pb-10 overflow-y-auto">
        <motion.h1
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-3xl font-black text-center mb-10 bg-gradient-to-r from-cyan-600 to-purple-600 bg-clip-text text-transparent"
        >
          Settings
        </motion.h1>

        <div className="w-full max-w-lg space-y-4">
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
    </motion.div>
  );
};

export default Settings;
