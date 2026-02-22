import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { LineChart, Line, AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

interface InsightCard {
    id: string;
    title: string;
    value: string;
    change: number;
    icon: string;
    color: string;
    trend: 'up' | 'down' | 'stable';
}

interface MarketData {
    time: string;
    revenue: number;
    orders: number;
    products: number;
    users: number;
}

export const LiveInsightsDashboard: React.FC = () => {
    const [currentTime, setCurrentTime] = useState(new Date());
    const [marketData, setMarketData] = useState<MarketData[]>([]);
    const [insights, setInsights] = useState<InsightCard[]>([]);
    const [activeMetric, setActiveMetric] = useState('revenue');

    // Generate realistic market data
    useEffect(() => {
        const generateData = () => {
            const now = new Date();
            const data: MarketData[] = [];
            
            for (let i = 23; i >= 0; i--) {
                const time = new Date(now.getTime() - i * 60 * 60 * 1000);
                data.push({
                    time: time.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
                    revenue: Math.floor(Math.random() * 5000) + 15000 + (i * 100),
                    orders: Math.floor(Math.random() * 50) + 80 + (i * 2),
                    products: Math.floor(Math.random() * 20) + 450 + (i * 1),
                    users: Math.floor(Math.random() * 30) + 200 + (i * 3)
                });
            }
            
            setMarketData(data);
        };

        generateData();
        const interval = setInterval(generateData, 30000); // Update every 30 seconds
        return () => clearInterval(interval);
    }, []);

    // Generate insights
    useEffect(() => {
        const generateInsights = () => {
            const newInsights: InsightCard[] = [
                {
                    id: 'revenue',
                    title: 'Total Revenue',
                    value: `${(Math.random() * 50000 + 150000).toLocaleString('en-US', { maximumFractionDigits: 0 })} ETB`,
                    change: Math.random() * 20 + 5,
                    icon: 'fa-coins',
                    color: 'ethiGreen',
                    trend: 'up'
                },
                {
                    id: 'orders',
                    title: 'Active Orders',
                    value: Math.floor(Math.random() * 200 + 800).toString(),
                    change: Math.random() * 15 + 2,
                    icon: 'fa-shopping-cart',
                    color: 'ethiBlue',
                    trend: 'up'
                },
                {
                    id: 'products',
                    title: 'Products Listed',
                    value: Math.floor(Math.random() * 100 + 1200).toString(),
                    change: Math.random() * 10 + 1,
                    icon: 'fa-box',
                    color: 'ethiYellow',
                    trend: 'up'
                },
                {
                    id: 'efficiency',
                    title: 'AI Efficiency',
                    value: `${(Math.random() * 5 + 95).toFixed(1)}%`,
                    change: Math.random() * 3 + 0.5,
                    icon: 'fa-brain',
                    color: 'ethiPurple',
                    trend: 'up'
                }
            ];
            
            setInsights(newInsights);
        };

        generateInsights();
        const interval = setInterval(generateInsights, 5000);
        return () => clearInterval(interval);
    }, []);

    // Update current time
    useEffect(() => {
        const timer = setInterval(() => setCurrentTime(new Date()), 1000);
        return () => clearInterval(timer);
    }, []);

    const categoryData = [
        { name: 'Grains', value: 35, color: '#10B981' },
        { name: 'Coffee', value: 25, color: '#F59E0B' },
        { name: 'Crafts', value: 20, color: '#EF4444' },
        { name: 'Oils', value: 12, color: '#8B5CF6' },
        { name: 'Others', value: 8, color: '#6B7280' }
    ];

    return (
        <div className="max-w-7xl mx-auto px-8">
            <motion.div
                initial={{ opacity: 0, y: 50 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8 }}
                className="text-center mb-16"
            >
                <h2 className="text-5xl font-black mb-6 tracking-tight text-slate-800">
                    <span className="text-ethiGreen">Live</span> Market Intelligence
                </h2>
                <p className="text-xl text-slate-700 max-w-3xl mx-auto">
                    Real-time insights powered by AI analysis of marketplace data
                </p>
                
                {/* Live Time Indicator */}
                <div className="flex items-center justify-center gap-3 mt-8">
                    <div className="w-3 h-3 bg-red-500 rounded-full animate-pulse" />
                    <span className="text-sm font-medium text-slate-700">
                        Live Data • {currentTime.toLocaleTimeString()}
                    </span>
                </div>
            </motion.div>

            {/* Insights Cards */}
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
                {insights.map((insight, index) => (
                    <motion.div
                        key={insight.id}
                        initial={{ opacity: 0, y: 50 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5, delay: index * 0.1 }}
                        whileHover={{ scale: 1.05, y: -5 }}
                        className="bg-white rounded-2xl shadow-xl border border-slate-100 p-6 cursor-pointer"
                        onClick={() => setActiveMetric(insight.id)}
                    >
                        <div className="flex items-center justify-between mb-4">
                            <div className={`w-12 h-12 rounded-xl bg-${insight.color} flex items-center justify-center text-white shadow-lg`}>
                                <i className={`fas ${insight.icon} text-xl`} />
                            </div>
                            <div className="flex items-center gap-1 text-green-500">
                                <i className="fas fa-arrow-up text-xs" />
                                <span className="text-sm font-bold">+{insight.change.toFixed(1)}%</span>
                            </div>
                        </div>
                        
                        <h3 className="text-slate-600 text-sm font-medium mb-2">{insight.title}</h3>
                        <p className="text-3xl font-black text-slate-800">{insight.value}</p>
                        
                        {/* Mini trend indicator */}
                        <div className="mt-4 h-1 bg-slate-100 rounded-full overflow-hidden">
                            <motion.div
                                className={`h-full bg-${insight.color}`}
                                initial={{ width: 0 }}
                                animate={{ width: `${Math.random() * 100}%` }}
                                transition={{ duration: 2, ease: "easeOut" }}
                            />
                        </div>
                    </motion.div>
                ))}
            </div>

            {/* Charts Section */}
            <div className="grid lg:grid-cols-3 gap-8">
                {/* Main Chart */}
                <div className="lg:col-span-2 bg-white rounded-3xl shadow-2xl border border-slate-100 p-8">
                    <div className="flex items-center justify-between mb-6">
                        <h3 className="text-2xl font-bold text-slate-800">Market Trends (24h)</h3>
                        <div className="flex gap-2">
                            {['revenue', 'orders', 'products'].map(metric => (
                                <button
                                    key={metric}
                                    onClick={() => setActiveMetric(metric)}
                                    className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                                        activeMetric === metric
                                            ? 'bg-ethiGreen text-white shadow-lg'
                                            : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                                    }`}
                                >
                                    {metric.charAt(0).toUpperCase() + metric.slice(1)}
                                </button>
                            ))}
                        </div>
                    </div>
                    
                    <div className="h-80">
                        <ResponsiveContainer width="100%" height="100%">
                            <AreaChart data={marketData}>
                                <defs>
                                    <linearGradient id="colorGradient" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="#10B981" stopOpacity={0.3}/>
                                        <stop offset="95%" stopColor="#10B981" stopOpacity={0}/>
                                    </linearGradient>
                                </defs>
                                <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
                                <XAxis dataKey="time" stroke="#64748B" fontSize={12} />
                                <YAxis stroke="#64748B" fontSize={12} />
                                <Tooltip 
                                    contentStyle={{
                                        backgroundColor: 'white',
                                        border: '1px solid #E2E8F0',
                                        borderRadius: '12px',
                                        boxShadow: '0 10px 25px rgba(0,0,0,0.1)'
                                    }}
                                    formatter={(value, name) => {
                                        if (name === 'revenue') {
                                            return [`${Number(value).toLocaleString()} ETB`, 'Revenue'];
                                        }
                                        return [value, name.charAt(0).toUpperCase() + name.slice(1)];
                                    }}
                                />
                                <Area
                                    type="monotone"
                                    dataKey={activeMetric}
                                    stroke="#10B981"
                                    strokeWidth={3}
                                    fill="url(#colorGradient)"
                                />
                            </AreaChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* Side Charts */}
                <div className="space-y-8">
                    {/* Category Distribution */}
                    <div className="bg-white rounded-3xl shadow-2xl border border-slate-100 p-6">
                        <h3 className="text-xl font-bold text-slate-800 mb-4">Category Distribution</h3>
                        <div className="h-48">
                            <ResponsiveContainer width="100%" height="100%">
                                <PieChart>
                                    <Pie
                                        data={categoryData}
                                        cx="50%"
                                        cy="50%"
                                        innerRadius={40}
                                        outerRadius={80}
                                        paddingAngle={5}
                                        dataKey="value"
                                    >
                                        {categoryData.map((entry, index) => (
                                            <Cell key={`cell-${index}`} fill={entry.color} />
                                        ))}
                                    </Pie>
                                    <Tooltip />
                                </PieChart>
                            </ResponsiveContainer>
                        </div>
                        <div className="space-y-2 mt-4">
                            {categoryData.map((item, index) => (
                                <div key={index} className="flex items-center justify-between text-sm">
                                    <div className="flex items-center gap-2">
                                        <div 
                                            className="w-3 h-3 rounded-full" 
                                            style={{ backgroundColor: item.color }}
                                        />
                                        <span className="text-slate-600">{item.name}</span>
                                    </div>
                                    <span className="font-bold text-slate-800">{item.value}%</span>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* AI Activity Monitor */}
                    <div className="bg-white rounded-3xl shadow-2xl border border-slate-100 p-6">
                        <h3 className="text-xl font-bold text-slate-800 mb-4">AI Agent Activity</h3>
                        <div className="space-y-4">
                            {['Workflow', 'SQL', 'RAG', 'Business'].map((agent, index) => (
                                <div key={agent} className="flex items-center justify-between">
                                    <div className="flex items-center gap-3">
                                        <div className={`w-2 h-2 rounded-full ${
                                            index % 2 === 0 ? 'bg-green-500 animate-pulse' : 'bg-yellow-500'
                                        }`} />
                                        <span className="text-sm font-medium text-slate-700">{agent} Agent</span>
                                    </div>
                                    <span className="text-xs text-slate-500">
                                        {index % 2 === 0 ? 'Active' : 'Processing'}
                                    </span>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>

            {/* Real-time Alerts */}
            <motion.div
                initial={{ opacity: 0, y: 50 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 0.4 }}
                className="mt-12 bg-gradient-to-r from-ethiGreen to-ethiBlue rounded-3xl p-8 text-white"
            >
                <div className="flex items-center gap-4 mb-4">
                    <div className="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center">
                        <i className="fas fa-bell text-xl" />
                    </div>
                    <div>
                        <h3 className="text-2xl font-bold">Smart Alerts</h3>
                        <p className="text-white/80">AI-powered notifications for critical market changes</p>
                    </div>
                </div>
                
                <div className="grid md:grid-cols-3 gap-4">
                    <div className="bg-white/10 rounded-xl p-4 backdrop-blur-sm">
                        <div className="flex items-center gap-2 mb-2">
                            <i className="fas fa-arrow-up text-green-300" />
                            <span className="font-bold">Price Surge</span>
                        </div>
                        <p className="text-sm text-white/80">Coffee prices up 15% in last hour</p>
                    </div>
                    
                    <div className="bg-white/10 rounded-xl p-4 backdrop-blur-sm">
                        <div className="flex items-center gap-2 mb-2">
                            <i className="fas fa-exclamation-triangle text-yellow-300" />
                            <span className="font-bold">Low Stock</span>
                        </div>
                        <p className="text-sm text-white/80">3 products need restocking</p>
                    </div>
                    
                    <div className="bg-white/10 rounded-xl p-4 backdrop-blur-sm">
                        <div className="flex items-center gap-2 mb-2">
                            <i className="fas fa-star text-blue-300" />
                            <span className="font-bold">High Demand</span>
                        </div>
                        <p className="text-sm text-white/80">Teff flour trending in Addis Ababa</p>
                    </div>
                </div>
            </motion.div>
        </div>
    );
};