import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Download, ExternalLink, Copy, CheckCircle } from 'lucide-react';
import FileUpload from '../components/ui/FileUpload';
import { UploadResponse } from '../types';
import { SOLANA_EXPLORER_URL } from '../utils/constants';
import { useScrollToTop } from '../hooks/useScrollToTop';

const Upload: React.FC = () => {
  const [uploadResult, setUploadResult] = useState<UploadResponse | null>(null);
  const [copied, setCopied] = useState(false);

  useScrollToTop();

  const handleUploadComplete = (result: UploadResponse) => {
    setUploadResult(result);
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const downloadFile = (url: string, filename: string) => {
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.click();
  };

  return (
    <div className="min-h-screen  bg-white dark:bg-black text-black dark:text-white py-20 mb-20 md:mb-20">
      <div className="container mx-auto px-4">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          className="max-w-4xl mx-auto"
        >
          <div className="text-center mb-12">
            <h1 className="text-4xl md:text-5xl font-bold mb-4">
              Clean Your Data
            </h1>
            <p className="text-xl text-gray-600 dark:text-gray-300">
              Upload your dataset and watch the magic happen
            </p>
          </div>

          {/* File Upload Component */}
          <FileUpload 
            onUploadComplete={handleUploadComplete}
            userId="demo-user" // Or get from user auth
          />

          {/* Results Panel */}
          <AnimatePresence>
            {uploadResult && (
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.9 }}
                className="futuristic-card p-6 mt-8"
              >
                <div className="flex items-center space-x-2 mb-4">
                  <CheckCircle className="w-6 h-6 text-green-500" />
                  <h3 className="text-2xl font-semibold">Cleaning Complete!</h3>
                </div>

                {/* Hash Display */}
                <div className="mb-6">
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Dataset Hash
                  </label>
                  <div className="flex items-center space-x-2">
                    <code className="flex-1 px-4 py-2 bg-gray-100 dark:bg-dark-300 rounded-lg font-mono text-sm break-all">
                      {uploadResult.hash}
                    </code>
                    <button
                      onClick={() => copyToClipboard(uploadResult.hash)}
                      className="p-2 hover:bg-gray-200 dark:hover:bg-dark-400 rounded-lg transition-colors"
                    >
                      {copied ? (
                        <CheckCircle className="w-5 h-5 text-green-500" />
                      ) : (
                        <Copy className="w-5 h-5" />
                      )}
                    </button>
                  </div>
                </div>

                {/* Actions */}
                <div className="flex flex-col sm:flex-row gap-4">
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => downloadFile(uploadResult.downloadUrl, `cleaned_${uploadResult.filename}`)}
                    className="flex-1 px-6 py-3 bg-primary-500 hover:bg-primary-600 text-white rounded-lg font-semibold flex items-center justify-center space-x-2 transition-colors"
                  >
                    <Download className="w-5 h-5" />
                    <span>Download Cleaned Dataset</span>
                  </motion.button>

                  {uploadResult.solanaTx && (
                    <motion.a
                      href={`${SOLANA_EXPLORER_URL}/tx/${uploadResult.solanaTx}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      className="px-6 py-3 border border-primary-500 text-primary-500 hover:bg-primary-500/10 rounded-lg font-semibold flex items-center justify-center space-x-2 transition-colors"
                    >
                      <ExternalLink className="w-5 h-5" />
                      <span>View on Solana</span>
                    </motion.a>
                  )}
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>
      </div>
    </div>
  );
};

export default Upload;