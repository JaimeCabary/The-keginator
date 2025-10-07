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
      {/* Apply dark theme to entire app and remove default margins/padding */}
      <div className="min-h-screen overflow-x-hidden">
        {/* Header positioned absolutely so content starts from top */}
        <div className="fixed top-0 left-0 right-0 z-50">
          <Header />
        </div>
        
        {/* Main content with padding to account for fixed header */}
        <main className="pt-20"> {/* Adjust this value based on your header height */}
          <AnimatePresence mode="wait">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/upload" element={<Upload />} />
              <Route path="/history" element={<History />} />
              <Route path="/verify" element={<Verify />} />
            </Routes>
          </AnimatePresence>
        </main>
        
        <Footer />
      </div>
    </Router>
  );
};

export default App;