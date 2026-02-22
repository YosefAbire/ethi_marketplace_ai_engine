import React, { useState } from 'react';
import { motion } from 'framer-motion';

interface CTASectionProps {
    onGetStarted: () => void;
}

export const CTASection: React.FC<CTASectionProps> = ({ onGetStarted }) => {
    const [email, setEmail] = useState('');
    const [isSubmitted, setIsSubmitted] = useState(false);

    const handleEmailSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (email.trim()) {
            setIsSubmitted(true);
            setTimeout(() => {
                onGetStarted();
            }, 1500);
        }
    };

    const features = [
        {
            icon: 'fa-brain',
            title: '6 AI Agents',
            description: 'Specialized intelligence for every task'
        },
        {
            icon: 'fa-chart-line',
            title: 'Real-time Analytics',
            description: 'Live insights and recommendations'
        },
        {
            icon: 'fa-shield-check',
            title: 'Enterprise Security',
            description: 'Bank-level data protection'
        },
        {
            icon: 'fa-headset',
            title: '24/7 Support',
            description: 'Always-on AI assistance'
        }
    ];

    return (
        <div className="relative overflow-hidden">
            {/* Floating Elements */}
            <div className="absolute inset-0 overflow-hidden">
                {[...Array(20)].map((_, i) => (
                    <motion.div
                        key={i}
                        className="absolute w-2 h-2 bg-ethiGreen rounded-full opacity-30"
                        style={{
                            left: `${Math.random() * 100}%`,
                            top: `${Math.random() * 100}%`,
                        }}
                        animate={{
                            y: [0, -100, 0],
                            opacity: [0.3, 0.8, 0.3],
                        }}
                        transition={{
                            duration: 3 + Math.random() * 2,
                            repeat: Infinity,
                            delay: Math.random() * 2,
                            ease: "easeInOut"
                        }}
                    />
                ))}
            </div>

            <div className="relative z-10 max-w-7xl mx-auto px-8 py-24">
                <div className="grid lg:grid-cols-2 gap-16 items-center">
                    {/* Left Content */}
                    <motion.div
                        initial={{ opacity: 0, x: -50 }}
                        whileInView={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.8 }}
                        className="text-white"
                    >
                        <div className="inline-flex items-center gap-3 px-6 py-3 rounded-full bg-ethiGreen/20 border border-ethiGreen/30 mb-8">
                            <div className="w-3 h-3 bg-ethiGreen rounded-full animate-pulse" />
                            <span className="text-sm font-bold text-ethiGreen">Ready to Deploy</span>
                        </div>

                        <h2 className="text-6xl font-black mb-8 leading-tight">
                            Transform Your <br />
                            <span className="text-ethiGreen">Marketplace</span> <br />
                            Today
                        </h2>

                        <p className="text-xl text-slate-300 leading-relaxed mb-12 max-w-lg">
                            Join the AI revolution in Ethiopian commerce. Get intelligent insights, 
                            automated operations, and unprecedented growth.
                        </p>

                        {/* Features Grid */}
                        <div className="grid grid-cols-2 gap-6 mb-12">
                            {features.map((feature, index) => (
                                <motion.div
                                    key={index}
                                    initial={{ opacity: 0, y: 20 }}
                                    whileInView={{ opacity: 1, y: 0 }}
                                    transition={{ duration: 0.5, delay: index * 0.1 }}
                                    className="flex items-start gap-3"
                                >
                                    <div className="w-10 h-10 bg-ethiGreen/20 rounded-xl flex items-center justify-center text-ethiGreen flex-shrink-0">
                                        <i className={`fas ${feature.icon}`} />
                                    </div>
                                    <div>
                                        <h3 className="font-bold text-white mb-1">{feature.title}</h3>
                                        <p className="text-sm text-slate-400">{feature.description}</p>
                                    </div>
                                </motion.div>
                            ))}
                        </div>

                        {/* Social Proof */}
                        <div className="flex items-center gap-6 text-sm text-slate-400">
                            <div className="flex items-center gap-2">
                                <i className="fas fa-users text-ethiGreen" />
                                <span>2,500+ Active Sellers</span>
                            </div>
                            <div className="flex items-center gap-2">
                                <i className="fas fa-star text-ethiYellow" />
                                <span>4.9/5 Rating</span>
                            </div>
                        </div>
                    </motion.div>

                    {/* Right Content - CTA Form */}
                    <motion.div
                        initial={{ opacity: 0, x: 50 }}
                        whileInView={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.8, delay: 0.2 }}
                        className="relative"
                    >
                        <div className="bg-white rounded-3xl shadow-2xl p-8 relative overflow-hidden">
                            {/* Background Pattern */}
                            <div className="absolute inset-0 tibeb-bg opacity-5" />
                            
                            <div className="relative z-10">
                                {!isSubmitted ? (
                                    <>
                                        <div className="text-center mb-8">
                                            <div className="w-16 h-16 bg-ethiGreen rounded-2xl flex items-center justify-center text-white shadow-lg mx-auto mb-4">
                                                <i className="fas fa-rocket text-2xl" />
                                            </div>
                                            <h3 className="text-3xl font-black text-slate-800 mb-2">
                                                Start Your AI Journey
                                            </h3>
                                            <p className="text-slate-600">
                                                Get instant access to the marketplace AI engine
                                            </p>
                                        </div>

                                        {/* Email Form */}
                                        <form onSubmit={handleEmailSubmit} className="space-y-6">
                                            <div>
                                                <label className="block text-sm font-bold text-slate-700 mb-2">
                                                    Email Address
                                                </label>
                                                <input
                                                    type="email"
                                                    value={email}
                                                    onChange={(e) => setEmail(e.target.value)}
                                                    placeholder="your@email.com"
                                                    className="w-full px-4 py-4 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-ethiGreen/20 focus:border-ethiGreen text-lg"
                                                    required
                                                />
                                            </div>

                                            <motion.button
                                                type="submit"
                                                whileHover={{ scale: 1.02 }}
                                                whileTap={{ scale: 0.98 }}
                                                className="w-full py-4 bg-ethiGreen text-white rounded-xl font-bold text-lg hover:bg-ethiGreen/90 transition-all shadow-xl shadow-ethiGreen/30"
                                            >
                                                Launch AI Engine • ጀምር
                                                <i className="fas fa-arrow-right ml-2" />
                                            </motion.button>
                                        </form>

                                        <div className="text-center mt-6">
                                            <p className="text-xs text-slate-500">
                                                Free 30-day trial • No credit card required
                                            </p>
                                        </div>
                                    </>
                                ) : (
                                    <motion.div
                                        initial={{ opacity: 0, scale: 0.8 }}
                                        animate={{ opacity: 1, scale: 1 }}
                                        className="text-center py-8"
                                    >
                                        <motion.div
                                            initial={{ scale: 0 }}
                                            animate={{ scale: 1 }}
                                            transition={{ delay: 0.2 }}
                                            className="w-20 h-20 bg-green-500 rounded-full flex items-center justify-center text-white shadow-lg mx-auto mb-6"
                                        >
                                            <i className="fas fa-check text-3xl" />
                                        </motion.div>
                                        <h3 className="text-2xl font-bold text-slate-800 mb-2">
                                            Welcome Aboard!
                                        </h3>
                                        <p className="text-slate-600 mb-6">
                                            Redirecting you to the AI engine...
                                        </p>
                                        <div className="flex justify-center">
                                            <motion.div
                                                animate={{ rotate: 360 }}
                                                transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                                                className="w-8 h-8 border-4 border-ethiGreen border-t-transparent rounded-full"
                                            />
                                        </div>
                                    </motion.div>
                                )}
                            </div>
                        </div>

                        {/* Floating Cards */}
                        <motion.div
                            animate={{ y: [0, -10, 0] }}
                            transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
                            className="absolute -top-4 -left-4 w-24 h-24 bg-ethiYellow rounded-2xl flex items-center justify-center text-white shadow-xl opacity-90"
                        >
                            <i className="fas fa-brain text-2xl" />
                        </motion.div>

                        <motion.div
                            animate={{ y: [0, 10, 0] }}
                            transition={{ duration: 3, repeat: Infinity, ease: "easeInOut", delay: 1 }}
                            className="absolute -bottom-4 -right-4 w-20 h-20 bg-ethiBlue rounded-2xl flex items-center justify-center text-white shadow-xl opacity-90"
                        >
                            <i className="fas fa-chart-line text-xl" />
                        </motion.div>
                    </motion.div>
                </div>
            </div>
        </div>
    );
};