import React, { useState, useEffect,  useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Terminal as TerminalIcon, Play, Square } from 'lucide-react';

interface TerminalProps {
  command?: string;
  onCommandComplete?: (output: string) => void;
}

const Terminal: React.FC<TerminalProps> = ({ 
  command = 'keginator upload dataset.csv',
  onCommandComplete 
}) => {
  const [isRunning, setIsRunning] = useState(false);
  const [output, setOutput] = useState<string[]>([]);
  const [currentLine, setCurrentLine] = useState(0);

  const terminalLines = useMemo(() => [
  '$ keginator upload dataset.csv',
  '🔍 Analyzing dataset structure...',
  '🧹 Cleaning 1,247 rows...',
  '✅ Removed 23 duplicate entries',
  '🔧 Fixed 156 formatting issues',
  '📊 Validated data types...',
  '⛓️  Generating Solana proof...',
  '✓ Dataset committed to blockchain!',
  '📄 Hash: 7x8a2b...f9e3c1',
  '🎉 Cleaning complete! Download ready.'
], []); // Wrapped in useMemo


  const startSimulation = () => {
    setIsRunning(true);
    setOutput([]);
    setCurrentLine(0);
  };

  const stopSimulation = () => {
    setIsRunning(false);
  };

  useEffect(() => {
    if (!isRunning || currentLine >= terminalLines.length) {
      if (isRunning && onCommandComplete) {
        onCommandComplete('Simulation completed successfully!');
      }
      return;
    }

    const timer = setTimeout(() => {
      setOutput(prev => [...prev, terminalLines[currentLine]]);
      setCurrentLine(prev => prev + 1);
    }, 500);

    return () => clearTimeout(timer);
  }, [isRunning, currentLine, terminalLines, onCommandComplete]);

  return (
    <div className="terminal-window max-w-2xl mx-auto">
      {/* Terminal Header */}
      <div className="flex items-center justify-between mb-4 p-2 bg-gray-900 rounded-t">
        <div className="flex items-center space-x-2">
          <TerminalIcon className="w-4 h-4 text-green-400" />
          <span className="text-sm font-medium text-white">Keginator CLI</span>
        </div>
        <div className="flex space-x-2">
          {!isRunning ? (
            <button
              onClick={startSimulation}
              className="p-1 rounded hover:bg-green-500/20 transition-colors"
            >
              <Play className="w-4 h-4 text-green-400" />
            </button>
          ) : (
            <button
              onClick={stopSimulation}
              className="p-1 rounded hover:bg-red-500/20 transition-colors"
            >
              <Square className="w-4 h-4 text-red-400" />
            </button>
          )}
        </div>
      </div>

      {/* Terminal Content */}
      <div className="font-mono text-sm h-64 overflow-y-auto p-4 bg-black/50 rounded">
        <AnimatePresence>
          {output.map((line, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.3, delay: index * 0.1 }}
              className="mb-1"
            >
              {line.startsWith('$') ? (
                <span className="text-blue-400">{line}</span>
              ) : line.startsWith('✓') || line.startsWith('✅') ? (
                <span className="text-green-400">{line}</span>
              ) : line.startsWith('❌') ? (
                <span className="text-red-400">{line}</span>
              ) : (
                <span className="text-yellow-400">{line}</span>
              )}
            </motion.div>
          ))}
        </AnimatePresence>

        {/* Cursor */}
        {isRunning && currentLine < terminalLines.length && (
          <motion.div
            animate={{ opacity: [1, 0] }}
            transition={{ duration: 0.5, repeat: Infinity }}
            className="inline-block w-2 h-4 bg-green-400 ml-1"
          />
        )}
      </div>
    </div>
  );
};

export default Terminal;