import React from 'react';
import { motion } from 'framer-motion';
import { Github, Twitter, Mail, Heart, Cpu, Shield } from 'lucide-react';

const Footer: React.FC = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className=" bg-white dark:bg-black text-black dark:text-white border-t border-cyan-500/20">
      <div className="container mx-auto px-4 py-16">
        <div className="grid md:grid-cols-4 gap-8">
          {/* Brand */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            className="md:col-span-2"
          >
            <div className="flex items-center space-x-3 mb-6">
         <div className="w-10 h-10 rounded-xl overflow-hidden flex items-center justify-center">
  <img src="/logo.png" alt="Logo" className="w-full h-full object-cover" />
</div>

              <span className="text-2xl font-black bg-gradient-to-r from-cyan-700 to-purple-700 dark:from-cyan-500 dark:to-purple-500 bg-clip-text text-transparent">
                KEGINATOR
              </span>
            </div>
            <p className="text-cyan-900 dark:text-cyan-200 mb-6 max-w-md text-lg leading-relaxed">
              Revolutionizing data integrity with Solana blockchain verification. 
              Built for the future of trusted data processing.
            </p>
            <div className="flex space-x-4">
              {[
                { icon: Github, href: 'https://github.com', label: 'GitHub' },
                { icon: Twitter, href: 'https://twitter.com', label: 'Twitter' },
                { icon: Mail, href: 'mailto:hello@keginator.com', label: 'Email' }
              ].map((social, index) => (
                <motion.a
                  key={social.label}
                  href={social.href}
                  whileHover={{ scale: 1.2, y: -2 }}
                  whileTap={{ scale: 0.9 }}
                  className="p-3 bg-cyan-500/20 rounded-xl text-cyan-800 hover:text-cyan-700 hover:bg-cyan-800/30 dark:text-cyan-400 dark:hover:text-cyan-300 dark:hover:bg-cyan-500/30 border border-cyan-500/30 transition-all duration-300"
                  aria-label={social.label}
                >
                  <social.icon className="w-5 h-5" />
                </motion.a>
              ))}
            </div>
          </motion.div>

          {/* Product Links */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
          >
            <h3 className="font-bold text-cyan-700 text-lg mb-6 flex items-center space-x-2">
              <Shield className="w-5 h-5" />
              <span>PRODUCT</span>
            </h3>
            <ul className="space-y-3">
              {['Data Cleaning', 'Blockchain Proof', 'Verification', 'API Access'].map((item) => (
                <li key={item}>
                  <a 
                    href="https://zeptaherself.netlify.app" 
                    className="text-cyan-800 dark:text-cyan-200 hover:text-cyan-400 transition-colors duration-300 hover:underline"
                  >
                    {item}
                  </a>
                </li>
              ))}
            </ul>
          </motion.div>

          {/* Company Links */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            <h3 className="font-bold text-purple-700 dark:text-purple-400 text-lg mb-6 flex items-center space-x-2">
              <Cpu className="w-5 h-5" />
              <span className='!dark:text-[#ffffff]'>COMPANY</span>
            </h3>
            <ul className="space-y-3">
              {['About', 'Documentation', 'Careers', 'Contact'].map((item) => (
                <li key={item}>
                  <a 
                    href="https://zeptaherself.netlify.app" 
                    className="text-cyan-900 hover:text-purple-900 dark:text-cyan-200 dark:hover:text-purple-400 transition-colors duration-300 hover:underline"
                  >
                    {item}
                  </a>
                </li>
              ))}
            </ul>
          </motion.div>
        </div>

        {/* Bottom */}
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
          className="border-t border-cyan-500/20 mt-12 pt-8 flex flex-col md:flex-row justify-between items-center"
        >
          <p className="text-cyan-800 dark:text-cyan-300 flex items-center text-sm">
            <span className="flex items-center">
              Built with <Heart className="w-4 h-4 text-red-400 mx-2" /> for the Solana Cypherpunk Hackathon
            </span>
          </p>
          <p className="text-cyan-900 dark:text-cyan-200 mt-4 md:mt-0 text-sm">
            © {currentYear} Keginator. All systems operational.
          </p>
        </motion.div>
      </div>
    </footer>
  );
};

export default Footer;