// import React, { useState, useEffect } from 'react';
// import { motion, AnimatePresence } from 'framer-motion';
// import { Search, Filter, Copy, CheckCircle, ExternalLink, Download, Calendar, FileText } from 'lucide-react';
// import AnimatedCard from '../components/ui/AnimatedCard';
// import { Dataset } from '../types';
// import { SOLANA_EXPLORER_URL } from '../utils/constants';
// import { useScrollToTop } from '../hooks/useScrollToTop';
// import { API_BASE_URL } from '../utils/constants';

// const History: React.FC = () => {
//   const [datasets, setDatasets] = useState<Dataset[]>([]);
//   const [searchTerm, setSearchTerm] = useState('');
//   const [filterStatus, setFilterStatus] = useState<'all' | 'completed' | 'processing' | 'failed'>('all');
//   const [copiedHash, setCopiedHash] = useState<string | null>(null);
//   const [loading, setLoading] = useState(false);
//   const [error, setError] = useState<string | null>(null);

//   useScrollToTop();

//   useEffect(() => {
//     loadHistory();
//   }, []);

//   const loadHistory = async () => {
//   setLoading(true);
//   setError(null);
  
//   try {
//     // Get user ID from localStorage or use demo
//     const user = JSON.parse(localStorage.getItem('user') || '{"id":"demo-user"}');
//     const userId = user.id || 'demo-user';
    
//     // REAL API CALL
//     const response = await fetch(`${API_BASE_URL}/history/${userId}`);
//     const data = await response.json();
    
//     // Transform to match Dataset type
//     const transformedData: Dataset[] = data.datasets.map((d: any) => ({
//       id: d.id,
//       filename: d.filename,
//       originalSize: d.originalSize,
//       cleanedSize: d.cleanedSize,
//       hash: d.hash,
//       timestamp: d.timestamp,
//       solanaTx: d.solanaTx,
//       status: d.status as 'completed' | 'processing' | 'failed'
//     }));
    
//     setDatasets(transformedData);
//   } catch (err) {
//     setError('Failed to load history');
//     console.error('Failed to load history:', err);
//   } finally {
//     setLoading(false);
//   }
// };

//   const copyToClipboard = (hash: string) => {
//     navigator.clipboard.writeText(hash);
//     setCopiedHash(hash);
//     setTimeout(() => setCopiedHash(null), 2000);
//   };

//   const formatFileSize = (bytes: number): string => {
//     if (bytes === 0) return '0 B';
//     const k = 1024;
//     const sizes = ['B', 'KB', 'MB', 'GB'];
//     const i = Math.floor(Math.log(bytes) / Math.log(k));
//     return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
//   };

//   const formatDate = (dateString: string): string => {
//     return new Date(dateString).toLocaleDateString('en-US', {
//       year: 'numeric',
//       month: 'short',
//       day: 'numeric',
//       hour: '2-digit',
//       minute: '2-digit'
//     });
//   };

//   const filteredDatasets = datasets.filter(dataset => {
//     const matchesSearch = dataset.filename.toLowerCase().includes(searchTerm.toLowerCase()) ||
//                          dataset.hash.toLowerCase().includes(searchTerm.toLowerCase());
//     const matchesFilter = filterStatus === 'all' || dataset.status === filterStatus;
//     return matchesSearch && matchesFilter;
//   });

//   const getStatusColor = (status: Dataset['status']) => {
//     switch (status) {
//       case 'completed': return 'text-green-500 bg-green-500/20';
//       case 'processing': return 'text-yellow-500 bg-yellow-500/20';
//       case 'failed': return 'text-red-500 bg-red-500/20';
//       default: return 'text-gray-500 bg-gray-500/20';
//     }
//   };

//   const getStatusIcon = (status: Dataset['status']) => {
//     switch (status) {
//       case 'completed': return <CheckCircle className="w-4 h-4" />;
//       case 'processing': 
//         return (
//           <motion.div
//             animate={{ rotate: 360 }}
//             transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
//             className="w-4 h-4 border-2 border-yellow-500 border-t-transparent rounded-full"
//           />
//         );
//       case 'failed': return <div className="w-4 h-4 bg-red-500 rounded-full" />;
//       default: return <div className="w-4 h-4 bg-gray-500 rounded-full" />;
//     }
//   };

//   return (
//     <div className="min-h-screen  bg-white dark:bg-black text-black dark:text-white py-20 mb-20 md:mb-20">
//       <div className="container mx-auto px-4">
//         <motion.div
//           initial={{ opacity: 0, y: 30 }}
//           animate={{ opacity: 1, y: 0 }}
//           className="text-center mb-12"
//         >
//           <h1 className="text-4xl md:text-5xl font-bold mb-4">Dataset History</h1>
//           <p className="text-xl text-gray-600 dark:text-gray-300">
//             Track your cleaned datasets and blockchain proofs
//           </p>
//         </motion.div>

//         <motion.div
//           initial={{ opacity: 0, y: 20 }}
//           animate={{ opacity: 1, y: 0 }}
//           transition={{ delay: 0.1 }}
//           className="futuristic-card p-6 mb-8"
//         >
//           <div className="flex flex-col md:flex-row gap-4">
//             <div className="flex-1 relative">
//               <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
//               <input
//                 type="text"
//                 placeholder="Search datasets by filename or hash..."
//                 value={searchTerm}
//                 onChange={(e) => setSearchTerm(e.target.value)}
//                 className="w-full pl-10 pr-4 py-3 bg-gray-100 dark:bg-dark-300 rounded-lg border border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
//               />
//             </div>

//             <div className="flex items-center space-x-2">
//               <Filter className="text-gray-400 w-5 h-5" />
//               <select
//                 value={filterStatus}
//                 onChange={(e) => setFilterStatus(e.target.value as any)}
//                 className="px-4 py-3 bg-gray-100 dark:bg-dark-300 rounded-lg border border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
//               >
//                 <option value="all">All Status</option>
//                 <option value="completed">Completed</option>
//                 <option value="processing">Processing</option>
//                 <option value="failed">Failed</option>
//               </select>
//             </div>
//           </div>
//         </motion.div>

//         {loading && (
//           <motion.div
//             initial={{ opacity: 0 }}
//             animate={{ opacity: 1 }}
//             className="text-center py-12"
//           >
//             <motion.div
//               animate={{ rotate: 360 }}
//               transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
//               className="w-12 h-12 border-4 border-primary-500 border-t-transparent rounded-full mx-auto mb-4"
//             />
//             <p className="text-gray-600 dark:text-gray-300">Loading your dataset history...</p>
//           </motion.div>
//         )}

//         {error && (
//           <motion.div
//             initial={{ opacity: 0 }}
//             animate={{ opacity: 1 }}
//             className="futuristic-card p-6 text-center text-red-500 bg-red-500/10 border border-red-500/20"
//           >
//             {error}
//           </motion.div>
//         )}

//         <AnimatePresence>
//           {!loading && !error && (
//             <motion.div
//               initial={{ opacity: 0 }}
//               animate={{ opacity: 1 }}
//               transition={{ delay: 0.2 }}
//               className="grid gap-6"
//             >
//               {filteredDatasets.length === 0 ? (
//                 <AnimatedCard className="text-center py-12">
//                   <FileText className="w-16 h-16 text-gray-400 mx-auto mb-4" />
//                   <h3 className="text-xl font-semibold mb-2">No datasets found</h3>
//                   <p className="text-gray-600 dark:text-gray-400">
//                     {searchTerm || filterStatus !== 'all' 
//                       ? 'Try adjusting your search or filter criteria'
//                       : 'Upload your first dataset to get started'
//                     }
//                   </p>
//                 </AnimatedCard>
//               ) : (
//                 filteredDatasets.map((dataset, index) => (
//                   <AnimatedCard
//                     key={dataset.id}
//                     delay={index * 0.1}
//                     className="p-6 hover:shadow-xl transition-all duration-300"
//                   >
//                     <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
//                       <div className="flex-1">
//                         <div className="flex items-center space-x-3 mb-3">
//                           <FileText className="w-6 h-6 text-primary-500" />
//                           <h3 className="text-lg font-semibold truncate">{dataset.filename}</h3>
//                           <span className={`px-2 py-1 rounded-full text-xs font-medium flex items-center space-x-1 ${getStatusColor(dataset.status)}`}>
//                             {getStatusIcon(dataset.status)}
//                             <span className="capitalize">{dataset.status}</span>
//                           </span>
//                         </div>

//                         <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-gray-600 dark:text-gray-400">
//                           <div className="flex items-center space-x-2">
//                             <Calendar className="w-4 h-4" />
//                             <span>{formatDate(dataset.timestamp)}</span>
//                           </div>
//                           <div>
//                             <span className="font-medium">Size: </span>
//                             {formatFileSize(dataset.originalSize)} → {formatFileSize(dataset.cleanedSize)}
//                           </div>
//                           {dataset.hash && (
//                             <div className="flex items-center space-x-2">
//                               <span className="font-medium">Hash: </span>
//                               <code className="text-xs bg-gray-100 dark:bg-dark-300 px-2 py-1 rounded">
//                                 {dataset.hash.slice(0, 8)}...{dataset.hash.slice(-8)}
//                               </code>
//                             </div>
//                           )}
//                         </div>
//                       </div>

//                       <div className="flex items-center space-x-2">
//                         {dataset.status === 'completed' && dataset.hash && (
//                           <>
//                             <motion.button
//                               whileHover={{ scale: 1.05 }}
//                               whileTap={{ scale: 0.95 }}
//                               onClick={() => copyToClipboard(dataset.hash)}
//                               className="p-2 hover:bg-gray-200 dark:hover:bg-dark-400 rounded-lg transition-colors"
//                               title="Copy hash"
//                             >
//                               {copiedHash === dataset.hash ? (
//                                 <CheckCircle className="w-5 h-5 text-green-500" />
//                               ) : (
//                                 <Copy className="w-5 h-5" />
//                               )}
//                             </motion.button>

//                             {dataset.solanaTx && (
//                               <motion.a
//                                 href={`${SOLANA_EXPLORER_URL}/tx/${dataset.solanaTx}`}
//                                 target="_blank"
//                                 rel="noopener noreferrer"
//                                 whileHover={{ scale: 1.05 }}
//                                 whileTap={{ scale: 0.95 }}
//                                 className="p-2 hover:bg-gray-200 dark:hover:bg-dark-400 rounded-lg transition-colors"
//                                 title="View on Solana Explorer"
//                               >
//                                 <ExternalLink className="w-5 h-5" />
//                               </motion.a>
//                             )}

//                             <motion.button
//                               whileHover={{ scale: 1.05 }}
//                               whileTap={{ scale: 0.95 }}
//                               className="px-4 py-2 bg-cyan-300 dark:bg-[#FFFFff] dark:text-[#000000] hover:bg-cyan-600 !text-[#000000] rounded-lg font-medium flex items-center space-x-2 transition-colors"
//                             >
//                               <Download className="w-4 h-4" />
//                               <span className='!text-[#000000]'>Download</span>
//                             </motion.button>
//                           </>
//                         )}
//                       </div>
//                     </div>
//                   </AnimatedCard>
//                 ))
//               )}
//             </motion.div>
//           )}
//         </AnimatePresence>
//       </div>
//     </div>
//   );
// };

// export default History;


import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, Filter, Copy, CheckCircle, ExternalLink, Download, Calendar, FileText, RefreshCw } from 'lucide-react';
import AnimatedCard from '../components/ui/AnimatedCard';
import { Dataset } from '../types';
import { SOLANA_EXPLORER_URL } from '../utils/constants';
import { useScrollToTop } from '../hooks/useScrollToTop';
import { API_BASE_URL } from '../utils/constants';

const History: React.FC = () => {
  const [datasets, setDatasets] = useState<Dataset[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState<'all' | 'completed' | 'processing' | 'failed'>('all');
  const [copiedHash, setCopiedHash] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useScrollToTop();

  const loadHistory = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const user = JSON.parse(localStorage.getItem('user') || '{"id":"demo-user"}');
      const userId = user.id || 'demo-user';
      
      const response = await fetch(`${API_BASE_URL}/history/${userId}`);
      const data = await response.json();
      
      const transformedData: Dataset[] = data.datasets.map((d: any) => ({
        id: d.id,
        filename: d.filename,
        originalSize: d.originalSize,
        cleanedSize: d.cleanedSize,
        hash: d.hash,
        timestamp: d.timestamp,
        solanaTx: d.solanaTx,
        status: d.status as 'completed' | 'processing' | 'failed'
      }));
      
      setDatasets(transformedData);
    } catch (err) {
      setError('Failed to load history');
      console.error('Failed to load history:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadHistory();
  }, []);

  // AUTO-REFRESH every 25 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      loadHistory();
    }, 25000);
    return () => clearInterval(interval);
  }, []);

  // LISTEN for upload events
  // useEffect(() => {
  //   const handleUploadComplete = () => {
  //     loadHistory();
  //   };
  //   window.addEventListener('datasetUploaded', handleUploadComplete);
  //   return () => window.removeEventListener('datasetUploaded', handleUploadComplete);
  // }, []);

  useEffect(() => {
  const handleUploadComplete = () => {
    loadHistory();
  };

  window.addEventListener('datasetUploaded', handleUploadComplete);

  // ✅ One-liner dispatch
  window.dispatchEvent(new CustomEvent('datasetUploaded'));

  return () => window.removeEventListener('datasetUploaded', handleUploadComplete);
}, []);


  const copyToClipboard = (hash: string) => {
    navigator.clipboard.writeText(hash);
    setCopiedHash(hash);
    setTimeout(() => setCopiedHash(null), 2000);
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const formatDate = (dateString: string): string => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const filteredDatasets = datasets.filter(dataset => {
    const matchesSearch = dataset.filename.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         dataset.hash.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filterStatus === 'all' || dataset.status === filterStatus;
    return matchesSearch && matchesFilter;
  });

  const getStatusColor = (status: Dataset['status']) => {
    switch (status) {
      case 'completed': return 'text-green-500 bg-green-500/20';
      case 'processing': return 'text-yellow-500 bg-yellow-500/20';
      case 'failed': return 'text-red-500 bg-red-500/20';
      default: return 'text-gray-500 bg-gray-500/20';
    }
  };

  const getStatusIcon = (status: Dataset['status']) => {
    switch (status) {
      case 'completed': return <CheckCircle className="w-4 h-4" />;
      case 'processing': 
        return (
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
            className="w-4 h-4 border-2 border-yellow-500 border-t-transparent rounded-full"
          />
        );
      case 'failed': return <div className="w-4 h-4 bg-red-500 rounded-full" />;
      default: return <div className="w-4 h-4 bg-gray-500 rounded-full" />;
    }
  };

  return (
    <div className="min-h-screen  bg-white dark:bg-black text-black dark:text-white py-20 mb-20 md:mb-20">
      <div className="container mx-auto px-4">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl md:text-5xl font-bold mb-4">Dataset History</h1>
          <p className="text-xl text-gray-600 dark:text-gray-300">
            Track your cleaned datasets and blockchain proofs
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="futuristic-card p-6 mb-8"
        >
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="text"
                placeholder="Search datasets by filename or hash..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-3 bg-gray-100 dark:bg-dark-300 rounded-lg border border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
              />
            </div>

            <div className="flex items-center space-x-2">
              <Filter className="text-gray-400 w-5 h-5" />
              <select
                value={filterStatus}
                onChange={(e) => setFilterStatus(e.target.value as any)}
                className="px-4 py-3 bg-gray-100 dark:bg-dark-300 rounded-lg border border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
              >
                <option value="all">All Status</option>
                <option value="completed">Completed</option>
                <option value="processing">Processing</option>
                <option value="failed">Failed</option>
              </select>
            </div>

            <motion.button
              onClick={loadHistory}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="px-4 py-3 bg-cyan-500 hover:bg-cyan-600 text-white rounded-lg font-medium flex items-center space-x-2"
            >
              <RefreshCw className="w-4 h-4" />
              <span>Refresh</span>
            </motion.button>
          </div>
        </motion.div>

        {loading && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center py-12"
          >
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
              className="w-12 h-12 border-4 border-primary-500 border-t-transparent rounded-full mx-auto mb-4"
            />
            <p className="text-gray-600 dark:text-gray-300">Loading your dataset history...</p>
          </motion.div>
        )}

        {error && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="futuristic-card p-6 text-center text-red-500 bg-red-500/10 border border-red-500/20"
          >
            {error}
          </motion.div>
        )}

        <AnimatePresence>
          {!loading && !error && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.2 }}
              className="grid gap-6"
            >
              {filteredDatasets.length === 0 ? (
                <AnimatedCard className="text-center py-12">
                  <FileText className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-xl font-semibold mb-2">No datasets found</h3>
                  <p className="text-gray-600 dark:text-gray-400">
                    {searchTerm || filterStatus !== 'all' 
                      ? 'Try adjusting your search or filter criteria'
                      : 'Upload your first dataset to get started'
                    }
                  </p>
                </AnimatedCard>
              ) : (
                filteredDatasets.map((dataset, index) => (
                  <AnimatedCard
                    key={dataset.id}
                    delay={index * 0.1}
                    className="p-6 hover:shadow-xl transition-all duration-300"
                  >
                    <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3 mb-3">
                          <FileText className="w-6 h-6 text-primary-500" />
                          <h3 className="text-lg font-semibold truncate">{dataset.filename}</h3>
                          <span className={`px-2 py-1 rounded-full text-xs font-medium flex items-center space-x-1 ${getStatusColor(dataset.status)}`}>
                            {getStatusIcon(dataset.status)}
                            <span className="capitalize">{dataset.status}</span>
                          </span>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-gray-600 dark:text-gray-400">
                          <div className="flex items-center space-x-2">
                            <Calendar className="w-4 h-4" />
                            <span>{formatDate(dataset.timestamp)}</span>
                          </div>
                          <div>
                            <span className="font-medium">Size: </span>
                            {formatFileSize(dataset.originalSize)} → {formatFileSize(dataset.cleanedSize)}
                          </div>
                          {dataset.hash && (
                            <div className="flex items-center space-x-2">
                              <span className="font-medium">Hash: </span>
                              <code className="text-xs bg-gray-100 dark:bg-dark-300 px-2 py-1 rounded">
                                {dataset.hash.slice(0, 8)}...{dataset.hash.slice(-8)}
                              </code>
                            </div>
                          )}
                        </div>
                      </div>

                      <div className="flex items-center space-x-2">
                        {dataset.status === 'completed' && dataset.hash && (
                          <>
                            <motion.button
                              whileHover={{ scale: 1.05 }}
                              whileTap={{ scale: 0.95 }}
                              onClick={() => copyToClipboard(dataset.hash)}
                              className="p-2 hover:bg-gray-200 dark:hover:bg-dark-400 rounded-lg transition-colors"
                              title="Copy hash"
                            >
                              {copiedHash === dataset.hash ? (
                                <CheckCircle className="w-5 h-5 text-green-500" />
                              ) : (
                                <Copy className="w-5 h-5" />
                              )}
                            </motion.button>

                            {dataset.solanaTx && (
                              <motion.a
                                href={`${SOLANA_EXPLORER_URL}/tx/${dataset.solanaTx}`}
                                target="_blank"
                                rel="noopener noreferrer"
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                                className="p-2 hover:bg-gray-200 dark:hover:bg-dark-400 rounded-lg transition-colors"
                                title="View on Solana Explorer"
                              >
                                <ExternalLink className="w-5 h-5" />
                              </motion.a>
                            )}

                            <motion.button
                              whileHover={{ scale: 1.05 }}
                              whileTap={{ scale: 0.95 }}
                              className="px-4 py-2 bg-cyan-300 dark:bg-[#FFFFff] dark:text-[#000000] hover:bg-cyan-600 !text-[#000000] rounded-lg font-medium flex items-center space-x-2 transition-colors"
                            >
                              <Download className="w-4 h-4" />
                              <span className='!text-[#000000]'>Download</span>
                            </motion.button>
                          </>
                        )}
                      </div>
                    </div>
                  </AnimatedCard>
                ))
              )}
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

export default History;