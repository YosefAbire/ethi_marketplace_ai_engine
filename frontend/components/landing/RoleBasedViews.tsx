import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface RoleBasedViewsProps {
    userRole: 'seller' | 'owner';
    onRoleChange: (role: 'seller' | 'owner') => void;
}

export const RoleBasedViews: React.FC<RoleBasedViewsProps> = ({
    userRole,
    onRoleChange
}) => {
    const [selectedInsight, setSelectedInsight] = useState(0);

    const sellerInsights = [
        {
            title: "Pricing Optimization",
            description: "AI suggests optimal prices based on market demand and competition",
            value: "+23% Revenue",
            icon: "fa-coins",
            color: "ethiGreen",
            details: "Your honey products are underpriced by 15%. Increase to 14.50 ETB for optimal profit."
        },
        {
            title: "Inventory Alerts",
            description: "Smart notifications when products need restocking",
            value: "3 Items Low",
            icon: "fa-box",
            color: "ethiYellow",
            details: "Teff flour, coffee beans, and bamboo baskets need immediate restocking."
        },
        {
            title: "Demand Forecasting",
            description: "Predict future demand based on seasonal patterns",
            value: "Meskel Season",
            icon: "fa-chart-line",
            color: "ethiBlue",
            details: "Expect 40% increase in honey demand during upcoming Meskel celebrations."
        }
    ];

    const ownerInsights = [
        {
            title: "Market Overview",
            description: "Complete marketplace performance analytics",
            value: "2.4M ETB Revenue",
            icon: "fa-chart-bar",
            color: "ethiGreen",
            details: "Total marketplace revenue up 18% this month with 1,247 active sellers."
        },
        {
            title: "Seller Performance",
            description: "Track top performing sellers and categories",
            value: "Top 10% Growth",
            icon: "fa-users",
            color: "ethiPurple",
            details: "Coffee and grains categories showing strongest growth with 89 new sellers."
        },
        {
            title: "System Health",
            description: "AI agents performance and system metrics",
            value: "98.5% Uptime",
            icon: "fa-server",
            color: "ethiBlue",
            details: "All AI agents operating optimally with average response time of 0.8 seconds."
        }
    ];

    const currentInsights = userRole === 'seller' ? sellerInsights : ownerInsights;

    return (
        <div className="max-w-7xl mx-auto px-8">
            <motion.div
                initial={{ opacity: 0, y: 50 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8 }}
                className="text-center mb-16"
            >
                <h2 className="text-5xl font-black mb-6 tracking-tight text-slate-800">
                    Your <span className="text-ethiGreen">Personalized</span> View
                </h2>
                <p className="text-xl text-slate-700 max-w-3xl mx-auto mb-8">
                    Experience tailored insights based on your role in the marketplace
                </p>

                {/* Role Selector */}
                <div className="inline-flex bg-white/80 backdrop-blur-sm rounded-2xl p-2 shadow-lg border border-white/20">
                    <button
                        onClick={() => onRoleChange('seller')}
                        className={`px-8 py-3 rounded-xl font-bold text-sm transition-all ${
                            userRole === 'seller'
                                ? 'bg-white text-ethiGreen shadow-lg'
                                : 'text-slate-600 hover:text-slate-800 hover:bg-white/50'
                        }`}
                    >
                        <i className="fas fa-store mr-2" />
                        Seller View
                    </button>
                    <button
                        onClick={() => onRoleChange('owner')}
                        className={`px-8 py-3 rounded-xl font-bold text-sm transition-all ${
                            userRole === 'owner'
                                ? 'bg-white text-ethiGreen shadow-lg'
                                : 'text-slate-600 hover:text-slate-800 hover:bg-white/50'
                        }`}
                    >
                        <i className="fas fa-crown mr-2" />
                        Market Owner
                    </button>
                </div>
            </motion.div>

            <div className="grid lg:grid-cols-2 gap-12 items-center">
                {/* Insights Cards */}
                <div className="space-y-6">
                    <AnimatePresence mode="wait">
                        <motion.div
                            key={userRole}
                            initial={{ opacity: 0, x: -50 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: 50 }}
                            transition={{ duration: 0.5 }}
                            className="space-y-4"
                        >
                            {currentInsights.map((insight, index) => (
                                <motion.div
                                    key={index}
                                    onClick={() => setSelectedInsight(index)}
                                    whileHover={{ scale: 1.02, x: 10 }}
                                    className={`p-6 rounded-2xl cursor-pointer transition-all ${
                                        selectedInsight === index
                                            ? `bg-${insight.color}/10 border-2 border-${insight.color}/30 shadow-xl`
                                            : 'bg-white border-2 border-slate-200 hover:border-slate-300'
                                    }`}
                                >
                                    <div className="flex items-center gap-4">
                                        <div className={`w-14 h-14 rounded-xl bg-${insight.color} flex items-center justify-center text-white shadow-lg`}>
                                            <i className={`fas ${insight.icon} text-xl`} />
                                        </div>
                                        <div className="flex-1">
                                            <h3 className="text-xl font-bold text-slate-800 mb-1">
                                                {insight.title}
                                            </h3>
                                            <p className="text-slate-600 text-sm mb-2">
                                                {insight.description}
                                            </p>
                                            <div className={`inline-flex items-center gap-2 px-3 py-1 rounded-full bg-${insight.color}/20 text-${insight.color} font-bold text-sm`}>
                                                <i className="fas fa-arrow-up text-xs" />
                                                {insight.value}
                                            </div>
                                        </div>
                                        {selectedInsight === index && (
                                            <motion.i
                                                initial={{ rotate: 0 }}
                                                animate={{ rotate: 90 }}
                                                className="fas fa-chevron-right text-slate-400"
                                            />
                                        )}
                                    </div>
                                </motion.div>
                            ))}
                        </motion.div>
                    </AnimatePresence>
                </div>

                {/* Detailed View */}
                <div className="relative">
                    <AnimatePresence mode="wait">
                        <motion.div
                            key={`${userRole}-${selectedInsight}`}
                            initial={{ opacity: 0, y: 50, scale: 0.9 }}
                            animate={{ opacity: 1, y: 0, scale: 1 }}
                            exit={{ opacity: 0, y: -50, scale: 0.9 }}
                            transition={{ duration: 0.5 }}
                            className="bg-white rounded-3xl shadow-2xl border border-slate-100 p-8 min-h-[400px]"
                        >
                            {/* Header */}
                            <div className="flex items-center gap-4 mb-6">
                                <div className={`w-16 h-16 rounded-2xl bg-${currentInsights[selectedInsight].color} flex items-center justify-center text-white shadow-lg`}>
                                    <i className={`fas ${currentInsights[selectedInsight].icon} text-2xl`} />
                                </div>
                                <div>
                                    <h3 className="text-2xl font-bold text-slate-800">
                                        {currentInsights[selectedInsight].title}
                                    </h3>
                                    <p className="text-slate-500">
                                        {userRole === 'seller' ? 'Seller Dashboard' : 'Market Owner Dashboard'}
                                    </p>
                                </div>
                            </div>

                            {/* Content */}
                            <div className="space-y-6">
                                <p className="text-lg text-slate-600 leading-relaxed">
                                    {currentInsights[selectedInsight].details}
                                </p>

                                {/* Mock Chart/Visualization */}
                                <div className="bg-slate-50 rounded-2xl p-6">
                                    <div className="flex items-center justify-between mb-4">
                                        <span className="font-bold text-slate-700">Performance Trend</span>
                                        <span className={`text-${currentInsights[selectedInsight].color} font-bold`}>
                                            {currentInsights[selectedInsight].value}
                                        </span>
                                    </div>
                                    
                                    {/* Simple bar visualization */}
                                    <div className="space-y-3">
                                        {[...Array(4)].map((_, i) => (
                                            <div key={i} className="flex items-center gap-3">
                                                <span className="text-xs text-slate-500 w-12">
                                                    Week {i + 1}
                                                </span>
                                                <div className="flex-1 bg-slate-200 rounded-full h-2 overflow-hidden">
                                                    <motion.div
                                                        initial={{ width: 0 }}
                                                        animate={{ width: `${Math.random() * 80 + 20}%` }}
                                                        transition={{ duration: 1, delay: i * 0.2 }}
                                                        className={`h-full bg-${currentInsights[selectedInsight].color} rounded-full`}
                                                    />
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </div>

                                {/* Action Button */}
                                <motion.button
                                    whileHover={{ scale: 1.05 }}
                                    whileTap={{ scale: 0.95 }}
                                    className={`w-full py-4 bg-${currentInsights[selectedInsight].color} text-white rounded-xl font-bold hover:opacity-90 transition-all`}
                                >
                                    View Detailed Analytics
                                </motion.button>
                            </div>
                        </motion.div>
                    </AnimatePresence>
                </div>
            </div>
        </div>
    );
};