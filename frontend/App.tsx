
import React, { useState, useEffect } from 'react';
import { Sidebar } from './components/Sidebar';
import { Dashboard } from './components/Dashboard';
import { ChatInterface } from './components/ChatInterface';
import { KnowledgeBase } from './components/KnowledgeBase';
import { DeveloperHub } from './components/DeveloperHub';
import { FraudDetectionDashboard } from './components/FraudDetectionDashboard';
import { ProductModal, OrderModal } from './components/Modals';
import { Document, Message, AgentRole, Toast, EmailConfig, Product, Order } from './types';
import { MOCK_PRODUCTS, MOCK_ORDERS } from './constants';
import { gemini } from './services/gemini';
import { apiService } from './services/api';

import { LandingPage } from './components/LandingPage';
import { InteractiveLandingPage } from './components/InteractiveLandingPage';
import { AuthPage } from './components/AuthPage';
import { RevenuePage, ActiveOrdersPage, InventoryPage, AlertsPage } from './components/MetricPages';

const App: React.FC = () => {
  const [view, setView] = useState<'landing' | 'auth' | 'app'>('landing');
  const [user, setUser] = useState<any>(null);
  const [activeTab, setActiveTab] = useState<'dashboard' | 'chat' | 'knowledge' | 'dev' | 'fraud' | 'revenue' | 'orders' | 'inventory' | 'alerts'>('dashboard');
  const [activeAgent, setActiveAgent] = useState<AgentRole>('workflow');
  const [documents, setDocuments] = useState<Document[]>([]);
  const [toasts, setToasts] = useState<Toast[]>([]);
  const [emailConfig, setEmailConfig] = useState<EmailConfig>({
    recipientEmail: '',
    enabled: true
  });
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  // Selection states for detailed views
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [selectedOrder, setSelectedOrder] = useState<Order | null>(null);

  const [products, setProducts] = useState<Product[]>(MOCK_PRODUCTS);
  const [orders, setOrders] = useState<Order[]>(MOCK_ORDERS);
  const [stats, setStats] = useState<any>(null);

  const [messages, setMessages] = useState<Message[]>(() => {
    const saved = localStorage.getItem('ethi_market_chat_history');
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        return parsed.map((m: any) => ({
          ...m,
          timestamp: new Date(m.timestamp)
        }));
      } catch (e) {
        console.error("Failed to parse chat history", e);
      }
    }
    return [{
      id: 'initial',
      role: 'assistant',
      agent: 'workflow',
      content: "Welcome to Ethi Marketplace AI Engine. I'm the Workflow Agent. How can I assist you today?",
      timestamp: new Date()
    }];
  });
  const [isTyping, setIsTyping] = useState(false);

  const toggleSidebar = () => setIsSidebarOpen(!isSidebarOpen);

  const fetchDocuments = async () => {
    try {
      const docs = await apiService.getDocuments();
      setDocuments(docs.map((doc: any) => ({
        ...doc,
        uploadedAt: new Date(doc.uploadedAt)
      })));
    } catch (err) {
      console.error("Failed to fetch documents:", err);
    }
  };

  const fetchDashboardData = async () => {
    try {
      const [s, p, o] = await Promise.all([
        apiService.getDashboardStats(),
        apiService.getProducts(),
        apiService.getOrders()
      ]);
      setStats(s);
      setProducts(p);
      setOrders(o);
    } catch (err) {
      console.error("Failed to fetch dashboard data:", err);
    }
  };

  useEffect(() => {
    const savedEmail = localStorage.getItem('ethi_market_email_config');
    const savedUser = localStorage.getItem('ethi_market_user');
    fetchDocuments();
    fetchDashboardData();

    if (savedEmail) {
      try {
        setEmailConfig(JSON.parse(savedEmail));
      } catch (e) { }
    }

    if (savedUser) {
      try {
        setUser(JSON.parse(savedUser));
        setView('app');
      } catch (e) { }
    }
  }, []);

  useEffect(() => {
    localStorage.setItem('ethi_market_email_config', JSON.stringify(emailConfig));
  }, [emailConfig]);

  useEffect(() => {
    localStorage.setItem('ethi_market_chat_history', JSON.stringify(messages));
  }, [messages]);

  const handleClearChat = () => {
    if (window.confirm("Are you sure you want to clear the chat history?")) {
      const initialMsg: Message = {
        id: 'initial-' + Date.now(),
        role: 'assistant',
        agent: 'workflow',
        content: "Chat history cleared. How can I help you now?",
        timestamp: new Date()
      };
      setMessages([initialMsg]);
      localStorage.removeItem('ethi_market_chat_history');
      addToast("Chat history cleared", "success");
    }
  };

  const addToast = (message: string, type: 'success' | 'error' | 'info' = 'info') => {
    const id = Math.random().toString(36).substring(2, 9);
    setToasts(prev => [...prev, { id, message, type }]);
    setTimeout(() => removeToast(id), 6000);
  };

  const removeToast = (id: string) => {
    setToasts(prev => prev.filter(t => t.id !== id));
  };

  const handleSendMessage = async (text: string) => {
    if (!text.trim()) return;

    const userMsg: Message = { id: Date.now().toString(), role: 'user', content: text, timestamp: new Date() };
    setMessages(prev => [...prev, userMsg]);
    setIsTyping(true);

    try {
      const result = await apiService.ask(text, activeAgent);

      if (!result || !result.answer) {
        throw new Error("Invalid response received from the specialized agent.");
      }

      const assistantMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        agent: result.agent || 'workflow',
        content: result.answer,
        sources: result.sources,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, assistantMsg]);

      // Handle Notifications
      if (result.notifications && result.notifications.length > 0) {
        result.notifications.forEach(note => {
          if (note.type === 'email') {
            addToast(`Email Sent to ${note.details.to}: ${note.details.subject}`, 'success');
          }
        });
      }
    } catch (err: any) {
      const errorMessage = err.message || "An error occurred during agent processing.";
      addToast(errorMessage, "error");

      // Add an error message to the chat as well so the UI doesn't just stay empty
      const errorChatMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        agent: 'workflow',
        content: `I encountered an error: ${errorMessage}. Please check if the backend is running correctly.`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorChatMsg]);
    } finally {
      setIsTyping(false);
    }
  };

  if (view === 'landing') {
    return <InteractiveLandingPage onGetStarted={() => setView('auth')} />;
  }

  if (view === 'auth') {
    return <AuthPage onLogin={(userData) => { setUser(userData); setView('app'); }} onBack={() => setView('landing')} />;
  }

  return (
    <div className="flex h-screen bg-slate-50 text-slate-900 overflow-hidden font-inter">
      <div className={`fixed inset-0 bg-black/50 z-[100] transition-opacity duration-300 ${isSidebarOpen ? 'opacity-100 pointer-events-auto' : 'opacity-0 pointer-events-none'}`} onClick={toggleSidebar}></div>
      <div className={`fixed inset-y-0 left-0 z-[101] w-72 transform transition-transform duration-500 ease-elastic ${isSidebarOpen ? 'translate-x-0' : '-translate-x-full'}`}>
        <Sidebar
          activeTab={activeTab}
          setActiveTab={(tab) => { setActiveTab(tab); setIsSidebarOpen(false); }}
          emailConfig={emailConfig}
          setEmailConfig={setEmailConfig}
          onLogout={() => {
            localStorage.removeItem('ethi_market_user');
            setUser(null);
            setView('landing');
          }}
        />
      </div>

      <main className="flex-1 flex flex-col relative overflow-hidden">
        {/* Modals */}
        {selectedProduct && (
          <ProductModal product={selectedProduct} onClose={() => setSelectedProduct(null)} />
        )}
        {selectedOrder && (
          <OrderModal order={selectedOrder} onClose={() => setSelectedOrder(null)} />
        )}

        <div className="fixed top-6 right-6 z-[9999] flex flex-col gap-3 pointer-events-none min-w-[320px]">
          {toasts.map(toast => (
            <div key={toast.id} className={`pointer-events-auto flex items-start gap-4 px-5 py-4 rounded-2xl shadow-2xl border backdrop-blur-md transition-all duration-500 animate-in slide-in-from-right-full ${toast.type === 'error' ? 'bg-red-500/95 border-red-400 text-white' :
              toast.type === 'success' ? 'bg-emerald-600/95 border-emerald-500 text-white' :
                'bg-slate-900/95 border-slate-700 text-white'
              }`}>
              <div className="mt-1"><i className={`fas ${toast.type === 'error' ? 'fa-circle-exclamation' : toast.type === 'success' ? 'fa-circle-check' : 'fa-circle-info'} text-xl`}></i></div>
              <div className="flex-1"><p className="text-sm font-bold">{toast.message}</p></div>
              <button onClick={() => removeToast(toast.id)} className="mt-1 opacity-60 hover:opacity-100"><i className="fas fa-xmark"></i></button>
            </div>
          ))}
        </div>

        <header className="h-24 bg-white border-b-4 border-ethiGreen px-8 flex items-center justify-between shadow-md z-10 relative">
          <div className="absolute inset-0 tibeb-bg pointer-events-none"></div>
          <div className="flex items-center gap-6 relative z-10">
            <button
              onClick={toggleSidebar}
              className="w-12 h-12 bg-slate-100 rounded-xl flex items-center justify-center text-slate-500 hover:bg-ethiGreen hover:text-white transition-all shadow-sm active:scale-95"
            >
              <i className={`fas ${isSidebarOpen ? 'fa-xmark' : 'fa-bars'} text-xl`}></i>
            </button>
            <div className="flex items-center gap-4">
              <div className="w-14 h-14 bg-ethiGreen rounded-2xl flex items-center justify-center text-white shadow-xl shadow-ethiGreen/20">
                <i className="fas fa-microchip text-2xl"></i>
              </div>
              <div>
                <h1 className="font-ethiopic font-black text-2xl leading-tight tracking-tight text-slate-800">
                  Ethi Marketplace <span className="text-ethiGreen ml-2">ኢትዮ ማርኬት</span>
                </h1>
                <p className="text-[10px] text-slate-500 font-black uppercase tracking-[0.2em]">Enterprise Multi-Agent Engine • ተለዋዋጭ ወኪል ሞተር</p>
              </div>
            </div>
          </div>
          <div className="flex items-center gap-6 relative z-10">
          </div>
        </header>

        <div className="flex-1 overflow-hidden relative">
          {activeTab === 'dashboard' && (
            <Dashboard
              products={products}
              orders={orders}
              stats={stats}
              onSelectProduct={setSelectedProduct}
              onSelectOrder={setSelectedOrder}
              onTabChange={setActiveTab}
            />
          )}
          {activeTab === 'fraud' && <FraudDetectionDashboard onTabChange={setActiveTab} />}
          {activeTab === 'revenue' && <RevenuePage orders={orders} onBack={() => setActiveTab('dashboard')} />}
          {activeTab === 'orders' && <ActiveOrdersPage orders={orders} onBack={() => setActiveTab('dashboard')} />}
          {activeTab === 'inventory' && <InventoryPage products={products} onBack={() => setActiveTab('dashboard')} />}
          {activeTab === 'alerts' && <AlertsPage products={products} onBack={() => setActiveTab('dashboard')} />}
          {activeTab === 'chat' && (
            <ChatInterface
              messages={messages}
              onSendMessage={handleSendMessage}
              onClearChat={handleClearChat}
              isTyping={isTyping}
              activeAgent={activeAgent}
              setActiveAgent={setActiveAgent}
            />
          )}
          {activeTab === 'knowledge' && (
            <KnowledgeBase
              documents={documents}
              onFileUpload={async (e) => {
                const files = e.target.files;
                if (!files) return;

                for (const file of Array.from(files) as File[]) {
                  try {
                    await apiService.uploadFile(file);
                    addToast(`Indexed ${file.name} successfully`, 'success');
                  } catch (err: any) {
                    addToast(`Failed to upload ${file.name}: ${err.message}`, 'error');
                  }
                }
                fetchDocuments();
              }}
              onDeleteDocument={async (id) => {
                try {
                  await apiService.deleteDocument(id);
                  addToast(`Document deleted`, 'success');
                  fetchDocuments();
                } catch (err: any) {
                  addToast(`Failed to delete: ${err.message}`, 'error');
                }
              }}
            />
          )}
        </div>
      </main>
    </div>
  );
};

export default App;
