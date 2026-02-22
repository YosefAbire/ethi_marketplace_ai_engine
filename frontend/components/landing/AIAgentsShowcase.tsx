import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { AgentCard } from './AgentCard';
import { AgentInteraction } from './AgentInteraction';

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

export const AIAgentsShowcase: React.FC = () => {
    const [selectedAgent, setSelectedAgent] = useState<string>('workflow');
    const [agentActivity, setAgentActivity] = useState<Record<string, boolean>>({});

    const agents: Agent[] = [
        {
            id: 'workflow',
            name: 'Workflow Agent',
            title: 'Master Orchestrator',
            description: 'Intelligently routes queries and coordinates all other agents for optimal task execution.',
            icon: 'fa-network-wired',
            color: 'ethiGreen',
            specialties: ['Query Routing', 'Task Coordination', 'System Orchestration'],
            status: 'active',
            metrics: {
                tasksCompleted: 1247,
                accuracy: 98.5,
                responseTime: '0.3s'
            }
        },
        {
            id: 'sql',
            name: 'SQL Agent',
            title: 'Data Analyst',
            description: 'Transforms natural language into precise SQL queries and provides intelligent data summaries.',
            icon: 'fa-database',
            color: 'ethiBlue',
            specialties: ['SQL Generation', 'Data Analysis', 'Report Creation'],
            status: 'processing',
            metrics: {
                tasksCompleted: 892,
                accuracy: 96.8,
                responseTime: '0.8s'
            }
        },
        {
            id: 'rag',
            name: 'Knowledge Agent',
            title: 'Document Specialist',
            description: 'Processes and retrieves information from your document library using advanced RAG technology.',
            icon: 'fa-book-open',
            color: 'ethiYellow',
            specialties: ['Document Processing', 'Semantic Search', 'Knowledge Retrieval'],
            status: 'active',
            metrics: {
                tasksCompleted: 634,
                accuracy: 94.2,
                responseTime: '1.2s'
            }
        },
        {
            id: 'seller',
            name: 'Business Agent',
            title: 'Strategic Advisor',
            description: 'Provides Ethiopian market-specific business insights and strategic recommendations.',
            icon: 'fa-chart-line',
            color: 'ethiOrange',
            specialties: ['Market Analysis', 'Strategy Planning', 'Cultural Insights'],
            status: 'active',
            metrics: {
                tasksCompleted: 445,
                accuracy: 97.1,
                responseTime: '1.5s'
            }
        },
        {
            id: 'ops',
            name: 'Operations Agent',
            title: 'Logistics Manager',
            description: 'Handles operational queries, delivery tracking, and supply chain optimization.',
            icon: 'fa-cogs',
            color: 'ethiRed',
            specialties: ['Logistics', 'Order Management', 'Supply Chain'],
            status: 'idle',
            metrics: {
                tasksCompleted: 328,
                accuracy: 95.7,
                responseTime: '0.9s'
            }
        },
        {
            id: 'recommendation',
            name: 'Recommendation Engine',
            title: 'Intelligence Core',
            description: 'Advanced ML system providing pricing, inventory, and demand forecasting recommendations.',
            icon: 'fa-brain',
            color: 'ethiPurple',
            specialties: ['Predictive Analytics', 'Price Optimization', 'Demand Forecasting'],
            status: 'processing',
            metrics: {
                tasksCompleted: 756,
                accuracy: 99.1,
                responseTime: '2.1s'
            }
        }
    ];

    // Simulate agent activity
    useEffect(() => {
        const interval = setInterval(() => {
            const randomAgent = agents[Math.floor(Math.random() * agents.length)];
            setAgentActivity(prev => ({
                ...prev,
                [randomAgent.id]: true
            }));
            
            setTimeout(() => {
                setAgentActivity(prev => ({
                    ...prev,
                    [randomAgent.id]: false
                }));
            }, 2000);
        }, 3000);

        return () => clearInterval(interval);
    }, []);

    const selectedAgentData = agents.find(agent => agent.id === selectedAgent);

    return (
        <div className="max-w-7xl mx-auto px-8">
            <motion.div
                initial={{ opacity: 0, y: 50 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8 }}
                className="text-center mb-16"
            >
                <h2 className="text-5xl font-black mb-6 tracking-tight text-slate-800">
                    Meet Your <span className="text-ethiGreen">AI Team</span>
                </h2>
                <p className="text-xl text-slate-700 max-w-3xl mx-auto">
                    Six specialized agents working together to transform your marketplace operations
                </p>
            </motion.div>

            <div className="grid lg:grid-cols-3 gap-8">
                {/* Agent Cards Grid */}
                <div className="lg:col-span-2 grid md:grid-cols-2 gap-6">
                    {agents.map((agent, index) => (
                        <motion.div
                            key={agent.id}
                            initial={{ opacity: 0, y: 50 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.5, delay: index * 0.1 }}
                        >
                            <AgentCard
                                agent={agent}
                                isSelected={selectedAgent === agent.id}
                                isActive={agentActivity[agent.id]}
                                onClick={() => setSelectedAgent(agent.id)}
                            />
                        </motion.div>
                    ))}
                </div>

                {/* Selected Agent Details */}
                <div className="lg:col-span-1">
                    <div className="sticky top-8">
                        <AnimatePresence mode="wait">
                            {selectedAgentData && (
                                <motion.div
                                    key={selectedAgent}
                                    initial={{ opacity: 0, x: 50 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    exit={{ opacity: 0, x: -50 }}
                                    transition={{ duration: 0.3 }}
                                    className="bg-white rounded-3xl shadow-2xl border border-slate-100 p-8"
                                >
                                    {/* Agent Header */}
                                    <div className="flex items-center gap-4 mb-6">
                                        <div className={`w-16 h-16 rounded-2xl bg-${selectedAgentData.color} flex items-center justify-center text-white shadow-lg`}>
                                            <i className={`fas ${selectedAgentData.icon} text-2xl`} />
                                        </div>
                                        <div>
                                            <h3 className="text-2xl font-bold text-slate-800">{selectedAgentData.name}</h3>
                                            <p className="text-slate-500 font-medium">{selectedAgentData.title}</p>
                                        </div>
                                    </div>

                                    {/* Status Indicator */}
                                    <div className="flex items-center gap-2 mb-6">
                                        <div className={`w-3 h-3 rounded-full ${
                                            selectedAgentData.status === 'active' ? 'bg-green-500 animate-pulse' :
                                            selectedAgentData.status === 'processing' ? 'bg-yellow-500 animate-pulse' :
                                            'bg-gray-400'
                                        }`} />
                                        <span className="text-sm font-medium capitalize text-slate-600">
                                            {selectedAgentData.status}
                                        </span>
                                    </div>

                                    {/* Description */}
                                    <p className="text-slate-600 leading-relaxed mb-6">
                                        {selectedAgentData.description}
                                    </p>

                                    {/* Specialties */}
                                    <div className="mb-6">
                                        <h4 className="font-bold text-slate-800 mb-3">Specialties</h4>
                                        <div className="flex flex-wrap gap-2">
                                            {selectedAgentData.specialties.map((specialty, index) => (
                                                <span
                                                    key={index}
                                                    className={`px-3 py-1 rounded-full text-xs font-medium bg-${selectedAgentData.color}/10 text-${selectedAgentData.color} border border-${selectedAgentData.color}/20`}
                                                >
                                                    {specialty}
                                                </span>
                                            ))}
                                        </div>
                                    </div>

                                    {/* Performance Metrics */}
                                    <div className="space-y-4">
                                        <h4 className="font-bold text-slate-800">Performance Metrics</h4>
                                        
                                        <div className="space-y-3">
                                            <div className="flex justify-between items-center">
                                                <span className="text-sm text-slate-600">Tasks Completed</span>
                                                <span className="font-bold text-slate-800">
                                                    {selectedAgentData.metrics.tasksCompleted.toLocaleString()}
                                                </span>
                                            </div>
                                            
                                            <div className="flex justify-between items-center">
                                                <span className="text-sm text-slate-600">Accuracy</span>
                                                <span className="font-bold text-slate-800">
                                                    {selectedAgentData.metrics.accuracy}%
                                                </span>
                                            </div>
                                            
                                            <div className="flex justify-between items-center">
                                                <span className="text-sm text-slate-600">Avg Response Time</span>
                                                <span className="font-bold text-slate-800">
                                                    {selectedAgentData.metrics.responseTime}
                                                </span>
                                            </div>
                                        </div>

                                        {/* Accuracy Progress Bar */}
                                        <div className="mt-4">
                                            <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
                                                <motion.div
                                                    className={`h-full bg-${selectedAgentData.color}`}
                                                    initial={{ width: 0 }}
                                                    animate={{ width: `${selectedAgentData.metrics.accuracy}%` }}
                                                    transition={{ duration: 1, ease: "easeOut" }}
                                                />
                                            </div>
                                        </div>
                                    </div>

                                    {/* Interactive Demo Button */}
                                    <motion.button
                                        whileHover={{ scale: 1.05 }}
                                        whileTap={{ scale: 0.95 }}
                                        className={`w-full mt-6 py-3 bg-${selectedAgentData.color} text-white rounded-xl font-bold hover:opacity-90 transition-all`}
                                    >
                                        Try {selectedAgentData.name}
                                    </motion.button>
                                </motion.div>
                            )}
                        </AnimatePresence>
                    </div>
                </div>
            </div>

            {/* Agent Interaction Demo */}
            <motion.div
                initial={{ opacity: 0, y: 50 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 0.3 }}
                className="mt-16"
            >
                <AgentInteraction selectedAgent={selectedAgent} />
            </motion.div>
        </div>
    );
};