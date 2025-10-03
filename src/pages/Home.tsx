import React from 'react';
import { motion } from 'framer-motion';
import { ArrowRight, Shield, Zap, Database } from 'lucide-react';
import Terminal from '../components/ui/Terminal';

const Home: React.FC = () => {
  return (
    <div className="min-h-screen bg-grid-pattern bg-[length:50px_50px]">
      {/* Hero Section */}
      <section className="relative py-20 overflow-hidden">
        {/* Animated Background Elements */}
        <div className="absolute inset-0 bg-space-gradient" />
        
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1 }}
          className="container mx-auto px-4 text-center relative z-10"
        >
          <motion.h1
            initial={{ y: 50, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.8 }}
            className="text-6xl md:text-8xl font-bold mb-6"
          >
            <span className="bg-gradient-to-r from-primary-500 via-purple-500 to-cyan-500 bg-clip-text text-transparent">
              Keginator
            </span>
          </motion.h1>
          
          <motion.p
            initial={{ y: 30, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="text-xl md:text-2xl text-gray-600 dark:text-gray-300 mb-8 max-w-3xl mx-auto"
          >
            Transform messy data into clean, verified datasets with immutable Solana blockchain proof
          </motion.p>

          <motion.div
            initial={{ y: 30, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-16"
          >
            <motion.a
              href="#upload"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="px-8 py-4 bg-primary-500 hover:bg-primary-600 text-white rounded-lg font-semibold flex items-center space-x-2 transition-colors"
            >
              <span>Start Cleaning</span>
              <ArrowRight className="w-5 h-5" />
            </motion.a>
            
            <motion.a
              href="#demo"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="px-8 py-4 border border-primary-500 text-primary-500 hover:bg-primary-500/10 rounded-lg font-semibold transition-colors"
            >
              See Demo
            </motion.a>
          </motion.div>
        </motion.div>

        {/* Features Grid */}
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.6 }}
          className="container mx-auto px-4 mt-20"
        >
          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                icon: <Zap className="w-8 h-8" />,
                title: "Lightning Fast",
                description: "Real-time data cleaning with instant results"
              },
              {
                icon: <Shield className="w-8 h-8" />,
                title: "Blockchain Verified",
                description: "Immutable proof stored on Solana"
              },
              {
                icon: <Database className="w-8 h-8" />,
                title: "Multi-format Support",
                description: "CSV, JSON, TXT and more"
              }
            ].map((feature, index) => (
              <motion.div
                key={index}
                whileHover={{ scale: 1.05, y: -5 }}
                className="futuristic-card p-6 text-center"
              >
                <div className="text-primary-500 mb-4 flex justify-center">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
                <p className="text-gray-600 dark:text-gray-400">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </section>

      {/* Terminal Demo Section */}
      <section id="demo" className="py-20 bg-dark-200/50">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            transition={{ duration: 0.8 }}
            className="text-center mb-12"
          >
            <h2 className="text-4xl font-bold mb-4">See it in Action</h2>
            <p className="text-xl text-gray-600 dark:text-gray-300">
              Experience the power of Keginator through our interactive CLI
            </p>
          </motion.div>
          
          <Terminal />
        </div>
      </section>
    </div>
  );
};

export default Home;