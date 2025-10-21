import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Settings, Sparkles, Upload, History, CheckCircle, User, LogIn } from 'lucide-react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import ThemeToggle from '../ui/ThemeToggle';
import { useAuth } from '../../hooks/useAuth';

const Header: React.FC = () => {
  const location = useLocation();
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  // // Check if user is authenticated
  // const isAuthenticated = !!localStorage.getItem('auth_token');
  // // const userData = localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user')!) : null;

  const navItems = [
    { path: '/', label: 'Home', icon: Sparkles },
    { path: '/upload', label: 'Upload', icon: Upload },
    { path: '/history', label: 'History', icon: History },
    { path: '/verify', label: 'Verify', icon: CheckCircle },
  ];

  const handleUserClick = () => {
    if (isAuthenticated) {
      navigate('/dashboard');
    } else {
      navigate('/auth');
    }
  };

  const mobileMenuVariants = {
    closed: {
      opacity: 0,
      scale: 0.8,
      y: -20,
      transition: {
        duration: 0.2,
        ease: "easeInOut" as const
      }
    },
    open: {
      opacity: 1,
      scale: 1,
      y: 0,
      transition: {
        duration: 0.3,
        ease: "easeOut" as const
      }
    }
  };

  const menuItemVariants = {
    closed: {
      x: -20,
      opacity: 0,
    },
    open: {
      x: 0,
      opacity: 1,
    }
  };

  return (
    <>
      {/* Desktop Header */}
      <motion.header
        initial={{ y: -50, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        className="hidden md:block sticky top-0 z-50"
      >
        <div className="container mx-auto px-4 py-3">
          <div className="flex items-center justify-between">
            {/* Left Side - GitHub Button */}
            <motion.div
              whileHover={{ scale: 1.05, y: -1 }}
              whileTap={{ scale: 0.95 }}
            >
              <Link
                to="/settings"
                className="p-3 rounded-xl bg-white/10  backdrop-blur-md hover:bg-white/20 text-cyan-400 hover:text-cyan-300 border border-cyan-500/40 hover:border-cyan-400/60 transition-all duration-300 shadow-lg flex items-center justify-center"
              >
                <Settings className="w-5 h-5" />
              </Link>
            </motion.div>

            {/* Centered Navigation Island */}
            <motion.nav 
              className="flex items-center gap-1 bg-white/70 dark:bg-black/50 backdrop-blur-md rounded-2xl border border-cyan-500/30 p-1 shadow-xl"
              whileHover={{ scale: 1.02 }}
              transition={{ type: "spring", stiffness: 300 }}
            >
              {navItems.map((item) => {
                const Icon = item.icon;
                const isActive = location.pathname === item.path;
                
                return (
                  <Link key={item.path} to={item.path}>
                    <motion.div
                      whileHover={{ scale: 1.05, y: -1 }}
                      whileTap={{ scale: 0.95 }}
                      className={`relative px-6 py-3 rounded-xl font-medium flex items-center  transition-all duration-300 overflow-hidden ${
                        isActive 
                          ? 'bg-cyan-500/20 text-cyan-800 ' 
                          : 'text-cyan-800 hover:text-cyan-400 hover:bg-white/5'
                      }`}
                    >
                      <Icon className="w-4 h-4" />
                      <span className="text-sm font-semibold">{item.label}</span>
                      
                      {/* Fixed Active indicator - contained within button */}
                      {isActive && (
                        <motion.div
                          layoutId="activeIndicator"
                          className="absolute inset-0 rounded-xl border border-cyan-400/60"
                          transition={{ type: "spring", stiffness: 300, damping: 30 }}
                        />
                      )}
                    </motion.div>
                  </Link>
                );
              })}
            </motion.nav>

            {/* Right Side - Theme Toggle & User */}
            <div className="flex items-center gap-2">
              <motion.div
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <ThemeToggle />
              </motion.div>
              
              {/* User Avatar - Shows different icon based on auth status */}
              <motion.button
                onClick={handleUserClick}
                whileHover={{ scale: 1.05, y: -1 }}
                whileTap={{ scale: 0.95 }}
                className="p-3 rounded-xl bg-white/10   hover:bg-white/20 text-cyan-400 hover:text-cyan-300 border border-cyan-500/40 hover:border-cyan-400/60 transition-all duration-300 backdrop-blur-md shadow-lg relative group"
                title={isAuthenticated ? 'Dashboard' : 'Sign In'}
              >
                {isAuthenticated ? (
                  <User className="w-5 h-5" />
                ) : (
                  <LogIn className="w-5 h-5" />
                )}
                
                {/* Tooltip */}
                <div className="absolute -bottom-10 left-1/2 transform -translate-x-1/2 bg-gray-900 text-white text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity duration-200 whitespace-nowrap">
                  {isAuthenticated ? 'Dashboard' : 'Sign In'}
                </div>
                
                {/* Online indicator for authenticated users */}
                {isAuthenticated && (
                  <div className="absolute -top-1 -right-1 w-3 h-3 bg-green-500 rounded-full border-2 border-white dark:border-gray-900"></div>
                )}
              </motion.button>
            </div>
          </div>
        </div>
      </motion.header>

      {/* Mobile Top HUD */}
      <motion.div
        initial={{ y: -50, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        className="md:hidden fixed top-0 left-0 right-0 z-50 bg-white/80 dark:bg-black/80 backdrop-blur-xl border-b border-cyan-500/20"
      >
        <div className="container mx-auto px-4 py-3">
          <div className="flex items-center justify-between">
            {/* Logo */}
            <Link to="/" className="flex items-center space-x-2">
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
                className="w-8 h-8 border border-cyan-500 backdrop-blur-md rounded-lg overflow-hidden flex items-center justify-center"
              >
                <img
                  src="/logo.png"
                  alt="Keginator Logo"
                  className="w-full h-full object-cover"
                />
              </motion.div>

              <span className="text-lg font-black bg-gradient-to-r from-cyan-700 to-purple-800 dark:from-cyan-400 dark:to-purple-400 bg-clip-text text-transparent">
                Keginator
              </span>
            </Link>

            {/* Right Side - GitHub, Theme, User */}
            <div className="flex items-center gap-1">
              <motion.div
                whileHover={{ scale: 1.05, y: -1 }}
                whileTap={{ scale: 0.95 }}
              >
                <Link
                  to="/settings"
                  className="p-3 rounded-xl bg-white/10 backdrop-blur-md hover:bg-white/20 text-cyan-400 hover:text-cyan-300 border border-cyan-500/40 hover:border-cyan-400/60 transition-all duration-300 shadow-lg flex items-center justify-center"
                >
                  <Settings className="w-5 h-5" />
                </Link>
              </motion.div>

              <motion.div
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                className="p-2 rounded-xl hover:bg-white/10 transition-all duration-300"
              >
                <ThemeToggle />
              </motion.div>

              <motion.button
                onClick={handleUserClick}
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                className="p-2 rounded-xl text-cyan-800 dark:text-cyan-400 backdrop-blur-xl hover:text-cyan-300 hover:bg-white/10 transition-all duration-300 relative"
                title={isAuthenticated ? 'Dashboard' : 'Sign In'}
              >
                {isAuthenticated ? (
                  <User className="w-4 h-4" />
                ) : (
                  <LogIn className="w-4 h-4" />
                )}
                
                {/* Online indicator for authenticated users */}
                {isAuthenticated && (
                  <div className="absolute -top-0.5 -right-0.5 w-2 h-2 bg-green-500 rounded-full border border-white dark:border-gray-900"></div>
                )}
              </motion.button>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Mobile Menu Overlay (for future use) */}
      <AnimatePresence>
        {isMobileMenuOpen && (
          <motion.div
            initial="closed"
            animate="open"
            exit="closed"
            variants={mobileMenuVariants}
            className="md:hidden fixed inset-0 z-40 pt-20 pb-24"
          >
            <div className="h-full bg-black/50 backdrop-blur-sm" onClick={() => setIsMobileMenuOpen(false)}>
              <div className="container mx-auto px-4 h-full flex items-center justify-center">
                <div className="bg-white/10 backdrop-blur-xl rounded-2xl border border-cyan-500/30 shadow-2xl p-6 w-full max-w-sm">
                  <div className="flex flex-col space-y-3">
                    {navItems.map((item, index) => {
                      const Icon = item.icon;
                      const isActive = location.pathname === item.path;
                      
                      return (
                        <motion.div
                          key={item.path}
                          initial="closed"
                          animate="open"
                          variants={menuItemVariants}
                          transition={{ delay: index * 0.1 }}
                        >
                          <Link 
                            to={item.path} 
                            onClick={() => setIsMobileMenuOpen(false)}
                          >
                            <motion.div
                              whileHover={{ x: 10, scale: 1.02 }}
                              whileTap={{ scale: 0.98 }}
                              className={`px-4 py-3 rounded-xl font-medium flex items-center space-x-3 transition-all duration-300 relative overflow-hidden ${
                                isActive 
                                  ? 'bg-cyan-500/20 text-cyan-400' 
                                  : 'text-cyan-200/90 hover:text-cyan-400 hover:bg-white/10'
                              }`}
                            >
                              {isActive && (
                                <div className="absolute inset-0 rounded-xl border border-cyan-400/60" />
                              )}
                              <Icon className="w-5 h-5 relative z-10" />
                              <span className="font-semibold relative z-10">{item.label}</span>
                            </motion.div>
                          </Link>
                        </motion.div>
                      );
                    })}
                    
                    {/* Auth button in mobile menu */}
                    <motion.div
                      initial="closed"
                      animate="open"
                      variants={menuItemVariants}
                      transition={{ delay: navItems.length * 0.1 }}
                    >
                      <motion.button
                        onClick={() => {
                          handleUserClick();
                          setIsMobileMenuOpen(false);
                        }}
                        whileHover={{ x: 10, scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                        className="w-full px-4 py-3 rounded-xl font-medium flex items-center space-x-3 transition-all duration-300 relative overflow-hidden bg-cyan-500/20 text-cyan-400 hover:bg-cyan-500/30"
                      >
                        {isAuthenticated ? (
                          <>
                            <User className="w-5 h-5 relative z-10" />
                            <span className="font-semibold relative z-10">Dashboard</span>
                          </>
                        ) : (
                          <>
                            <LogIn className="w-5 h-5 relative z-10" />
                            <span className="font-semibold relative z-10">Sign In</span>
                          </>
                        )}
                      </motion.button>
                    </motion.div>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
};

export default Header;