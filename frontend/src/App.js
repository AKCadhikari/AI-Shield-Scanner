import React, { useState } from 'react';
import { 
  LayoutDashboard, Settings, ShieldAlert, 
  PlayCircle, FileText, ChevronRight, 
  User, LogOut 
} from 'lucide-react';

import DashboardView from './components/DashboardView';
import ScanConfigView from './components/ScanConfigView';
import ReportsView from './components/ReportsView';
import SettingsView from './components/SettingsView';
// Import other views as they are created

const AIShieldScanner = () => {
  const [activeTab, setActiveTab] = useState('Dashboard');

  const menuItems = [
    { name: 'Dashboard', icon: <LayoutDashboard size={20} /> },
    { name: 'Scan Configurations', icon: <ShieldAlert size={20} /> },
    { name: 'Test Runs', icon: <PlayCircle size={20} /> },
    { name: 'Reports', icon: <FileText size={20} /> },
    { name: 'Settings', icon: <Settings size={20} /> },
  ];

  return (
    <div className="flex h-screen bg-[#0b0e14] text-slate-300 font-sans">
      {/* SIDEBAR */}
      <aside className="w-64 flex flex-col h-full border-r border-slate-800/40">
        
        {/* Logo Section */}
        <div className="p-8 flex items-center justify-center">
          <div className="w-40 h-auto">
             <img 
               src={new URL('./logo.png', import.meta.url).href} 
               alt="AI Shield Logo" 
               className="w-full h-full object-contain filter drop-shadow-[0_0_8px_rgba(6,182,212,0.3)]" 
             />
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 px-4 space-y-2">
          {menuItems.map((item) => (
            <button
              key={item.name}
              onClick={() => setActiveTab(item.name)}
              className={`w-full flex items-center justify-between px-4 py-3 rounded-lg transition-all ${
                activeTab === item.name 
                ? 'bg-cyan-500 text-white shadow-[0_0_15px_rgba(6,182,212,0.4)]' 
                : 'hover:bg-slate-800/50'
              }`}
            >
              <div className="flex items-center gap-3">
                {item.icon}
                <span className="text-sm font-medium">{item.name}</span>
              </div>
              {activeTab === item.name && <ChevronRight size={16} />}
            </button>
          ))}
        </nav>

        {/* SIDEBAR BOTTOM: Enhanced Profile & Centered Divider */}
        <div className="mt-auto p-4 pl-6 pb-6">
          
          {/* Centered Divider: Does not touch edges (image_94d638.png) */}
          <div className="border-t border-slate-800/60 mb-6 mr-2" /> 

          <div className="flex items-center gap-4 group">
            
            {/* User Profile Info (image_94da76.png) */}
            <div className="flex items-center gap-3 cursor-pointer overflow-hidden">
              <div className="shrink-0 w-11 h-11 rounded-full bg-slate-800 flex items-center justify-center text-cyan-500 border border-slate-700">
                <User size={22} />
              </div>
              <div className="flex flex-col min-w-0 leading-tight">
                <span className="text-sm font-bold text-white truncate">Admin User</span>
                <span className="text-[11px] text-slate-500 uppercase tracking-tighter">Security Lead</span>
              </div>
            </div>
            
            {/* Logout Button: Positioned close but aligned right */}
            <button 
              title="Logout"
              className="p-1.5 rounded-lg text-slate-500 hover:bg-red-500/10 hover:text-red-500 transition-all shrink-0 ml-auto pr-2"
            >
              <LogOut size={20} />
            </button>
          </div>
        </div>
      </aside>

      {/* MAIN CONTENT AREA */}
      <main className="flex-1 flex flex-col overflow-hidden">
        <div className="flex-1 overflow-y-auto p-10">
          {activeTab === 'Dashboard' && <DashboardView />}
          {activeTab === 'Scan Configurations' && <ScanConfigView />}
          {/* Default fallbacks for coming soon sections */}
          {!['Dashboard', 'Scan Configurations'].includes(activeTab) && (
            <div className="h-full flex items-center justify-center text-slate-500 italic">
              {activeTab} View is under development
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default AIShieldScanner;