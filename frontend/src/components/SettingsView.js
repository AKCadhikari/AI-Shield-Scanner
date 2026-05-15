import React from 'react';

const SettingsView = () => (
  <div className="space-y-8">
    <div className="bg-[#151921] border border-slate-800 rounded-xl p-6">
      <h3 className="text-xl font-bold text-white mb-6">Role Permissions</h3>
      <table className="w-full text-left">
        <thead>
          <tr className="text-slate-500 border-b border-slate-800">
            <th className="pb-4 font-medium">Permission</th>
            <th className="pb-4 font-medium">Admin</th>
            <th className="pb-4 font-medium">Tester</th>
            <th className="pb-4 font-medium">Viewer</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-800">
          {[
            'View Dashboard', 'Run Security Scans', 'Configure Scans', 
            'View Reports', 'Manage Users', 'Modify Settings'
          ].map((perm) => (
            <tr key={perm}>
              <td className="py-4">{perm}</td>
              <td className="py-4"><div className="w-4 h-4 rounded-full bg-green-500/20 border border-green-500 flex items-center justify-center"><div className="w-1.5 h-1.5 rounded-full bg-green-500"></div></div></td>
              <td className="py-4"><div className="w-4 h-4 rounded-full bg-green-500/20 border border-green-500 flex items-center justify-center"><div className="w-1.5 h-1.5 rounded-full bg-green-500"></div></div></td>
              <td className="py-4"><div className="w-4 h-4 rounded-full bg-slate-800 border border-slate-700"></div></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>

    <div className="bg-[#151921] border border-slate-800 rounded-xl p-6">
      <h3 className="text-xl font-bold text-white mb-6">Security Settings</h3>
      <div className="flex items-center justify-between py-4 border-b border-slate-800">
        <div>
          <p className="text-white">Two-Factor Authentication</p>
          <p className="text-xs text-slate-500">Require 2FA for all admin users</p>
        </div>
        <div className="w-12 h-6 bg-cyan-500 rounded-full relative">
          <div className="absolute right-1 top-1 w-4 h-4 bg-white rounded-full"></div>
        </div>
      </div>
    </div>
  </div>
);

export default SettingsView;