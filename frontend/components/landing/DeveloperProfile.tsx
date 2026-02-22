import React, { useState } from 'react';
import { ContactForm } from '../ContactForm';

interface DeveloperCard {
  id: string;
  title: string;
  icon: string;
  description: string;
  skills: string[];
  color: string;
  gradient: string;
}

const developerCards: DeveloperCard[] = [
  {
    id: 'backend-engineer',
    title: 'Backend Engineer',
    icon: 'fa-server',
    description: 'Architecting robust, scalable server-side systems with focus on performance, security, and maintainability. Expert in API design, microservices, and distributed systems.',
    skills: ['Python', 'FastAPI', 'PostgreSQL', 'System Design'],
    color: 'text-blue-600',
    gradient: 'from-blue-500 to-indigo-600'
  },
  {
    id: 'ai-architect',
    title: 'AI Systems Architect',
    icon: 'fa-brain',
    description: 'Designing intelligent systems that solve real-world problems. Specializing in multi-agent architectures, machine learning pipelines, and AI-driven automation.',
    skills: ['LangChain', 'Vector Databases', 'AI Agents', 'ML Ops'],
    color: 'text-purple-600',
    gradient: 'from-purple-500 to-pink-600'
  },
  {
    id: 'systems-analyst',
    title: 'Information Systems Analyst',
    icon: 'fa-sitemap',
    description: 'Bridging business requirements with technical solutions. Expert in system analysis, process optimization, and enterprise architecture design.',
    skills: ['System Analysis', 'Process Design', 'Architecture', 'Requirements'],
    color: 'text-green-600',
    gradient: 'from-green-500 to-emerald-600'
  },
  {
    id: 'fullstack-dev',
    title: 'Fullstack Developer',
    icon: 'fa-code',
    description: 'Building end-to-end solutions with backend expertise. Creating seamless user experiences backed by powerful, efficient server architectures.',
    skills: ['React', 'TypeScript', 'Python', 'Database Design'],
    color: 'text-orange-600',
    gradient: 'from-orange-500 to-red-600'
  },
  {
    id: 'pythonista',
    title: 'Pythonista',
    icon: 'fa-python',
    description: 'Mastering Python for everything from web development to AI systems. Writing clean, efficient, and maintainable code that scales.',
    skills: ['Django', 'FastAPI', 'Data Science', 'Automation'],
    color: 'text-yellow-600',
    gradient: 'from-yellow-500 to-orange-500'
  },
  {
    id: 'data-systems',
    title: 'Data Systems Expert',
    icon: 'fa-database',
    description: 'Designing and optimizing data architectures for modern applications. Expert in relational, NoSQL, and vector databases for AI applications.',
    skills: ['MySQL', 'PostgreSQL', 'Vector DB', 'Data Architecture'],
    color: 'text-teal-600',
    gradient: 'from-teal-500 to-cyan-600'
  }
];

export const DeveloperProfile: React.FC = () => {
  const [hoveredCard, setHoveredCard] = useState<string | null>(null);
  const [showContactForm, setShowContactForm] = useState(false);

  return (
    <section className="py-20 bg-gradient-to-br from-slate-50 via-white to-slate-100 relative overflow-hidden">
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-5">
        <div className="absolute inset-0" style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23000000' fill-opacity='0.1'%3E%3Ccircle cx='30' cy='30' r='2'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
        }} />
      </div>

      <div className="max-w-7xl mx-auto px-6 relative">
        {/* Header Section */}
        <div className="text-center mb-16">
          <div className="flex items-center justify-center mb-8">
            <div className="relative">
              <div className="w-32 h-32 rounded-full overflow-hidden border-4 border-white shadow-2xl">
                <img 
                  src="/yosef-profile.jpg" 
                  alt="Yosef Abire - Developer" 
                  className="w-full h-full object-cover"
                  onError={(e) => {
                    // Professional fallback with Ethiopian colors
                    const target = e.currentTarget;
                    target.src = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='128' height='128' viewBox='0 0 128 128'%3E%3Cdefs%3E%3ClinearGradient id='grad' x1='0%25' y1='0%25' x2='100%25' y2='100%25'%3E%3Cstop offset='0%25' style='stop-color:%23009739;stop-opacity:1' /%3E%3Cstop offset='100%25' style='stop-color:%2300C851;stop-opacity:1' /%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='128' height='128' fill='url(%23grad)'/%3E%3Ctext x='50%25' y='45%25' font-size='24' font-weight='bold' text-anchor='middle' fill='white'%3EYosef%3C/text%3E%3Ctext x='50%25' y='65%25' font-size='16' text-anchor='middle' fill='white' opacity='0.9'%3EAbire%3C/text%3E%3Ccircle cx='64' cy='35' r='12' fill='white' opacity='0.3'/%3E%3Cpath d='M52 45 Q64 35 76 45 Q70 55 64 50 Q58 55 52 45' fill='white' opacity='0.3'/%3E%3C/svg%3E";
                  }}
                />
              </div>
              <div className="absolute -bottom-2 -right-2 w-8 h-8 bg-green-500 rounded-full border-4 border-white flex items-center justify-center">
                <div className="w-3 h-3 bg-white rounded-full animate-pulse"></div>
              </div>
            </div>
          </div>
          
          <h2 className="text-4xl font-bold text-slate-800 mb-4">
            Yosef Abire
          </h2>
          <p className="text-xl text-slate-600 mb-2">
            Information Systems Graduate • Bahir Dar University
          </p>
          <div className="flex items-center justify-center gap-2 text-sm text-slate-500">
            <i className="fas fa-map-marker-alt text-ethiGreen"></i>
            <span>Ethiopia</span>
            <span className="mx-2">•</span>
            <i className="fas fa-graduation-cap text-ethiGreen"></i>
            <span>Information Systems</span>
          </div>
        </div>

        {/* Interactive Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
          {developerCards.map((card, index) => (
            <div
              key={card.id}
              className="group relative"
              onMouseEnter={() => setHoveredCard(card.id)}
              onMouseLeave={() => setHoveredCard(null)}
              style={{ animationDelay: `${index * 100}ms` }}
            >
              <div className={`
                relative bg-white rounded-2xl p-6 border border-slate-200 shadow-sm
                transition-all duration-500 ease-out cursor-pointer
                ${hoveredCard === card.id 
                  ? 'transform -translate-y-2 shadow-2xl border-transparent' 
                  : 'hover:shadow-lg hover:-translate-y-1'
                }
              `}>
                {/* Gradient Background on Hover */}
                <div className={`
                  absolute inset-0 rounded-2xl opacity-0 transition-opacity duration-500
                  bg-gradient-to-br ${card.gradient}
                  ${hoveredCard === card.id ? 'opacity-5' : ''}
                `} />
                
                {/* Card Content */}
                <div className="relative z-10">
                  {/* Icon */}
                  <div className={`
                    w-12 h-12 rounded-xl flex items-center justify-center mb-4
                    transition-all duration-500
                    ${hoveredCard === card.id 
                      ? `bg-gradient-to-br ${card.gradient} text-white shadow-lg` 
                      : 'bg-slate-100 text-slate-600'
                    }
                  `}>
                    <i className={`fas ${card.icon} text-lg`}></i>
                  </div>

                  {/* Title */}
                  <h3 className={`
                    text-lg font-bold mb-3 transition-colors duration-300
                    ${hoveredCard === card.id ? card.color : 'text-slate-800'}
                  `}>
                    {card.title}
                  </h3>

                  {/* Description */}
                  <div className={`
                    transition-all duration-500 overflow-hidden
                    ${hoveredCard === card.id ? 'max-h-96 opacity-100' : 'max-h-16 opacity-70'}
                  `}>
                    <p className="text-slate-600 text-sm leading-relaxed mb-4">
                      {card.description}
                    </p>
                  </div>

                  {/* Skills Tags */}
                  <div className={`
                    flex flex-wrap gap-2 transition-all duration-500
                    ${hoveredCard === card.id ? 'opacity-100 transform translate-y-0' : 'opacity-0 transform translate-y-2'}
                  `}>
                    {card.skills.map((skill, skillIndex) => (
                      <span
                        key={skill}
                        className={`
                          px-2 py-1 text-xs font-medium rounded-lg
                          bg-gradient-to-r ${card.gradient} text-white
                          transform transition-all duration-300
                        `}
                        style={{ 
                          animationDelay: `${skillIndex * 50}ms`,
                          opacity: hoveredCard === card.id ? 1 : 0,
                          transform: hoveredCard === card.id ? 'translateY(0)' : 'translateY(10px)'
                        }}
                      >
                        {skill}
                      </span>
                    ))}
                  </div>

                  {/* Hover Indicator */}
                  <div className={`
                    absolute top-4 right-4 w-6 h-6 rounded-full
                    flex items-center justify-center transition-all duration-300
                    ${hoveredCard === card.id 
                      ? `bg-gradient-to-br ${card.gradient} text-white shadow-lg scale-110` 
                      : 'bg-slate-100 text-slate-400 scale-100'
                    }
                  `}>
                    <i className={`fas fa-arrow-right text-xs transition-transform duration-300 ${
                      hoveredCard === card.id ? 'transform rotate-45' : ''
                    }`}></i>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Bottom CTA */}
        <div className="text-center">
          <div className="inline-flex items-center gap-4 bg-white rounded-2xl p-6 shadow-lg border border-slate-200">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-ethiGreen to-emerald-600 rounded-xl flex items-center justify-center text-white">
                <i className="fas fa-rocket text-sm"></i>
              </div>
              <div className="text-left">
                <p className="font-bold text-slate-800">Ready to build something amazing?</p>
                <p className="text-sm text-slate-600">Let's create intelligent systems together</p>
              </div>
            </div>
            <button 
              className="bg-gradient-to-r from-ethiGreen to-emerald-600 text-white px-6 py-3 rounded-xl font-semibold hover:shadow-lg transition-all duration-300 hover:scale-105"
              onClick={() => setShowContactForm(true)}
            >
              Get In Touch
            </button>
          </div>
        </div>
      </div>

      {/* Floating Elements */}
      <div className="absolute top-20 left-10 w-20 h-20 bg-gradient-to-br from-blue-400 to-purple-500 rounded-full opacity-10 animate-pulse"></div>
      <div className="absolute bottom-20 right-10 w-16 h-16 bg-gradient-to-br from-green-400 to-teal-500 rounded-full opacity-10 animate-pulse" style={{ animationDelay: '1s' }}></div>
      <div className="absolute top-1/2 left-20 w-12 h-12 bg-gradient-to-br from-orange-400 to-red-500 rounded-full opacity-10 animate-pulse" style={{ animationDelay: '2s' }}></div>
      
      {/* Contact Form Modal */}
      {showContactForm && (
        <ContactForm onClose={() => setShowContactForm(false)} />
      )}
    </section>
  );
};