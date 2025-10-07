import React from 'react';
import { Moon, Sun } from 'lucide-react';
import { useTheme } from '../../hooks/useTheme';
import { motion } from 'framer-motion';

const ThemeToggle: React.FC = () => {
  const { theme, toggleTheme } = useTheme();

  return (
    <motion.button
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      onClick={toggleTheme}
      className="relative p-3 rounded-xl bg-gradient-to-br from-cyan-500/20 to-purple-500/20 text-cyan-400 hover:text-cyan-300 border border-cyan-500/30 hover:border-cyan-400/50 transition-all duration-300 group"
      aria-label="Toggle theme"
    >
      <motion.div
        initial={false}
        animate={{ 
          rotate: theme === 'dark' ? 180 : 0,
          scale: theme === 'dark' ? 1.1 : 1
        }}
        transition={{ duration: 0.4, type: "spring", stiffness: 200 }}
        className="relative z-10"
      >
        {theme === 'dark' ? (
          <Sun className="w-5 h-5" />
        ) : (
          <Moon className="w-5 h-5" />
        )}
      </motion.div>
      
      {/* Animated background gradient */}
      <motion.div
        className="absolute inset-0 rounded-xl bg-gradient-to-r from-cyan-500 to-purple-500 opacity-0 group-hover:opacity-10"
        animate={{ 
          opacity: theme === 'dark' ? 0.1 : 0,
          rotate: theme === 'dark' ? 180 : 0 
        }}
        transition={{ duration: 0.5 }}
      />
      
      {/* Pulsing glow effect */}
      <motion.div
        className="absolute inset-0 rounded-xl bg-cyan-400/20"
        animate={{
          opacity: theme === 'dark' ? [0.3, 0.1, 0.3] : 0,
          scale: theme === 'dark' ? [1, 1.1, 1] : 1
        }}
        transition={{
          duration: 2,
          repeat: Infinity,
          repeatType: "reverse"
        }}
      />
    </motion.button>
  );
};

export default ThemeToggle;