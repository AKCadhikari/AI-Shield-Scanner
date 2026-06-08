import React, { useState } from 'react';
import { Download, ChevronDown, SlidersHorizontal, ChevronRight } from 'lucide-react';

const ReportsView = () => {
  const [selectedConfig, setSelectedConfig] = useState('TST-2026-01');
  const [activeFilter, setActiveFilter] = useState('all');

  const reportRecords = [
    { id: 'TST-1234', category: 'Prompt Injection', status: 'Failed', severity: 'Critical', score: 95, colorClass: 'bg-red-500' },
    { id: 'TST-1235', category: 'Prompt Injection', status: 'Failed', severity: 'Critical', score: 95, colorClass: 'bg-red-500' },
    { id: 'TST-1236', category: 'Data Leakage', status: 'Warning', severity: 'Medium', score: 45, colorClass: 'bg-orange-500' },
    { id: 'TST-1237', category: 'Data Leakage', status: 'Warning', severity: 'Medium', score: 45, colorClass: 'bg-orange-500' },
    { id: 'TST-1238', category: 'Data Leakage', status: 'Warning', severity: 'Medium', score: 45, colorClass: 'bg-orange-500' },
    { id: 'TST-1240', category: 'Data Leakage', status: 'Warning', severity: 'Medium', score: 45, colorClass: 'bg-orange-500' },
  ];

  // FIXED: Restored the missing severity filters definition array here
  const filters = ['all', 'Critical', 'High', 'Medium', 'Low'];

  return (
    <div className="w-full flex-1 flex flex-col space-y-6 text-slate-300 font-sans overflow-hidden h-full max-h-full max-w-full">
      
      {/* HEADER SECTION ROW */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 shrink-0">
        <div>
          <h1 className="text-2xl md:text-3xl font-bold text-white tracking-tight">Scan Results</h1>
          <p className="text-xs md:text-sm text-slate-400 mt-0.5">Detailed analysis of security test results</p>
        </div>
        <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 w-full sm:w-auto">
          <div className="relative w-full sm:w-auto">
            <select value={selectedConfig} onChange={(e) => setSelectedConfig(e.target.value)} className="w-full sm:w-auto bg-[#1a1f29] border border-slate-800 text-slate-300 text-xs md:text-sm rounded-lg pl-4 pr-10 py-2.5 outline-none appearance-none cursor-pointer">
              <option value="TST-2026-01">TST-2026-001</option>
              <option value="TST-2026-02">TST-2026-002</option>
            </select>
            <ChevronDown className="absolute right-3 top-3 text-slate-400 pointer-events-none" size={14} />
          </div>
          <button className="flex items-center justify-center gap-2 bg-cyan-500 hover:bg-cyan-400 text-slate-900 font-bold text-xs md:text-sm px-4 py-2.5 rounded-lg transition-colors shadow-sm whitespace-nowrap">
            <Download size={15} /> Export Report
          </button>
        </div>
      </div>

      {/* SCALED METRICS PANELS ROW COMPACT STACK */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 shrink-0">
        {[["Total Tests", "5", "text-white"], ["Passed", "2", "text-emerald-500"], ["Failed", "2", "text-red-500"], ["Risk Score", "48", "text-amber-500"]].map(([lbl, val, col]) => (
          <div key={lbl} className="bg-[#151921] border border-slate-800/80 rounded-xl p-4 md:p-5 flex flex-col justify-between h-28 md:h-32 transition-all hover:border-slate-700/50">
            <span className="text-slate-400 text-[10px] md:text-xs font-semibold tracking-wide uppercase">{lbl}</span>
            <span className={`text-2xl md:text-4xl font-bold font-mono leading-none ${col}`}>{val}</span>
          </div>
        ))}
      </div>

      {/* FILTER CONTROL BAR SYSTEM */}
      <div className="bg-[#151921] border border-slate-800/80 rounded-xl px-4 md:px-6 py-3 md:py-4 flex items-center gap-3 md:gap-4 shrink-0 overflow-x-auto custom-scrollbar max-w-full">
        <div className="flex items-center gap-2 text-slate-400 text-xs font-semibold whitespace-nowrap shrink-0">
          <SlidersHorizontal size={14} /> Filter severity:
        </div>
        <div className="flex gap-2 shrink-0">
          {filters.map((filter) => (
            <button key={filter} onClick={() => setActiveFilter(filter)} className={`px-3 py-1 rounded-lg text-xs font-medium transition-all ${activeFilter === filter ? 'bg-cyan-500 text-slate-950 font-bold shadow-md' : 'bg-[#1a1f29] hover:bg-slate-800 text-slate-400'}`}>
              {filter}
            </button>
          ))}
        </div>
      </div>

      {/* CORE STATS DATA MATRIX BOARD GRID TABLE */}
      <div className="bg-[#151921] border border-slate-800/80 rounded-xl shadow-sm max-w-full overflow-x-auto overflow-y-hidden flex flex-col flex-1 min-h-0 custom-scrollbar">
        <div className="w-full flex flex-col flex-1 min-h-0 min-w-200">
          
          {/* STABLE UPPER HEADER ROW LABEL COLUMNS */}
          <table className="w-full text-left border-collapse table-fixed shrink-0">
            <thead>
              <tr className="text-slate-400 text-xs font-semibold border-b border-slate-800/60 bg-[#151921]">
                <th className="w-12 py-4 pl-6 bg-[#151921]"></th>
                <th className="py-4 px-4 font-semibold bg-[#151921] w-[15%]">Test ID</th>
                <th className="py-4 px-4 font-semibold bg-[#151921] w-[35%]">Category</th>
                <th className="py-4 px-4 font-semibold text-center bg-[#151921] w-[15%]">Status</th>
                <th className="py-4 px-4 font-semibold text-center bg-[#151921] w-[15%]">Severity</th>
                <th className="py-4 pr-6 pl-4 font-semibold bg-[#151921] w-[20%]">Risk Score</th>
              </tr>
            </thead>
          </table>

          {/* INNER SCROLL LOG ENTRIES DATA STREAM GRID */}
          <div className="overflow-y-auto custom-scrollbar flex-1 min-h-0 w-full">
            <table className="w-full text-left border-collapse table-fixed">
              <tbody className="divide-y divide-slate-800/30">
                {reportRecords.map((record, index) => (
                  <tr key={`${record.id}-${index}`} className="hover:bg-slate-800/10 transition-colors group">
                    <td className="w-12 py-4 pl-6 text-slate-600 group-hover:text-slate-400 cursor-pointer transition-colors"><ChevronRight size={16} /></td>
                    <td className="py-4 px-4 text-xs md:text-sm font-mono text-cyan-500 font-semibold cursor-pointer hover:underline w-[15%] truncate">{record.id}</td>
                    <td className="py-4 px-4 text-xs md:text-sm font-semibold text-slate-200 w-[35%] truncate">{record.category}</td>
                    <td className="py-4 px-4 text-center w-[15%]">
                      <span className={`inline-block min-w-16 text-center px-2.5 py-0.5 rounded text-[10px] font-bold uppercase border ${record.status === 'Failed' ? 'bg-red-500/10 text-red-500 border-red-500/20' : 'bg-amber-500/10 text-amber-500 border-amber-500/20'}`}>{record.status}</span>
                    </td>
                    <td className="py-4 px-4 text-center w-[15%]">
                      <span className={`inline-block min-w-16 text-center px-2.5 py-0.5 rounded text-[10px] font-bold uppercase ${record.severity === 'Critical' ? 'bg-red-600/20 text-red-400' : 'bg-blue-600/20 text-blue-400'}`}>{record.severity}</span>
                    </td>
                    <td className="py-4 pr-6 pl-4 w-[20%]">
                      <div className="flex items-center gap-3">
                        <span className="text-xs md:text-sm font-bold font-mono text-white min-w-5 text-right">{record.score}</span>
                        <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden max-w-30">
                          <div className={`h-full rounded-full ${record.colorClass}`} style={{ width: `${record.score}%` }} />
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
    </div>
  );
};

export default ReportsView;