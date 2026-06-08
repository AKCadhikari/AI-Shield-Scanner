import React, { useState } from 'react';
import { 
  LayoutDashboard, Settings, ShieldAlert, 
  PlayCircle, FileText, ChevronRight, 
  User, LogOut, Menu, X 
} from 'lucide-react';

// USE THE RELATIVE PATH WITH './'
import logoUrl from './logo.png';

import DashboardView from './components/DashboardView';
import ScanConfigView from './components/ScanConfigView';
import ReportsView from './components/ReportsView';
import SettingsView from './components/SettingsView';
import TestRunsView from './components/TestRunsView';

const AIShieldScanner = () => {
  const [activeTab, setActiveTab] = useState('Dashboard');
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const menuItems = [
    { name: 'Dashboard', icon: <LayoutDashboard size={20} /> },
    { name: 'Scan Configurations', icon: <ShieldAlert size={20} /> },
    { name: 'Test Runs', icon: <PlayCircle size={20} /> },
    { name: 'Reports', icon: <FileText size={20} /> },
    { name: 'Settings', icon: <Settings size={20} /> },
  ];

  const handleTabChange = (tabName) => {
    setActiveTab(tabName);
    setMobileMenuOpen(false);
  };

  return (
    <div 
      className="flex flex-col xl:flex-row bg-[#0b0e14] text-slate-300 font-sans overflow-hidden relative"
      style={{ height: '100vh', width: '100vw' }}
    >
      
      {/* MOBILE HEADER */}
      <header className="xl:hidden w-full h-16 bg-[#0b0e14] border-b border-slate-800/60 flex items-center justify-between px-6 shrink-0 z-40">
        <div className="w-28 h-auto">
          <img 
            src={logoUrl}
            alt="AI Shield Logo" 
            className="w-full h-full object-contain filter drop-shadow-[0_0_8px_rgba(6,182,212,0.3)]" 
          />
        </div>
        <button 
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          className="p-1 text-slate-400 hover:text-cyan-400 transition-colors cursor-pointer"
        >
          {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </header>

      {/* SIDEBAR */}
      <aside className={`w-64 flex flex-col h-full border-r border-slate-800/40 shrink-0 bg-[#0b0e14] absolute xl:relative z-50 xl:translate-x-0 transition-transform duration-300 ease-in-out ${
        mobileMenuOpen ? 'translate-x-0 top-0 left-0 bottom-0' : '-translate-x-full xl:translate-x-0'
      }`}>
        <div className="p-8 hidden xl:flex items-center justify-center">
          <div className="w-40 h-auto">
             <img 
               src={logoUrl} 
               alt="AI Shield Logo" 
               className="w-full h-full object-contain filter drop-shadow-[0_0_8px_rgba(6,182,212,0.3)]" 
             />
          </div>
        </div>

        <div className="h-16 xl:hidden shrink-0" />

        <nav className="flex-1 px-4 space-y-2 mt-4 xl:mt-0 overflow-y-auto custom-scrollbar">
          {menuItems.map((item) => (
            <button
              key={item.name}
              onClick={() => handleTabChange(item.name)}
              className={`w-full flex items-center justify-between px-4 py-3 rounded-lg transition-all cursor-pointer ${
                activeTab === item.name 
                ? 'bg-cyan-500 text-white shadow-[0_0_15px_rgba(6,182,212,0.4)] font-semibold' 
                : 'hover:bg-slate-800/50 text-slate-400 hover:text-slate-200'
              }`}
            >
              <div className="flex items-center gap-3">
                {item.icon}
                <span className="text-sm">{item.name}</span>
              </div>
              {activeTab === item.name && <ChevronRight size={16} />}
            </button>
          ))}
        </nav>

        <div className="mt-auto p-4 pl-6 pb-6 bg-[#0b0e14]">
          <div className="border-t border-slate-800/60 mb-6 mr-2" /> 
          <div className="flex items-center gap-4 group">
            <div className="flex items-center gap-3 cursor-pointer overflow-hidden min-w-0 flex-1">
              <div className="shrink-0 w-11 h-11 rounded-full bg-slate-800 flex items-center justify-center text-cyan-500 border border-slate-700">
                <User size={22} />
              </div>
              <div className="flex flex-col min-w-0 leading-tight">
                <span className="text-sm font-bold text-white truncate">Admin User</span>
                <span className="text-[11px] text-slate-500 uppercase tracking-tighter truncate">Security Lead</span>
              </div>
            </div>
            <button title="Logout" className="p-1.5 rounded-lg text-slate-500 hover:bg-red-500/10 hover:text-red-500 transition-all shrink-0 ml-auto pr-2 cursor-pointer">
              <LogOut size={20} />
            </button>
          </div>
        </div>
      </aside>

      {mobileMenuOpen && (
        <div 
          className="fixed inset-0 bg-black/70 backdrop-blur-xs xl:hidden z-35"
          onClick={() => setMobileMenuOpen(false)}
        />
      )}

      <main 
        className="flex-1 flex flex-col overflow-hidden w-full min-w-0"
        style={{ height: '100%', minHeight: '0px' }}
      >
        <div className="flex-1 overflow-y-auto p-4 md:p-8 xl:p-10 custom-scrollbar max-w-full">
          {activeTab === 'Dashboard' && <DashboardView />}
          {activeTab === 'Scan Configurations' && <ScanConfigView />}
          {activeTab === 'Test Runs' && <TestRunsView />}
          {activeTab === 'Reports' && <ReportsView />}
          {activeTab === 'Settings' && <SettingsView />}
        </div>
      </main>

    </div>
  );
};

export default AIShieldScanner;