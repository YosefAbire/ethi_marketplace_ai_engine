import React, { useState, useEffect } from 'react';
import { motion, useInView } from 'framer-motion';
import { useRef } from 'react';

interface StatItem {
    label: string;
    value: number;
    suffix: string;
    icon: string;
    color: string;
    description: string;
}

export const InteractiveStats: React.FC = () => {
    const [animatedValues, setAnimatedValues] = useState<Record<string, number>>({});
    const ref = useRef(null);
    const isInView = useInView(ref, { once: true });

    const stats: StatItem[] = [
        {
            label: "AI Agents",
            value: 6,
            suffix: "",
            icon: "fa-brain",
            color: "ethiGreen",
            description: "Specialized agents working 24/7"
        },
        {
            label: "Response Time",
            value: 0.8,
            suffix: "s",
            icon: "fa-bolt",
            color: "ethiYellow",
            description: "Average AI response time"
        },
        {
            label: "Accuracy Rate",
            value: 98.5,
            suffix: "%",
            icon: "fa-target",
            color: "ethiBlue",
            description: "AI prediction accuracy"
        },
        {
            label: "Tasks Automated",
            value: 15000,
            suffix: "+",
            icon: "fa-cogs",
            color: "ethiPurple",
            description: "Daily automated operations"
        },
        {
            label: "Cost Reduction",
            value: 45,
            suffix: "%",
            icon: "fa-chart-line-down",
            color: "ethiRed",
            description: "Operational cost savings"
        },
        {
            label: "Revenue Growth",
            value: 127,
            suffix: "%",
            icon: "fa-arrow-trend-up",
            color: "ethiOrange",
            description: "Average seller revenue increase"
        }
    ];

    useEffect(() => {
        if (isInView) {
            stats.forEach((stat, index) => {
                setTimeout(() => {
                    const duration = 2000;
                    const steps = 60;
                    const increment = stat.value / steps;
                    let current = 0;
                    
                    const timer = setInterval(() => {
                        current += increment;
                        if (current >= stat.value) {
                            current = stat.value;
                            clearInterval(timer);
                        }
                        setAnimatedValues(prev => ({
                            ...prev,
                            [stat.label]: current
                        }));
                    }, duration / steps);
                }, index * 200);
            });
        }
    }, [isInView]);

    const formatValue = (value: number, suffix: string) => {
        if (suffix === '+' && value >= 1000) {
            return `${(value / 1000).toFixed(1)}k${suffix}`;
        }
        if (suffix === '%' || suffix === 's') {
            return `${value.toFixed(1)}${suffix}`;
        }
        return `${Math.floor(value)}${suffix}`;
    };

    return (
        <div ref={ref} className="max-w-7xl mx-auto px-8">
            <motion.div
                initial={{ opacity: 0, y: 50 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8 }}
                className="text-center mb-16"
            >
                <h2 className="text-5xl font-black mb-6 tracking-tight text-slate-800">
                    Powered by <span className="text-ethiGreen">Intelligence</span>
                </h2>
                <p className="text-xl text-slate-700 max-w-3xl mx-auto">
                    Real performance metrics from our AI-powered marketplace engine
                </p>
            </motion.div>

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
                {stats.map((stat, index) => (
                    <motion.div
                        key={stat.label}
                        initial={{ opacity: 0, y: 50 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.6, delay: index * 0.1 }}
                        whileHover={{ scale: 1.05, y: -10 }}
                        className="relative bg-white rounded-3xl shadow-xl border border-slate-100 p-8 text-center overflow-hidden group cursor-pointer"
                    >
                        {/* Background Pattern */}
                        <div className="absolute inset-0 opacity-5 group-hover:opacity-10 transition-opacity">
                            <div className="absolute inset-0 tibeb-bg" />
                        </div>

                        {/* Icon */}
                        <motion.div
                            whileHover={{ rotate: 360 }}
                            transition={{ duration: 0.6 }}
                            className={`w-20 h-20 mx-auto mb-6 rounded-2xl bg-${stat.color} flex items-center justify-center text-white shadow-lg shadow-${stat.color}/30 relative z-10`}
                        >
                            <i className={`fas ${stat.icon} text-3xl`} />
                        </motion.div>

                        {/* Value */}
                        <motion.div
                            className="relative z-10 mb-4"
                        >
                            <div className="text-5xl font-black text-slate-800 mb-2">
                                {formatValue(animatedValues[stat.label] || 0, stat.suffix)}
                            </div>
                            <h3 className="text-xl font-bold text-slate-700 mb-2">{stat.label}</h3>
                            <p className="text-slate-500 text-sm leading-relaxed">{stat.description}</p>
                        </motion.div>

                        {/* Progress Bar */}
                        <div className="relative z-10 mt-6">
                            <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
                                <motion.div
                                    initial={{ width: 0 }}
                                    animate={{ 
                                        width: isInView ? `${Math.min((animatedValues[stat.label] || 0) / stat.value * 100, 100)}%` : 0 
                                    }}
                                    transition={{ duration: 2, delay: index * 0.2 }}
                                    className={`h-full bg-${stat.color} rounded-full`}
                                />
                            </div>
                        </div>

                        {/* Hover Effect */}
                        <motion.div
                            initial={{ scale: 0, opacity: 0 }}
                            whileHover={{ scale: 1, opacity: 1 }}
                            className={`absolute top-4 right-4 w-8 h-8 bg-${stat.color} rounded-full flex items-center justify-center text-white shadow-lg`}
                        >
                            <i className="fas fa-arrow-up text-sm" />
                        </motion.div>
                    </motion.div>
                ))}
            </div>

            {/* Bottom CTA */}
            <motion.div
                initial={{ opacity: 0, y: 50 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 0.6 }}
                className="text-center mt-16"
            >
                <div className="inline-flex items-center gap-4 px-8 py-4 bg-gradient-to-r from-ethiGreen to-ethiBlue rounded-2xl text-white shadow-xl">
                    <div className="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center">
                        <i className="fas fa-rocket text-xl" />
                    </div>
                    <div className="text-left">
                        <p className="font-bold text-lg">Ready to experience these results?</p>
                        <p className="text-white/80 text-sm">Join thousands of successful Ethiopian sellers</p>
                    </div>
                </div>
            </motion.div>
        </div>
    );
};