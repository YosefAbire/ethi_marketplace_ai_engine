import React, { useState, useRef, useEffect } from 'react';
import { Message, AgentRole } from '../types';
import { AGENTS } from '../constants';

interface ChatInterfaceProps {
  messages: Message[];
  onSendMessage: (text: string) => void;
  onClearChat: () => void;
  isTyping: boolean;
  activeAgent: AgentRole;
  setActiveAgent: (role: AgentRole) => void;
}

export const ChatInterface: React.FC<ChatInterfaceProps> = ({
  messages, onSendMessage, onClearChat, isTyping, activeAgent, setActiveAgent
}) => {
  const [input, setInput] = useState('');
  const [thinkingText, setThinkingText] = useState('Thinking...');
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom whenever messages change or typing status changes
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTo({
        top: scrollRef.current.scrollHeight,
        behavior: 'smooth'
      });
    }
  }, [messages, isTyping]);

  // Cycle thinking text when typing to give more descriptive feedback
  useEffect(() => {
    let interval: any;
    if (isTyping) {
      const texts = activeAgent === 'workflow'
        ? ['Orchestrating agents...', 'Analyzing intent...', 'Processing request...']
        : activeAgent === 'sql'
          ? ['Querying marketplace database...', 'Analyzing inventory numbers...', 'Calculating statistics...']
          : activeAgent === 'rag'
            ? ['Searching documents...', 'Retrieving context...', 'Synthesizing knowledge...']
            : activeAgent === 'seller'
              ? ['Analyzing market strategy...', 'Optimizing pricing models...', 'Consulting business logic...']
              : ['Checking logistics...', 'Coordinating operations...', 'Reviewing order flows...'];

      let i = 0;
      setThinkingText(texts[0]);
      interval = setInterval(() => {
        i = (i + 1) % texts.length;
        setThinkingText(texts[i]);
      }, 2000);
    }
    return () => clearInterval(interval);
  }, [isTyping, activeAgent]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim() && !isTyping) {
      onSendMessage(input);
      setInput('');
    }
  };

  const currentAgent = AGENTS.find(a => a.id === activeAgent) || AGENTS[0];

  return (
    <div className="h-full flex flex-col bg-slate-50">
      {/* Agent Selector Bar */}
      <div className="bg-white border-b px-8 py-3 flex gap-4 overflow-x-auto whitespace-nowrap custom-scrollbar items-center justify-between">
        <div className="flex gap-4">
          {AGENTS.map(agent => (
            <button
              key={agent.id}
              onClick={() => setActiveAgent(agent.id)}
              className={`flex items-center gap-2 px-4 py-2 rounded-full border transition-all text-xs font-bold ${activeAgent === agent.id
                ? 'bg-slate-900 border-slate-900 text-white shadow-md'
                : 'bg-white border-slate-200 text-slate-500 hover:bg-slate-50'
                }`}
            >
              <i className={`fas ${agent.icon}`}></i>
              {agent.name}
            </button>
          ))}
        </div>
        <button
          onClick={onClearChat}
          className="text-slate-400 hover:text-red-500 transition-colors px-3 py-2 rounded-lg hover:bg-red-50"
          title="Clear Chat History"
        >
          <i className="fas fa-trash-alt text-sm"></i>
        </button>
      </div>

      {/* Message Area */}
      <div ref={scrollRef} className="flex-1 overflow-y-auto p-8 space-y-6 custom-scrollbar">
        {messages.map(msg => {
          const msgAgent = AGENTS.find(a => a.id === msg.agent);
          const timestampStr = msg.timestamp instanceof Date
            ? msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
            : 'Unknown';

          return (
            <div key={msg.id} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-[80%] flex ${msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'} gap-4`}>
                <div className={`w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 shadow-sm ${msg.role === 'user'
                  ? 'bg-slate-200 text-slate-600'
                  : (msgAgent?.color || 'bg-indigo-600') + ' text-white'
                  }`}>
                  <i className={`fas ${msg.role === 'user' ? 'fa-user' : (msgAgent?.icon || 'fa-robot')}`}></i>
                </div>

                <div className={`p-5 rounded-2xl shadow-sm ${msg.role === 'user'
                  ? 'bg-slate-900 text-white rounded-tr-none'
                  : 'bg-white border border-slate-200 text-slate-800 rounded-tl-none'
                  }`}>
                  {msg.agent && msg.role === 'assistant' && (
                    <p className="text-[10px] font-black uppercase text-ethiGreen mb-2 tracking-widest">
                      Agent • ወኪል: {msgAgent?.name || 'Unknown Agent'}
                    </p>
                  )}
                  <div className="text-sm leading-relaxed whitespace-pre-wrap">
                    {(() => {
                      if (!msg.content) return null;
                      if (typeof msg.content === 'string') return msg.content;
                      if (Array.isArray(msg.content)) {
                        return msg.content.map((item: any, idx: number) => (
                          <div key={idx} className="mb-2 last:mb-0">
                            {typeof item === 'string'
                              ? item
                              : item.text || item.content || JSON.stringify(item)}
                          </div>
                        ));
                      }
                      return typeof msg.content === 'object'
                        ? (msg.content.text || msg.content.answer || msg.content.response || JSON.stringify(msg.content))
                        : String(msg.content);
                    })()}
                  </div>

                  {msg.sources && msg.sources.length > 0 && (
                    <div className="mt-4 pt-3 border-t border-slate-100">
                      <p className="text-[10px] font-black uppercase text-slate-400 mb-2 flex items-center gap-1.5">
                        <i className="fas fa-link text-[8px]"></i> Verified Sources • ማረጋገጫዎች
                      </p>
                      <div className="flex flex-wrap gap-2">
                        {msg.sources.map((source, idx) => (
                          <span key={idx} className="px-2 py-1 bg-ethiGreen/10 text-ethiGreen rounded text-[10px] font-bold border border-ethiGreen/20 flex items-center gap-1">
                            <i className="fas fa-file-alt text-[8px] opacity-50"></i>
                            {source}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  <p className="mt-3 text-[10px] opacity-40 font-bold uppercase">
                    {timestampStr}
                  </p>
                </div>
              </div>
            </div>
          );
        })}

        {/* Dynamic Typing Indicator with Context-Aware Text */}
        {isTyping && (
          <div className="flex justify-start items-center gap-4 animate-in fade-in slide-in-from-bottom-2 duration-300">
            <div className={`w-10 h-10 ${currentAgent.color} rounded-xl flex items-center justify-center text-white shadow-lg shadow-indigo-100 animate-pulse`}>
              <i className={`fas ${currentAgent.icon}`}></i>
            </div>
            <div className="bg-white border border-slate-200 px-5 py-4 rounded-2xl rounded-tl-none shadow-sm flex flex-col gap-1">
              <div className="flex items-center gap-1.5 mb-0.5">
                <span className="w-1.5 h-1.5 bg-ethiGreen rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></span>
                <span className="w-1.5 h-1.5 bg-ethiGreen rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
                <span className="w-1.5 h-1.5 bg-ethiGreen rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
              </div>
              <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest transition-opacity duration-500">
                {thinkingText} • በማሰብ ላይ
              </span>
            </div>
          </div>
        )}
      </div>

      {/* Input Area */}
      <div className="p-8 bg-white border-t">
        <form onSubmit={handleSubmit} className="max-w-4xl mx-auto flex gap-4">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={isTyping}
            placeholder={`Message ${currentAgent.name}...`}
            className="flex-1 px-6 py-4 bg-slate-50 border border-slate-200 rounded-2xl focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all font-medium text-sm shadow-inner disabled:opacity-50"
          />
          <button
            type="submit"
            disabled={!input.trim() || isTyping}
            className="px-8 bg-ethiGreen text-white rounded-2xl hover:bg-ethiGreen/80 disabled:opacity-50 transition-all shadow-lg shadow-ethiGreen/10 flex items-center justify-center font-bold"
          >
            <i className={`fas ${isTyping ? 'fa-circle-notch fa-spin' : 'fa-paper-plane'} mr-2`}></i>
            {isTyping ? 'Thinking...' : 'Send • ላክ'}
          </button>
        </form>
      </div>
    </div>
  );
};
