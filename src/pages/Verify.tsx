import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, CheckCircle, XCircle, ExternalLink, Copy } from 'lucide-react';
import AnimatedCard from '../components/ui/AnimatedCard';
import { useApi } from '../hooks/useApi';
import { VerificationResponse } from '../types';
import { SOLANA_EXPLORER_URL } from '../utils/constants';
import { useScrollToTop } from '../hooks/useScrollToTop';

const Verify: React.FC = () => {
  const [hash, setHash] = useState('');
  const [verificationResult, setVerificationResult] = useState<VerificationResponse | null>(null);
  const [isVerifying, setIsVerifying] = useState(false);
  const [copied, setCopied] = useState(false);
  const { error } = useApi();

    
  useScrollToTop();

  const handleVerify = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!hash.trim()) return;

    setIsVerifying(true);
    setVerificationResult(null);

    try {
      // For demo, using mock data. Replace with actual API call
      const mockResult: VerificationResponse = {
        verified: Math.random() > 0.3, // 70% chance of verification for demo
        hash: hash,
        timestamp: new Date().toISOString(),
        solanaTx: '5g2X8h9j3k4l7m8n9b0v1c2x3z4a5s6d7f8g9h0j',
        metadata: {
          filename: 'dataset.csv',
          size: 2457600,
          rows: 1247,
          cleanedAt: new Date().toISOString()
        }
      };
      
      setVerificationResult(mockResult);
      
      // Uncomment for real API call:
      // const result = await verifyHash(hash);
      // setVerificationResult(result);
    } catch (err) {
      console.error('Verification failed:', err);
    } finally {
      setIsVerifying(false);
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const getVerificationIcon = (verified: boolean) => {
    if (isVerifying) {
      return (
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
          className="w-16 h-16 border-4 border-yellow-500 border-t-transparent rounded-full"
        />
      );
    }
    
    return verified ? (
      <CheckCircle className="w-16 h-16 text-green-500" />
    ) : (
      <XCircle className="w-16 h-16 text-red-500" />
    );
  };

  const getVerificationMessage = (verified: boolean) => {
    if (isVerifying) {
      return {
        title: 'Verifying Dataset',
        description: 'Checking blockchain for verification proof...',
        color: 'text-yellow-500'
      };
    }
    
    return verified ? {
      title: 'Dataset Verified!',
      description: 'This dataset has been successfully verified on the Solana blockchain.',
      color: 'text-green-500'
    } : {
      title: 'Verification Failed',
      description: 'This dataset could not be verified on the blockchain.',
      color: 'text-red-500'
    };
  };

  const verificationInfo = verificationResult ? getVerificationMessage(verificationResult.verified) : null;

  return (
    <div className="min-h-screen py-20  bg-white dark:bg-black text-black dark:text-white">
      <div className="container mx-auto px-4">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          className="max-w-4xl mx-auto"
        >
          {/* Header */}
          <div className="text-center mb-12">
            <h1 className="text-4xl md:text-5xl font-bold mb-4">Verify Dataset</h1>
            <p className="text-xl text-gray-600 dark:text-gray-300">
              Check the authenticity of any dataset using its blockchain hash
            </p>
          </div>

          {/* Verification Form */}
          <AnimatedCard className="p-8 mb-8">
            <form onSubmit={handleVerify} className="space-y-6">
              <div>
                <label htmlFor="hash" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Dataset Hash
                </label>
                <div className="relative">
                  <input
                    type="text"
                    id="hash"
                    value={hash}
                    onChange={(e) => setHash(e.target.value)}
                    placeholder="Enter dataset hash (e.g., 7x8a2b9f4c1e6d3a5f9e3c1b8a2d4f7e6)"
                    className="w-full px-4 py-3 bg-gray-100 dark:bg-dark-300 rounded-lg border border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all font-mono"
                  />
                  {hash && (
                    <button
                      type="button"
                      onClick={() => copyToClipboard(hash)}
                      className="absolute right-3 top-1/2 transform -translate-y-1/2 p-1 hover:bg-gray-200 dark:hover:bg-dark-400 rounded transition-colors"
                    >
                      {copied ? (
                        <CheckCircle className="w-4 h-4 text-green-500" />
                      ) : (
                        <Copy className="w-4 h-4" />
                      )}
                    </button>
                  )}
                </div>
              </div>

              <motion.button
                type="submit"
                disabled={!hash.trim() || isVerifying}
                whileHover={{ scale: !hash.trim() || isVerifying ? 1 : 1.05 }}
                whileTap={{ scale: !hash.trim() || isVerifying ? 1 : 0.95 }}
                className="w-full px-6 py-4 bg-primary-500 hover:bg-primary-600 disabled:bg-gray-400 disabled:cursor-not-allowed text-white rounded-lg font-semibold flex items-center justify-center space-x-2 transition-colors"
              >
                <Search className="w-5 h-5" />
                <span>
                  {isVerifying ? 'Verifying...' : 'Verify Dataset'}
                </span>
              </motion.button>
            </form>
          </AnimatedCard>

          {/* Error Message */}
          {error && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="futuristic-card p-6 text-red-500 bg-red-500/10 border border-red-500/20 mb-8"
            >
              <div className="flex items-center space-x-2">
                <XCircle className="w-5 h-5" />
                <span>{error}</span>
              </div>
            </motion.div>
          )}

          {/* Verification Result */}
          <AnimatePresence>
            {verificationResult && verificationInfo && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
              >
                <AnimatedCard className="p-8 text-center">
                  <div className="flex justify-center mb-6">
                    {getVerificationIcon(verificationResult.verified)}
                  </div>

                  <h2 className={`text-2xl font-bold mb-4 ${verificationInfo.color}`}>
                    {verificationInfo.title}
                  </h2>
                  
                  <p className="text-gray-600 dark:text-gray-300 mb-6">
                    {verificationInfo.description}
                  </p>

                  {/* Verification Details */}
                  <div className="grid md:grid-cols-2 gap-6 text-left">
                    <div className="space-y-4">
                      <h3 className="font-semibold text-lg mb-4">Blockchain Proof</h3>
                      
                      <div>
                        <label className="text-sm text-gray-500 dark:text-gray-400">Hash</label>
                        <div className="flex items-center space-x-2 mt-1">
                          <code className="flex-1 px-3 py-2 bg-gray-100 dark:bg-dark-300 rounded text-sm font-mono break-all">
                            {verificationResult.hash}
                          </code>
                          <button
                            onClick={() => copyToClipboard(verificationResult.hash)}
                            className="p-2 hover:bg-gray-200 dark:hover:bg-dark-400 rounded transition-colors"
                          >
                            {copied ? (
                              <CheckCircle className="w-4 h-4 text-green-500" />
                            ) : (
                              <Copy className="w-4 h-4" />
                            )}
                          </button>
                        </div>
                      </div>

                      {verificationResult.timestamp && (
                        <div>
                          <label className="text-sm text-gray-500 dark:text-gray-400">Timestamp</label>
                          <p className="mt-1 font-medium">
                            {new Date(verificationResult.timestamp).toLocaleString()}
                          </p>
                        </div>
                      )}

                      {verificationResult.solanaTx && (
                        <div>
                          <label className="text-sm text-gray-500 dark:text-gray-400">Solana Transaction</label>
                          <div className="flex items-center space-x-2 mt-1">
                            <code className="flex-1 px-3 py-2 bg-gray-100 dark:bg-dark-300 rounded text-sm font-mono">
                              {verificationResult.solanaTx.slice(0, 8)}...{verificationResult.solanaTx.slice(-8)}
                            </code>
                            <motion.a
                              href={`${SOLANA_EXPLORER_URL}/tx/${verificationResult.solanaTx}`}
                              target="_blank"
                              rel="noopener noreferrer"
                              whileHover={{ scale: 1.05 }}
                              whileTap={{ scale: 0.95 }}
                              className="p-2 hover:bg-gray-200 dark:hover:bg-dark-400 rounded transition-colors"
                            >
                              <ExternalLink className="w-4 h-4" />
                            </motion.a>
                          </div>
                        </div>
                      )}
                    </div>

                    {/* Metadata */}
                    {verificationResult.metadata && (
                      <div className="space-y-4">
                        <h3 className="font-semibold text-lg mb-4">Dataset Info</h3>
                        
                        {verificationResult.metadata.filename && (
                          <div>
                            <label className="text-sm text-gray-500 dark:text-gray-400">Filename</label>
                            <p className="mt-1 font-medium">{verificationResult.metadata.filename}</p>
                          </div>
                        )}

                        {verificationResult.metadata.size && (
                          <div>
                            <label className="text-sm text-gray-500 dark:text-gray-400">Size</label>
                            <p className="mt-1 font-medium">
                              {(verificationResult.metadata.size / 1024 / 1024).toFixed(2)} MB
                            </p>
                          </div>
                        )}

                        {verificationResult.metadata.rows && (
                          <div>
                            <label className="text-sm text-gray-500 dark:text-gray-400">Rows</label>
                            <p className="mt-1 font-medium">{verificationResult.metadata.rows.toLocaleString()}</p>
                          </div>
                        )}

                        {verificationResult.metadata.cleanedAt && (
                          <div>
                            <label className="text-sm text-gray-500 dark:text-gray-400">Cleaned At</label>
                            <p className="mt-1 font-medium">
                              {new Date(verificationResult.metadata.cleanedAt).toLocaleString()}
                            </p>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                </AnimatedCard>
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>
      </div>
    </div>
  );
};

export default Verify;