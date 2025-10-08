import React from 'react';
import { motion } from 'framer-motion';
import { Github, Twitter, Mail, Heart, Cpu, Shield, LogOut } from 'lucide-react';
import { useNavigate,  } from 'react-router-dom';

const Info: React.FC = () => {
  const currentYear = new Date().getFullYear();
  const navigate = useNavigate();
    const handleLogout = () => {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user');
    navigate('/');
  };

  return (
    <div className="min-h-screen bg-white dark:bg-black text-black dark:text-white pb-32 pt-8"> 
      <div className="container mx-auto px-4">
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
              { icon: Mail, href: 'mailto:hello@keginator.com', label: 'Email' }
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
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="mb-12"
        >
          <h3 className="font-bold text-red-700 dark:text-red-400 text-xl mb-6 flex items-center justify-center space-x-2">
            <LogOut className="w-6 h-6" />
            <span>LOGOUT</span>
          </h3>
          <div className="grid grid-cols-2 gap-3 max-w-md mx-auto">
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
        </motion.div>

        {/* Bottom Text */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="border-t border-cyan-500/20 pt-8 text-center space-y-4"
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
    </div>
  );
};

export default Info;