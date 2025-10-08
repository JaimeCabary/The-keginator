import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AnimatePresence } from 'framer-motion';
import Header from './components/layout/Header';
import MobileBottomNav from './components/layout/MobileBottomNav';
import Footer from './components/layout/Footer';
import Home from './pages/Home';
import Upload from './pages/Upload';
import History from './pages/History';
import Verify from './pages/Verify';
import Auth from './pages/Auth';
import Dashboard from './pages/Dashboard';
import Pricing from './pages/Pricing';
import Info from './pages/Info';
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
        
        {/* Main content with padding to account for fixed header and mobile bottom nav */}
        <main className="pt-20 pb-20 md:pb-0"> {/* Added bottom padding for mobile nav */}
          <AnimatePresence mode="wait">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/upload" element={<Upload />} />
              <Route path="/history" element={<History />} />
              <Route path="/verify" element={<Verify />} />
              <Route path="/auth" element={<Auth />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/pricing" element={<Pricing />} />
              {/* Info route only for mobile - acts as mobile footer */}
              <Route path="/info" element={
                <div className="md:hidden">
                  <Info />
                </div>
              } />
            </Routes>
          </AnimatePresence>
        </main>
        
        {/* Mobile Bottom Navigation - only on mobile */}
        <div className="md:hidden">
          <MobileBottomNav />
        </div>
        
        {/* Footer only for desktop */}
        <div className="hidden md:block">
          <Footer />
        </div>
      </div>
    </Router>
  );
};

export default App;


