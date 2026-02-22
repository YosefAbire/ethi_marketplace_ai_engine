import React from 'react';
import { motion } from 'framer-motion';

export const VisionSection: React.FC = () => {
    const visionPoints = [
        {
            icon: 'fa-globe-africa',
            title: 'Empowering Ethiopian Commerce',
            description: 'Building AI solutions specifically designed for Ethiopian businesses, understanding local culture, languages, and market dynamics.',
            color: 'ethiGreen'
        },
        {
            icon: 'fa-brain',
            title: 'Democratizing AI Technology',
            description: 'Making advanced artificial intelligence accessible to small and medium businesses across Ethiopia.',
            color: 'ethiBlue'
        },
        {
            icon: 'fa-handshake',
            title: 'Bridging Traditional & Modern',
            description: 'Connecting time-honored Ethiopian business practices with cutting-edge technology for sustainable growth.',
            color: 'ethiYellow'
        },
        {
            icon: 'fa-rocket',
            title: 'Driving Innovation',
            description: 'Leading the digital transformation of African marketplaces through intelligent automation and data-driven insights.',
            color: 'ethiPurple'
        }
    ];

    const milestones = [
        { year: '2025', title: 'Project Planning', description: 'Initial research and planning phase for Ethiopian AI marketplace technology' },
        { year: '2026', title: 'AI Engine Development', description: 'Building and launching the first Ethiopian AI-powered marketplace engine prototype' },
        { year: '2027', title: 'Multi-Language Support', description: 'Expanding to support Amharic, Oromo, and Tigrinya languages with cultural context' },
        { year: '2028', title: 'Gamo Zone Launch', description: 'Official launch starting from Gamo Zone, Arba Minch - bringing AI marketplace technology to Southern Ethiopia, supporting local crafts, agriculture, and traditional products' }
    ];

    return (
        <div className="relative overflow-hidden">
            <div className="relative z-10 max-w-7xl mx-auto px-8 py-24">
                <motion.div
                    initial={{ opacity: 0, y: 50 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8 }}
                    className="text-center mb-16"
                >
                    <h2 className="text-5xl font-black mb-6 tracking-tight text-slate-800">
                        Our <span className="text-ethiGreen">Vision</span> & Mission
                    </h2>
                    <p className="text-xl text-slate-700 max-w-4xl mx-auto leading-relaxed">
                        To revolutionize Ethiopian commerce by making advanced AI technology accessible, 
                        culturally relevant, and economically empowering for businesses of all sizes.
                    </p>
                </motion.div>

                {/* Vision Points */}
                <div className="grid md:grid-cols-2 gap-8 mb-20">
                    {visionPoints.map((point, index) => (
                        <motion.div
                            key={index}
                            initial={{ opacity: 0, y: 50 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.6, delay: index * 0.1 }}
                            whileHover={{ scale: 1.02, y: -5 }}
                            className="bg-white rounded-3xl shadow-xl border border-slate-100 p-8 relative overflow-hidden group"
                        >
                            {/* Background Pattern */}
                            <div className="absolute inset-0 tibeb-bg opacity-5 group-hover:opacity-10 transition-opacity" />
                            
                            <div className="relative z-10">
                                <div className={`w-16 h-16 bg-${point.color} rounded-2xl flex items-center justify-center text-white shadow-lg shadow-${point.color}/30 mb-6`}>
                                    <i className={`fas ${point.icon} text-2xl`} />
                                </div>
                                
                                <h3 className="text-2xl font-bold text-slate-800 mb-4">{point.title}</h3>
                                <p className="text-slate-700 leading-relaxed">{point.description}</p>
                                
                                {/* Hover Effect */}
                                <motion.div
                                    initial={{ width: 0 }}
                                    whileHover={{ width: '100%' }}
                                    className={`absolute bottom-0 left-0 h-1 bg-${point.color} rounded-full`}
                                />
                            </div>
                        </motion.div>
                    ))}
                </div>

                {/* Mission Statement */}
                <motion.div
                    initial={{ opacity: 0, y: 50 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8 }}
                    className="bg-gradient-to-r from-ethiGreen to-ethiBlue rounded-3xl p-12 text-white text-center mb-20"
                >
                    <div className="max-w-4xl mx-auto">
                        <h3 className="text-3xl font-bold mb-6">Our Mission</h3>
                        <p className="text-xl leading-relaxed mb-8 text-white/90">
                            "To build intelligent systems that understand Ethiopian culture, speak local languages, 
                            and empower every business owner to compete in the global digital economy while 
                            preserving their unique identity and values."
                        </p>
                        <div className="flex items-center justify-center gap-8 text-white/80">
                            <div className="text-center">
                                <div className="text-3xl font-bold">2,500+</div>
                                <div className="text-sm">Businesses Empowered</div>
                            </div>
                            <div className="w-px h-12 bg-white/30" />
                            <div className="text-center">
                                <div className="text-3xl font-bold">6</div>
                                <div className="text-sm">AI Agents</div>
                            </div>
                            <div className="w-px h-12 bg-white/30" />
                            <div className="text-center">
                                <div className="text-3xl font-bold">98.5%</div>
                                <div className="text-sm">Accuracy Rate</div>
                            </div>
                        </div>
                    </div>
                </motion.div>

                {/* Roadmap */}
                <motion.div
                    initial={{ opacity: 0, y: 50 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8 }}
                    className="text-center mb-12"
                >
                    <h3 className="text-4xl font-black mb-6 tracking-tight text-slate-800">
                        Our <span className="text-ethiGreen">Roadmap</span>
                    </h3>
                    <p className="text-xl text-slate-700 max-w-3xl mx-auto">
                        Building the future of Ethiopian commerce, one milestone at a time
                    </p>
                </motion.div>

                <div className="relative">
                    {/* Timeline Line */}
                    <div className="absolute left-1/2 transform -translate-x-1/2 w-1 h-full bg-gradient-to-b from-ethiGreen to-ethiBlue rounded-full" />
                    
                    <div className="space-y-12">
                        {milestones.map((milestone, index) => (
                            <motion.div
                                key={index}
                                initial={{ opacity: 0, x: index % 2 === 0 ? -50 : 50 }}
                                whileInView={{ opacity: 1, x: 0 }}
                                transition={{ duration: 0.6, delay: index * 0.2 }}
                                className={`flex items-center ${index % 2 === 0 ? 'flex-row' : 'flex-row-reverse'}`}
                            >
                                <div className={`w-1/2 ${index % 2 === 0 ? 'pr-8 text-right' : 'pl-8 text-left'}`}>
                                    <div className="bg-white rounded-2xl shadow-xl border border-slate-100 p-6">
                                        <div className={`inline-flex items-center gap-2 px-4 py-2 rounded-full text-sm font-bold mb-4 ${
                                            index === 0 ? 'bg-ethiGreen text-white' : 
                                            index === 1 ? 'bg-ethiBlue text-white' :
                                            index === 3 ? 'bg-ethiOrange text-white' :
                                            'bg-slate-100 text-slate-600'
                                        }`}>
                                            <i className={`fas ${
                                                index === 0 ? 'fa-check' : 
                                                index === 1 ? 'fa-cogs' :
                                                index === 3 ? 'fa-rocket' :
                                                'fa-clock'
                                            }`} />
                                            {milestone.year}
                                        </div>
                                        <h4 className="text-xl font-bold text-slate-800 mb-2">{milestone.title}</h4>
                                        <p className="text-slate-700">{milestone.description}</p>
                                    </div>
                                </div>
                                
                                {/* Timeline Node */}
                                <div className="relative z-10">
                                    <div className={`w-6 h-6 rounded-full border-4 border-white shadow-lg ${
                                        index === 0 ? 'bg-ethiGreen' : 
                                        index === 1 ? 'bg-ethiBlue' :
                                        index === 3 ? 'bg-ethiOrange' :
                                        'bg-slate-300'
                                    }`} />
                                </div>
                                
                                <div className="w-1/2" />
                            </motion.div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};