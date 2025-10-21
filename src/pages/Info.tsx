import React from 'react';
import { motion } from 'framer-motion';
import { Github, Twitter, Mail, Heart, Cpu, Shield, LogOut, ArrowLeft } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

const Info: React.FC = () => {
  const { isAuthenticated, logout } = useAuth();
  const currentYear = new Date().getFullYear();
  const navigate = useNavigate();

  return (
    <motion.div
      initial={{ y: '100%' }}
      animate={{ y: 0 }}
      exit={{ y: '100%' }}
      transition={{ duration: 0.3, ease: 'easeInOut' }}
      className="fixed inset-0 z-[999] bg-white dark:bg-black text-black dark:text-white overflow-y-auto flex flex-col"
    >
      {/* Back Button */}
      <div className="absolute top-4 left-4 z-50">
        <button
          onClick={() => navigate(-1)}
          className="flex items-center space-x-2 px-4 py-2 rounded-full bg-cyan-500/10 hover:bg-cyan-500/20 border border-cyan-500/30 dark:border-cyan-500/40 transition-all"
        >
          <ArrowLeft className="w-5 h-5 text-cyan-600 dark:text-cyan-300" />
          <span className="font-medium text-cyan-700 dark:text-cyan-300">Back</span>
        </button>
      </div>

      {/* Main Content */}
      <div className="flex-1 container mx-auto px-4 pt-20 pb-32 sm:pt-24">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl font-black bg-gradient-to-r from-cyan-700 to-purple-700 dark:from-cyan-500 dark:to-purple-500 bg-clip-text text-transparent mb-4">
            About Keginator
          </h1>
          <p className="text-cyan-900 dark:text-cyan-200 text-lg">
            Built for the Solana Cypherpunk Hackathon
          </p>
        </motion.div>

        {/* Brand Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="mb-12"
        >
          <div className="flex items-center space-x-3 mb-6 justify-center">
            <div className="w-16 h-16 rounded-xl overflow-hidden flex items-center justify-center">
              <img src="/logo.png" alt="Logo" className="w-full h-full object-cover" />
            </div>
            <span className="text-3xl font-black bg-gradient-to-r from-cyan-700 to-purple-700 dark:from-cyan-500 dark:to-purple-500 bg-clip-text text-transparent">
              KEGINATOR
            </span>
          </div>
          <p className="text-cyan-900 dark:text-cyan-200 text-center max-w-2xl mx-auto text-lg leading-relaxed mb-8">
            Revolutionizing data integrity with Solana blockchain verification. 
            Built for the future of trusted data processing.
          </p>

          {/* Social Links */}
          <div className="flex justify-center space-x-4">
            {[
              { icon: Github, href: 'https://github.com', label: 'GitHub' },
              { icon: Twitter, href: 'https://twitter.com', label: 'Twitter' },
              { icon: Mail, href: 'mailto:hello@keginator.com', label: 'Email' },
            ].map((social) => (
              <motion.a
                key={social.label}
                href={social.href}
                whileHover={{ scale: 1.2, y: -2 }}
                whileTap={{ scale: 0.9 }}
                className="p-4 bg-cyan-500/20 rounded-xl text-cyan-800 hover:text-cyan-700 hover:bg-cyan-800/30 dark:text-cyan-400 dark:hover:text-cyan-300 dark:hover:bg-cyan-500/30 border border-cyan-500/30 transition-all duration-300"
                aria-label={social.label}
              >
                <social.icon className="w-6 h-6" />
              </motion.a>
            ))}
          </div>
        </motion.div>

        {/* Product Links */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mb-12"
        >
          <h3 className="font-bold text-cyan-700 text-xl mb-6 flex items-center justify-center space-x-2">
            <Shield className="w-6 h-6" />
            <span>PRODUCT</span>
          </h3>
          <div className="grid grid-cols-2 gap-3 max-w-md mx-auto">
            {['Data Cleaning', 'Blockchain Proof', 'Verification', 'API Access'].map((item) => (
              <motion.a
                key={item}
                href="https://zeptaherself.netlify.app"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="p-4 bg-cyan-500/10 border border-cyan-500/30 rounded-xl text-cyan-800 dark:text-cyan-200 hover:bg-cyan-500/20 transition-all duration-300 text-center font-medium"
              >
                {item}
              </motion.a>
            ))}
          </div>
        </motion.div>

        {/* Company Links */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="mb-12"
        >
          <h3 className="font-bold text-purple-700 dark:text-purple-400 text-xl mb-6 flex items-center justify-center space-x-2">
            <Cpu className="w-6 h-6" />
            <span>COMPANY</span>
          </h3>
          <div className="grid grid-cols-2 gap-3 max-w-md mx-auto">
            {['About', 'Documentation', 'Careers', 'Contact'].map((item) => (
              <motion.a
                key={item}
                href="https://zeptaherself.netlify.app"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="p-4 bg-purple-500/10 border border-purple-500/30 rounded-xl text-purple-800 dark:text-purple-300 hover:bg-purple-500/20 transition-all duration-300 text-center font-medium"
              >
                {item}
              </motion.a>
            ))}
          </div>
        </motion.div>

        {isAuthenticated && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.35 }}
            className="mb-12"
          >
            <h3 className="font-bold text-red-700 dark:text-red-400 text-xl mb-6 flex items-center justify-center space-x-2">
              <LogOut className="w-6 h-6" />
              <span>LOGOUT</span>
            </h3>
            <div className="grid grid-cols-2 gap-3 max-w-md mx-auto">
              <motion.button
                onClick={logout}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="p-4 bg-red-500/10 border border-red-500/30 rounded-xl text-red-800 dark:text-red-300 hover:bg-red-500/20 transition-all duration-300 text-center font-medium"
              >
                Logout
              </motion.button>
            </div>
          </motion.div>
        )}

        {/* Footer */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="border-t border-cyan-500/20 pt-8 text-center space-y-4 mb-10"
        >
          <p className="text-cyan-800 dark:text-cyan-300 flex items-center justify-center text-sm">
            <span className="flex items-center">
              Built with <Heart className="w-4 h-4 text-red-400 mx-2" /> for the Solana Cypherpunk Hackathon
            </span>
          </p>
          <p className="text-cyan-900 dark:text-cyan-200 text-sm">
            © {currentYear} Keginator. All systems operational.
          </p>
        </motion.div>
      </div>
    </motion.div>
  );
};

export default Info;
