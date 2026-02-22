import React, { useState, useEffect } from 'react';
import { motion, useAnimation } from 'framer-motion';
import { TypewriterText } from './TypewriterText';
import { FloatingElements } from './FloatingElements';

interface HeroSectionProps {
    onGetStarted: () => void;
}

export const HeroSection: React.FC<HeroSectionProps> = ({ onGetStarted }) => {
    const [currentPhase, setCurrentPhase] = useState(0);
    const controls = useAnimation();

    const phases = [
        "Analyzing Market Data",
        "Processing AI Insights", 
        "Generating Recommendations",
        "Optimizing Operations"
    ];

    useEffect(() => {
        const interval = setInterval(() => {
            setCurrentPhase(prev => (prev + 1) % phases.length);
        }, 3000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="relative min-h-screen flex items-center justify-center px-8 overflow-hidden">
            <FloatingElements />
            
            <div className="max-w-7xl mx-auto grid lg:grid-cols-2 gap-16 items-center relative z-10">
                {/* Left Content */}
                <motion.div
                    initial={{ opacity: 0, x: -50 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.8, delay: 0.2 }}
                    className="space-y-8"
                >
                    <h1 className="text-6xl lg:text-7xl font-black tracking-tight leading-[0.9]">
                        <span className="block">Intelligent</span>
                        <span className="block text-ethiGreen">Ethiopian</span>
                        <span className="block">Marketplace</span>
                    </h1>

                    <div className="h-16 flex items-center">
                        <TypewriterText 
                            texts={[
                                "Powered by Advanced AI Agents",
                                "Real-time Market Intelligence", 
                                "Automated Business Optimization",
                                "የኢትዮጵያ ዘመናዊ ገበያ"
                            ]}
                            className="text-2xl text-slate-600 font-medium"
                        />
                    </div>

                    <p className="text-xl text-slate-500 leading-relaxed max-w-2xl">
                        Transform your marketplace operations with our multi-agent AI system. 
                        Get real-time insights, automated recommendations, and intelligent 
                        decision-making tools designed for Ethiopian commerce.
                    </p>

                    <div className="flex flex-col sm:flex-row gap-4">
                        <motion.button
                            onClick={onGetStarted}
                            whileHover={{ scale: 1.05, y: -2 }}
                            whileTap={{ scale: 0.95 }}
                            className="px-8 py-4 bg-ethiGreen text-white rounded-2xl font-bold text-lg shadow-xl shadow-ethiGreen/30 hover:shadow-2xl transition-all flex items-center justify-center gap-3"
                        >
                            Launch AI Engine
                            <motion.i 
                                className="fas fa-rocket"
                                animate={{ rotate: [0, 10, 0] }}
                                transition={{ repeat: Infinity, duration: 2 }}
                            />
                        </motion.button>
                        
                        <motion.button
                            whileHover={{ scale: 1.05 }}
                            className="px-8 py-4 bg-white border-2 border-slate-200 text-slate-700 rounded-2xl font-bold text-lg hover:bg-slate-50 transition-all"
                        >
                            Watch Demo
                            <i className="fas fa-play ml-2" />
                        </motion.button>
                    </div>

                    {/* Current Phase Indicator */}
                    <motion.div
                        key={currentPhase}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="flex items-center gap-3 text-sm text-slate-500"
                    >
                        <div className="w-3 h-3 bg-ethiGreen rounded-full animate-pulse" />
                        <span className="font-medium">{phases[currentPhase]}...</span>
                    </motion.div>
                </motion.div>

                {/* Right Content - Profile Image */}
                <motion.div
                    initial={{ opacity: 0, x: 50 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.8, delay: 0.4 }}
                    className="relative"
                >
                    {/* Profile Image with Blur Effect */}
                    <div className="relative rounded-3xl shadow-2xl border border-slate-100 h-[600px] overflow-hidden">
                        {/* Blurred Background Image */}
                        <div 
                            className="absolute inset-0 bg-cover bg-center"
                            style={{
                                backgroundImage: 'url(/yosef-profile.jpg)',
                                filter: 'blur(8px)',
                                transform: 'scale(1.1)'
                            }}
                        ></div>
                        
                        {/* Overlay for better text visibility */}
                        <div className="absolute inset-0 bg-gradient-to-br from-ethiGreen/30 to-emerald-900/40 backdrop-blur-sm"></div>
                        
                        {/* Content */}
                        <div className="relative h-full flex items-center justify-center p-8">
                            <div className="text-center">
                                <motion.div
                                    animate={{ 
                                        scale: [1, 1.05, 1],
                                    }}
                                    transition={{ 
                                        duration: 3, 
                                        repeat: Infinity,
                                        ease: "easeInOut"
                                    }}
                                    className="mb-8"
                                >
                                    <div className="w-32 h-32 mx-auto rounded-full border-4 border-white shadow-2xl overflow-hidden">
                                        <img 
                                            src="/yosef-profile.jpg" 
                                            alt="Developer Profile"
                                            className="w-full h-full object-cover"
                                        />
                                    </div>
                                </motion.div>
                                <h3 className="text-4xl font-black text-white mb-4 drop-shadow-lg">
                                    Ethiopian Marketplace
                                </h3>
                                <p className="text-xl text-white/90 font-medium drop-shadow-md">
                                    ኢትዮጵያዊ የገበያ መድረክ
                                </p>
                                <div className="mt-8 flex items-center justify-center gap-2 bg-white/20 backdrop-blur-md px-6 py-3 rounded-full border border-white/30">
                                    <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse shadow-lg shadow-green-400/50" />
                                    <span className="text-sm font-bold text-white">System Ready</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </motion.div>
            </div>
        </div>
    );
};