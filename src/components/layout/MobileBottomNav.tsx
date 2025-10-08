import React from 'react';
import { motion } from 'framer-motion';
import { Link, useLocation } from 'react-router-dom';
import { Sparkles, Upload, History, CheckCircle, Info } from 'lucide-react';

const MobileBottomNav: React.FC = () => {
  const location = useLocation();

  const navItems = [
    { path: '/', label: 'Home', icon: Sparkles },
    { path: '/upload', label: 'Upload', icon: Upload },
    { path: '/history', label: 'History', icon: History },
    { path: '/verify', label: 'Verify', icon: CheckCircle },
    { path: '/info', label: 'More', icon: Info },
  ];

  return (
    <motion.nav
      initial={{ y: 50, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ delay: 0.1 }}
      className="md:hidden fixed bottom-0 backdrop-blur-xl left-0 right-0 z-50"
    >
      <div className="container mx-auto px-4 pb-3">
        <div className="bg-white/10 backdrop-blur-xl rounded-2xl border border-cyan-500/30 shadow-2xl p-2">
          <div className="flex items-center justify-around">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path;
              
              return (
                <Link key={item.path} to={item.path} className="flex-1">
                  <motion.div
                    whileHover={{ scale: 1.05, y: -2 }}
                    whileTap={{ scale: 0.95 }}
                    className={`relative flex flex-col items-center p-2 rounded-xl transition-all duration-300 ${
                      isActive 
                        ? 'text-cyan-500' 
                        : 'text-cyan-800 dark:text-cyan-200/90 hover:text-cyan-400'
                    }`}
                  >
                    <Icon className="w-5 h-5 mb-1" />
                    <span className="text-xs font-semibold">{item.label}</span>
                    
                    {/* Active indicator dot */}
                    {isActive && (
                      <motion.div
                        layoutId="mobileActive"
                        className="absolute -top-1 w-1.5 h-1.5 bg-cyan-400 rounded-full"
                        transition={{ type: "spring", stiffness: 300, damping: 30 }}
                      />
                    )}
                  </motion.div>
                </Link>
              );
            })}
          </div>
        </div>
      </div>
    </motion.nav>
  );
};

export default MobileBottomNav;