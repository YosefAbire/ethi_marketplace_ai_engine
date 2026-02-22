import React from 'react';
import { motion } from 'framer-motion';

export const Footer: React.FC = () => {
    const footerSections = [
        {
            title: 'Product',
            links: [
                { name: 'AI Agents', href: '#agents' },
                { name: 'Live Analytics', href: '#insights' },
                { name: 'Workflow Engine', href: '#workflow' },
                { name: 'API Documentation', href: '#' },
                { name: 'Pricing', href: '#' }
            ]
        },
        {
            title: 'Company',
            links: [
                { name: 'About Us', href: '#about' },
                { name: 'Our Vision', href: '#vision' },
                { name: 'Careers', href: '#' },
                { name: 'Press Kit', href: '#' },
                { name: 'Contact', href: '#' }
            ]
        },
        {
            title: 'Resources',
            links: [
                { name: 'Documentation', href: '#' },
                { name: 'Help Center', href: '#' },
                { name: 'Community', href: '#' },
                { name: 'Blog', href: '#' },
                { name: 'Status Page', href: '#' }
            ]
        },
        {
            title: 'Legal',
            links: [
                { name: 'Privacy Policy', href: '#' },
                { name: 'Terms of Service', href: '#' },
                { name: 'Cookie Policy', href: '#' },
                { name: 'GDPR', href: '#' },
                { name: 'Security', href: '#' }
            ]
        }
    ];

    const socialLinks = [
        { name: 'GitHub', icon: 'fab fa-github', href: '#', color: 'hover:text-gray-900' },
        { name: 'LinkedIn', icon: 'fab fa-linkedin', href: '#', color: 'hover:text-blue-600' },
        { name: 'Twitter', icon: 'fab fa-twitter', href: '#', color: 'hover:text-blue-400' },
        { name: 'YouTube', icon: 'fab fa-youtube', href: '#', color: 'hover:text-red-600' },
        { name: 'Telegram', icon: 'fab fa-telegram', href: '#', color: 'hover:text-blue-500' }
    ];

    const features = [
        { icon: 'fa-shield-check', text: 'Enterprise Security' },
        { icon: 'fa-clock', text: '99.9% Uptime' },
        { icon: 'fa-headset', text: '24/7 Support' },
        { icon: 'fa-globe', text: 'Global Scale' }
    ];

    return (
        <footer className="relative bg-slate-900 text-white overflow-hidden">
            {/* Background Pattern */}
            <div className="absolute inset-0 tibeb-bg opacity-10" />
            
            {/* Floating Elements */}
            <div className="absolute inset-0 overflow-hidden">
                {[...Array(15)].map((_, i) => (
                    <motion.div
                        key={i}
                        className="absolute w-1 h-1 bg-ethiGreen rounded-full opacity-30"
                        style={{
                            left: `${Math.random() * 100}%`,
                            top: `${Math.random() * 100}%`,
                        }}
                        animate={{
                            y: [0, -50, 0],
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

            <div className="relative z-10 max-w-7xl mx-auto px-8">
                {/* Main Footer Content */}
                <div className="py-16">
                    <div className="grid lg:grid-cols-6 gap-12">
                        {/* Brand Section */}
                        <div className="lg:col-span-2">
                            <motion.div
                                initial={{ opacity: 0, y: 20 }}
                                whileInView={{ opacity: 1, y: 0 }}
                                transition={{ duration: 0.6 }}
                            >
                                {/* Logo */}
                                <div className="flex items-center gap-3 mb-6">
                                    <div className="w-12 h-12 bg-ethiGreen rounded-xl flex items-center justify-center text-white shadow-lg shadow-ethiGreen/20">
                                        <i className="fas fa-microchip text-xl" />
                                    </div>
                                    <div>
                                        <h3 className="font-black text-2xl tracking-tight">
                                            Ethi <span className="text-ethiGreen">AI</span>
                                        </h3>
                                        <p className="text-xs text-slate-400 font-medium">Marketplace Engine</p>
                                    </div>
                                </div>

                                <p className="text-slate-300 leading-relaxed mb-6">
                                    Empowering Ethiopian businesses with intelligent AI agents, 
                                    real-time analytics, and automated marketplace operations.
                                </p>

                                {/* Features */}
                                <div className="grid grid-cols-2 gap-3 mb-6">
                                    {features.map((feature, index) => (
                                        <div key={index} className="flex items-center gap-2 text-sm text-slate-400">
                                            <i className={`fas ${feature.icon} text-ethiGreen`} />
                                            <span>{feature.text}</span>
                                        </div>
                                    ))}
                                </div>

                                {/* Social Links */}
                                <div className="flex gap-3">
                                    {socialLinks.map((social, index) => (
                                        <motion.a
                                            key={index}
                                            href={social.href}
                                            whileHover={{ scale: 1.1, y: -2 }}
                                            className={`w-10 h-10 bg-slate-800 rounded-xl flex items-center justify-center text-slate-400 transition-all ${social.color}`}
                                        >
                                            <i className={`${social.icon} text-lg`} />
                                        </motion.a>
                                    ))}
                                </div>
                            </motion.div>
                        </div>

                        {/* Links Sections */}
                        <div className="lg:col-span-4 grid md:grid-cols-4 gap-8">
                            {footerSections.map((section, sectionIndex) => (
                                <motion.div
                                    key={sectionIndex}
                                    initial={{ opacity: 0, y: 20 }}
                                    whileInView={{ opacity: 1, y: 0 }}
                                    transition={{ duration: 0.6, delay: sectionIndex * 0.1 }}
                                >
                                    <h4 className="font-bold text-white mb-4">{section.title}</h4>
                                    <ul className="space-y-3">
                                        {section.links.map((link, linkIndex) => (
                                            <li key={linkIndex}>
                                                <a
                                                    href={link.href}
                                                    className="text-slate-400 hover:text-ethiGreen transition-colors text-sm"
                                                >
                                                    {link.name}
                                                </a>
                                            </li>
                                        ))}
                                    </ul>
                                </motion.div>
                            ))}
                        </div>
                    </div>
                </div>

                {/* Newsletter Section */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6 }}
                    className="border-t border-slate-800 py-12"
                >
                    <div className="grid lg:grid-cols-2 gap-8 items-center">
                        <div>
                            <h3 className="text-2xl font-bold mb-2">Stay Updated</h3>
                            <p className="text-slate-400">
                                Get the latest updates on AI features, marketplace insights, and Ethiopian business trends.
                            </p>
                        </div>
                        <div className="flex gap-3">
                            <input
                                type="email"
                                placeholder="Enter your email"
                                className="flex-1 px-4 py-3 bg-slate-800 border border-slate-700 rounded-xl text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-ethiGreen/20 focus:border-ethiGreen"
                            />
                            <motion.button
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                                className="px-6 py-3 bg-ethiGreen text-white rounded-xl font-bold hover:bg-ethiGreen/90 transition-all"
                            >
                                Subscribe
                            </motion.button>
                        </div>
                    </div>
                </motion.div>

                {/* Bottom Section */}
                <div className="border-t border-slate-800 py-8">
                    <div className="flex flex-col md:flex-row justify-between items-center gap-4">
                        <div className="flex items-center gap-6 text-sm text-slate-400">
                            <span>© 2024 Ethi AI Marketplace Engine. All rights reserved.</span>
                            <div className="flex items-center gap-2">
                                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                                <span>System Status: Operational</span>
                            </div>
                        </div>
                        
                        <div className="flex items-center gap-6 text-sm text-slate-400">
                            <span>Made with ❤️ in Ethiopia</span>
                            <div className="flex items-center gap-2">
                                <span>🇪🇹</span>
                                <span className="font-ethiopic">ኢትዮጵያ</span>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Back to Top Button */}
                <motion.button
                    onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
                    whileHover={{ scale: 1.1, y: -2 }}
                    whileTap={{ scale: 0.9 }}
                    className="fixed bottom-8 right-8 w-12 h-12 bg-ethiGreen text-white rounded-full shadow-xl shadow-ethiGreen/30 flex items-center justify-center hover:bg-ethiGreen/90 transition-all z-50"
                >
                    <i className="fas fa-arrow-up" />
                </motion.button>
            </div>
        </footer>
    );
};