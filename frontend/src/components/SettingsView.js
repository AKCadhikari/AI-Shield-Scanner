import React from 'react';
import { Shield, Database, Eye } from 'lucide-react';

const SettingsView = () => {
  // Ordered array mapping to the screenshot entries exactly
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

  return (
    <div className="w-full space-y-6 text-slate-300 font-sans pb-4">
      
      {/* 1. ROLE PERMISSIONS PANEL */}
      <div className="bg-[#151921] border border-slate-800 rounded-xl p-8 space-y-6 shadow-sm">
        <h3 className="flex items-center gap-3 text-white font-semibold text-lg">
          <div className="p-1.5 rounded border border-purple-500/30 bg-purple-500/10">
            <Shield className="text-purple-400" size={18} />
          </div>
          <div>
            Role Permissions
            <p className="text-xs text-slate-500 font-normal mt-0.5">Define what each role can do</p>
          </div>
        </h3>

        <div className="overflow-x-auto w-full">
          <table className="w-full text-left border-collapse min-w-150">
            <thead>
              <tr className="text-slate-400 text-xs font-semibold border-b border-slate-800/80">
                <th className="pb-4 font-semibold w-1/2">Permission</th>
                <th className="pb-4 font-semibold text-center w-1/6">Admin</th>
                <th className="pb-4 font-semibold text-center w-1/6">Tester</th>
                <th className="pb-4 font-semibold text-center w-1/6">Viewer</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/40 text-sm font-medium">
              {permissionsData.map((perm) => (
                <tr key={perm.name} className="hover:bg-slate-800/5 transition-colors">
                  <td className="py-4 text-slate-200">{perm.name}</td>
                  
                  {/* Admin Column Badge Indicators */}
                  <td className="py-4 text-center">
                    <div className="inline-flex items-center justify-center">
                      {perm.admin ? (
                        <div className="w-5 h-5 rounded-full bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
                          <Eye size={11} strokeWidth={3} />
                        </div>
                      ) : (
                        <div className="w-5 h-5 rounded-full bg-[#0b0e14] border border-slate-800" />
                      )}
                    </div>
                  </td>

                  {/* Tester Column Badge Indicators */}
                  <td className="py-4 text-center">
                    <div className="inline-flex items-center justify-center">
                      {perm.tester ? (
                        <div className="w-5 h-5 rounded-full bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
                          <Eye size={11} strokeWidth={3} />
                        </div>
                      ) : (
                        <div className="w-5 h-5 rounded-full bg-[#0b0e14] border border-slate-800/60" />
                      )}
                    </div>
                  </td>

                  {/* Viewer Column Badge Indicators */}
                  <td className="py-4 text-center">
                    <div className="inline-flex items-center justify-center">
                      {perm.viewer ? (
                        <div className="w-5 h-5 rounded-full bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
                          <Eye size={11} strokeWidth={3} />
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

      {/* 2. SECURITY SETTINGS PANEL */}
      <div className="bg-[#151921] border border-slate-800 rounded-xl p-8 space-y-6 shadow-sm">
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
          {/* Data Retention Dropdown Context Menu Block */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-5 border-b border-slate-800/60">
            <div className="space-y-0.5">
              <label className="text-sm font-semibold text-slate-200 block">Data Retention Policy</label>
              <span className="text-xs text-slate-500 block">Scan results and logs will be automatically deleted after this period</span>
            </div>
            <div className="w-full sm:w-48 shrink-0">
              <select className="w-full bg-[#0b0e14] border border-slate-800 rounded-lg p-3 text-xs text-slate-200 outline-none focus:border-cyan-500 cursor-pointer transition-colors">
                <option value="90">90 Days</option>
                <option value="60">60 Days</option>
                <option value="30">30 Days</option>
              </select>
            </div>
          </div>

          {/* Log Encryption Segment Line Item */}
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

          {/* Two-Factor Authentication Line Item */}
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