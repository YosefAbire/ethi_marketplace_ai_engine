import React, { useState, useEffect, useRef } from 'react';
import { motion, useScroll, useTransform, AnimatePresence } from 'framer-motion';
import { HeroSection } from './landing/HeroSection';
import { WorkflowVisualization } from './landing/WorkflowVisualization';
import { AIAgentsShowcase } from './landing/AIAgentsShowcase';
import { LiveInsightsDashboard } from './landing/LiveInsightsDashboard';
import { RoleBasedViews } from './landing/RoleBasedViews';
import { InteractiveStats } from './landing/InteractiveStats';
import { AboutDeveloper } from './landing/AboutDeveloper';
import { VisionSection } from './landing/VisionSection';
import { CTASection } from './landing/CTASection';
import { NavigationBar } from './landing/NavigationBar';
import { Footer } from './landing/Footer';

interface InteractiveLandingPageProps {
    onGetStarted: () => void;
}

export const InteractiveLandingPage: React.FC<InteractiveLandingPageProps> = ({ onGetStarted }) => {
    const [activeSection, setActiveSection] = useState('hero');
    const [userRole, setUserRole] = useState<'seller' | 'owner'>('seller');
    const [isLoaded, setIsLoaded] = useState(false);
    const containerRef = useRef<HTMLDivElement>(null);
    
    const { scrollYProgress } = useScroll({
        target: containerRef,
        offset: ["start start", "end end"]
    });

    const backgroundY = useTransform(scrollYProgress, [0, 1], ["0%", "100%"]);
    const opacity = useTransform(scrollYProgress, [0, 0.5, 1], [1, 0.8, 0.6]);

    useEffect(() => {
        setIsLoaded(true);
    }, []);

    const sections = [
        { id: 'hero', label: 'Overview' },
        { id: 'workflow', label: 'How It Works' },
        { id: 'agents', label: 'AI Agents' },
        { id: 'insights', label: 'Live Insights' },
        { id: 'roles', label: 'Your View' },
        { id: 'about', label: 'Developer' },
        { id: 'vision', label: 'Vision' },
        { id: 'cta', label: 'Get Started' }
    ];

    return (
        <div 
            ref={containerRef}
            className="min-h-screen bg-slate-50 text-slate-900 font-inter selection:bg-ethiGreen/20 overflow-x-hidden"
        >
            <NavigationBar 
                sections={sections}
                activeSection={activeSection}
                onSectionChange={setActiveSection}
                onGetStarted={onGetStarted}
            />

            <motion.div
                style={{ y: backgroundY, opacity }}
                className="fixed inset-0 pointer-events-none z-0"
            >
                <div className="absolute inset-0 tibeb-bg opacity-[0.02]" />
                <div className="absolute inset-0 bg-gradient-to-br from-ethiGreen/5 via-transparent to-ethiYellow/5" />
            </motion.div>

            <AnimatePresence mode="wait">
                {isLoaded && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ duration: 0.8 }}
                        className="relative z-10"
                    >
                        {/* Hero Section */}
                        <section id="hero" className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-blue-50 relative">
                            <div className="absolute inset-0 pattern-dots opacity-30" />
                            <div className="relative z-10">
                                <HeroSection onGetStarted={onGetStarted} />
                            </div>
                        </section>

                        {/* Workflow Visualization */}
                        <section id="workflow" className="min-h-screen py-20 bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50 relative">
                            <div className="absolute inset-0 pattern-grid opacity-40" />
                            <div className="relative z-10">
                                <WorkflowVisualization />
                            </div>
                        </section>

                        {/* AI Agents Showcase */}
                        <section id="agents" className="min-h-screen py-20 bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 relative">
                            <div className="absolute inset-0 pattern-diagonal opacity-30" />
                            <div className="relative z-10">
                                <AIAgentsShowcase />
                            </div>
                        </section>

                        {/* Live Insights Dashboard */}
                        <section id="insights" className="min-h-screen py-20 bg-gradient-to-br from-orange-50 via-amber-50 to-yellow-50 relative">
                            <div className="absolute inset-0 pattern-dots opacity-25" />
                            <div className="relative z-10">
                                <LiveInsightsDashboard />
                            </div>
                        </section>

                        {/* Role-Based Views */}
                        <section id="roles" className="min-h-screen py-20 bg-gradient-to-br from-purple-50 via-violet-50 to-fuchsia-50 relative">
                            <div className="absolute inset-0 pattern-grid opacity-30" />
                            <div className="relative z-10">
                                <RoleBasedViews 
                                    userRole={userRole}
                                    onRoleChange={setUserRole}
                                />
                            </div>
                        </section>

                        {/* Interactive Stats */}
                        <section className="py-20 bg-gradient-to-br from-slate-100 via-gray-50 to-zinc-50 relative">
                            <div className="absolute inset-0 pattern-diagonal opacity-20" />
                            <div className="relative z-10">
                                <InteractiveStats />
                            </div>
                        </section>

                        {/* About Developer */}
                        <section id="about" className="py-20 bg-gradient-to-br from-cyan-50 via-sky-50 to-blue-100 relative">
                            <div className="absolute inset-0 pattern-dots opacity-35" />
                            <div className="relative z-10">
                                <AboutDeveloper />
                            </div>
                        </section>

                        {/* Vision Section */}
                        <section id="vision" className="py-20 bg-gradient-to-br from-emerald-50 via-green-50 to-lime-50 relative">
                            <div className="absolute inset-0 pattern-grid opacity-25" />
                            <div className="relative z-10">
                                <VisionSection />
                            </div>
                        </section>

                        {/* CTA Section */}
                        <section id="cta" className="py-20 bg-gradient-to-br from-slate-800 via-gray-900 to-black relative">
                            <div className="absolute inset-0 tibeb-bg opacity-10" />
                            <div className="relative z-10">
                                <CTASection onGetStarted={onGetStarted} />
                            </div>
                        </section>

                        {/* Footer */}
                        <Footer />
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};