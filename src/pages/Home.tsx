// // Home.tsx
// import React, { useState, useRef } from 'react';
// import { motion, AnimatePresence } from 'framer-motion';
// import { 
//   ArrowRight, Shield, Zap, Database, Rocket, 
//   Upload, CheckCircle, Cpu, Globe, Lock, Play, 
//   Code, Cloud, Settings,  Wallet,
//   ShieldCheck, Github
// } from 'lucide-react';
// import { Link } from 'react-router-dom';
// import Terminal from '../components/ui/Terminal';

// const Home: React.FC = () => {
//   // const [isLoaded, setIsLoaded] = useState(false);
//   const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
//   const gridRef = useRef<HTMLDivElement>(null);
//   const terminalRef = useRef<HTMLDivElement>(null);


//   // useEffect(() => {
//   //   setIsLoaded(true);
//   // }, []);
//   const companies = [
//   {
//     name: "Solana",
//     logo: "/sol.png",
//   },
//   {
//     name: "Chainlink",
//     logo: "/cha.png",
//   },
//   {
//     name: "Serum",
//     logo: "/ser.png",
//   },
//   {
//     name: "Raydium",
//     logo: "/ray.png",
//   },
//   {
//     name: "Magic Eden",
//     logo: "/med.png",
//   },
//   {
//     name: "OpenSea",
//     logo: "/os.png",
//   },
// ];

//   // CODEX Grid Background with hover interaction
//   const CodexGrid = () => {
//     const handleMouseMove = (e: React.MouseEvent) => {
//       if (gridRef.current) {
//         const rect = gridRef.current.getBoundingClientRect();
//         setMousePosition({
//           x: e.clientX - rect.left,
//           y: e.clientY - rect.top
//         });
//       }
//     };

//     return (
//       <div 
//         ref={gridRef}
//         className="fixed inset-0 pointer-events-none z-0 opacity-20 dark:opacity-40"
//         onMouseMove={handleMouseMove}
//       >
//         {/* Base Grid */}
//         <div 
//           className="absolute inset-0 dark:block hidden"
//           style={{
//             backgroundImage: `
//               linear-gradient(rgba(120, 120, 120, 0.15) 1px, transparent 1px),
//               linear-gradient(90deg, rgba(120, 120, 120, 0.15) 1px, transparent 1px)
//             `,
//             backgroundSize: '30px 30px',
//             backgroundPosition: 'center center'
//           }}
//         />
        
//         {/* Light mode grid */}
//         <div 
//           className="absolute inset-0 dark:hidden block"
//           style={{
//             backgroundImage: `
//               linear-gradient(rgba(200, 200, 200, 0.3) 1px, transparent 1px),
//               linear-gradient(90deg, rgba(200, 200, 200, 0.3) 1px, transparent 1px)
//             `,
//             backgroundSize: '30px 30px',
//             backgroundPosition: 'center center'
//           }}
//         />
        
//         {/* Animated Grid Lines */}
//         <motion.div
//           className="absolute inset-0"
//           style={{
//             backgroundImage: `
//               linear-gradient(90deg, transparent 0%, rgba(70, 130, 180, 0.3) 50%, transparent 100%)
//             `,
//             backgroundSize: '200% 100%',
//           }}
//           animate={{
//             backgroundPosition: ['200% 0', '-200% 0']
//           }}
//           transition={{
//             duration: 8,
//             repeat: Infinity,
//             ease: "linear"
//           }}
//         />
        
//         {/* Hover Effect */}
//         <motion.div
//           className="absolute w-64 h-64 bg-blue-500/5 dark:bg-blue-500/10 rounded-full blur-xl"
//           animate={{
//             x: mousePosition.x - 128,
//             y: mousePosition.y - 128,
//           }}
//           transition={{ type: "tween", ease: "backOut", duration: 0.5 }}
//         />
//       </div>
//     );
//   };

//   // Binary Rain Effect
//   const BinaryRain = () => (
//     <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
//       {[...Array(50)].map((_, i) => (
//         <motion.div
//           key={i}
//           className="absolute text-xs font-mono text-blue-400/30 dark:text-blue-400/50"
//           initial={{
//             x: Math.random() * window.innerWidth,
//             y: -20,
//             opacity: 0,
//           }}
//           animate={{
//             y: window.innerHeight + 20,
//             opacity: [0, 1, 0],
//           }}
//           transition={{
//             duration: Math.random() * 3 + 2,
//             repeat: Infinity,
//             delay: Math.random() * 5,
//             ease: "linear",
//           }}
//         >
//           {Math.random() > 0.5 ? '1' : '0'}
//         </motion.div>
//       ))}
//     </div>
//   );

//   // Metallic Border Component
//   const MetallicBorder = ({ isActive = false }: { isActive?: boolean }) => (
//     <div className="absolute inset-0 rounded-lg overflow-hidden pointer-events-none">
//       {/* Base metallic border */}
//       <div 
//         className="absolute inset-0 rounded-lg border"
//         style={{
//           borderColor: 'rgba(100, 100, 100, 0.3)',
//           background: 'linear-gradient(135deg, rgba(100, 100, 100, 0.1), rgba(70, 130, 180, 0.05))'
//         }}
//       />
      
//       {/* Corner accents */}
//       <div className="absolute top-0 left-0 w-3 h-3 border-t border-l border-cyan-600 dark:border-cyan-400" />
//       <div className="absolute top-0 right-0 w-3 h-3 border-t border-r border-cyan-600 dark:border-cyan-400" />
//       <div className="absolute bottom-0 left-0 w-3 h-3 border-b border-l border-cyan-600 dark:border-cyan-400" />
//       <div className="absolute bottom-0 right-0 w-3 h-3 border-b border-r border-cyan-600 dark:border-cyan-400" />
      
//       {/* Active state */}
//       <AnimatePresence>
//         {isActive && (
//           <motion.div
//             initial={{ opacity: 0 }}
//             animate={{ opacity: 1 }}
//             exit={{ opacity: 0 }}
//             className="absolute inset-0 rounded-lg border border-blue-500 dark:border-blue-400 shadow-lg shadow-blue-500/20 dark:shadow-blue-400/20"
//           />
//         )}
//       </AnimatePresence>
//     </div>
//   );

//   // Enhanced Feature Card with CODEX design
//   interface FeatureCardProps {
//     icon: React.ReactNode;
//     title: string;
//     description: string;
//     delay?: number;
//     features: string[];
//   }

//   const FeatureCard: React.FC<FeatureCardProps> = ({ icon, title, description, delay = 0, features }) => {
//     const [isHovered, setIsHovered] = useState(false);

//     return (
//       <motion.div
//         initial={{ opacity: 0, y: 50 }}
//         animate={{ opacity: 1, y: 0 }}
//         transition={{ duration: 0.8, delay }}
//         whileHover={{ 
//           scale: 1.02,
//           y: -5,
//         }}
//         onHoverStart={() => setIsHovered(true)}
//         onHoverEnd={() => setIsHovered(false)}
//         className="relative p-6 group cursor-pointer bg-white/80 dark:bg-black/40 backdrop-blur-sm rounded-lg border border-gray-300/50 dark:border-gray-800/50 shadow-lg dark:shadow-none"
//         style={{ fontFamily: 'JetBrains Mono, monospace' }}
//       >
//         <MetallicBorder isActive={isHovered} />
        
//         <div className="flex justify-center mb-4">
//           <div 
//             className="p-3 rounded-lg border border-blue-600/30 dark:border-blue-400/30"
//             style={{ 
//               background: 'linear-gradient(135deg, rgba(70, 130, 180, 0.1), rgba(232, 232, 232, 0.05))'
//             }}
//           >
//             {icon}
//           </div>
//         </div>
        
//         <h3 className="text-xl font-bold mb-3 text-center text-blue-700 dark:text-blue-400">
//           {title}
//         </h3>
//         <p className="text-gray-700 dark:text-gray-300 leading-relaxed mb-4 text-sm">
//           {description}
//         </p>
        
//         <div className="space-y-2">
//           {features.map((feature, index) => (
//             <motion.div
//               key={index}
//               initial={{ opacity: 0, x: -20 }}
//               animate={{ opacity: 1, x: 0 }}
//               transition={{ delay: delay + index * 0.1 }}
//               className="flex items-center space-x-2 text-xs text-gray-800 dark:text-gray-200"
//             >
//               <div className="w-1.5 h-1.5 bg-blue-500 dark:bg-blue-400 rounded-full" />
//               <span>{feature}</span>
//             </motion.div>
//           ))}
//         </div>
//       </motion.div>
//     );
//   };

//   // Stats Section
//   const StatsSection = () => (
//     <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-16">
//       {[
//         { number: '50K+', label: 'Datasets Processed', icon: <Database className="w-5 h-5" /> },
//         { number: '99.97%', label: 'Accuracy Rate', icon: <Shield className="w-5 h-5" /> },
//         { number: '1.8s', label: 'Avg Processing', icon: <Zap className="w-5 h-5" /> },
//         { number: '24/7', label: 'Blockchain Secured', icon: <Lock className="w-5 h-5" /> }
//       ].map((stat, index) => (
//         <motion.div
//           key={stat.label}
//           initial={{ opacity: 0, scale: 0.5 }}
//           animate={{ opacity: 1, scale: 1 }}
//           transition={{ duration: 0.5, delay: index * 0.1 }}
//           whileHover={{ scale: 1.05 }}
//           className="relative p-4 text-center bg-white/80 dark:bg-black/40 backdrop-blur-sm rounded-lg border border-gray-300/50 dark:border-gray-800/50 shadow-lg dark:shadow-none"
//         >
//           <MetallicBorder />
//           <div className="flex justify-center mb-2 text-blue-600 dark:text-blue-400">
//             {stat.icon}
//           </div>
//           <div className="text-lg font-bold mb-1 text-gray-900 dark:text-gray-100">{stat.number}</div>
//           <div className="text-xs text-gray-600 dark:text-gray-400">{stat.label}</div>
//         </motion.div>
//       ))}
//     </div>
//   );

//   // Trusted Companies Section
//   const CompaniesSection = () => (
//   <section className="relative py-16">
//     <div className="container mx-auto px-4">
//       <motion.div
//         initial={{ opacity: 0 }}
//         whileInView={{ opacity: 1 }}
//         transition={{ duration: 0.8 }}
//         className="text-center mb-12"
//       >
//         <h3 className="text-lg font-semibold text-gray-600 dark:text-gray-400 mb-4">
//           TRUSTED BY INDUSTRY LEADERS
//         </h3>
//       </motion.div>

//       <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-8 items-center opacity-90">
//         {companies.map((company, index) => (
//           <motion.div
//             key={company.name}
//             initial={{ opacity: 0, y: 20 }}
//             whileInView={{ opacity: 1, y: 0 }}
//             transition={{ delay: index * 0.1 }}
//             className="flex flex-col items-center justify-center p-4 bg-white/50 dark:bg-black/30 rounded-lg border border-gray-300/30 dark:border-gray-800/30 shadow-md hover:shadow-lg transition-shadow"
//           >
//             <img
//               src={company.logo}
//               alt={`${company.name} logo`}
//               className="w-10 h-10 object-contain mb-2"
//             />
//             <div className="text-gray-900 dark:text-white font-semibold text-sm">
//               {company.name}
//             </div>
//           </motion.div>
//         ))}
//       </div>
//     </div>
//   </section>
// );

//   // Integration Tools Section
//   const IntegrationSection = () => (
//     <section className="relative py-20">
//       <div className="container mx-auto px-4">
//         <motion.div
//           initial={{ opacity: 0 }}
//           whileInView={{ opacity: 1 }}
//           transition={{ duration: 0.8 }}
//           className="text-center mb-16"
//         >
//           <h2 className="text-3xl font-bold mb-6 text-gray-900 dark:text-gray-100">
//             SEAMLESS INTEGRATION
//           </h2>
//           <p className="text-sm text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
//             Works with your favorite tools and platforms
//           </p>
//         </motion.div>

//         <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
//           {[
//             { name: 'VS Code', icon: <Code className="w-8 h-8" />, description: 'IDE Extension' },
//             { name: 'GitHub', icon: <Github className="w-8 h-8" />, description: 'CI/CD Pipelines' },
//             { name: 'Docker', icon: <Settings className="w-8 h-8" />, description: 'Container Ready' },
//             { name: 'AWS', icon: <Cloud className="w-8 h-8" />, description: 'Cloud Native' },
//           ].map((tool, index) => (
//             <motion.div
//               key={tool.name}
//               initial={{ opacity: 0, scale: 0.9 }}
//               whileInView={{ opacity: 1, scale: 1 }}
//               transition={{ delay: index * 0.1 }}
//               whileHover={{ scale: 1.05 }}
//               className="text-center p-6 bg-white/80 dark:bg-black/40 backdrop-blur-sm rounded-lg border border-gray-300/50 dark:border-gray-800/50 shadow-lg dark:shadow-none"
//             >
//               <div className="text-blue-600 dark:text-blue-400 mb-3 flex justify-center">{tool.icon}</div>
//               <h4 className="font-bold text-gray-900 dark:text-white mb-2">{tool.name}</h4>
//               <p className="text-xs text-gray-600 dark:text-gray-400">{tool.description}</p>
//             </motion.div>
//           ))}
//         </div>
//       </div>
//     </section>
//   );

//   // Use Cases Section
//   const UseCasesSection = () => (
//     <section className="relative py-20">
//       <div className="container mx-auto px-4">
//         <motion.div
//           initial={{ opacity: 0 }}
//           whileInView={{ opacity: 1 }}
//           transition={{ duration: 0.8 }}
//           className="text-center mb-16"
//         >
//           <h2 className="text-3xl font-bold mb-6 text-gray-900 dark:text-gray-100">
//             ENTERPRISE USE CASES
//           </h2>
//           <p className="text-sm text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
//             Powering data integrity across industries
//           </p>
//         </motion.div>

//         <div className="grid md:grid-cols-3 gap-8">
//           {[
//             {
//               title: "Financial Services",
//               description: "Audit trails and compliance reporting with immutable blockchain verification",
//               features: ["Regulatory Compliance", "Audit Trails", "Fraud Detection"],
//               icon: <Wallet className="w-6 h-6" />
//             },
//             {
//               title: "Healthcare",
//               description: "Secure patient data processing with HIPAA-compliant blockchain proofs",
//               features: ["HIPAA Compliance", "Patient Data Integrity", "Research Validation"],
//               icon: <ShieldCheck className="w-6 h-6" />
//             },
//             {
//               title: "Supply Chain",
//               description: "Track and verify product data across global supply chains",
//               features: ["Product Provenance", "Quality Assurance", "Logistics Tracking"],
//               icon: <Globe className="w-6 h-6" />
//             }
//           ].map((usecase, index) => (
//             <motion.div
//               key={usecase.title}
//               initial={{ opacity: 0, y: 30 }}
//               whileInView={{ opacity: 1, y: 0 }}
//               transition={{ delay: index * 0.2 }}
//               className="p-6 bg-white/80 dark:bg-black/40 backdrop-blur-sm rounded-lg border border-gray-300/50 dark:border-gray-800/50 shadow-lg dark:shadow-none"
//             >
//               <div className="text-blue-600 dark:text-blue-400 mb-4 flex justify-center">
//                 {usecase.icon}
//               </div>
//               <h3 className="text-xl font-bold mb-3 text-center text-blue-700 dark:text-blue-400">
//                 {usecase.title}
//               </h3>
//               <p className="text-gray-700 dark:text-gray-300 text-sm mb-4 text-center">
//                 {usecase.description}
//               </p>
//               <div className="space-y-2">
//                 {usecase.features.map((feature, featureIndex) => (
//                   <div key={featureIndex} className="flex items-center space-x-2 text-xs text-gray-600 dark:text-gray-400">
//                     <div className="w-1.5 h-1.5 bg-blue-500 dark:bg-blue-400 rounded-full" />
//                     <span>{feature}</span>
//                   </div>
//                 ))}
//               </div>
//             </motion.div>
//           ))}
//         </div>
//       </div>
//     </section>
//   );

//   // Pricing Preview Section
//   const PricingPreview = () => (
//     <section className="relative py-20">
//       <div className="container mx-auto px-4">
//         <motion.div
//           initial={{ opacity: 0 }}
//           whileInView={{ opacity: 1 }}
//           transition={{ duration: 0.8 }}
//           className="text-center mb-16"
//         >
//           <h2 className="text-3xl font-bold mb-6 text-gray-900 dark:text-gray-100">
//             SIMPLE PRICING
//           </h2>
//           <p className="text-sm text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
//             Start free, scale as you grow
//           </p>
//         </motion.div>

//         <div className="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
//           {[
//             {
//               name: "Starter",
//               price: "Free",
//               description: "Perfect for individuals and small projects",
//               features: ["1GB Processing", "Basic Cleaning", "Community Support"]
//             },
//             {
//               name: "Professional",
//               price: "$49",
//               description: "For growing teams and businesses",
//               features: ["100GB Processing", "AI-Powered Cleaning", "Priority Support", "API Access"]
//             },
//             {
//               name: "Enterprise",
//               price: "Custom",
//               description: "For large organizations with custom needs",
//               features: ["Unlimited Processing", "Custom AI Models", "Dedicated Support", "SLA Guarantee"]
//             }
//           ].map((plan, index) => (
//             <motion.div
//               key={plan.name}
//               initial={{ opacity: 0, y: 30 }}
//               whileInView={{ opacity: 1, y: 0 }}
//               transition={{ delay: index * 0.1 }}
//               className="p-6 bg-white/80 dark:bg-black/40 backdrop-blur-sm rounded-lg border border-gray-300/50 dark:border-gray-800/50 shadow-lg dark:shadow-none"
//             >
//               <h3 className="text-xl font-bold mb-2 text-gray-900 dark:text-white">{plan.name}</h3>
//               <div className="text-2xl font-bold mb-4 text-blue-600 dark:text-blue-400">{plan.price}</div>
//               <p className="text-gray-600 dark:text-gray-400 text-sm mb-6">{plan.description}</p>
//               <div className="space-y-3">
//                 {plan.features.map((feature, featureIndex) => (
//                   <div key={featureIndex} className="flex items-center space-x-2 text-sm text-gray-700 dark:text-gray-300">
//                     <CheckCircle className="w-4 h-4 text-green-500" />
//                     <span>{feature}</span>
//                   </div>
//                 ))}
//               </div>
//             </motion.div>
//           ))}
//         </div>
//       </div>
//     </section>
//   );

//   return (
//     <div className="min-h-screen bg-white dark:bg-black overflow-hidden relative" style={{ fontFamily: 'JetBrains Mono, monospace' }}>
//       <CodexGrid />
//       <BinaryRain />

//       {/* Hero Section */}
//       <section className="relative min-h-screen flex items-center justify-center pt-20">
//         <div className="container mx-auto px-4 text-center relative z-10">
//           <motion.div
//             initial={{ opacity: 0, y: 50 }}
//             animate={{ opacity: 1, y: 0 }}
//             transition={{ duration: 1 }}
//             className="mb-8"
//           >
//             <motion.h1
//               initial={{ opacity: 0, scale: 0.5 }}
//               animate={{ opacity: 1, scale: 1 }}
//               transition={{ duration: 0.8 }}
//               className="text-5xl md:text-7xl font-black mb-6 tracking-tighter text-gray-900 dark:text-gray-100"
//             >
//               KEGINATOR
//             </motion.h1>
            
//             <motion.p
//               initial={{ opacity: 0 }}
//               animate={{ opacity: 1 }}
//               transition={{ delay: 0.5, duration: 1 }}
//               className="text-lg md:text-xl mb-8 max-w-4xl mx-auto leading-relaxed text-blue-700 dark:text-blue-400"
//             >
//               THE DATA INTEGRITY PROTOCOL
//             </motion.p>

//             <motion.p
//               initial={{ opacity: 0 }}
//               animate={{ opacity: 1 }}
//               transition={{ delay: 0.8, duration: 1 }}
//               className="text-sm text-gray-600 dark:text-gray-400 mb-12 max-w-2xl mx-auto"
//             >
//               Enterprise-grade data cleaning meets blockchain verification. Process, clean, and verify datasets with immutable proof on Solana.
//             </motion.p>
//           </motion.div>

//           <motion.div
//             initial={{ opacity: 0, y: 30 }}
//             animate={{ opacity: 1, y: 0 }}
//             transition={{ duration: 0.8, delay: 1 }}
//             className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-16"
//           >
//             <Link to="/upload">
//               <motion.button
//                 whileHover={{ scale: 1.05 }}
//                 whileTap={{ scale: 0.95 }}
//                 className="px-8 py-3 rounded-lg font-bold text-sm flex items-center space-x-2 transition-all duration-300 bg-cyan-300 border-cyan-600 dark:bg-[#FFFFff] dark:text-[#000000] dark:border-blue-400 hover:bg-cyan-300 text-[#000000] shadow-lg"
//               >
//                 <Rocket className="w-4 h-4" />
//                 <span className='!text-[#000000]'>LAUNCH KEGINATOR</span>
//                 <ArrowRight className="w-4 h-4" />
//               </motion.button>
//             </Link>
            
//             <motion.button
//               whileHover={{ scale: 1.05 }}
//               whileTap={{ scale: 0.95 }}
//               className="px-8 py-3 border border-blue-600 dark:border-blue-400 rounded-lg font-bold text-sm flex items-center space-x-2 transition-all duration-300 text-blue-600 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20"
//               onClick={() => terminalRef.current?.scrollIntoView({ behavior: 'smooth' })}
//             >
//               <Play className="w-4 h-4" />
//               <span>WATCH DEMO</span>
//             </motion.button>
//           </motion.div>

//           <StatsSection />
//         </div>
//       </section>

//       <CompaniesSection />

//       {/* Features Grid - Modern Layout */}
// <section className="relative py-20">
//   <div className="container mx-auto px-4">
//     <motion.div
//       initial={{ opacity: 0 }}
//       whileInView={{ opacity: 1 }}
//       transition={{ duration: 0.8 }}
//       className="text-center mb-16"
//     >
//       <h2 className="text-3xl font-bold mb-6 text-gray-900 dark:text-gray-100">
//         ENTERPRISE DATA PLATFORM
//       </h2>
//       <p className="text-sm text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
//         Everything you need for data integrity, cleaning, and blockchain verification in one platform.
//       </p>
//     </motion.div>

//     {/* Interactive Feature Matrix */}
//     <div className="relative max-w-6xl mx-auto">
//       {/* Animated Background Grid */}
      
//       <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 relative">
//         {/* Left Side - Feature Showcase */}
//         <div className="space-y-6">
//           {[
//             {
//               icon: <Zap className="w-5 h-5" />,
//               title: "AI-Powered Cleaning",
//               description: "Advanced ML algorithms detect and fix data quality issues in real-time",
//               stats: "99.7% Accuracy",
//               color: "text-purple-500"
//             },
//             {
//               icon: <Shield className="w-5 h-5" />,
//               title: "Blockchain Verification",
//               description: "Immutable Solana proofs with instant verification",
//               stats: "1.2s Average",
//               color: "text-green-500"
//             },
//             {
//               icon: <Database className="w-5 h-5" />,
//               title: "Multi-Format Support",
//               description: "All major formats with intelligent detection",
//               stats: "15+ Formats",
//               color: "text-blue-500"
//             }
//           ].map((feature, index) => (
//             <motion.div
//               key={feature.title}
//               initial={{ opacity: 0, x: -20 }}
//               whileInView={{ opacity: 1, x: 0 }}
//               transition={{ duration: 0.6, delay: index * 0.15 }}
//               whileHover={{ x: 10 }}
//               className="group p-6 rounded-2xl bg-white/40 dark:bg-gray-900/30 backdrop-blur-sm border border-gray-200/30 dark:border-gray-700/30 hover:border-gray-300/50 dark:hover:border-gray-600/50 transition-all duration-300 cursor-pointer"
//             >
//               <div className="flex items-center justify-between">
//                 <div className="flex items-center space-x-4">
//                   <div className={`${feature.color} group-hover:scale-110 transition-transform duration-300`}>
//                     {feature.icon}
//                   </div>
//                   <div>
//                     <h3 className="font-bold text-gray-900 dark:text-white text-lg">
//                       {feature.title}
//                     </h3>
//                     <p className="text-sm text-gray-600 dark:text-gray-300 mt-1">
//                       {feature.description}
//                     </p>
//                   </div>
//                 </div>
//                 <div className={`text-xs font-bold px-3 py-1 rounded-full bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 border border-gray-200 dark:border-gray-700`}>
//                   {feature.stats}
//                 </div>
//               </div>
//             </motion.div>
//           ))}
//         </div>

//         {/* Right Side - Feature Showcase */}
//         <div className="space-y-6">
//           {[
//             {
//               icon: <Cpu className="w-5 h-5" />,
//               title: "Real-time Processing",
//               description: "Sub-second latency with real-time streaming capabilities",
//               stats: "0.8s Latency",
//               color: "text-indigo-500"
//             },
//             {
//               icon: <Globe className="w-5 h-5" />,
//               title: "Global Infrastructure",
//               description: "15 regions worldwide with 99.9% uptime guarantee",
//               stats: "99.9% Uptime",
//               color: "text-teal-500"
//             },
//             {
//               icon: <Lock className="w-5 h-5" />,
//               title: "Enterprise Security",
//               description: "Military-grade encryption and zero-trust architecture",
//               stats: "SOC 2 Compliant",
//               color: "text-amber-500"
//             }
//           ].map((feature, index) => (
//             <motion.div
//               key={feature.title}
//               initial={{ opacity: 0, x: 20 }}
//               whileInView={{ opacity: 1, x: 0 }}
//               transition={{ duration: 0.6, delay: index * 0.15 }}
//               whileHover={{ x: -10 }}
//               className="group p-6 rounded-2xl bg-white/40 dark:bg-gray-900/30 backdrop-blur-sm border border-gray-200/30 dark:border-gray-700/30 hover:border-gray-300/50 dark:hover:border-gray-600/50 transition-all duration-300 cursor-pointer"
//             >
//               <div className="flex items-center justify-between">
//                 <div className="flex items-center space-x-4">
//                   <div className={`${feature.color} group-hover:scale-110 transition-transform duration-300`}>
//                     {feature.icon}
//                   </div>
//                   <div>
//                     <h3 className="font-bold text-gray-900 dark:text-white text-lg">
//                       {feature.title}
//                     </h3>
//                     <p className="text-sm text-gray-600 dark:text-gray-300 mt-1">
//                       {feature.description}
//                     </p>
//                   </div>
//                 </div>
//                 <div className={`text-xs font-bold px-3 py-1 rounded-full bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 border border-gray-200 dark:border-gray-700`}>
//                   {feature.stats}
//                 </div>
//               </div>
//             </motion.div>
//           ))}
//         </div>
//       </div>

      
//     </div>
//       </div>
// </section>
//       <IntegrationSection />
//       <UseCasesSection />

//       {/* Terminal Demo Section */}
//       <section ref={terminalRef} className="relative py-20">
//         <div className="container mx-auto px-4">
//           <motion.div
//             initial={{ opacity: 0 }}
//             whileInView={{ opacity: 1 }}
//             transition={{ duration: 0.8 }}
//             className="text-center mb-16"
//           >
//             <h2 className="text-3xl font-bold mb-6 text-gray-900 dark:text-gray-100">
//               EXPERIENCE THE POWER
//             </h2>
//             <p className="text-sm text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
//               See Keginator in action with our interactive terminal demo.
//             </p>
//           </motion.div>
          
//           <motion.div
//             initial={{ opacity: 0, scale: 0.9 }}
//             whileInView={{ opacity: 1, scale: 1 }}
//             transition={{ duration: 0.8 }}
//             className="max-w-4xl mx-auto"
//           >
//             <Terminal />
//           </motion.div>
//         </div>
//       </section>

//       <PricingPreview />

//       {/* Final CTA Section */}
//       <section className="relative py-20 mb-20 md:mb-20">
//         <div className="container mx-auto px-4 text-center">
//           <motion.div
//             initial={{ opacity: 0, y: 50 }}
//             whileInView={{ opacity: 1, y: 0 }}
//             transition={{ duration: 0.8 }}
//             className="relative p-8 max-w-3xl mx-auto bg-white/80 dark:bg-black/40 backdrop-blur-sm rounded-lg border border-gray-300/50 dark:border-gray-800/50 shadow-lg dark:shadow-none"
//           >
//             <MetallicBorder isActive={true} />
            
//             <h2 className="text-2xl md:text-4xl font-bold mb-6 text-gray-900 dark:text-gray-100">
//               READY TO TRANSFORM YOUR DATA?
//             </h2>
//             <p className="text-sm text-gray-700 dark:text-gray-300 mb-8 max-w-2xl mx-auto">
//               Join thousands of data professionals who trust Keginator for blockchain-verified data integrity.
//             </p>
//             <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
//               <Link to="/upload">
//                 <motion.button
//                   whileHover={{ scale: 1.05 }}
//                   whileTap={{ scale: 0.95 }}
//                   className="px-8 py-3 rounded-lg font-bold text-sm flex items-center space-x-2 transition-all duration-300 bg-cyan-300 border-cyan-600 dark:bg-[#FFFFff] dark:text-[#000000] dark:border-blue-400 hover:bg-cyan-300 text-[#000000] shadow-lg"
//                 >
//                   <Upload className="w-4 h-4" />
//                   <span className='!text-[#000000]'>UPLOAD DATASET</span>
//                 </motion.button>
//               </Link>
//               <Link to="/verify">
//                 <motion.button
//                   whileHover={{ scale: 1.05 }}
//                   whileTap={{ scale: 0.95 }}
//                   className="px-8 py-3 border border-blue-600 dark:border-blue-400 rounded-lg font-bold text-sm flex items-center space-x-2 transition-all duration-300 text-blue-600 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20"
//                 >
//                   <CheckCircle className="w-4 h-4" />
//                   <span>VERIFY DATA</span>
//                 </motion.button>
//               </Link>
//             </div>
//           </motion.div>
//         </div>
//       </section>
//     </div>
//   );
// };

// export default Home;


// src/pages/Home.tsx - IMPLEMENTED: Rolling Text, Glitch, High-Contrast Style on Original Code
import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowRight, Shield, Zap, Database, Rocket, 
  Upload, CheckCircle, Cpu, Globe, Lock, Play, 
  Code, Cloud, Settings, Wallet,
  ShieldCheck, Github
} from 'lucide-react';
import { Link } from 'react-router-dom';
import Terminal from '../components/ui/Terminal';

// --- NEW: Rolling Text Component (The "speedometer" effect) ---
const SYMBOLS = '!@#$%^&*()_+{}:"<>?|~`-=[]\\;,./';

interface RollingTextProps {
    text: string;
    duration?: number;
    delay?: number;
    className?: string;
}

const RollingText: React.FC<RollingTextProps> = ({ text, duration = 1.5, delay = 0.5, className = '' }) => {
    const [scrambledText, setScrambledText] = useState<string>(text.split('').map(() => SYMBOLS[Math.floor(Math.random() * SYMBOLS.length)]).join(''));
    const intervalRef = useRef<number | null>(null);
    const finalCharacters = text.split('');
    const symbolsLength = SYMBOLS.length;

    useEffect(() => {
        const startTimestamp = Date.now();
        const revealTime = duration * 1000;

        const animate = () => {
            const elapsedTime = Date.now() - startTimestamp;
            const progress = Math.min(elapsedTime / revealTime, 1);
            
            const newText = finalCharacters.map((char, index) => {
                // Characters are revealed one by one
                if (index < Math.floor(progress * finalCharacters.length)) {
                    return char;
                }
                // Scramble the rest, prioritizing final characters near the end
                if (Math.random() > progress * 0.8) {
                    return SYMBOLS[Math.floor(Math.random() * symbolsLength)];
                }
                return char;
            }).join('');
            
            setScrambledText(newText);

            if (progress === 1) {
                if (intervalRef.current !== null) {
                    clearInterval(intervalRef.current);
                }
                setScrambledText(text); // Ensure final text is set
            }
        };

        const startAnimation = () => {
            intervalRef.current = setInterval(animate, 50) as unknown as number;
        };

        const timeout = setTimeout(startAnimation, delay * 1000);

        return () => {
            if (intervalRef.current !== null) {
                clearInterval(intervalRef.current);
            }
            clearTimeout(timeout);
        };
    }, [text, duration, delay, finalCharacters, symbolsLength]);

    // Use GlitchText style wrapper
    return (
        <span className={`glitch ${className}`} data-text={scrambledText}>
            {scrambledText}
        </span>
    );
};
// --- END: Rolling Text Component ---

// Glitch Text Component (used for the H1 style)
const GlitchText: React.FC<{ children: React.ReactNode, className?: string, 'data-text'?: string }> = ({ children, className = '', ...props }) => (
    <div className={`glitch ${className}`} {...props}>
        {children}
    </div>
);


const Home: React.FC = () => {
  // const [isLoaded, setIsLoaded] = useState(false);
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const gridRef = useRef<HTMLDivElement>(null);
  const terminalRef = useRef<HTMLDivElement>(null);


  // useEffect(() => {
  //   setIsLoaded(true);
  // }, []);
  const companies = [
  {
    name: "Solana",
    logo: "/sol.png",
  },
  {
    name: "Chainlink",
    logo: "/cha.png",
  },
  {
    name: "Serum",
    logo: "/ser.png",
  },
  {
    name: "Raydium",
    logo: "/ray.png",
  },
  {
    name: "Magic Eden",
    logo: "/med.png",
  },
  {
    name: "OpenSea",
    logo: "/os.png",
  },
];

  // CODEX Grid Background with hover interaction - UPDATED for Solana colors
  const CodexGrid = () => {
    const handleMouseMove = (e: React.MouseEvent) => {
      if (gridRef.current) {
        const rect = gridRef.current.getBoundingClientRect();
        setMousePosition({
          x: e.clientX - rect.left,
          y: e.clientY - rect.top
        });
      }
    };

    return (
      <div 
        ref={gridRef}
        className="fixed inset-0 pointer-events-none z-0 opacity-20 dark:opacity-40"
        onMouseMove={handleMouseMove}
      >
        {/* Base Grid - High Contrast Solana Mint Grid for Dark Mode */}
        <div 
          className="absolute inset-0 dark:block hidden"
          style={{
            backgroundImage: `
              linear-gradient(rgba(0, 255, 209, 0.15) 1px, transparent 1px),
              linear-gradient(90deg, rgba(0, 255, 209, 0.15) 1px, transparent 1px)
            `,
            backgroundSize: '30px 30px',
            backgroundPosition: 'center center'
          }}
        />
        
        {/* Light mode grid - High Contrast Solana Purple Grid */}
        <div 
          className="absolute inset-0 dark:hidden block"
          style={{
            backgroundImage: `
              linear-gradient(rgba(153, 69, 255, 0.3) 1px, transparent 1px),
              linear-gradient(90deg, rgba(153, 69, 255, 0.3) 1px, transparent 1px)
            `,
            backgroundSize: '30px 30px',
            backgroundPosition: 'center center'
          }}
        />
        
        {/* Animated Grid Lines - Updated to use Solana Purple in Light Mode */}
        <motion.div
          className="absolute inset-0"
          style={{
            backgroundImage: `
              linear-gradient(90deg, transparent 0%, rgba(153, 69, 255, 0.3) 50%, transparent 100%)
            `,
            backgroundSize: '200% 100%',
          }}
          animate={{
            backgroundPosition: ['200% 0', '-200% 0']
          }}
          transition={{
            duration: 8,
            repeat: Infinity,
            ease: "linear"
          }}
        />
        
        {/* Hover Effect - Uses global styling for blue/primary which maps to Solana colors */}
        <motion.div
          className="absolute w-64 h-64 bg-blue-500/5 dark:bg-blue-500/10 rounded-full blur-xl"
          animate={{
            x: mousePosition.x - 128,
            y: mousePosition.y - 128,
          }}
          transition={{ type: "tween", ease: "backOut", duration: 0.5 }}
        />
      </div>
    );
  };

  // Binary Rain Effect - UPDATED for Solana colors
  const BinaryRain = () => (
    <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
      {[...Array(50)].map((_, i) => (
        <motion.div
          key={i}
          className="absolute text-xs font-mono text-cyan-500/30 dark:text-cyan-400/50" 
          initial={{
            x: Math.random() * window.innerWidth,
            y: -20,
            opacity: 0,
          }}
          animate={{
            y: window.innerHeight + 20,
            opacity: [0, 1, 0],
          }}
          transition={{
            duration: Math.random() * 3 + 2,
            repeat: Infinity,
            delay: Math.random() * 5,
            ease: "linear",
          }}
        >
          {Math.random() > 0.5 ? '1' : '0'}
        </motion.div>
      ))}
    </div>
  );

  // Metallic Border Component (Reused from original)
  const MetallicBorder = ({ isActive = false }: { isActive?: boolean }) => (
    <div className="absolute inset-0 rounded-lg overflow-hidden pointer-events-none">
      {/* Base metallic border */}
      <div 
        className="absolute inset-0 rounded-lg border"
        style={{
          borderColor: 'rgba(100, 100, 100, 0.3)',
          background: 'linear-gradient(135deg, rgba(100, 100, 100, 0.1), rgba(70, 130, 180, 0.05))'
        }}
      />
      
      {/* Corner accents */}
      <div className="absolute top-0 left-0 w-3 h-3 border-t border-l border-cyan-600 dark:border-cyan-400" />
      <div className="absolute top-0 right-0 w-3 h-3 border-t border-r border-cyan-600 dark:border-cyan-400" />
      <div className="absolute bottom-0 left-0 w-3 h-3 border-b border-l border-cyan-600 dark:border-cyan-400" />
      <div className="absolute bottom-0 right-0 w-3 h-3 border-b border-r border-cyan-600 dark:border-cyan-400" />
      
      {/* Active state */}
      <AnimatePresence>
        {isActive && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="absolute inset-0 rounded-lg border border-blue-500 dark:border-blue-400 shadow-lg shadow-blue-500/20 dark:shadow-blue-400/20"
          />
        )}
      </AnimatePresence>
    </div>
  );

  // Enhanced Feature Card with CODEX design (Reused from original)
  interface FeatureCardProps {
    icon: React.ReactNode;
    title: string;
    description: string;
    delay?: number;
    features: string[];
  }

  const FeatureCard: React.FC<FeatureCardProps> = ({ icon, title, description, delay = 0, features }) => {
    const [isHovered, setIsHovered] = useState(false);

    return (
      <motion.div
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay }}
        whileHover={{ 
          scale: 1.02,
          y: -5,
        }}
        onHoverStart={() => setIsHovered(true)}
        onHoverEnd={() => setIsHovered(false)}
        className="relative p-6 group cursor-pointer bg-white/80 dark:bg-black/40 backdrop-blur-sm rounded-lg border border-gray-300/50 dark:border-gray-800/50 shadow-lg dark:shadow-none"
        style={{ fontFamily: 'JetBrains Mono, monospace' }}
      >
        <MetallicBorder isActive={isHovered} />
        
        <div className="flex justify-center mb-4">
          <div 
            className="p-3 rounded-lg border border-blue-600/30 dark:border-blue-400/30"
            style={{ 
              background: 'linear-gradient(135deg, rgba(70, 130, 180, 0.1), rgba(232, 232, 232, 0.05))'
            }}
          >
            {icon}
          </div>
        </div>
        
        <h3 className="text-xl font-bold mb-3 text-center text-blue-700 dark:text-blue-400">
          {title}
        </h3>
        <p className="text-gray-700 dark:text-gray-300 leading-relaxed mb-4 text-sm">
          {description}
        </p>
        
        <div className="space-y-2">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: delay + index * 0.1 }}
              className="flex items-center space-x-2 text-xs text-gray-800 dark:text-gray-200"
            >
              <div className="w-1.5 h-1.5 bg-blue-500 dark:bg-blue-400 rounded-full" />
              <span>{feature}</span>
            </motion.div>
          ))}
        </div>
      </motion.div>
    );
  };

  // Stats Section (Reused from original)
  const StatsSection = () => (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-16">
      {[
        { number: '50K+', label: 'Datasets Processed', icon: <Database className="w-5 h-5" /> },
        { number: '99.97%', label: 'Accuracy Rate', icon: <Shield className="w-5 h-5" /> },
        { number: '1.8s', label: 'Avg Processing', icon: <Zap className="w-5 h-5" /> },
        { number: '24/7', label: 'Blockchain Secured', icon: <Lock className="w-5 h-5" /> }
      ].map((stat, index) => (
        <motion.div
          key={stat.label}
          initial={{ opacity: 0, scale: 0.5 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5, delay: index * 0.1 }}
          whileHover={{ scale: 1.05 }}
          className="relative p-4 text-center bg-white/80 dark:bg-black/40 backdrop-blur-sm rounded-lg border border-gray-300/50 dark:border-gray-800/50 shadow-lg dark:shadow-none"
        >
          <MetallicBorder />
          <div className="flex justify-center mb-2 text-blue-600 dark:text-blue-400">
            {stat.icon}
          </div>
          <div className="text-lg font-bold mb-1 text-gray-900 dark:text-gray-100">{stat.number}</div>
          <div className="text-xs text-gray-600 dark:text-gray-400">{stat.label}</div>
        </motion.div>
      ))}
    </div>
  );

  // Trusted Companies Section (Reused from original)
  const CompaniesSection = () => (
  <section className="relative py-16">
    <div className="container mx-auto px-4">
      <motion.div
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        transition={{ duration: 0.8 }}
        className="text-center mb-12"
      >
        <h3 className="text-lg font-semibold text-gray-600 dark:text-gray-400 mb-4">
          TRUSTED BY INDUSTRY LEADERS
        </h3>
      </motion.div>

      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-8 items-center opacity-90">
        {companies.map((company, index) => (
          <motion.div
            key={company.name}
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="flex flex-col items-center justify-center p-4 bg-white/50 dark:bg-black/30 rounded-lg border border-gray-300/30 dark:border-gray-800/30 shadow-md hover:shadow-lg transition-shadow"
          >
            <img
              src={company.logo}
              alt={`${company.name} logo`}
              className="w-10 h-10 object-contain mb-2"
            />
            <div className="text-gray-900 dark:text-white font-semibold text-sm">
              {company.name}
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  </section>
);

  // Integration Tools Section (Reused from original)
  const IntegrationSection = () => (
    <section className="relative py-20">
      <div className="container mx-auto px-4">
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl font-bold mb-6 text-gray-900 dark:text-gray-100">
            SEAMLESS INTEGRATION
          </h2>
          <p className="text-sm text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
            Works with your favorite tools and platforms
          </p>
        </motion.div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          {[
            { name: 'VS Code', icon: <Code className="w-8 h-8" />, description: 'IDE Extension' },
            { name: 'GitHub', icon: <Github className="w-8 h-8" />, description: 'CI/CD Pipelines' },
            { name: 'Docker', icon: <Settings className="w-8 h-8" />, description: 'Container Ready' },
            { name: 'AWS', icon: <Cloud className="w-8 h-8" />, description: 'Cloud Native' },
          ].map((tool, index) => (
            <motion.div
              key={tool.name}
              initial={{ opacity: 0, scale: 0.9 }}
              whileInView={{ opacity: 1, scale: 1 }}
              transition={{ delay: index * 0.1 }}
              whileHover={{ scale: 1.05 }}
              className="text-center p-6 bg-white/80 dark:bg-black/40 backdrop-blur-sm rounded-lg border border-gray-300/50 dark:border-gray-800/50 shadow-lg dark:shadow-none"
            >
              <div className="text-blue-600 dark:text-blue-400 mb-3 flex justify-center">{tool.icon}</div>
              <h4 className="font-bold text-gray-900 dark:text-white mb-2">{tool.name}</h4>
              <p className="text-xs text-gray-600 dark:text-gray-400">{tool.description}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );

  // Use Cases Section (Reused from original)
  const UseCasesSection = () => (
    <section className="relative py-20">
      <div className="container mx-auto px-4">
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl font-bold mb-6 text-gray-900 dark:text-gray-100">
            ENTERPRISE USE CASES
          </h2>
          <p className="text-sm text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
            Powering data integrity across industries
          </p>
        </motion.div>

        <div className="grid md:grid-cols-3 gap-8">
          {[
            {
              title: "Financial Services",
              description: "Audit trails and compliance reporting with immutable blockchain verification",
              features: ["Regulatory Compliance", "Audit Trails", "Fraud Detection"],
              icon: <Wallet className="w-6 h-6" />
            },
            {
              title: "Healthcare",
              description: "Secure patient data processing with HIPAA-compliant blockchain proofs",
              features: ["HIPAA Compliance", "Patient Data Integrity", "Research Validation"],
              icon: <ShieldCheck className="w-6 h-6" />
            },
            {
              title: "Supply Chain",
              description: "Track and verify product data across global supply chains",
              features: ["Product Provenance", "Quality Assurance", "Logistics Tracking"],
              icon: <Globe className="w-6 h-6" />
            }
          ].map((usecase, index) => (
            <motion.div
              key={usecase.title}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.2 }}
              className="p-6 bg-white/80 dark:bg-black/40 backdrop-blur-sm rounded-lg border border-gray-300/50 dark:border-gray-800/50 shadow-lg dark:shadow-none"
            >
              <div className="text-blue-600 dark:text-blue-400 mb-4 flex justify-center">
                {usecase.icon}
              </div>
              <h3 className="text-xl font-bold mb-3 text-center text-blue-700 dark:text-blue-400">
                {usecase.title}
              </h3>
              <p className="text-gray-700 dark:text-gray-300 text-sm mb-4 text-center">
                {usecase.description}
              </p>
              <div className="space-y-2">
                {usecase.features.map((feature, featureIndex) => (
                  <div key={featureIndex} className="flex items-center space-x-2 text-xs text-gray-600 dark:text-gray-400">
                    <div className="w-1.5 h-1.5 bg-blue-500 dark:bg-blue-400 rounded-full" />
                    <span>{feature}</span>
                  </div>
                ))}
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );

  // Pricing Preview Section (Reused from original)
  const PricingPreview = () => (
    <section className="relative py-20">
      <div className="container mx-auto px-4">
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl font-bold mb-6 text-gray-900 dark:text-gray-100">
            SIMPLE PRICING
          </h2>
          <p className="text-sm text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
            Start free, scale as you grow
          </p>
        </motion.div>

        <div className="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
          {[
            {
              name: "Starter",
              price: "Free",
              description: "Perfect for individuals and small projects",
              features: ["1GB Processing", "Basic Cleaning", "Community Support"]
            },
            {
              name: "Professional",
              price: "$49",
              description: "For growing teams and businesses",
              features: ["100GB Processing", "AI-Powered Cleaning", "Priority Support", "API Access"]
            },
            {
              name: "Enterprise",
              price: "Custom",
              description: "For large organizations with custom needs",
              features: ["Unlimited Processing", "Custom AI Models", "Dedicated Support", "SLA Guarantee"]
            }
          ].map((plan, index) => (
            <motion.div
              key={plan.name}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="p-6 bg-white/80 dark:bg-black/40 backdrop-blur-sm rounded-lg border border-gray-300/50 dark:border-gray-800/50 shadow-lg dark:shadow-none"
            >
              <h3 className="text-xl font-bold mb-2 text-gray-900 dark:text-white">{plan.name}</h3>
              <div className="text-2xl font-bold mb-4 text-blue-600 dark:text-blue-400">{plan.price}</div>
              <p className="text-gray-600 dark:text-gray-400 text-sm mb-6">{plan.description}</p>
              <div className="space-y-3">
                {plan.features.map((feature, featureIndex) => (
                  <div key={featureIndex} className="flex items-center space-x-2 text-sm text-gray-700 dark:text-gray-300">
                    <CheckCircle className="w-4 h-4 text-green-500" />
                    <span>{feature}</span>
                  </div>
                ))}
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );

  return (
    <div className="min-h-screen bg-white dark:bg-black overflow-hidden relative" style={{ fontFamily: 'JetBrains Mono, monospace' }}>
      <CodexGrid />
      <BinaryRain />

      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center pt-20">
        <div className="container mx-auto px-4 text-center relative z-10">
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 1 }}
            className="mb-8"
          >
            <motion.h1
              initial={{ opacity: 0, scale: 0.5 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.8 }}
              className="text-5xl md:text-7xl font-black mb-6 tracking-tighter text-gray-900 dark:text-gray-100"
            >
                {/* Implemented Text Roll and Glitch */}
                <RollingText
                    text="KEGINATOR"
                    duration={1.5}
                    delay={0.5}
                    className="dark:text-white text-gray-900"
                />
            </motion.h1>
            
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.5, duration: 1 }}
              className="text-lg md:text-xl mb-8 max-w-4xl mx-auto leading-relaxed text-blue-700 dark:text-blue-400"
            >
              THE DATA INTEGRITY PROTOCOL
            </motion.p>

            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.8, duration: 1 }}
              className="text-sm text-gray-600 dark:text-gray-400 mb-12 max-w-2xl mx-auto"
            >
              Enterprise-grade data cleaning meets blockchain verification. Process, clean, and verify datasets with immutable proof on Solana.
            </motion.p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 1 }}
            className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-16"
          >
            <Link to="/upload">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="px-8 py-3 rounded-lg font-bold text-sm flex items-center space-x-2 transition-all duration-300 bg-cyan-300 border-cyan-600 dark:bg-[#FFFFff] dark:text-[#000000] dark:border-blue-400 hover:bg-cyan-300 text-[#000000] shadow-lg"
              >
                <Rocket className="w-4 h-4" />
                <span className='!text-[#000000]'>LAUNCH KEGINATOR</span>
                <ArrowRight className="w-4 h-4" />
              </motion.button>
            </Link>
            
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="px-8 py-3 border border-blue-600 dark:border-blue-400 rounded-lg font-bold text-sm flex items-center space-x-2 transition-all duration-300 text-blue-600 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20"
              onClick={() => terminalRef.current?.scrollIntoView({ behavior: 'smooth' })}
            >
              <Play className="w-4 h-4" />
              <span>WATCH DEMO</span>
            </motion.button>
          </motion.div>

          <StatsSection />
        </div>
      </section>

      <CompaniesSection />

      {/* Features Grid - Modern Layout */}
<section className="relative py-20">
  <div className="container mx-auto px-4">
    <motion.div
      initial={{ opacity: 0 }}
      whileInView={{ opacity: 1 }}
      transition={{ duration: 0.8 }}
      className="text-center mb-16"
    >
      <h2 className="text-3xl font-bold mb-6 text-gray-900 dark:text-gray-100">
        ENTERPRISE DATA PLATFORM
      </h2>
      <p className="text-sm text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
        Everything you need for data integrity, cleaning, and blockchain verification in one platform.
      </p>
    </motion.div>

    {/* Interactive Feature Matrix */}
    <div className="relative max-w-6xl mx-auto">
      {/* Animated Background Grid */}
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 relative">
        {/* Left Side - Feature Showcase */}
        <div className="space-y-6">
          {[
            {
              icon: <Zap className="w-5 h-5" />,
              title: "AI-Powered Cleaning",
              description: "Advanced ML algorithms detect and fix data quality issues in real-time",
              stats: "99.7% Accuracy",
              color: "text-purple-500"
            },
            {
              icon: <Shield className="w-5 h-5" />,
              title: "Blockchain Verification",
              description: "Immutable Solana proofs with instant verification",
              stats: "1.2s Average",
              color: "text-green-500"
            },
            {
              icon: <Database className="w-5 h-5" />,
              title: "Multi-Format Support",
              description: "All major formats with intelligent detection",
              stats: "15+ Formats",
              color: "text-blue-500"
            }
          ].map((feature, index) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: index * 0.15 }}
              whileHover={{ x: 10 }}
              className="group p-6 rounded-2xl bg-white/40 dark:bg-gray-900/30 backdrop-blur-sm border border-gray-200/30 dark:border-gray-700/30 hover:border-gray-300/50 dark:hover:border-gray-600/50 transition-all duration-300 cursor-pointer"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <div className={`${feature.color} group-hover:scale-110 transition-transform duration-300`}>
                    {feature.icon}
                  </div>
                  <div>
                    <h3 className="font-bold text-gray-900 dark:text-white text-lg">
                      {feature.title}
                    </h3>
                    <p className="text-sm text-gray-600 dark:text-gray-300 mt-1">
                      {feature.description}
                    </p>
                  </div>
                </div>
                <div className={`text-xs font-bold px-3 py-1 rounded-full bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 border border-gray-200 dark:border-gray-700`}>
                  {feature.stats}
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Right Side - Feature Showcase */}
        <div className="space-y-6">
          {[
            {
              icon: <Cpu className="w-5 h-5" />,
              title: "Real-time Processing",
              description: "Sub-second latency with real-time streaming capabilities",
              stats: "0.8s Latency",
              color: "text-indigo-500"
            },
            {
              icon: <Globe className="w-5 h-5" />,
              title: "Global Infrastructure",
              description: "15 regions worldwide with 99.9% uptime guarantee",
              stats: "99.9% Uptime",
              color: "text-teal-500"
            },
            {
              icon: <Lock className="w-5 h-5" />,
              title: "Enterprise Security",
              description: "Military-grade encryption and zero-trust architecture",
              stats: "SOC 2 Compliant",
              color: "text-amber-500"
            }
          ].map((feature, index) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, x: 20 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: index * 0.15 }}
              whileHover={{ x: -10 }}
              className="group p-6 rounded-2xl bg-white/40 dark:bg-gray-900/30 backdrop-blur-sm border border-gray-200/30 dark:border-gray-700/30 hover:border-gray-300/50 dark:hover:border-gray-600/50 transition-all duration-300 cursor-pointer"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <div className={`${feature.color} group-hover:scale-110 transition-transform duration-300`}>
                    {feature.icon}
                  </div>
                  <div>
                    <h3 className="font-bold text-gray-900 dark:text-white text-lg">
                      {feature.title}
                    </h3>
                    <p className="text-sm text-gray-600 dark:text-gray-300 mt-1">
                      {feature.description}
                    </p>
                  </div>
                </div>
                <div className={`text-xs font-bold px-3 py-1 rounded-full bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 border border-gray-200 dark:border-gray-700`}>
                  {feature.stats}
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>

      
    </div>
      </div>
</section>
      <IntegrationSection />
      <UseCasesSection />

      {/* Terminal Demo Section */}
      <section ref={terminalRef} className="relative py-20">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            transition={{ duration: 0.8 }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl font-bold mb-6 text-gray-900 dark:text-gray-100">
              EXPERIENCE THE POWER
            </h2>
            <p className="text-sm text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
              See Keginator in action with our interactive terminal demo.
            </p>
          </motion.div>
          
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            whileInView={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8 }}
            className="max-w-4xl mx-auto"
          >
            <Terminal />
          </motion.div>
        </div>
      </section>

      <PricingPreview />

      {/* Final CTA Section - UPDATED to link to all main pages */}
      <section className="relative py-20 mb-20 md:mb-20">
        <div className="container mx-auto px-4 text-center">
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="relative p-8 max-w-3xl mx-auto bg-white/80 dark:bg-black/40 backdrop-blur-sm rounded-lg border border-gray-300/50 dark:border-gray-800/50 shadow-lg dark:shadow-none"
          >
            <MetallicBorder isActive={true} />
            
            <h2 className="text-2xl md:text-4xl font-bold mb-6 text-gray-900 dark:text-gray-100">
              READY TO TRANSFORM YOUR DATA?
            </h2>
            <p className="text-sm text-gray-700 dark:text-gray-300 mb-8 max-w-2xl mx-auto">
              Join thousands of data professionals who trust Keginator for blockchain-verified data integrity.
            </p>
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4 justify-center items-center">
              
              <Link to="/upload">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="w-full px-4 py-2 rounded-lg font-bold text-xs flex items-center justify-center space-x-1 transition-all duration-300 bg-cyan-500 hover:bg-cyan-600 text-white shadow-lg"
                >
                  <Upload className="w-3 h-3" />
                  <span>UPLOAD</span>
                </motion.button>
              </Link>
              <Link to="/verify">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="w-full px-4 py-2 border border-blue-600 dark:border-blue-400 rounded-lg font-bold text-xs flex items-center justify-center space-x-1 transition-all duration-300 text-blue-600 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20"
                >
                  <CheckCircle className="w-3 h-3" />
                  <span>VERIFY</span>
                </motion.button>
              </Link>
              <Link to="/history">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="w-full px-4 py-2 border border-purple-600 dark:border-purple-400 rounded-lg font-bold text-xs flex items-center justify-center space-x-1 transition-all duration-300 text-purple-600 dark:text-purple-400 hover:bg-purple-50 dark:hover:bg-purple-900/20"
                >
                  <i className="lucide-history w-3 h-3" />
                  <span>HISTORY</span>
                </motion.button>
              </Link>
              <Link to="/dashboard">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="w-full px-4 py-2 border border-gray-600 dark:border-gray-400 rounded-lg font-bold text-xs flex items-center justify-center space-x-1 transition-all duration-300 text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800/20"
                >
                  <i className="lucide-dashboard w-3 h-3" />
                  <span>DASHBOARD</span>
                </motion.button>
              </Link>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  );
};

export default Home;