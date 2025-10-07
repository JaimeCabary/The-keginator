import React, { useCallback, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Upload, FileText, X, CheckCircle } from 'lucide-react';
import { useApi } from '../../hooks/useApi';
import { UploadResponse } from '../../types';

interface FileUploadProps {
  onUploadComplete: (response: UploadResponse) => void;
  userId?: string;
}

const FileUpload: React.FC<FileUploadProps> = ({ onUploadComplete }) => {
  const [isDragOver, setIsDragOver] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const { uploadDataset, loading, error } = useApi();

  // Define processFile first to avoid reference issues
  const processFile = useCallback(async (file: File) => {
    setUploadedFile(file);
    try {
      const response = await uploadDataset(file);
      onUploadComplete(response);
    } catch (err) {
      console.error('Upload failed:', err);
      // Optional: Remove file on error
      setUploadedFile(null);
    }
  }, [uploadDataset, onUploadComplete]);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
  }, []);

  const handleDrop = useCallback(async (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    
    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0) {
      // Check for supported file types
      const file = files[0];
      const supportedTypes = ['text/csv', 'application/json', 'text/plain'];
      const supportedExtensions = ['.csv', '.json', '.txt'];
      const fileExtension = file.name.toLowerCase().substring(file.name.lastIndexOf('.'));
      
      if (supportedTypes.includes(file.type) || supportedExtensions.includes(fileExtension)) {
        await processFile(file);
      } else {
        console.error('Unsupported file type');
        // You could set an error state here
      }
    }
  }, [processFile]); // Now processFile is properly defined

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      await processFile(files[0]);
    }
  };

  const removeFile = useCallback(() => {
    setUploadedFile(null);
  }, []);

  return (
    <div className="space-y-4">
      <motion.div
        className={`border-2 border-dashed rounded-xl p-8 text-center transition-all duration-300 ${
          isDragOver
            ? 'border-primary-500 bg-primary-500/10'
            : 'border-gray-300 dark:border-gray-600 hover:border-primary-500'
        }`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
      >
        <input
          type="file"
          accept=".csv,.json,.txt,text/csv,application/json,text/plain"
          onChange={handleFileSelect}
          className="hidden"
          id="file-upload"
        />
        
        <label htmlFor="file-upload" className="cursor-pointer">
          <motion.div
            initial={{ scale: 0.8 }}
            animate={{ scale: 1 }}
            className="flex flex-col items-center space-y-4"
          >
            <Upload className="w-12 h-12 text-gray-400" />
            <div>
              <p className="text-lg font-semibold">
                Drop your dataset here or click to browse
              </p>
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">
                Supports CSV, JSON, TXT files
              </p>
            </div>
          </motion.div>
        </label>
      </motion.div>

      {/* Uploaded File Preview */}
      <AnimatePresence>
        {uploadedFile && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="futuristic-card p-4"
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <FileText className="w-8 h-8 text-primary-500" />
                <div>
                  <p className="font-medium">{uploadedFile.name}</p>
                  <p className="text-sm text-gray-500">
                    {(uploadedFile.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                </div>
              </div>
              
              <div className="flex items-center space-x-2">
                {loading ? (
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                    className="w-6 h-6 border-2 border-primary-500 border-t-transparent rounded-full"
                  />
                ) : (
                  <CheckCircle className="w-6 h-6 text-green-500" />
                )}
                <button
                  onClick={removeFile}
                  className="p-1 hover:bg-red-500/20 rounded transition-colors"
                  disabled={loading}
                >
                  <X className="w-4 h-4 text-red-500" />
                </button>
              </div>
            </div>

            {/* Progress indicator during upload */}
            {loading && (
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: '100%' }}
                transition={{ duration: 2, ease: 'easeInOut' }}
                className="mt-3 h-1 bg-primary-500 rounded-full"
              />
            )}
          </motion.div>
        )}
      </AnimatePresence>

      {/* Error Message */}
      {error && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="p-4 bg-red-500/10 border border-red-500 rounded-lg text-red-500"
        >
          {error}
        </motion.div>
      )}
    </div>
  );
};

export default FileUpload;