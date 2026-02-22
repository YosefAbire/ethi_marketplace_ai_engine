import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';

interface Section {
    id: string;
    label: string;
}

interface NavigationBarProps {
    sections: Section[];
    activeSection: string;
    onSectionChange: (sectionId: string) => void;
    onGetStarted: () => void;
}

export const NavigationBar: React.FC<NavigationBarProps> = ({
    sections,
    activeSection,
    onSectionChange,
    onGetStarted
}) => {
    const [isScrolled, setIsScrolled] = useState(false);

    useEffect(() => {
        const handleScroll = () => {
            setIsScrolled(window.scrollY > 50);
        };

        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    const scrollToSection = (sectionId: string) => {
        const element = document.getElementById(sectionId);
        if (element) {
            element.scrollIntoView({ behavior: 'smooth' });
            onSectionChange(sectionId);
        }
    };

    return (
        <motion.nav
            initial={{ y: -100 }}
            animate={{ y: 0 }}
            className={`fixed top-0 inset-x-0 z-50 transition-all duration-300 ${
                isScrolled 
                    ? 'bg-white/90 backdrop-blur-xl border-b border-slate-200 shadow-lg' 
                    : 'bg-transparent'
            }`}
        >
            <div className="max-w-7xl mx-auto px-8 h-20 flex items-center justify-between">
                {/* Logo */}
                <motion.div 
                    className="flex items-center gap-3"
                    whileHover={{ scale: 1.05 }}
                >
                    <div className="w-10 h-10 bg-ethiGreen rounded-xl flex items-center justify-center text-white shadow-lg shadow-ethiGreen/20">
                        <i className="fas fa-microchip" />
                    </div>
                    <span className="font-black text-xl tracking-tight">
                        Ethi <span className="text-ethiGreen">AI</span>
                    </span>
                </motion.div>

                {/* Navigation Links */}
                <div className="hidden lg:flex items-center gap-8">
                    {sections.map((section) => (
                        <button
                            key={section.id}
                            onClick={() => scrollToSection(section.id)}
                            className={`relative text-sm font-medium transition-colors ${
                                activeSection === section.id
                                    ? 'text-ethiGreen'
                                    : 'text-slate-600 hover:text-ethiGreen'
                            }`}
                        >
                            {section.label}
                            {activeSection === section.id && (
                                <motion.div
                                    layoutId="activeSection"
                                    className="absolute -bottom-1 left-0 right-0 h-0.5 bg-ethiGreen rounded-full"
                                />
                            )}
                        </button>
                    ))}
                </div>

                {/* CTA Button */}
                <motion.button
                    onClick={onGetStarted}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className="px-6 py-3 bg-ethiGreen text-white rounded-xl font-bold text-sm hover:bg-ethiGreen/90 transition-all shadow-lg shadow-ethiGreen/20"
                >
                    Launch Engine
                </motion.button>
            </div>
        </motion.nav>
    );
};