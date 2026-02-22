import React, { useState } from 'react';

interface LandingPageProps {
    onGetStarted: () => void;
}

export const LandingPage: React.FC<LandingPageProps> = ({ onGetStarted }) => {
    const [activeFeature, setActiveFeature] = useState(0);

    const features = [
        {
            title: "Orchestration Engine",
            amharic: "የስራ ፍሰት አስተዳዳሪ",
            icon: "fa-network-wired",
            color: "ethiGreen",
            placeholder: "https://images.unsplash.com/photo-1639322537228-f710d846310a?auto=format&fit=crop&q=80&w=1000",
            description: "A centralized intelligent brain that analyzes user intent and dynamically routes tasks to the most efficient specialized agents.",
            details: "Utilizing advanced state-machine logic, the engine handles complex multi-step workflows, ensuring seamless coordination between data retrieval and action execution."
        },
        {
            title: "Knowledge Specialist (RAG)",
            amharic: "የእውቀት ባለሙያ",
            icon: "fa-book-open",
            color: "ethiYellow",
            placeholder: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&q=80&w=1000",
            description: "Proprietary Retrieval Augmented Generation system that allows agents to 'read' and learn from your own private document libraries.",
            details: "Support for PDF, CSV, and TXT indexing with semantic search capabilities. Documents are processed into vector embeddings for instant, accurate cross-referencing."
        },
        {
            title: "Strategic Market Analyst",
            amharic: "የገበያ ስትራቴጂ ተንታኝ",
            icon: "fa-chart-line",
            color: "ethiRed",
            placeholder: "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&q=80&w=1000",
            description: "Real-time SQL analytics combined with LLM reasoning to provide actionable business growth advice based on live inventory sales data.",
            details: "Generates predictive insights, pricing recommendations, and competitive analysis to help sellers dominate the Ethiopian marketplace."
        }
    ];

    return (
        <div className="min-h-screen bg-white text-slate-900 font-inter selection:bg-ethiGreen/20 overflow-x-hidden">
            {/* Navigation */}
            <nav className="fixed top-0 inset-x-0 h-20 bg-white/80 backdrop-blur-xl border-b border-slate-100 z-[100] px-8 flex items-center justify-between">
                <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-ethiGreen rounded-xl flex items-center justify-center text-white shadow-lg shadow-ethiGreen/20">
                        <i className="fas fa-microchip"></i>
                    </div>
                    <span className="font-black text-xl tracking-tighter uppercase">Ethi <span className="text-ethiGreen italic">AI</span></span>
                </div>
                <div className="hidden md:flex items-center gap-8">
                    <a href="#system" className="text-sm font-bold text-slate-500 hover:text-ethiGreen transition-colors">Architecture</a>
                    <a href="#vision" className="text-sm font-bold text-slate-500 hover:text-ethiGreen transition-colors">Vision</a>
                    <button
                        onClick={onGetStarted}
                        className="px-6 py-2.5 bg-ethiGreen text-white rounded-xl font-bold text-sm hover:bg-ethiGreen/90 transition-all shadow-lg shadow-ethiGreen/20"
                    >
                        Launch Engine • ጀምር
                    </button>
                </div>
            </nav>

            {/* Hero Section */}
            <section className="relative pt-48 pb-32 px-8 flex flex-col items-center text-center">
                <div className="absolute inset-0 tibeb-bg opacity-[0.03] pointer-events-none"></div>

                <div className="max-w-5xl mx-auto relative z-10">
                    <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-slate-100 border border-slate-200 mb-10">
                        <span className="flex gap-1">
                            <span className="w-1.5 h-1.5 bg-ethiGreen rounded-full pulse"></span>
                            <span className="w-1.5 h-1.5 bg-ethiYellow rounded-full pulse delay-100"></span>
                            <span className="w-1.5 h-1.5 bg-ethiRed rounded-full pulse delay-200"></span>
                        </span>
                        <span className="text-[10px] font-black uppercase tracking-[0.2em] text-slate-500">Enterprise AI Orchestration</span>
                    </div>

                    <h1 className="text-7xl md:text-8xl font-black tracking-tighter leading-[0.9] mb-10">
                        Automating the Future of <br />
                        <span className="text-ethiGreen italic">Ethiopian Commerce.</span>
                    </h1>

                    <p className="max-w-3xl mx-auto text-xl text-slate-500 font-medium leading-relaxed mb-14">
                        A specialized multi-agent ecosystem designed to analyze, optimize, and scale business operations through intelligent sovereign AI.
                    </p>

                    <div className="flex flex-col sm:flex-row gap-6 justify-center">
                        <button
                            onClick={onGetStarted}
                            className="px-12 py-6 bg-ethiGreen text-white rounded-[2rem] font-black text-xl hover:bg-ethiGreen/90 shadow-2xl shadow-ethiGreen/30 transition-all hover:-translate-y-1 flex items-center justify-center gap-4"
                        >
                            Get Started • ጀምር
                            <i className="fas fa-arrow-right text-sm"></i>
                        </button>
                        <a
                            href="#system"
                            className="px-12 py-6 bg-white border-2 border-slate-200 text-slate-800 rounded-[2rem] font-black text-xl hover:bg-slate-50 transition-all flex items-center justify-center"
                        >
                            System Specs
                        </a>
                    </div>
                </div>

                {/* Hero Image / Placeholder */}
                <div className="mt-32 w-full max-w-6xl mx-auto relative px-4">
                    <div className="aspect-[21/9] bg-slate-900 rounded-[3.5rem] overflow-hidden shadow-3xl border border-white/10 relative group">
                        <img
                            src="https://images.unsplash.com/photo-1551288049-bbbda50a8661?auto=format&fit=crop&q=80&w=2000"
                            alt="AI Marketplace Dashboard"
                            className="w-full h-full object-cover opacity-50 group-hover:scale-105 transition-transform duration-1000"
                        />
                        <div className="absolute inset-0 bg-gradient-to-t from-slate-900 via-transparent to-transparent"></div>
                        <div className="absolute bottom-12 left-12 text-left">
                            <p className="text-ethiGreen font-black uppercase tracking-[0.4em] text-[10px] mb-2">Live Marketplace Node</p>
                            <h3 className="text-3xl font-black text-white">Visual Intelligence Dashboard</h3>
                            <p className="text-slate-400 font-medium text-sm mt-2 max-w-sm">The dashboard provides a real-time visual representation of all agent activities and marketplace metrics across Ethiopia.</p>
                        </div>
                    </div>
                </div>
            </section>

            {/* System Architecture Section */}
            <section id="system" className="py-40 bg-slate-50 px-8 relative overflow-hidden">
                <div className="max-w-7xl mx-auto">
                    <div className="flex flex-col lg:flex-row gap-24 items-center">
                        <div className="lg:w-1/2">
                            <p className="text-sm font-black text-ethiGreen uppercase tracking-widest mb-4">The Engine Components</p>
                            <h2 className="text-6xl font-black mb-12 tracking-tight leading-tight">
                                Specialized Agents. <br /> <span className="text-ethiGold italic">Unified Success.</span>
                            </h2>

                            <div className="space-y-4">
                                {features.map((f, i) => (
                                    <div
                                        key={i}
                                        onMouseEnter={() => setActiveFeature(i)}
                                        className={`p-8 rounded-[2.5rem] transition-all cursor-pointer border ${activeFeature === i ? `bg-white shadow-2xl border-${f.color}/20 scale-[1.03] shadow-${f.color}/10` : 'bg-transparent border-transparent grayscale opacity-50 hover:opacity-100 hover:grayscale-0'}`}
                                    >
                                        <div className="flex items-start gap-6">
                                            <div className={`w-14 h-14 rounded-2xl flex items-center justify-center text-white shadow-lg bg-${f.color}`}>
                                                <i className={`fas ${f.icon} text-xl`}></i>
                                            </div>
                                            <div className="flex-1">
                                                <h3 className={`text-2xl font-black mb-1 ${activeFeature === i ? `text-${f.color}` : 'text-slate-800'}`}>{f.title}</h3>
                                                <p className="text-slate-400 font-ethiopic text-sm mb-4 uppercase tracking-widest">{f.amharic}</p>
                                                <p className="text-slate-500 font-medium leading-relaxed">{f.description}</p>
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>

                        {/* Feature Image & Description */}
                        <div className="lg:w-1/2 w-full">
                            <div className="bg-white rounded-[4rem] shadow-2xl border border-slate-100 p-8 h-[700px] flex flex-col overflow-hidden relative">
                                <div className="absolute inset-0 tibeb-bg opacity-[0.03]"></div>

                                <div className="relative z-10 flex flex-col h-full" key={activeFeature}>
                                    {/* Image Container */}
                                    <div className="w-full aspect-video rounded-[2.5rem] overflow-hidden bg-slate-100 mb-10 shadow-inner group">
                                        <img
                                            src={features[activeFeature].placeholder}
                                            alt={features[activeFeature].title}
                                            className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-1000"
                                        />
                                    </div>

                                    <div className="px-4 animate-in fade-in slide-in-from-bottom-4 duration-500">
                                        <h4 className="text-4xl font-black mb-6">{features[activeFeature].title}</h4>
                                        <p className="text-lg text-slate-500 font-medium leading-relaxed mb-8">
                                            {features[activeFeature].details}
                                        </p>
                                        <div className="p-6 bg-slate-50 rounded-2xl border border-slate-100 italic text-sm text-slate-400 font-medium">
                                            "The specialized {features[activeFeature].title.toLowerCase()} enables high-precision operations in complex environments."
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Developer Leadership */}
            <section id="vision" className="py-40 px-8 bg-slate-900 relative overflow-hidden text-white">
                <div className="absolute inset-0 tibeb-bg opacity-[0.08] mix-blend-overlay"></div>
                <div className="max-w-6xl mx-auto relative z-10">
                    <div className="flex flex-col md:flex-row items-center gap-24">
                        <div className="md:w-2/5 relative">
                            <div className="aspect-[3/4] rounded-[4rem] overflow-hidden border-8 border-white/5 relative group">
                                <img
                                    src="/director-ai.jpg"
                                    alt="Lead AI Developer"
                                    className="w-full h-full object-cover opacity-80 group-hover:opacity-100 transition-all duration-700"
                                />
                                <div className="absolute inset-0 bg-gradient-to-t from-slate-900 via-transparent to-transparent"></div>
                                <div className="absolute bottom-10 left-10">
                                    <p className="text-ethiGreen font-black text-2xl tracking-tight mb-1">Director of AI</p>
                                    <p className="text-white/40 font-bold uppercase tracking-widest text-[10px]">Lead System Architect</p>
                                </div>
                            </div>
                            {/* Floating badge */}
                            <div className="absolute -top-6 -right-6 w-24 h-24 bg-ethiGold rounded-3xl flex items-center justify-center -rotate-12 shadow-2xl animate-bounce">
                                <i className="fas fa-microchip text-3xl text-white"></i>
                            </div>
                        </div>

                        <div className="md:w-3/5">
                            <p className="text-ethiGreen font-black uppercase tracking-[0.5em] text-xs mb-8">System Visionary</p>
                            <h2 className="text-6xl md:text-7xl font-black mb-12 tracking-tighter leading-[0.9]">
                                Engineering for a <br /> <span className="text-ethiGreen italic">Modern Ethiopia.</span>
                            </h2>
                            <p className="text-2xl text-slate-400 font-medium leading-relaxed mb-12">
                                "My mission is to deliver world-class AI capabilities that respect and enhance the unique economic landscape of our nation. Every line of code is written to empower local sellers and streamline our national commerce."
                            </p>
                            <div className="flex gap-6">
                                <button className="h-16 px-10 bg-white text-slate-900 rounded-2xl font-black hover:bg-ethiGreen hover:text-white transition-all text-sm">
                                    GitHub Portfolio
                                </button>
                                <button className="h-16 px-10 bg-slate-800 text-white rounded-2xl font-black hover:bg-slate-700 transition-all text-sm">
                                    Professional LinkedIn
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Conversion */}
            <section className="py-40 px-8 text-center bg-white">
                <div className="max-w-4xl mx-auto bg-ethiGreen rounded-[4rem] p-24 relative overflow-hidden shadow-3xl shadow-ethiGreen/20">
                    <div className="absolute inset-0 tibeb-bg opacity-10"></div>
                    <h2 className="text-5xl font-black text-white mb-10 leading-tight relative z-10">Scale your business with <br /> the Power of Agentic AI.</h2>
                    <button
                        onClick={onGetStarted}
                        className="px-16 py-6 bg-white text-ethiGreen rounded-3xl font-black text-2xl hover:bg-slate-50 shadow-2xl transition-all hover:-translate-y-2 relative z-10"
                    >
                        Deploy Engine • ይግቡ
                    </button>
                </div>
            </section>

            {/* Footer */}
            <footer className="py-20 bg-slate-50 border-t border-slate-100 text-center">
                <div className="flex flex-col items-center gap-8">
                    <div className="w-12 h-12 bg-slate-900 rounded-2xl flex items-center justify-center text-white">
                        <i className="fas fa-microchip"></i>
                    </div>
                    <p className="text-[10px] font-black text-slate-400 uppercase tracking-[0.4em]">
                        Ethi Marketplace AI Engine • Developed for the Ethiopian Renaissance
                    </p>
                    <p className="text-[9px] text-slate-300 font-medium">© 2026. All rights reserved. Professional assets and AI Logic are property of the lead development team.</p>
                </div>
            </footer>
        </div>
    );
};
