import React from 'react';
import { motion } from 'framer-motion';

interface Agent {
    id: string;
    name: string;
    title: string;
    description: string;
    icon: string;
    color: string;
    specialties: string[];
    status: 'active' | 'processing' | 'idle';
    metrics: {
        tasksCompleted: number;
        accuracy: number;
        responseTime: string;
    };
}

interface AgentCardProps {
    agent: Agent;
    isSelected: boolean;
    isActive: boolean;
    onClick: () => void;
}

export const AgentCard: React.FC<AgentCardProps> = ({
    agent,
    isSelected,
    isActive,
    onClick
}) => {
    return (
        <motion.div
            onClick={onClick}
            whileHover={{ scale: 1.02, y: -5 }}
            whileTap={{ scale: 0.98 }}
            className={`relative bg-white rounded-2xl shadow-xl border cursor-pointer transition-all duration-300 overflow-hidden ${
                isSelected 
                    ? `border-${agent.color} shadow-${agent.color}/20 shadow-2xl` 
                    : 'border-slate-200 hover:border-slate-300'
            }`}
        >
            {/* Active Indicator */}
            {isActive && (
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-ethiGreen to-ethiBlue"
                />
            )}

            <div className="p-6">
                {/* Header */}
                <div className="flex items-center justify-between mb-4">
                    <div className={`w-14 h-14 rounded-xl bg-${agent.color} flex items-center justify-center text-white shadow-lg ${
                        isActive ? 'animate-pulse' : ''
                    }`}>
                        <i className={`fas ${agent.icon} text-xl`} />
                    </div>
                    
                    <div className="flex items-center gap-2">
                        <div className={`w-2 h-2 rounded-full ${
                            agent.status === 'active' ? 'bg-green-500 animate-pulse' :
                            agent.status === 'processing' ? 'bg-yellow-500 animate-pulse' :
                            'bg-gray-400'
                        }`} />
                        <span className="text-xs font-medium text-slate-500 capitalize">
                            {agent.status}
                        </span>
                    </div>
                </div>

                {/* Content */}
                <h3 className="text-xl font-bold text-slate-800 mb-2">{agent.name}</h3>
                <p className="text-slate-500 font-medium text-sm mb-4">{agent.title}</p>
                <p className="text-slate-600 text-sm leading-relaxed mb-4 line-clamp-3">
                    {agent.description}
                </p>

                {/* Specialties */}
                <div className="flex flex-wrap gap-1 mb-4">
                    {agent.specialties.slice(0, 2).map((specialty, index) => (
                        <span
                            key={index}
                            className={`px-2 py-1 rounded-full text-xs font-medium bg-${agent.color}/10 text-${agent.color} border border-${agent.color}/20`}
                        >
                            {specialty}
                        </span>
                    ))}
                    {agent.specialties.length > 2 && (
                        <span className="px-2 py-1 rounded-full text-xs font-medium bg-slate-100 text-slate-500">
                            +{agent.specialties.length - 2}
                        </span>
                    )}
                </div>

                {/* Quick Metrics */}
                <div className="grid grid-cols-2 gap-4 text-center">
                    <div>
                        <p className="text-lg font-bold text-slate-800">
                            {agent.metrics.tasksCompleted > 1000 
                                ? `${(agent.metrics.tasksCompleted / 1000).toFixed(1)}k`
                                : agent.metrics.tasksCompleted
                            }
                        </p>
                        <p className="text-xs text-slate-500">Tasks</p>
                    </div>
                    <div>
                        <p className="text-lg font-bold text-slate-800">{agent.metrics.accuracy}%</p>
                        <p className="text-xs text-slate-500">Accuracy</p>
                    </div>
                </div>

                {/* Activity Indicator */}
                {isActive && (
                    <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="mt-4 flex items-center gap-2 text-xs text-ethiGreen font-medium"
                    >
                        <motion.div
                            animate={{ rotate: 360 }}
                            transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                            className="w-3 h-3 border border-ethiGreen border-t-transparent rounded-full"
                        />
                        Currently processing...
                    </motion.div>
                )}
            </div>

            {/* Selection Indicator */}
            {isSelected && (
                <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    className={`absolute top-4 right-4 w-6 h-6 bg-${agent.color} rounded-full flex items-center justify-center text-white shadow-lg`}
                >
                    <i className="fas fa-check text-xs" />
                </motion.div>
            )}
        </motion.div>
    );
};