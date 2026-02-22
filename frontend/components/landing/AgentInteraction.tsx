import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface AgentInteractionProps {
    selectedAgent: string;
}

export const AgentInteraction: React.FC<AgentInteractionProps> = ({ selectedAgent }) => {
    const [messages, setMessages] = useState<Array<{ role: 'user' | 'agent'; content: string; timestamp: Date }>>([]);
    const [isTyping, setIsTyping] = useState(false);
    const [inputValue, setInputValue] = useState('');

    const agentResponses = {
        workflow: [
            "I'll coordinate with our specialized agents to provide you with comprehensive insights about your Ethiopian marketplace operations.",
            "Based on your query, I'm routing this to our SQL and Business agents who understand Ethiopian market dynamics.",
            "Your request has been processed through our multi-agent system designed specifically for Ethiopian commerce."
        ],
        sql: [
            "Analyzing your database... Found 247 products including teff, coffee, and honey with prices in Ethiopian Birr.",
            "Based on sales data, coffee sales increased 23% during the harvest season, with Yirgacheffe leading at 850 Birr per kg.",
            "Inventory analysis shows teff flour, berbere spice, and honey need restocking before Meskel celebrations."
        ],
        rag: [
            "I've searched your documents and found information about Ethiopian trade regulations and marketplace policies.",
            "According to your uploaded documents, the return period follows Ethiopian commercial law - 30 days for most products.",
            "Found detailed information about seasonal trading patterns during Ethiopian holidays in your knowledge base."
        ],
        seller: [
            "For the upcoming Meskel holiday, I recommend increasing honey and teff inventory by 40% based on historical demand.",
            "Your pricing strategy could be optimized - consider raising premium coffee prices to 950 Birr per kg during peak season.",
            "Market analysis shows strong demand for traditional crafts in Addis Ababa, especially during wedding seasons."
        ],
        ops: [
            "Your order #1247 is in transit from Addis Ababa to Bahir Dar and will arrive within 2 business days via Ethiopian postal service.",
            "I've optimized delivery routes across Ethiopian cities including Arba Minch to reduce shipping costs by 15% while maintaining quality.",
            "Supply chain analysis indicates potential delays in coffee shipments from Sidama region due to seasonal road conditions."
        ],
        recommendation: [
            "Based on Ethiopian market analysis, focus on grains (teff, barley) and coffee during harvest seasons for maximum profit.",
            "Demand forecasting shows 35% increase in traditional items during Timkat and Easter celebrations.",
            "Price optimization suggests adjusting honey to 475 Birr and teff flour to 2,600 Birr for optimal revenue in current market."
        ]
    };

    const sampleQueries = {
        workflow: "How can I optimize my Ethiopian marketplace operations for the upcoming holiday season?",
        sql: "Show me the top selling Ethiopian products this month with prices in Birr",
        rag: "What are the return policies for traditional Ethiopian products in my marketplace?",
        seller: "How should I prepare my inventory for Meskel and Timkat celebrations?",
        ops: "What's the delivery status for orders going to different Ethiopian regions?",
        recommendation: "What traditional Ethiopian products should I focus on for maximum profit during harvest season?"
    };

    const handleSendMessage = async (message: string) => {
        if (!message.trim()) return;

        const userMessage = { role: 'user' as const, content: message, timestamp: new Date() };
        setMessages(prev => [...prev, userMessage]);
        setInputValue('');
        setIsTyping(true);

        // Simulate agent processing time
        setTimeout(() => {
            const responses = agentResponses[selectedAgent as keyof typeof agentResponses] || agentResponses.workflow;
            const randomResponse = responses[Math.floor(Math.random() * responses.length)];
            
            const agentMessage = { role: 'agent' as const, content: randomResponse, timestamp: new Date() };
            setMessages(prev => [...prev, agentMessage]);
            setIsTyping(false);
        }, 1500 + Math.random() * 1000);
    };

    const handleQuickQuery = () => {
        const query = sampleQueries[selectedAgent as keyof typeof sampleQueries] || sampleQueries.workflow;
        handleSendMessage(query);
    };

    return (
        <div className="bg-white rounded-3xl shadow-2xl border border-slate-100 overflow-hidden">
            <div className="bg-gradient-to-r from-ethiGreen to-ethiBlue p-6 text-white">
                <h3 className="text-2xl font-bold mb-2">Try the AI Agent</h3>
                <p className="text-white/80">Experience real-time interaction with our intelligent agents</p>
            </div>

            <div className="p-6">
                {/* Chat Messages */}
                <div className="h-64 overflow-y-auto mb-6 space-y-4">
                    <AnimatePresence>
                        {messages.length === 0 && (
                            <motion.div
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                className="text-center text-slate-500 py-8"
                            >
                                <i className="fas fa-comments text-4xl mb-4 text-slate-300" />
                                <p>Start a conversation with the {selectedAgent} agent</p>
                            </motion.div>
                        )}
                        
                        {messages.map((message, index) => (
                            <motion.div
                                key={index}
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                            >
                                <div className={`max-w-xs lg:max-w-md px-4 py-3 rounded-2xl ${
                                    message.role === 'user'
                                        ? 'bg-ethiGreen text-white'
                                        : 'bg-slate-100 text-slate-800'
                                }`}>
                                    <p className="text-sm">{message.content}</p>
                                    <p className="text-xs opacity-70 mt-1">
                                        {message.timestamp.toLocaleTimeString()}
                                    </p>
                                </div>
                            </motion.div>
                        ))}
                        
                        {isTyping && (
                            <motion.div
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                className="flex justify-start"
                            >
                                <div className="bg-slate-100 px-4 py-3 rounded-2xl">
                                    <div className="flex gap-1">
                                        <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" />
                                        <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce delay-100" />
                                        <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce delay-200" />
                                    </div>
                                </div>
                            </motion.div>
                        )}
                    </AnimatePresence>
                </div>

                {/* Quick Action Button */}
                <div className="mb-4">
                    <motion.button
                        onClick={handleQuickQuery}
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                        className="w-full p-3 bg-slate-50 border border-slate-200 rounded-xl text-slate-600 hover:bg-slate-100 transition-all text-sm"
                    >
                        <i className="fas fa-magic-wand-sparkles mr-2" />
                        Try sample query: "{sampleQueries[selectedAgent as keyof typeof sampleQueries]}"
                    </motion.button>
                </div>

                {/* Input Area */}
                <div className="flex gap-3">
                    <input
                        type="text"
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && handleSendMessage(inputValue)}
                        placeholder="Ask the AI agent anything..."
                        className="flex-1 px-4 py-3 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-ethiGreen/20 focus:border-ethiGreen"
                        disabled={isTyping}
                    />
                    <motion.button
                        onClick={() => handleSendMessage(inputValue)}
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        disabled={isTyping || !inputValue.trim()}
                        className="px-6 py-3 bg-ethiGreen text-white rounded-xl font-medium hover:bg-ethiGreen/90 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        <i className="fas fa-paper-plane" />
                    </motion.button>
                </div>
            </div>
        </div>
    );
};