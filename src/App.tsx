import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AnimatePresence } from 'framer-motion';
import Header from './components/layout/Header';
import Footer from './components/layout/Footer';
import Home from './pages/Home';
import Upload from './pages/Upload';
import History from './pages/History';
import Verify from './pages/Verify';
import { useTheme } from './hooks/useTheme';
import './styles/globals.css';

const App: React.FC = () => {
  useTheme(); // Initialize theme

  return (
    <Router>
      <div className="min-h-screen bg-white dark:bg-dark-100 transition-colors duration-300">
        <Header />
        
        <AnimatePresence mode="wait">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/upload" element={<Upload />} />
            <Route path="/history" element={<History />} />
            <Route path="/verify" element={<Verify />} />
          </Routes>
        </AnimatePresence>
        <Footer />
      </div>
    </Router>
  );
};

export default App;