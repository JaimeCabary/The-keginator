// // import React, { useState } from 'react';
// // import { motion, AnimatePresence } from 'framer-motion';
// // import { Download, ExternalLink, Copy, CheckCircle } from 'lucide-react';
// // import FileUpload from '../components/ui/FileUpload';
// // import { UploadResponse } from '../types';
// // import { SOLANA_EXPLORER_URL } from '../utils/constants';
// // import { useScrollToTop } from '../hooks/useScrollToTop';

// // const Upload: React.FC = () => {
// //   const [uploadResult, setUploadResult] = useState<UploadResponse | null>(null);
// //   const [copied, setCopied] = useState(false);

// //   useScrollToTop();

// //   const handleUploadComplete = (result: UploadResponse) => {
// //     setUploadResult(result);
// //   };

// //   const copyToClipboard = (text: string) => {
// //     navigator.clipboard.writeText(text);
// //     setCopied(true);
// //     setTimeout(() => setCopied(false), 2000);
// //   };

// //   const downloadFile = (url: string, filename: string) => {
// //     const link = document.createElement('a');
// //     link.href = url;
// //     link.download = filename;
// //     link.click();
// //   };

// //   return (
// //     <div className="min-h-screen  bg-white dark:bg-black text-black dark:text-white py-20 mb-20 md:mb-20">
// //       <div className="container mx-auto px-4">
// //         <motion.div
// //           initial={{ opacity: 0, y: 30 }}
// //           animate={{ opacity: 1, y: 0 }}
// //           className="max-w-4xl mx-auto"
// //         >
// //           <div className="text-center mb-12">
// //             <h1 className="text-4xl md:text-5xl font-bold mb-4">
// //               Clean Your Data
// //             </h1>
// //             <p className="text-xl text-gray-600 dark:text-gray-300">
// //               Upload your dataset and watch the magic happen
// //             </p>
// //           </div>

// //           {/* File Upload Component */}
// //           <FileUpload 
// //             onUploadComplete={handleUploadComplete}
// //             userId="demo-user" // Or get from user auth
// //           />

// //           {/* Results Panel */}
// //           <AnimatePresence>
// //             {uploadResult && (
// //               <motion.div
// //                 initial={{ opacity: 0, scale: 0.9 }}
// //                 animate={{ opacity: 1, scale: 1 }}
// //                 exit={{ opacity: 0, scale: 0.9 }}
// //                 className="futuristic-card p-6 mt-8"
// //               >
// //                 <div className="flex items-center space-x-2 mb-4">
// //                   <CheckCircle className="w-6 h-6 text-green-500" />
// //                   <h3 className="text-2xl font-semibold">Cleaning Complete!</h3>
// //                 </div>

// //                 {/* Hash Display */}
// //                 <div className="mb-6">
// //                   <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
// //                     Dataset Hash
// //                   </label>
// //                   <div className="flex items-center space-x-2">
// //                     <code className="flex-1 px-4 py-2 bg-gray-100 dark:bg-dark-300 rounded-lg font-mono text-sm break-all">
// //                       {uploadResult.hash}
// //                     </code>
// //                     <button
// //                       onClick={() => copyToClipboard(uploadResult.hash)}
// //                       className="p-2 hover:bg-gray-200 dark:hover:bg-dark-400 rounded-lg transition-colors"
// //                     >
// //                       {copied ? (
// //                         <CheckCircle className="w-5 h-5 text-green-500" />
// //                       ) : (
// //                         <Copy className="w-5 h-5" />
// //                       )}
// //                     </button>
// //                   </div>
// //                 </div>

// //                 {/* Actions */}
// //                 <div className="flex flex-col sm:flex-row gap-4">
// //                   <motion.button
// //                     whileHover={{ scale: 1.05 }}
// //                     whileTap={{ scale: 0.95 }}
// //                     onClick={() => downloadFile(uploadResult.downloadUrl, `cleaned_${uploadResult.filename}`)}
// //                     className="flex-1 px-6 py-3 bg-primary-500 hover:bg-primary-600 text-white rounded-lg font-semibold flex items-center justify-center space-x-2 transition-colors"
// //                   >
// //                     <Download className="w-5 h-5" />
// //                     <span>Download Cleaned Dataset</span>
// //                   </motion.button>

// //                   {uploadResult.solanaTx && (
// //                     <motion.a
// //                       href={`${SOLANA_EXPLORER_URL}/tx/${uploadResult.solanaTx}`}
// //                       target="_blank"
// //                       rel="noopener noreferrer"
// //                       whileHover={{ scale: 1.05 }}
// //                       whileTap={{ scale: 0.95 }}
// //                       className="px-6 py-3 border border-primary-500 text-primary-500 hover:bg-primary-500/10 rounded-lg font-semibold flex items-center justify-center space-x-2 transition-colors"
// //                     >
// //                       <ExternalLink className="w-5 h-5" />
// //                       <span>View on Solana</span>
// //                     </motion.a>
// //                   )}
// //                 </div>
// //               </motion.div>
// //             )}
// //           </AnimatePresence>
// //         </motion.div>
// //       </div>
// //     </div>
// //   );
// // };

// // export default Upload;


// import React, { useState } from 'react';
// import { motion, AnimatePresence } from 'framer-motion';
// import { Download, ExternalLink, Copy, CheckCircle, Cpu, FileText } from 'lucide-react';
// import FileUpload from '../components/ui/FileUpload';
// import { SOLANA_EXPLORER_URL } from '../utils/constants';
// import { useScrollToTop } from '../hooks/useScrollToTop';

// // NOTE: This interface is synchronized with the new backend /upload response
// interface UploadResponse {
//   success: boolean;
//   hash: string;
//   filename: string;
//   download_ml_url: string; // New: ML-Ready (Encoded/Embedded)
//   download_text_url: string; // New: Human-Readable (Imputed Text)
//   solana_signature?: string;
//   cleaned_rows: number;
//   columns: number;
//   type: string;
// }

// const Upload: React.FC = () => {
//   const [uploadResult, setUploadResult] = useState<UploadResponse | null>(null);
//   const [copied, setCopied] = useState(false);

//   useScrollToTop();

//   const handleUploadComplete = (result: UploadResponse) => {
//     setUploadResult(result);
//     // Dispatch event to trigger history refresh
//     window.dispatchEvent(new CustomEvent('datasetUploaded'));
//   };

//   const copyToClipboard = (text: string) => {
//     navigator.clipboard.writeText(text);
//     setCopied(true);
//     setTimeout(() => setCopied(false), 2000);
//   };

//   const downloadFile = (url: string, prefix: string, extension: string, mode: string) => {
//     const link = document.createElement('a');
//     link.href = url;
//     // Filename structure: [original_name]_[mode].csv
//     const baseName = prefix.replace(/\.[^/.]+$/, ""); // Remove extension
//     link.download = `${baseName}_${mode.toUpperCase()}.${extension}`;
//     link.click();
//   };

//   // Prevent rendering tabular UI for audio results, focusing on the dual output for tabular data.
//   if (uploadResult && uploadResult.type === 'audio') {
//     // Note: A dedicated AudioResults component should be rendered here if necessary.
//     return (
//       <div className="min-h-screen py-20 px-4 text-center">
//         <p className="text-xl text-green-500">Audio Transcription Completed!</p>
//         <p className="text-gray-400">Check History for details and Solana proof.</p>
//       </div>
//     );
//   }

//   return (
//     <div className="min-h-screen bg-white dark:bg-black text-black dark:text-white py-20 mb-20 md:mb-20">
//       <div className="container mx-auto px-4">
//         <motion.div
//           initial={{ opacity: 0, y: 30 }}
//           animate={{ opacity: 1, y: 0 }}
//           className="max-w-4xl mx-auto"
//         >
//           <div className="text-center mb-12">
//             <h1 className="text-4xl md:text-5xl font-bold mb-4">
//               Clean Your Data
//             </h1>
//             <p className="text-xl text-gray-600 dark:text-gray-300">
//               Upload your dataset and watch the magic happen
//             </p>
//           </div>

//           {/* File Upload Component */}
//           {/* NOTE: Ensure FileUpload component uses the correct user ID */}
//           <FileUpload 
//             onUploadComplete={handleUploadComplete}
//             userId={localStorage.getItem('auth_token') ? (JSON.parse(localStorage.getItem('user') || '{}').id || 'demo-user') : 'demo-user'}
//           />

//           {/* Results Panel */}
//           <AnimatePresence>
//             {uploadResult && (
//               <motion.div
//                 initial={{ opacity: 0, scale: 0.9 }}
//                 animate={{ opacity: 1, scale: 1 }}
//                 exit={{ opacity: 0, scale: 0.9 }}
//                 className="futuristic-card p-6 mt-8"
//               >
//                 <div className="flex items-center space-x-2 mb-4">
//                   <CheckCircle className="w-6 h-6 text-green-500" />
//                   <h3 className="text-2xl font-semibold">Cleaning Complete!</h3>
//                 </div>

//                 <div className="grid md:grid-cols-3 gap-4 text-sm text-gray-600 dark:text-gray-400 mb-6">
//                     <div>
//                         <FileText className="w-5 h-5 text-cyan-500 mb-1" />
//                         <span className="font-medium">Original File:</span> {uploadResult.filename}
//                     </div>
//                     <div>
//                         <span className="font-medium">Cleaned Rows:</span> {uploadResult.cleaned_rows}
//                     </div>
//                     <div>
//                         <span className="font-medium">Final Columns:</span> {uploadResult.columns}
//                     </div>
//                 </div>

//                 {/* Hash Display */}
//                 <div className="mb-8">
//                   <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
//                     Dataset Hash (Solana Proof)
//                   </label>
//                   <div className="flex items-center space-x-2">
//                     <code className="flex-1 px-4 py-2 bg-gray-100 dark:bg-dark-300 rounded-lg font-mono text-sm break-all">
//                       {uploadResult.hash}
//                     </code>
//                     <button
//                       onClick={() => copyToClipboard(uploadResult.hash)}
//                       className="p-2 hover:bg-gray-200 dark:hover:bg-dark-400 rounded-lg transition-colors"
//                       title="Copy Hash"
//                     >
//                       {copied ? (
//                         <CheckCircle className="w-5 h-5 text-green-500" />
//                       ) : (
//                         <Copy className="w-5 h-5" />
//                       )}
//                     </button>
//                   </div>
//                 </div>

//                 {/* Dual Download Actions */}
//                 <div className="space-y-4">
//                     <h4 className="text-lg font-bold flex items-center space-x-2">
//                         <Download className="w-5 h-5 text-primary-500" />
//                         <span>Download Output Formats</span>
//                     </h4>
                    
//                     {/* ML READY OUTPUT */}
//                     <motion.button
//                         whileHover={{ scale: 1.02 }}
//                         whileTap={{ scale: 0.98 }}
//                         // Use download_ml_url, naming convention is ML
//                         onClick={() => downloadFile(uploadResult.download_ml_url, uploadResult.filename, 'csv', 'ML')}
//                         className="w-full px-6 py-3 bg-purple-500 hover:bg-purple-600 text-white rounded-lg font-semibold flex items-center justify-center space-x-2 transition-colors"
//                     >
//                         <Cpu className="w-5 h-5" />
//                         <span>Download ML-Ready Output (Encoded/Embedded)</span>
//                     </motion.button>
                    
//                     {/* HUMAN-READABLE OUTPUT */}
//                     <motion.button
//                         whileHover={{ scale: 1.02 }}
//                         whileTap={{ scale: 0.98 }}
//                         // Use download_text_url, naming convention is Text
//                         onClick={() => downloadFile(uploadResult.download_text_url, uploadResult.filename, 'csv', 'Text')}
//                         className="w-full px-6 py-3 border border-cyan-500 text-cyan-500 hover:bg-cyan-500/10 rounded-lg font-semibold flex items-center justify-center space-x-2 transition-colors"
//                     >
//                         <FileText className="w-5 h-5" />
//                         <span>Download Human-Readable Output (Clean Text)</span>
//                     </motion.button>

//                     {/* Solana Link */}
//                     {uploadResult.solana_signature && (
//                         <motion.a
//                             href={`${SOLANA_EXPLORER_URL}/tx/${uploadResult.solana_signature}`}
//                             target="_blank"
//                             rel="noopener noreferrer"
//                             whileHover={{ scale: 1.05 }}
//                             whileTap={{ scale: 0.95 }}
//                             className="w-full px-6 py-3 border border-gray-500 text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg font-semibold flex items-center justify-center space-x-2 transition-colors mt-4"
//                         >
//                             <ExternalLink className="w-5 h-5" />
//                             <span>View Solana Commitment</span>
//                         </motion.a>
//                     )}
//                 </div>
//               </motion.div>
//             )}
//           </AnimatePresence>
//         </motion.div>
//       </div>
//     </div>
//   );
// };

// export default Upload;




// pages/Upload.tsx - FIXED VERSION

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Download, ExternalLink, Copy, CheckCircle, Cpu, FileText } from 'lucide-react';
import FileUpload from '../components/ui/FileUpload';
import { SOLANA_EXPLORER_URL } from '../utils/constants';
import { useScrollToTop } from '../hooks/useScrollToTop';

// NOTE: This interface is synchronized with the new backend /upload response
interface UploadResponse {
  success: boolean;
  hash: string; // dataset_hash
  filename: string; // original_filename
  download_ml_url: string; // New: ML-Ready (Encoded/Embedded)
  download_text_url: string; // New: Human-Readable (Imputed Text)
  solana_signature?: string;
  cleaned_rows: number;
  columns: number;
  type: string;
}

const Upload: React.FC = () => {
  const [uploadResult, setUploadResult] = useState<UploadResponse | null>(null);
  const [copied, setCopied] = useState(false);

  useScrollToTop();

  const handleUploadComplete = (result: UploadResponse) => {
    setUploadResult(result);
    // Dispatch event to trigger history refresh
    window.dispatchEvent(new CustomEvent('datasetUploaded'));
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  // FIX: Updated to handle dual downloads and naming convention
  const downloadFile = (url: string, prefix: string, extension: string, mode: string) => {
    const link = document.createElement('a');
    link.href = url;
    // Filename structure: [original_name]_[mode].csv
    const baseName = prefix.replace(/\.[^/.]+$/, ""); // Remove extension
    link.download = `${baseName}_${mode.toUpperCase()}.${extension}`;
    link.click();
  };

  // Prevent rendering tabular UI for audio results, focusing on the dual output for tabular data.
  if (uploadResult && uploadResult.type === 'audio') {
    // Note: A dedicated AudioResults component should be rendered here if necessary.
    return (
      <div className="min-h-screen py-20 px-4 text-center">
        <p className="text-xl text-green-500">Audio Transcription Completed!</p>
        <p className="text-gray-400">Check History for details and Solana proof.</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white dark:bg-black text-black dark:text-white py-20 mb-20 md:mb-20">
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
          {/* NOTE: Ensure FileUpload component uses the correct user ID */}
          <FileUpload 
            onUploadComplete={handleUploadComplete}
            userId={localStorage.getItem('auth_token') ? (JSON.parse(localStorage.getItem('user') || '{}').id || 'demo-user') : 'demo-user'}
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

                <div className="grid md:grid-cols-3 gap-4 text-sm text-gray-600 dark:text-gray-400 mb-6">
                    <div>
                        <FileText className="w-5 h-5 text-cyan-500 mb-1" />
                        <span className="font-medium">Original File:</span> {uploadResult.filename}
                    </div>
                    <div>
                        <span className="font-medium">Cleaned Rows:</span> {uploadResult.cleaned_rows}
                    </div>
                    <div>
                        <span className="font-medium">Final Columns:</span> {uploadResult.columns}
                    </div>
                </div>

                {/* Hash Display */}
                <div className="mb-8">
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Dataset Hash (Solana Proof)
                  </label>
                  <div className="flex items-center space-x-2">
                    <code className="flex-1 px-4 py-2 bg-gray-100 dark:bg-dark-300 rounded-lg font-mono text-sm break-all">
                      {uploadResult.hash}
                    </code>
                    <button
                      onClick={() => copyToClipboard(uploadResult.hash)}
                      className="p-2 hover:bg-gray-200 dark:hover:bg-dark-400 rounded-lg transition-colors"
                      title="Copy Hash"
                    >
                      {copied ? (
                        <CheckCircle className="w-5 h-5 text-green-500" />
                      ) : (
                        <Copy className="w-5 h-5" />
                      )}
                    </button>
                  </div>
                </div>

                {/* Dual Download Actions */}
                <div className="space-y-4">
                    <h4 className="text-lg font-bold flex items-center space-x-2">
                        <Download className="w-5 h-5 text-primary-500" />
                        <span>Download Output Formats</span>
                    </h4>
                    
                    {/* ML READY OUTPUT */}
                    <motion.button
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                        // Use download_ml_url, naming convention is ML
                        onClick={() => downloadFile(uploadResult.download_ml_url, uploadResult.filename, 'csv', 'ML')}
                        className="w-full px-6 py-3 bg-purple-500 hover:bg-purple-600 text-white rounded-lg font-semibold flex items-center justify-center space-x-2 transition-colors"
                    >
                        <Cpu className="w-5 h-5" />
                        <span>Download ML-Ready Output (Encoded/Embedded)</span>
                    </motion.button>
                    
                    {/* HUMAN-READABLE OUTPUT */}
                    <motion.button
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                        // Use download_text_url, naming convention is Text
                        onClick={() => downloadFile(uploadResult.download_text_url, uploadResult.filename, 'csv', 'Text')}
                        className="w-full px-6 py-3 border border-cyan-500 text-cyan-500 hover:bg-cyan-500/10 rounded-lg font-semibold flex items-center justify-center space-x-2 transition-colors"
                    >
                        <FileText className="w-5 h-5" />
                        <span>Download Human-Readable Output (Clean Text)</span>
                    </motion.button>

                    {/* Solana Link */}
                    {uploadResult.solana_signature && (
                        <motion.a
                            href={`${SOLANA_EXPLORER_URL}/tx/${uploadResult.solana_signature}`}
                            target="_blank"
                            rel="noopener noreferrer"
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                            className="w-full px-6 py-3 border border-gray-500 text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg font-semibold flex items-center justify-center space-x-2 transition-colors mt-4"
                        >
                            <ExternalLink className="w-5 h-5" />
                            <span>View Solana Commitment</span>
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