import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface WorkflowStep {
    id: string;
    title: string;
    description: string;
    icon: string;
    color: string;
    position: { x: number; y: number };
    connections: string[];
}

export const WorkflowVisualization: React.FC = () => {
    const [activeStep, setActiveStep] = useState<string>('data-input');
    const [animationPhase, setAnimationPhase] = useState(0);

    const steps: WorkflowStep[] = [
        {
            id: 'data-input',
            title: 'Data Collection',
            description: 'Ethiopian marketplace data: products (teff, coffee, honey), prices in Birr, customer transactions, and seasonal patterns flow into our secure system',
            icon: 'fa-database',
            color: 'ethiBlue',
            position: { x: 10, y: 50 },
            connections: ['ai-processing']
        },
        {
            id: 'ai-processing',
            title: 'Multi-Agent AI Processing',
            description: 'Six specialized AI agents (Workflow, SQL, RAG, Seller, Operations, Recommendation) work together to analyze data with Ethiopian market context',
            icon: 'fa-brain',
            color: 'ethiGreen',
            position: { x: 35, y: 30 },
            connections: ['insights-generation', 'recommendations']
        },
        {
            id: 'insights-generation',
            title: 'Cultural Intelligence',
            description: 'Generate insights considering Ethiopian holidays (Meskel, Timkat), regional preferences, and local business practices',
            icon: 'fa-chart-line',
            color: 'ethiYellow',
            position: { x: 65, y: 20 },
            connections: ['actions']
        },
        {
            id: 'recommendations',
            title: 'Smart Recommendations',
            description: 'AI suggests optimal pricing in Birr, inventory management for seasonal demands, and culturally-aware marketing strategies',
            icon: 'fa-lightbulb',
            color: 'ethiOrange',
            position: { x: 65, y: 60 },
            connections: ['actions']
        },
        {
            id: 'actions',
            title: 'Automated Execution',
            description: 'Execute price adjustments, send notifications in Amharic/English, optimize delivery routes across Ethiopian cities, and generate reports',
            icon: 'fa-cogs',
            color: 'ethiRed',
            position: { x: 80, y: 40 },
            connections: []
        }
    ];

    useEffect(() => {
        const interval = setInterval(() => {
            setAnimationPhase(prev => (prev + 1) % steps.length);
            setActiveStep(steps[animationPhase].id);
        }, 2500);
        return () => clearInterval(interval);
    }, [animationPhase]);

    const getConnectionPath = (from: WorkflowStep, to: WorkflowStep) => {
        const startX = from.position.x + 5;
        const startY = from.position.y;
        const endX = to.position.x - 5;
        const endY = to.position.y;
        
        const midX = (startX + endX) / 2;
        
        return `M ${startX} ${startY} Q ${midX} ${startY} ${endX} ${endY}`;
    };

    return (
        <div className="max-w-7xl mx-auto px-8">
            <motion.div
                initial={{ opacity: 0, y: 50 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8 }}
                className="text-center mb-16"
            >
                <h2 className="text-5xl font-black mb-6 tracking-tight text-slate-800">
                    How the <span className="text-ethiGreen">AI Engine</span> Works
                </h2>
                <p className="text-xl text-slate-700 max-w-3xl mx-auto">
                    Watch data transform into actionable insights through our intelligent workflow
                </p>
            </motion.div>

            <div className="relative bg-white rounded-3xl shadow-2xl border border-slate-100 p-8 min-h-[600px] overflow-visible">
                {/* Background Pattern */}
                <div className="absolute inset-0 opacity-5" style={{ zIndex: 0 }}>
                    <div className="absolute inset-0 tibeb-bg" />
                </div>

                {/* SVG Connections */}
                <svg className="absolute inset-0 w-full h-full pointer-events-none" style={{ zIndex: 1 }}>
                    {steps.map(step => 
                        step.connections.map(connectionId => {
                            const targetStep = steps.find(s => s.id === connectionId);
                            if (!targetStep) return null;
                            
                            return (
                                <motion.path
                                    key={`${step.id}-${connectionId}`}
                                    d={getConnectionPath(step, targetStep)}
                                    stroke={activeStep === step.id ? '#10B981' : '#E2E8F0'}
                                    strokeWidth="3"
                                    fill="none"
                                    strokeDasharray="10,5"
                                    initial={{ pathLength: 0 }}
                                    animate={{ 
                                        pathLength: activeStep === step.id ? 1 : 0.3,
                                        stroke: activeStep === step.id ? '#10B981' : '#E2E8F0'
                                    }}
                                    transition={{ duration: 1, ease: "easeInOut" }}
                                />
                            );
                        })
                    )}
                </svg>

                {/* Workflow Steps */}
                {steps.map((step, index) => (
                    <motion.div
                        key={step.id}
                        className="absolute cursor-pointer"
                        style={{
                            left: `${step.position.x}%`,
                            top: `${step.position.y}%`,
                            transform: 'translate(-50%, -50%)',
                            zIndex: activeStep === step.id ? 50 : 20
                        }}
                        onClick={() => setActiveStep(step.id)}
                        whileHover={{ scale: 1.1 }}
                        animate={{
                            scale: activeStep === step.id ? 1.2 : 1
                        }}
                    >
                        {/* Step Circle */}
                        <div className={`w-20 h-20 rounded-full flex items-center justify-center text-white shadow-xl transition-all duration-500 ${
                            activeStep === step.id 
                                ? `bg-${step.color} shadow-${step.color}/50` 
                                : 'bg-slate-400'
                        }`}>
                            <i className={`fas ${step.icon} text-2xl`} />
                        </div>

                        {/* Step Info Card */}
                        <AnimatePresence>
                            {activeStep === step.id && (
                                <motion.div
                                    initial={{ opacity: 0, y: 20, scale: 0.8 }}
                                    animate={{ opacity: 1, y: 0, scale: 1 }}
                                    exit={{ opacity: 0, y: 20, scale: 0.8 }}
                                    className={`absolute ${
                                        step.position.y < 50 ? 'top-24' : 'bottom-24'
                                    } ${
                                        step.position.x > 70 ? 'right-0' : 'left-1/2 transform -translate-x-1/2'
                                    } w-80 bg-white rounded-2xl shadow-2xl border border-slate-100 p-6`}
                                    style={{ zIndex: 100 }}
                                >
                                    <h3 className="font-bold text-lg mb-2 text-slate-800">{step.title}</h3>
                                    <p className="text-sm text-slate-600 leading-relaxed mb-4">{step.description}</p>
                                    
                                    {/* Animated Progress Bar */}
                                    <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
                                        <motion.div
                                            className={`h-full bg-${step.color}`}
                                            initial={{ width: 0 }}
                                            animate={{ width: '100%' }}
                                            transition={{ duration: 2, ease: "easeOut" }}
                                        />
                                    </div>
                                    
                                    {/* Arrow pointing to step */}
                                    <div className={`absolute ${
                                        step.position.y < 50 ? '-bottom-3' : '-top-3'
                                    } ${
                                        step.position.x > 70 ? 'left-6' : 'left-1/2 transform -translate-x-1/2'
                                    } w-0 h-0 ${
                                        step.position.y < 50 
                                            ? 'border-l-8 border-r-8 border-t-8 border-l-transparent border-r-transparent border-t-white' 
                                            : 'border-l-8 border-r-8 border-b-8 border-l-transparent border-r-transparent border-b-white'
                                    } drop-shadow-lg`} />
                                </motion.div>
                            )}
                        </AnimatePresence>

                        {/* Pulse Animation for Active Step */}
                        {activeStep === step.id && (
                            <motion.div
                                className={`absolute inset-0 rounded-full bg-${step.color} opacity-30`}
                                style={{ zIndex: -1 }}
                                animate={{
                                    scale: [1, 1.5, 1],
                                    opacity: [0.3, 0, 0.3]
                                }}
                                transition={{
                                    duration: 2,
                                    repeat: Infinity,
                                    ease: "easeInOut"
                                }}
                            />
                        )}
                    </motion.div>
                ))}

                {/* Data Flow Particles */}
                <div className="absolute inset-0 pointer-events-none" style={{ zIndex: 5 }}>
                    {[...Array(5)].map((_, i) => (
                        <motion.div
                            key={i}
                            className="absolute w-2 h-2 bg-ethiGreen rounded-full"
                            animate={{
                                x: [0, 200, 400, 600, 800],
                                y: [300, 200, 150, 200, 250],
                                opacity: [0, 1, 1, 1, 0]
                            }}
                            transition={{
                                duration: 4,
                                repeat: Infinity,
                                delay: i * 0.8,
                                ease: "easeInOut"
                            }}
                        />
                    ))}
                </div>
            </div>

            {/* Step Navigation */}
            <div className="flex justify-center mt-8 gap-4">
                {steps.map((step, index) => (
                    <button
                        key={step.id}
                        onClick={() => setActiveStep(step.id)}
                        className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
                            activeStep === step.id
                                ? 'bg-ethiGreen text-white shadow-lg'
                                : 'bg-white/80 text-slate-700 hover:bg-white border border-slate-200 shadow-sm'
                        }`}
                    >
                        {index + 1}. {step.title}
                    </button>
                ))}
            </div>
        </div>
    );
};