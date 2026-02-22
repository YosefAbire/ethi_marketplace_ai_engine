
import React from 'react';
import { EmailConfig } from '../types';

interface SidebarProps {
  activeTab: 'dashboard' | 'chat' | 'knowledge' | 'dev' | 'fraud' | 'revenue' | 'orders' | 'inventory' | 'alerts';
  setActiveTab: (tab: any) => void;
  emailConfig: EmailConfig;
  setEmailConfig: (config: EmailConfig) => void;
  onLogout: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ activeTab, setActiveTab, emailConfig, setEmailConfig, onLogout }) => {
  const [showMapModal, setShowMapModal] = React.useState(false);

  const coreItems = [
    { id: 'dashboard', icon: 'fa-chart-pie', label: 'Dashboard', am: 'ዳሽቦርድ' },
    { id: 'chat', icon: 'fa-robot', label: 'AI Agents', am: 'ወኪሎች' },
    { id: 'knowledge', icon: 'fa-folder-open', label: 'Knowledge Base', am: 'እውቀት' },
    { id: 'fraud', icon: 'fa-shield-alt', label: 'Fraud Detection', am: 'ማጭበርበር ማወቂያ' },
  ];

  const analysisItems = [
    { id: 'revenue', icon: 'fa-money-bill-trend-up', label: 'Revenue', am: 'ገቢ' },
    { id: 'orders', icon: 'fa-basket-shopping', label: 'Active Orders', am: 'ትዕዛዞች' },
    { id: 'inventory', icon: 'fa-warehouse', label: 'Inventory', am: 'ክምችት' },
    { id: 'alerts', icon: 'fa-bell', label: 'Alerts', am: 'ማስጠንቀቂያ' },
  ];

  const cityItems = [
    { id: 'addis', label: 'Addis Ababa', am: 'አዲስ አበባ' },
    { id: 'arbaminch', label: 'Arba Minch', am: 'አርባ ምንጭ' },
    { id: 'adama', label: 'Adama', am: 'አዳማ' },
    { id: 'bahirdar', label: 'Bahir Dar', am: 'ባህር ዳር' },
    { id: 'hawassa', label: 'Hawassa', am: 'ሀዋሳ' },
    { id: 'dire', label: 'Dire Dawa', am: 'ድሬዳዋ' },
    { id: 'gondar', label: 'Gondar', am: 'ጎንደር' },
    { id: 'mekelle', label: 'Mekelle', am: 'መቐለ' },
    { id: 'jimma', label: 'Jimma', am: 'ጅማ' },
  ];

  return (
    <>
      {/* Map Modal */}
      {showMapModal && (
        <div 
          className="fixed inset-0 bg-black/95 z-[9999] flex items-center justify-center animate-in fade-in duration-300"
          onClick={() => setShowMapModal(false)}
        >
          <div 
            className="bg-white w-full h-full flex flex-col animate-in zoom-in-95 duration-300"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="bg-gradient-to-r from-ethiGreen to-emerald-600 text-white p-6 flex items-center justify-between shadow-lg">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center backdrop-blur-sm">
                  <i className="fas fa-map-marked-alt text-2xl"></i>
                </div>
                <div>
                  <h3 className="text-2xl font-black">Gamo Zone Map</h3>
                  <p className="text-sm text-white/80 font-medium">Arba Minch & Surrounding Areas • አርባ ምንጭ እና አካባቢው</p>
                </div>
              </div>
              <button
                onClick={() => setShowMapModal(false)}
                className="w-12 h-12 bg-white/20 hover:bg-white/30 rounded-xl flex items-center justify-center transition-all hover:rotate-90 duration-300"
              >
                <i className="fas fa-times text-2xl"></i>
              </button>
            </div>
            <div className="flex-1 relative">
              <iframe
                src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d504579.5979156494!2d37.28956!3d6.03891!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x17b7d8f3c5c5c5c5%3A0x5c5c5c5c5c5c5c5c!2sGamo%20Zone%2C%20Ethiopia!5e0!3m2!1sen!2sus!4v1234567890"
                width="100%"
                height="100%"
                style={{ border: 0 }}
                allowFullScreen
                loading="lazy"
                referrerPolicy="no-referrer-when-downgrade"
                title="Gamo Zone Map"
                className="absolute inset-0"
              ></iframe>
            </div>
            <div className="bg-white border-t border-slate-200 p-4 flex items-center justify-between shadow-lg">
              <div className="flex items-center gap-3 text-sm text-slate-600">
                <i className="fas fa-info-circle text-ethiGreen text-lg"></i>
                <span className="font-medium">Interactive map showing Gamo Zone and Arba Minch region</span>
              </div>
              <button
                onClick={() => setShowMapModal(false)}
                className="px-6 py-2.5 bg-slate-100 hover:bg-slate-200 rounded-lg font-bold transition-all flex items-center gap-2"
              >
                <i className="fas fa-times"></i>
                Close
              </button>
            </div>
          </div>
        </div>
      )}

      <nav className="w-full h-full bg-white text-slate-600 flex flex-col border-r border-slate-200 shadow-xl">
      <div className="p-8 pb-4">
        <div className="flex items-center gap-2 mb-8">
          <span className="text-slate-900 font-black text-2xl tracking-tighter">ETHI</span>
          <span className="px-1.5 py-0.5 bg-ethiGreen text-white text-[10px] font-bold rounded">AI</span>
        </div>
      </div>

      <div className="flex-1 px-4 space-y-8 overflow-y-auto custom-scrollbar">
        <div>
          <p className="text-[10px] font-black text-slate-400 uppercase mb-4 tracking-[0.2em] px-4">Core Engine</p>
          <div className="space-y-1">
            {coreItems.map(item => (
              <SidebarItem key={item.id} item={item} activeTab={activeTab} setActiveTab={setActiveTab} />
            ))}
          </div>
        </div>

        <div>
          <p className="text-[10px] font-black text-slate-400 uppercase mb-4 tracking-[0.2em] px-4">Market Analysis</p>
          <div className="space-y-1">
            {analysisItems.map(item => (
              <SidebarItem key={item.id} item={item} activeTab={activeTab} setActiveTab={setActiveTab} />
            ))}
          </div>
        </div>

        <div>
          <div className="flex justify-between items-center px-4 mb-4">
            <p className="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">Nearby Cities</p>
            <button className="text-[10px] text-ethiGreen font-bold hover:underline">Edit</button>
          </div>
          <div className="space-y-1">
            {cityItems.map(city => (
              <button
                key={city.id}
                onClick={() => {
                  if (city.id === 'arbaminch') {
                    setShowMapModal(true);
                  }
                }}
                className="w-full flex items-center gap-3 px-4 py-2.5 rounded-xl transition-all font-medium text-sm group hover:bg-slate-50 hover:text-slate-900 text-slate-500"
              >
                <div className="w-8 h-8 rounded-lg flex items-center justify-center bg-slate-100 group-hover:bg-white group-hover:shadow-sm transition-all border border-transparent group-hover:border-slate-200">
                  <i className={`fas ${city.id === 'arbaminch' ? 'fa-map-marked-alt' : 'fa-map-marker-alt'} text-xs text-slate-400 group-hover:text-ethiRed`}></i>
                </div>
                <div className="flex flex-col items-start leading-tight">
                  <span className="font-bold text-xs">{city.label}</span>
                  <span className="text-[8px] uppercase tracking-widest text-slate-400 group-hover:text-slate-500">{city.am}</span>
                </div>
                {city.id === 'arbaminch' && (
                  <i className="fas fa-external-link-alt text-[10px] text-slate-400 ml-auto opacity-0 group-hover:opacity-100 transition-opacity"></i>
                )}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="p-6 mt-auto border-t border-slate-100 space-y-4">
        <div className="bg-slate-50 p-4 rounded-2xl border border-slate-200 space-y-4">
          <div>
            <p className="text-[10px] font-black text-slate-400 uppercase mb-2 tracking-widest">Notification Email</p>
            <input
              type="email"
              value={emailConfig.recipientEmail}
              onChange={(e) => setEmailConfig({ ...emailConfig, recipientEmail: e.target.value })}
              placeholder="recipient@example.com"
              className="w-full bg-white border border-slate-200 text-slate-700 text-xs rounded-lg px-3 py-2 focus:border-ethiGreen focus:outline-none placeholder:text-slate-400 shadow-sm"
            />
          </div>
          <div className="flex justify-between items-center text-xs">
            <span className="font-bold text-slate-600">Notifications</span>
            <button
              onClick={() => setEmailConfig({ ...emailConfig, enabled: !emailConfig.enabled })}
              className={`w-10 h-5 rounded-full relative transition-colors ${emailConfig.enabled ? 'bg-ethiGreen' : 'bg-slate-200'}`}
            >
              <div className={`absolute top-1 w-3 h-3 bg-white rounded-full transition-all shadow-sm ${emailConfig.enabled ? 'left-6' : 'left-1'}`}></div>
            </button>
          </div>
        </div>

        <button
          onClick={onLogout}
          className="w-full flex items-center gap-4 px-4 py-3 rounded-xl hover:bg-red-50 text-slate-500 hover:text-red-500 transition-all font-bold text-xs"
        >
          <i className="fas fa-sign-out-alt w-5"></i>
          Logout • ውጣ
        </button>
      </div>
    </nav>
    </>
  );
};

const SidebarItem = ({ item, activeTab, setActiveTab }: any) => (
  <button
    onClick={() => setActiveTab(item.id)}
    className={`w-full flex items-center gap-4 px-4 py-3 rounded-xl transition-all font-medium text-sm group ${activeTab === item.id
      ? 'bg-ethiGreen text-white shadow-lg shadow-ethiGreen/20'
      : 'hover:bg-slate-50 text-slate-500 hover:text-slate-900'
      }`}
  >
    <div className={`w-8 h-8 rounded-lg flex items-center justify-center transition-all ${activeTab === item.id ? 'bg-white/20' : 'bg-slate-100 group-hover:bg-white group-hover:shadow-sm border border-transparent group-hover:border-slate-200'}`}>
      <i className={`fas ${item.icon} text-xs ${activeTab === item.id ? 'text-white' : 'text-slate-400 group-hover:text-ethiGreen'}`}></i>
    </div>
    <div className="flex flex-col items-start leading-tight">
      <span className="font-bold">{item.label}</span>
      <span className={`text-[8px] uppercase tracking-widest ${activeTab === item.id ? 'text-white/60' : 'text-slate-400 group-hover:text-slate-500'}`}>{item.am}</span>
    </div>
    {activeTab === item.id && (
      <div className="ml-auto w-1.5 h-1.5 bg-white rounded-full"></div>
    )}
  </button>
);
