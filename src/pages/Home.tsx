// Home.tsx
import React, { useState, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowRight, Shield, Zap, Database, Rocket, 
  Upload, CheckCircle, Cpu, Globe, Lock, Play, 
  Code, Cloud, GitBranch, Settings,  Wallet,
  ShieldCheck
} from 'lucide-react';
import { Link } from 'react-router-dom';
import Terminal from '../components/ui/Terminal';

const Home: React.FC = () => {
  // const [isLoaded, setIsLoaded] = useState(false);
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const gridRef = useRef<HTMLDivElement>(null);


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

  // CODEX Grid Background with hover interaction
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
        {/* Base Grid */}
        <div 
          className="absolute inset-0 dark:block hidden"
          style={{
            backgroundImage: `
              linear-gradient(rgba(120, 120, 120, 0.15) 1px, transparent 1px),
              linear-gradient(90deg, rgba(120, 120, 120, 0.15) 1px, transparent 1px)
            `,
            backgroundSize: '30px 30px',
            backgroundPosition: 'center center'
          }}
        />
        
        {/* Light mode grid */}
        <div 
          className="absolute inset-0 dark:hidden block"
          style={{
            backgroundImage: `
              linear-gradient(rgba(200, 200, 200, 0.3) 1px, transparent 1px),
              linear-gradient(90deg, rgba(200, 200, 200, 0.3) 1px, transparent 1px)
            `,
            backgroundSize: '30px 30px',
            backgroundPosition: 'center center'
          }}
        />
        
        {/* Animated Grid Lines */}
        <motion.div
          className="absolute inset-0"
          style={{
            backgroundImage: `
              linear-gradient(90deg, transparent 0%, rgba(70, 130, 180, 0.3) 50%, transparent 100%)
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
        
        {/* Hover Effect */}
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

  // Binary Rain Effect
  const BinaryRain = () => (
    <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
      {[...Array(50)].map((_, i) => (
        <motion.div
          key={i}
          className="absolute text-xs font-mono text-blue-400/30 dark:text-blue-400/50"
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

  // Metallic Border Component
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

  // Enhanced Feature Card with CODEX design
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

  // Stats Section
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

  // Trusted Companies Section
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

  // Integration Tools Section
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
            { name: 'GitHub', icon: <GitBranch className="w-8 h-8" />, description: 'CI/CD Pipelines' },
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

  // Use Cases Section
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

  // Pricing Preview Section
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
              KEGINATOR
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
            >
              <Play className="w-4 h-4" />
              <span>WATCH DEMO</span>
            </motion.button>
          </motion.div>

          <StatsSection />
        </div>
      </section>

      <CompaniesSection />

      {/* Features Grid */}
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

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-20">
            <FeatureCard
              icon={<Zap className="w-6 h-6 text-blue-600 dark:text-blue-400" />}
              title="AI-Powered Cleaning"
              description="Advanced machine learning algorithms automatically detect and fix data quality issues in real-time"
              delay={0}
              features={[
                "Smart anomaly detection",
                "Pattern recognition AI",
                "Automated formatting",
                "Real-time validation"
              ]}
            />
            <FeatureCard
              icon={<Shield className="w-6 h-6 text-blue-600 dark:text-blue-400" />}
              title="Blockchain Verification"
              description="Immutable Solana blockchain proofs for every dataset with instant verification"
              delay={0.2}
              features={[
                "Solana blockchain integration",
                "Instant verification",
                "Immutable proof storage",
                "Public audit trail"
              ]}
            />
            <FeatureCard
              icon={<Database className="w-6 h-6 text-blue-600 dark:text-blue-400" />}
              title="Multi-Format Support"
              description="Support for all major data formats with intelligent format detection and conversion"
              delay={0.4}
              features={[
                "CSV, JSON, Parquet, XML",
                "Auto-format detection",
                "Batch processing",
                "Streaming data support"
              ]}
            />
            <FeatureCard
              icon={<Cpu className="w-6 h-6 text-blue-600 dark:text-blue-400" />}
              title="Real-time Processing"
              description="Lightning-fast data processing with sub-second latency and real-time streaming"
              delay={0.6}
              features={[
                "Sub-second processing",
                "Real-time data streams",
                "WebSocket API",
                "Live monitoring dashboard"
              ]}
            />
            <FeatureCard
              icon={<Globe className="w-6 h-6 text-blue-600 dark:text-blue-400" />}
              title="Global Infrastructure"
              description="Distributed nodes across 15 regions ensuring 99.9% uptime and low latency worldwide"
              delay={0.8}
              features={[
                "15 global regions",
                "99.9% uptime SLA",
                "Edge computing nodes",
                "Auto-scaling clusters"
              ]}
            />
            <FeatureCard
              icon={<Lock className="w-6 h-6 text-blue-600 dark:text-blue-400" />}
              title="Enterprise Security"
              description="Military-grade encryption, SOC 2 compliance, and zero-trust architecture"
              delay={1}
              features={[
                "End-to-end encryption",
                "SOC 2 Type II compliant",
                "Zero-trust security model",
                "Comprehensive audit logging"
              ]}
            />
          </div>
        </div>
      </section>

      <IntegrationSection />
      <UseCasesSection />

      {/* Terminal Demo Section */}
      <section className="relative py-20">
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

      {/* Final CTA Section */}
      <section className="relative py-20">
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
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <Link to="/upload">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="px-8 py-3 rounded-lg font-bold text-sm flex items-center space-x-2 transition-all duration-300 bg-cyan-300 border-cyan-600 dark:bg-[#FFFFff] dark:text-[#000000] dark:border-blue-400 hover:bg-cyan-300 text-[#000000] shadow-lg"
                >
                  <Upload className="w-4 h-4" />
                  <span className='!text-[#000000]'>UPLOAD DATASET</span>
                </motion.button>
              </Link>
              <Link to="/verify">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="px-8 py-3 border border-blue-600 dark:border-blue-400 rounded-lg font-bold text-sm flex items-center space-x-2 transition-all duration-300 text-blue-600 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20"
                >
                  <CheckCircle className="w-4 h-4" />
                  <span>VERIFY DATA</span>
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