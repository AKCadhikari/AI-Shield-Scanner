import React, { useState } from 'react';
import { 
  Download, 
  ChevronDown, 
  SlidersHorizontal, 
  ChevronRight 
} from 'lucide-react';

const ReportsView = () => {
  // State for handling dropdown configuration selection
  const [selectedConfig, setSelectedConfig] = useState('TST-2026-01');
  const [activeFilter, setActiveFilter] = useState('all');

  // Hardcoded mockup data matching image_0ac43e.png exactly
  const reportRecords = [
    { id: 'TST-1234', category: 'Prompt Injection', status: 'Failed', severity: 'Critical', score: 95, colorClass: 'bg-red-500' },
    { id: 'TST-1235', category: 'Data Leakage', status: 'Warning', severity: 'Medium', score: 45, colorClass: 'bg-orange-500' },
    { id: 'TST-1236', category: 'Prompt Injection', status: 'Passed', severity: 'Low', score: 5, colorClass: 'bg-emerald-500' },
    { id: 'TST-1237', category: 'Data Leakage', status: 'Failed', severity: 'Critical', score: 98, colorClass: 'bg-red-500' },
    { id: 'TST-1238', category: 'Social Engineering', status: 'Passed', severity: 'Low', score: 10, colorClass: 'bg-emerald-500' },
  ];

  const filters = ['all', 'Critical', 'High', 'Medium', 'Low'];

  return (
    <div className="w-full space-y-6 pb-4 text-slate-300 font-sans">
      
      {/* HEADER ROW */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold text-white mb-1">Scan Results</h1>
          <p className="text-sm text-slate-400">Detailed analysis of security test results</p>
        </div>
        
        {/* Actions Container */}
        <div className="flex items-center gap-3 w-full sm:w-auto">
          {/* Configuration Selection Dropdown */}
          <div className="relative">
            <select 
              value={selectedConfig}
              onChange={(e) => setSelectedConfig(e.target.value)}
              className="bg-[#1a1f29] border border-slate-800 text-slate-300 text-sm rounded-lg pl-4 pr-10 py-2.5 outline-none appearance-none cursor-pointer focus:border-slate-700 transition-colors"
            >
              <option value="TST-2026-01">TST-2026-001</option>
              <option value="TST-2026-02">TST-2026-002</option>
            </select>
            <ChevronDown className="absolute right-3 top-3 text-slate-400 pointer-events-none" size={16} />
          </div>

          {/* Export Report Action Button */}
          <button className="flex items-center gap-2 bg-cyan-500 hover:bg-cyan-400 text-slate-900 font-semibold text-sm px-4 py-2.5 rounded-lg transition-colors shadow-sm">
            <Download size={16} />
            Export Report
          </button>
        </div>
      </div>

      {/* KPI METRICS AND VISUALIZATION ROW */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {/* Metric 1: Total Tests */}
        <div className="bg-[#151921] border border-slate-800/80 rounded-xl p-6 flex flex-col justify-between h-44">
          <span className="text-slate-400 text-xs font-medium tracking-wide">Total Tests</span>
          <span className="text-4xl font-semibold text-white tracking-tight">5</span>
          <div></div>
        </div>

        {/* Metric 2: Passed */}
        <div className="bg-[#151921] border border-slate-800/80 rounded-xl p-6 flex flex-col justify-between h-44">
          <span className="text-slate-400 text-xs font-medium tracking-wide">Passed</span>
          <span className="text-4xl font-semibold text-emerald-500 tracking-tight">2</span>
          <div></div>
        </div>

        {/* Metric 3: Failed */}
        <div className="bg-[#151921] border border-slate-800/80 rounded-xl p-6 flex flex-col justify-between h-44">
          <span className="text-slate-400 text-xs font-medium tracking-wide">Failed</span>
          <span className="text-4xl font-semibold text-red-500 tracking-tight">2</span>
          <div></div>
        </div>

        {/* Metric 4: Risk Score Radial mock */}
        <div className="bg-[#151921] border border-slate-800/80 rounded-xl p-6 flex flex-col justify-between items-center h-44 relative">
          <span className="text-slate-400 text-xs font-medium tracking-wide self-start">Overall Risk Score</span>
          
          {/* Custom SVG Donut Chart Mockup */}
          <div className="relative w-24 h-24 flex items-center justify-center">
            <svg className="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
              {/* Background circle */}
              <circle cx="18" cy="18" r="15.915" fill="transparent" stroke="#1f293d" strokeWidth="3.5" />
              {/* Emerald/Passed Segment */}
              <circle cx="18" cy="18" r="15.915" fill="transparent" stroke="#10b981" strokeWidth="3.5" strokeDasharray="40 100" strokeDashoffset="0" />
              {/* Orange/Warning Segment */}
              <circle cx="18" cy="18" r="15.915" fill="transparent" stroke="#f97316" strokeWidth="3.5" strokeDasharray="20 100" strokeDashoffset="-40" />
              {/* Red/Failed Segment */}
              <circle cx="18" cy="18" r="15.915" fill="transparent" stroke="#ef4444" strokeWidth="3.5" strokeDasharray="40 100" strokeDashoffset="-60" />
            </svg>
            <div className="absolute flex flex-col items-center justify-center text-center">
              <span className="text-xl font-bold text-amber-500 leading-none">48</span>
              <span className="text-[9px] text-slate-500 mt-0.5">Risk Score</span>
            </div>
          </div>
          <div></div>
        </div>
      </div>

      {/* FILTER CONTROL BAR */}
      <div className="bg-[#151921] border border-slate-800/80 rounded-xl px-6 py-4 flex items-center gap-4">
        <div className="flex items-center gap-2 text-slate-400 text-xs font-medium">
          <SlidersHorizontal size={14} />
          Filter by severity:
        </div>
        <div className="flex flex-wrap gap-2">
          {filters.map((filter) => (
            <button
              key={filter}
              onClick={() => setActiveFilter(filter)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium capitalize transition-all ${
                activeFilter === filter
                  ? 'bg-cyan-500 text-slate-950 font-semibold'
                  : 'bg-[#1a1f29] hover:bg-slate-800 text-slate-400 hover:text-slate-200'
              }`}
            >
              {filter}
            </button>
          ))}
        </div>
      </div>

      {/* DETAILED RESULTS TABLE CONTAINER */}
      <div className="bg-[#151921] border border-slate-800/80 rounded-xl overflow-hidden shadow-sm">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse min-w-175">
            <thead>
              <tr className="text-slate-400 text-xs font-medium border-b border-slate-800/60 bg-slate-800/10">
                <th className="w-12 py-4 pl-6"></th>
                <th className="py-4 px-4 font-medium">Test ID</th>
                <th className="py-4 px-4 font-medium">Category</th>
                <th className="py-4 px-4 font-medium text-center">Status</th>
                <th className="py-4 px-4 font-medium text-center">Severity</th>
                <th className="py-4 pr-6 pl-4 font-medium">Risk Score</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/40">
              {reportRecords.map((record) => (
                <tr key={record.id} className="hover:bg-slate-800/10 transition-colors group">
                  {/* Chevron Expander */}
                  <td className="py-4 pl-6 text-slate-600 group-hover:text-slate-400 cursor-pointer transition-colors">
                    <ChevronRight size={16} />
                  </td>
                  
                  {/* Test ID */}
                  <td className="py-4 px-4 text-sm font-mono text-cyan-500 cursor-pointer hover:underline">
                    {record.id}
                  </td>
                  
                  {/* Category */}
                  <td className="py-4 px-4 text-sm font-medium text-slate-200">
                    {record.category}
                  </td>
                  
                  {/* Status Badge */}
                  <td className="py-4 px-4 text-center">
                    <span className={`inline-block min-w-16 px-2.5 py-1 rounded text-[10px] font-bold uppercase border tracking-wider ${
                      record.status === 'Failed' ? 'bg-red-500/10 text-red-500 border-red-500/20' :
                      record.status === 'Warning' ? 'bg-amber-500/10 text-amber-500 border-amber-500/20' :
                      'bg-emerald-500/10 text-emerald-500 border-emerald-500/20'
                    }`}>
                      {record.status}
                    </span>
                  </td>
                  
                  {/* Severity Badge */}
                  <td className="py-4 px-4 text-center">
                    <span className={`inline-block min-w-16 px-2.5 py-1 rounded text-[10px] font-bold uppercase tracking-wider ${
                      record.severity === 'Critical' ? 'bg-red-600/20 text-red-400' :
                      record.severity === 'Medium' ? 'bg-blue-600/20 text-blue-400' :
                      'bg-emerald-600/20 text-emerald-400'
                    }`}>
                      {record.severity}
                    </span>
                  </td>
                  
                  {/* Risk Score Progress Row */}
                  <td className="py-4 pr-6 pl-4">
                    <div className="flex items-center gap-3">
                      <span className="text-sm font-semibold font-mono text-white min-w-5 text-right">
                        {record.score}
                      </span>
                      <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden max-w-30">
                        <div 
                          className={`h-full rounded-full ${record.colorClass}`} 
                          style={{ width: `${record.score}%` }}
                        ></div>
                      </div>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
};

export default ReportsView;