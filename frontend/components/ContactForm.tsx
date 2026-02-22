import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';

interface ContactFormProps {
  onClose: () => void;
}

interface FormData {
  name: string;
  email: string;
  company: string;
  subject: string;
  message: string;
  projectType: string;
}

export const ContactForm: React.FC<ContactFormProps> = ({ onClose }) => {
  const [formData, setFormData] = useState<FormData>({
    name: '',
    email: '',
    company: '',
    subject: '',
    message: '',
    projectType: 'consultation'
  });
  
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitStatus, setSubmitStatus] = useState<'idle' | 'success' | 'error'>('idle');
  const [errorMessage, setErrorMessage] = useState('');

  // Prevent background scrolling when modal is open
  useEffect(() => {
    // Save current body overflow style
    const originalStyle = window.getComputedStyle(document.body).overflow;
    
    // Disable scrolling
    document.body.style.overflow = 'hidden';
    
    // Handle Escape key to close modal
    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        onClose();
      }
    };
    
    // Add event listener
    document.addEventListener('keydown', handleEscape);
    
    // Cleanup function to restore scrolling and remove event listener
    return () => {
      document.body.style.overflow = originalStyle;
      document.removeEventListener('keydown', handleEscape);
    };
  }, [onClose]);

  const projectTypes = [
    { value: 'consultation', label: 'Technical Consultation', icon: 'fa-lightbulb' },
    { value: 'ai-development', label: 'AI System Development', icon: 'fa-brain' },
    { value: 'backend-development', label: 'Backend Development', icon: 'fa-server' },
    { value: 'fullstack-project', label: 'Full-Stack Project', icon: 'fa-code' },
    { value: 'database-design', label: 'Database Architecture', icon: 'fa-database' },
    { value: 'system-integration', label: 'System Integration', icon: 'fa-plug' },
    { value: 'other', label: 'Other Services', icon: 'fa-cogs' }
  ];

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setSubmitStatus('idle');
    setErrorMessage('');

    try {
      const result = await apiService.submitContactForm(formData);
      
      if (result.status === 'success') {
        setSubmitStatus('success');
        // Reset form after successful submission
        setTimeout(() => {
          setFormData({
            name: '',
            email: '',
            company: '',
            subject: '',
            message: '',
            projectType: 'consultation'
          });
        }, 2000);
      } else {
        setSubmitStatus('error');
        setErrorMessage(result.message || 'Failed to send message. Please try again.');
      }
    } catch (error: any) {
      setSubmitStatus('error');
      setErrorMessage(error.message || 'Network error. Please check your connection and try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div 
      className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-6 overflow-hidden animate-fadeIn"
      onClick={(e) => {
        // Close modal when clicking on backdrop
        if (e.target === e.currentTarget) {
          onClose();
        }
      }}
    >
      <div 
        className="bg-white rounded-3xl max-w-4xl w-full shadow-2xl flex flex-col relative animate-slideUp"
        onClick={(e) => e.stopPropagation()} // Prevent closing when clicking inside modal
        style={{ 
          maxHeight: 'calc(100vh - 6rem)', // More space for header visibility
          minHeight: '500px' // Increased minimum height
        }}
      >
        {/* Header */}
        <div className="relative bg-gradient-to-br from-ethiGreen to-emerald-600 text-white p-8 rounded-t-3xl flex-shrink-0 modal-header-fixed">
          <button
            onClick={onClose}
            className="absolute top-6 right-6 w-10 h-10 rounded-full bg-white/20 hover:bg-white/30 flex items-center justify-center transition-colors"
          >
            <i className="fas fa-times text-lg"></i>
          </button>
          
          <div className="flex items-center gap-6">
            <div className="w-20 h-20 bg-white/20 rounded-2xl flex items-center justify-center">
              <i className="fas fa-envelope text-3xl"></i>
            </div>
            <div>
              <h2 className="text-3xl font-bold mb-2">Get In Touch</h2>
              <p className="text-white/90 text-lg">
                Let's discuss your next AI or backend project
              </p>
            </div>
          </div>
          
          {/* Decorative Elements */}
          <div className="absolute top-4 right-20 w-16 h-16 bg-white/10 rounded-full"></div>
          <div className="absolute bottom-4 right-32 w-8 h-8 bg-white/10 rounded-full"></div>
        </div>

        {/* Form Content */}
        <div className="flex-1 overflow-y-auto modal-content-safe">
          <div className="p-8 pt-4">
            <form onSubmit={handleSubmit} className="space-y-6">
            {/* Personal Information */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-2">
                  Full Name *
                </label>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleInputChange}
                  required
                  className="w-full px-4 py-3 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-ethiGreen/20 focus:border-ethiGreen transition-colors"
                  placeholder="Your full name"
                />
              </div>
              
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-2">
                  Email Address *
                </label>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  required
                  className="w-full px-4 py-3 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-ethiGreen/20 focus:border-ethiGreen transition-colors"
                  placeholder="your.email@example.com"
                />
              </div>
            </div>

            {/* Company and Subject */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-2">
                  Company/Organization
                </label>
                <input
                  type="text"
                  name="company"
                  value={formData.company}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-ethiGreen/20 focus:border-ethiGreen transition-colors"
                  placeholder="Your company name (optional)"
                />
              </div>
              
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-2">
                  Subject *
                </label>
                <input
                  type="text"
                  name="subject"
                  value={formData.subject}
                  onChange={handleInputChange}
                  required
                  className="w-full px-4 py-3 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-ethiGreen/20 focus:border-ethiGreen transition-colors"
                  placeholder="Brief subject of your inquiry"
                />
              </div>
            </div>

            {/* Project Type Selection */}
            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-3">
                Project Type *
              </label>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                {projectTypes.map((type) => (
                  <label
                    key={type.value}
                    className={`relative flex items-center p-4 border-2 rounded-xl cursor-pointer transition-all ${
                      formData.projectType === type.value
                        ? 'border-ethiGreen bg-ethiGreen/5'
                        : 'border-slate-200 hover:border-slate-300'
                    }`}
                  >
                    <input
                      type="radio"
                      name="projectType"
                      value={type.value}
                      checked={formData.projectType === type.value}
                      onChange={handleInputChange}
                      className="sr-only"
                    />
                    <div className={`w-8 h-8 rounded-lg flex items-center justify-center mr-3 ${
                      formData.projectType === type.value
                        ? 'bg-ethiGreen text-white'
                        : 'bg-slate-100 text-slate-600'
                    }`}>
                      <i className={`fas ${type.icon} text-sm`}></i>
                    </div>
                    <div>
                      <div className="font-medium text-slate-800 text-sm">{type.label}</div>
                    </div>
                    {formData.projectType === type.value && (
                      <div className="absolute top-2 right-2 w-5 h-5 bg-ethiGreen rounded-full flex items-center justify-center">
                        <i className="fas fa-check text-white text-xs"></i>
                      </div>
                    )}
                  </label>
                ))}
              </div>
            </div>

            {/* Message */}
            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-2">
                Message *
              </label>
              <textarea
                name="message"
                value={formData.message}
                onChange={handleInputChange}
                required
                rows={6}
                className="w-full px-4 py-3 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-ethiGreen/20 focus:border-ethiGreen transition-colors resize-none"
                placeholder="Tell me about your project, requirements, timeline, and any specific questions you have..."
              />
              <div className="text-xs text-slate-500 mt-1">
                {formData.message.length}/1000 characters
              </div>
            </div>

            {/* Status Messages */}
            {submitStatus === 'success' && (
              <div className="bg-green-50 border border-green-200 rounded-xl p-4 flex items-center gap-3">
                <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                  <i className="fas fa-check text-green-600"></i>
                </div>
                <div>
                  <p className="font-semibold text-green-800">Message sent successfully!</p>
                  <p className="text-green-700 text-sm">I'll get back to you within 24 hours.</p>
                </div>
              </div>
            )}

            {submitStatus === 'error' && (
              <div className="bg-red-50 border border-red-200 rounded-xl p-4 flex items-center gap-3">
                <div className="w-8 h-8 bg-red-100 rounded-full flex items-center justify-center">
                  <i className="fas fa-exclamation-triangle text-red-600"></i>
                </div>
                <div>
                  <p className="font-semibold text-red-800">Failed to send message</p>
                  <p className="text-red-700 text-sm">{errorMessage}</p>
                </div>
              </div>
            )}

            {/* Submit Button */}
            <div className="flex items-center justify-between pt-4">
              <div className="text-sm text-slate-600">
                <i className="fas fa-shield-alt text-ethiGreen mr-2"></i>
                Your information is secure and will not be shared.
              </div>
              
              <button
                type="submit"
                disabled={isSubmitting}
                className="bg-gradient-to-r from-ethiGreen to-emerald-600 text-white px-8 py-3 rounded-xl font-semibold hover:shadow-lg transition-all duration-300 hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
              >
                {isSubmitting ? (
                  <>
                    <i className="fas fa-spinner fa-spin"></i>
                    Sending...
                  </>
                ) : (
                  <>
                    <i className="fas fa-paper-plane"></i>
                    Send Message
                  </>
                )}
              </button>
            </div>
          </form>
          </div>
        </div>

        {/* Footer */}
        <div className="bg-slate-50 px-8 py-6 rounded-b-3xl border-t border-slate-100 flex-shrink-0">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-6 text-sm text-slate-600">
              <div className="flex items-center gap-2">
                <i className="fas fa-clock text-ethiGreen"></i>
                <span>Response within 24 hours</span>
              </div>
              <div className="flex items-center gap-2">
                <i className="fas fa-map-marker-alt text-ethiGreen"></i>
                <span>Based in Ethiopia</span>
              </div>
            </div>
            
            <div className="flex items-center gap-3">
              <span className="text-sm text-slate-600">Connect with me:</span>
              <div className="flex gap-2">
                <a href="#" className="w-8 h-8 bg-slate-200 hover:bg-ethiGreen hover:text-white rounded-lg flex items-center justify-center transition-colors">
                  <i className="fab fa-linkedin text-sm"></i>
                </a>
                <a href="#" className="w-8 h-8 bg-slate-200 hover:bg-ethiGreen hover:text-white rounded-lg flex items-center justify-center transition-colors">
                  <i className="fab fa-github text-sm"></i>
                </a>
                <a href="mailto:jossyyasub@gmail.com" className="w-8 h-8 bg-slate-200 hover:bg-ethiGreen hover:text-white rounded-lg flex items-center justify-center transition-colors">
                  <i className="fas fa-envelope text-sm"></i>
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};