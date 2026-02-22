import React from 'react';
import { motion } from 'framer-motion';

export const FloatingElements: React.FC = () => {
    const elements = [
        { icon: 'fa-database', color: 'ethiBlue', size: 'w-8 h-8', delay: 0 },
        { icon: 'fa-brain', color: 'ethiGreen', size: 'w-6 h-6', delay: 0.5 },
        { icon: 'fa-chart-line', color: 'ethiYellow', size: 'w-10 h-10', delay: 1 },
        { icon: 'fa-cogs', color: 'ethiRed', size: 'w-7 h-7', delay: 1.5 },
        { icon: 'fa-lightbulb', color: 'ethiOrange', size: 'w-9 h-9', delay: 2 },
        { icon: 'fa-network-wired', color: 'ethiPurple', size: 'w-8 h-8', delay: 2.5 }
    ];

    return (
        <div className="absolute inset-0 pointer-events-none overflow-hidden">
            {elements.map((element, index) => (
                <motion.div
                    key={index}
                    className={`absolute ${element.size} bg-${element.color} rounded-xl flex items-center justify-center text-white shadow-lg opacity-20`}
                    style={{
                        left: `${Math.random() * 80 + 10}%`,
                        top: `${Math.random() * 80 + 10}%`,
                    }}
                    animate={{
                        y: [0, -20, 0],
                        rotate: [0, 5, -5, 0],
                        scale: [1, 1.1, 1],
                    }}
                    transition={{
                        duration: 4 + Math.random() * 2,
                        repeat: Infinity,
                        delay: element.delay,
                        ease: "easeInOut"
                    }}
                >
                    <i className={`fas ${element.icon} text-sm`} />
                </motion.div>
            ))}
            
            {/* Floating particles */}
            {[...Array(20)].map((_, i) => (
                <motion.div
                    key={`particle-${i}`}
                    className="absolute w-1 h-1 bg-ethiGreen rounded-full opacity-30"
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
    );
};