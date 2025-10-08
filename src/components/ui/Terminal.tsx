import React, { useState, useEffect, useMemo, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Terminal as TerminalIcon, Play, Square, Maximize2, Minimize2 } from 'lucide-react';

interface TerminalProps {
  command?: string;
  onCommandComplete?: (output: string) => void;
  autoStart?: boolean;
}

const Terminal: React.FC<TerminalProps> = ({ 
  command = 'keginator upload dataset.csv',
  onCommandComplete,
  autoStart = false
}) => {
  const [isRunning, setIsRunning] = useState(false);
  const [output, setOutput] = useState<string[]>([]);
  const [currentLine, setCurrentLine] = useState(0);
  const [isMaximized, setIsMaximized] = useState(false);
  const terminalRef = useRef<HTMLDivElement>(null);
  const hasAutoStarted = useRef(false);

  const terminalLines = useMemo(() => [
    { text: '$ keginator upload dataset.csv', type: 'command', delay: 0 },
    { text: '>>> Initializing Keginator Data Cleaner v2.1.0', type: 'info', delay: 300 },
    { text: '>>> Python 3.11.5 | pandas 2.1.0 | numpy 1.25.2', type: 'info', delay: 100 },
    { text: '[INFO] Loading dataset: dataset.csv', type: 'info', delay: 200 },
    { text: '[INFO] Detected format: CSV (UTF-8)', type: 'info', delay: 150 },
    { text: '[SCAN] Analyzing 1,247 rows × 15 columns...', type: 'scan', delay: 400 },
    { text: '[CLEAN] Removing duplicate entries... ✓', type: 'success', delay: 350 },
    { text: '  ├─ Found: 23 duplicates', type: 'detail', delay: 100 },
    { text: '  └─ Removed: 23 rows', type: 'detail', delay: 100 },
    { text: '[CLEAN] Fixing data type inconsistencies... ✓', type: 'success', delay: 300 },
    { text: '  ├─ Fixed: 156 type errors', type: 'detail', delay: 100 },
    { text: '  └─ Standardized: 12 date formats', type: 'detail', delay: 100 },
    { text: '[VALIDATE] Running integrity checks... ✓', type: 'success', delay: 400 },
    { text: '[BLOCKCHAIN] Connecting to Solana devnet...', type: 'blockchain', delay: 350 },
    { text: '[BLOCKCHAIN] Generating cryptographic proof... ✓', type: 'blockchain', delay: 500 },
    { text: '[BLOCKCHAIN] Committing to chain... ⛓️', type: 'blockchain', delay: 600 },
    { text: '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━', type: 'separator', delay: 200 },
    { text: '✓ Dataset committed to Solana blockchain!', type: 'success', delay: 300 },
    { text: '📊 Final Stats:', type: 'info', delay: 200 },
    { text: '  • Original rows: 1,247', type: 'stat', delay: 100 },
    { text: '  • Cleaned rows: 1,224', type: 'stat', delay: 100 },
    { text: '  • Quality score: 98.2%', type: 'stat', delay: 100 },
    { text: '🔗 Transaction: 7x8a2b4f...9e3c1d2a', type: 'hash', delay: 200 },
    { text: '🎉 Process complete! Download ready.', type: 'complete', delay: 300 },
  ], []);

  const startSimulation = () => {
    setIsRunning(true);
    setOutput([]);
    setCurrentLine(0);
  };

  const stopSimulation = () => {
    setIsRunning(false);
  };

  const toggleMaximize = () => {
    setIsMaximized(!isMaximized);
  };

  // Auto-start on scroll into view
  useEffect(() => {
    if (!autoStart || hasAutoStarted.current) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting && !hasAutoStarted.current) {
            hasAutoStarted.current = true;
            setTimeout(() => startSimulation(), 500);
          }
        });
      },
      { threshold: 0.3 }
    );

    if (terminalRef.current) {
      observer.observe(terminalRef.current);
    }

    return () => observer.disconnect();
  }, [autoStart]);

  useEffect(() => {
    if (!isRunning || currentLine >= terminalLines.length) {
      if (isRunning && currentLine >= terminalLines.length) {
        setIsRunning(false);
        if (onCommandComplete) {
          onCommandComplete('Simulation completed successfully!');
        }
      }
      return;
    }

    const currentLineData = terminalLines[currentLine];
    const timer = setTimeout(() => {
      setOutput(prev => [...prev, currentLineData.text]);
      setCurrentLine(prev => prev + 1);
    }, currentLineData.delay);

    return () => clearTimeout(timer);
  }, [isRunning, currentLine, terminalLines, onCommandComplete]);

  const getLineStyle = (line: string) => {
    if (line.startsWith('$')) return 'text-cyan-400 font-bold';
    if (line.startsWith('>>>')) return 'text-purple-400';
    if (line.startsWith('[INFO]')) return 'text-blue-400';
    if (line.startsWith('[SCAN]')) return 'text-yellow-400';
    if (line.startsWith('[CLEAN]')) return 'text-green-400';
    if (line.startsWith('[VALIDATE]')) return 'text-emerald-400';
    if (line.startsWith('[BLOCKCHAIN]')) return 'text-orange-400';
    if (line.startsWith('✓') || line.includes('✓')) return 'text-green-400';
    if (line.startsWith('  ├─') || line.startsWith('  └─')) return 'text-gray-500 dark:text-gray-500';
    if (line.startsWith('  •')) return 'text-cyan-300 dark:text-cyan-400';
    if (line.startsWith('━')) return 'text-gray-600 dark:text-gray-600';
    if (line.startsWith('📊') || line.startsWith('🔗') || line.startsWith('🎉')) return 'text-white font-semibold';
    return 'text-gray-300 dark:text-gray-400';
  };

  return (
    <motion.div
      ref={terminalRef}
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className={`relative ${isMaximized ? 'fixed inset-4 z-50' : 'max-w-4xl mx-auto'}`}
    >
      {/* Terminal Window */}
      <div className="bg-[#ffffff] dark:bg-black rounded-lg shadow-2xl border border-gray-500 dark:border-cyan-500/30 overflow-hidden">
        {/* Title Bar */}
        <div className="flex items-center justify-between px-4 py-2 bg-[#ffffff] dark:bg-gray-950 border-b border-gray-200 dark:border-cyan-500/20">
          <div className="flex items-center space-x-3">
            <div className="flex space-x-2">
              <div className="w-3 h-3 rounded-full bg-red-500 hover:bg-red-600 cursor-pointer" onClick={stopSimulation}></div>
              <div className="w-3 h-3 rounded-full bg-yellow-500 hover:bg-yellow-600 cursor-pointer" onClick={toggleMaximize}></div>
              <div className="w-3 h-3 rounded-full bg-green-500 hover:bg-green-600 cursor-pointer" onClick={startSimulation}></div>
            </div>
            <div className="flex items-center space-x-2">
              <TerminalIcon className="w-4 h-4 text-cyan-700 dark:text-cyan-400" />
              <span className="text-sm font-mono text-cyan-900 dark:text-cyan-400">keginator@terminal:~</span>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            {!isRunning ? (
              <motion.button
                onClick={startSimulation}
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                className="p-1.5 rounded hover:bg-green-500/20 transition-colors group"
              >
                <Play className="w-4 h-4 text-green-700 dark:text-green-400 group-hover:text-green-300" />
              </motion.button>
            ) : (
              <motion.button
                onClick={stopSimulation}
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                className="p-1.5 rounded hover:bg-red-500/20 transition-colors group"
              >
                <Square className="w-4 h-4 text-red-400 group-hover:text-red-300" />
              </motion.button>
            )}
            <motion.button
              onClick={toggleMaximize}
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              className="p-1.5 rounded hover:bg-cyan-500/20 transition-colors group"
            >
              {isMaximized ? (
                <Minimize2 className="w-4 h-4 text-cyan-400 group-hover:text-cyan-300" />
              ) : (
                <Maximize2 className="w-4 h-4 text-cyan-400 group-hover:text-cyan-300" />
              )}
            </motion.button>
          </div>
        </div>

        {/* Terminal Content */}
        <div className={`font-mono text-sm ${isMaximized ? 'h-[calc(100vh-8rem)]' : 'h-96'} overflow-y-auto p-4 bg-black/10 dark:bg-black custom-scrollbar`}>
          {/* System Info Banner */}
          <div className="mb-4 pb-4 border-b border-gray-800">
            <div className="text-cyan-400 mb-1">Keginator Data Cleaner v2.1.0</div>
            <div className="text-gray-500 text-xs">Python 3.11.5 | Solana Integration Active</div>
          </div>

          <AnimatePresence>
            {output.map((line, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.2 }}
                className={`mb-1 ${getLineStyle(line)}`}
              >
                {line}
              </motion.div>
            ))}
          </AnimatePresence>

          {/* Blinking Cursor */}
          {isRunning && currentLine < terminalLines.length && (
            <motion.span
              animate={{ opacity: [1, 0] }}
              transition={{ duration: 0.7, repeat: Infinity }}
              className="inline-block w-2 h-4 bg-cyan-400 ml-1"
            />
          )}

          {/* Completion Prompt */}
          {!isRunning && output.length > 0 && currentLine >= terminalLines.length && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="mt-4 pt-4 border-t border-gray-800"
            >
              <span className="text-cyan-400">$ </span>
              <motion.span
                animate={{ opacity: [0.5, 1] }}
                transition={{ duration: 1, repeat: Infinity }}
                className="text-gray-500"
              >
                _
              </motion.span>
            </motion.div>
          )}
        </div>
      </div>

      {/* Scan Line Effect */}
      {isRunning && (
        <motion.div
          initial={{ top: 0 }}
          animate={{ top: '100%' }}
          transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
          className="absolute left-0 right-0 h-px bg-gradient-to-r from-transparent via-cyan-400/50 to-transparent pointer-events-none"
        />
      )}
    </motion.div>
  );
};

export default Terminal;