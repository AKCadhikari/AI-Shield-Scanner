import React, { useState, useRef, useEffect } from 'react';
import { Shield, Database, ChevronDown } from 'lucide-react';

const SettingsView = () => {
  // Matrix data matching the target mockup table state exactly
  const permissionsData = [
    { name: 'View Dashboard', admin: true, tester: true, viewer: true },
    { name: 'Run Security Scans', admin: true, tester: true, viewer: false },
    { name: 'Configure Scans', admin: true, tester: true, viewer: false },
    { name: 'View Reports', admin: true, tester: true, viewer: true },
    { name: 'Generate Reports', admin: true, tester: true, viewer: false },
    { name: 'Manage Users', admin: true, tester: false, viewer: false },
    { name: 'Edit Detection Rules', admin: true, tester: false, viewer: false },
    { name: 'Modify Settings', admin: true, tester: false, viewer: false },
  ];

  // Custom dropdown states for the Data Retention Policy field
  const [retentionPolicy, setRetentionPolicy] = useState('90 Days');
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const dropdownRef = useRef(null);
  
  const retentionOptions = ['30 Days', '60 Days', '90 Days'];

  // Close the dropdown window gracefully if a click occurs outside of its bounds
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsDropdownOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <div className="w-full space-y-6 text-slate-300 font-sans pb-4">
      
      {/* TOP HEADER BLOCK */}
      <div>
        <h1 className="text-3xl font-bold text-white mb-1">Settings</h1>
        <p className="text-sm text-slate-400">Manage application permissions and global security rules</p>
      </div>

      {/* 1. ROLE PERMISSIONS PANEL */}
      <div className="bg-[#151921] border border-slate-800/80 rounded-xl p-8 space-y-6 shadow-sm">
        <h3 className="flex items-center gap-3 text-white font-semibold text-lg">
          <div className="p-1.5 rounded border border-purple-500/30 bg-purple-500/10">
            <Shield className="text-purple-400" size={18} />
          </div>
          <div>
            Role Permissions
            <p className="text-xs text-slate-500 font-normal mt-0.5">Define what each role can do</p>
          </div>
        </h3>

        <div className="overflow-x-auto w-full custom-scrollbar">
          <table className="w-full text-left border-collapse min-w-150">
            <thead>
              <tr className="text-slate-400 text-xs font-semibold border-b border-slate-800/60">
                <th className="pb-4 font-semibold w-1/2">Permission</th>
                <th className="pb-4 font-semibold text-center w-1/6">Admin</th>
                <th className="pb-4 font-semibold text-center w-1/6">Tester</th>
                <th className="pb-4 font-semibold text-center w-1/6">Viewer</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/40 text-sm font-medium">
              {permissionsData.map((perm) => (
                <tr key={perm.name} className="hover:bg-slate-800/10 transition-colors">
                  <td className="py-4 text-slate-200">{perm.name}</td>
                  
                  {/* Admin Grid Column */}
                  <td className="py-4 text-center">
                    <div className="inline-flex items-center justify-center">
                      {perm.admin ? (
                        <div className="w-5 h-5 rounded-full bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center">
                          <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 shadow-[0_0_8px_#10b981]" />
                        </div>
                      ) : (
                        <div className="w-5 h-5 rounded-full bg-[#0b0e14] border border-slate-800/60" />
                      )}
                    </div>
                  </td>

                  {/* Tester Grid Column */}
                  <td className="py-4 text-center">
                    <div className="inline-flex items-center justify-center">
                      {perm.tester ? (
                        <div className="w-5 h-5 rounded-full bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center">
                          <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 shadow-[0_0_8px_#10b981]" />
                        </div>
                      ) : (
                        <div className="w-5 h-5 rounded-full bg-[#0b0e14] border border-slate-800/60" />
                      )}
                    </div>
                  </td>

                  {/* Viewer Grid Column */}
                  <td className="py-4 text-center">
                    <div className="inline-flex items-center justify-center">
                      {perm.viewer ? (
                        <div className="w-5 h-5 rounded-full bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center">
                          <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 shadow-[0_0_8px_#10b981]" />
                        </div>
                      ) : (
                        <div className="w-5 h-5 rounded-full bg-[#0b0e14] border border-slate-800/60" />
                      )}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* 2. SECURITY SYSTEM POLICIES CARD */}
      <div className="bg-[#151921] border border-slate-800/80 rounded-xl p-8 space-y-6 shadow-sm">
        <h3 className="flex items-center gap-3 text-white font-semibold text-lg">
          <div className="p-1.5 rounded border border-amber-500/30 bg-amber-500/10">
            <Database className="text-amber-400" size={18} />
          </div>
          <div>
            Security Settings
            <p className="text-xs text-slate-500 font-normal mt-0.5">Configure data retention and encryption</p>
          </div>
        </h3>

        <div className="space-y-6 pt-2">
          {/* Form Block: Custom Themed Dropdown Selection Menu */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-5 border-b border-slate-800/60 relative">
            <div className="space-y-0.5">
              <label className="text-sm font-semibold text-slate-200 block">Data Retention Policy</label>
              <span className="text-xs text-slate-500 block">Scan results and logs will be automatically deleted after this period</span>
            </div>
            
            {/* Custom UI Dropdown Component Container */}
            <div className="w-full sm:w-48 shrink-0 relative" ref={dropdownRef}>
              <button
                type="button"
                onClick={() => setIsDropdownOpen(!isDropdownOpen)}
                className={`w-full bg-[#0b0e14] border rounded-lg px-4 py-3 text-xs text-slate-200 flex items-center justify-between transition-all duration-200 ${
                  isDropdownOpen ? 'border-cyan-500 ring-1 ring-cyan-500/20' : 'border-slate-800'
                }`}
              >
                <span>{retentionPolicy}</span>
                <ChevronDown className={`text-slate-400 transition-transform duration-200 ${isDropdownOpen ? 'rotate-180' : ''}`} size={14} />
              </button>

              {isDropdownOpen && (
                <div className="absolute top-full left-0 w-full mt-2 bg-[#0b0e14] border border-slate-800 rounded-lg shadow-2xl z-100 overflow-hidden">
                  {retentionOptions.map((option) => (
                    <div
                      key={option}
                      onClick={() => {
                        setRetentionPolicy(option);
                        setIsDropdownOpen(false);
                      }}
                      className={`px-4 py-3 text-xs cursor-pointer transition-colors ${
                        retentionPolicy === option 
                          ? 'bg-cyan-500 text-slate-900 font-bold' 
                          : 'text-slate-300 hover:bg-slate-800 hover:text-white'
                      }`}
                    >
                      {option}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Form Block: Encryption Status Flag */}
          <div className="flex items-center justify-between py-2 border-b border-slate-800/60">
            <div className="space-y-0.5">
              <p className="text-sm font-semibold text-slate-200">Log Encryption</p>
              <p className="text-xs text-slate-500">Encrypt all stored test logs and results</p>
            </div>
            <div className="flex items-center gap-2 text-xs font-semibold text-emerald-400 bg-emerald-500/5 border border-emerald-500/10 px-2.5 py-1 rounded-md select-none">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
              Enabled
            </div>
          </div>

          {/* Form Block: 2FA Policy Status Flag */}
          <div className="flex items-center justify-between py-2">
            <div className="space-y-0.5">
              <p className="text-sm font-semibold text-slate-200">Two-Factor Authentication</p>
              <p className="text-xs text-slate-500">Require 2FA for all admin users</p>
            </div>
            <div className="flex items-center gap-2 text-xs font-semibold text-emerald-400 bg-emerald-500/5 border border-emerald-500/10 px-2.5 py-1 rounded-md select-none">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
              Enabled
            </div>
          </div>
        </div>
      </div>

    </div>
  );
};

export default SettingsView;