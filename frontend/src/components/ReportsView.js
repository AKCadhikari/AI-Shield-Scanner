import React, { useState } from 'react';
import { 
  Download, 
  ChevronDown, 
  SlidersHorizontal, 
  ChevronRight 
} from 'lucide-react';

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
    { id: 'TST-1241', category: 'Data Leakage', status: 'Warning', severity: 'Medium', score: 45, colorClass: 'bg-orange-500' },
    { id: 'TST-1242', category: 'Data Leakage', status: 'Warning', severity: 'Medium', score: 45, colorClass: 'bg-orange-500' },
    { id: 'TST-1243', category: 'Data Leakage', status: 'Warning', severity: 'Medium', score: 45, colorClass: 'bg-orange-500' },
    { id: 'TST-1244', category: 'Data Leakage', status: 'Warning', severity: 'Medium', score: 45, colorClass: 'bg-orange-500' },
  ];

  const filters = ['all', 'Critical', 'High', 'Medium', 'Low'];

  return (
    <div className="w-full flex-1 flex flex-col space-y-6 text-slate-300 font-sans overflow-hidden max-h-full">
      
      {/* HEADER ROW */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 shrink-0">
        <div>
          <h1 className="text-3xl font-bold text-white mb-1">Scan Results</h1>
          <p className="text-sm text-slate-400">Detailed analysis of security test results</p>
        </div>
        
        <div className="flex items-center gap-3 w-full sm:w-auto">
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

          <button className="flex items-center gap-2 bg-cyan-500 hover:bg-cyan-400 text-slate-900 font-semibold text-sm px-4 py-2.5 rounded-lg transition-colors shadow-sm">
            <Download size={16} />
            Export Report
          </button>
        </div>
      </div>

      {/* COMPACT METRICS SECTION CARDS */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 shrink-0">
        <div className="bg-[#151921] border border-slate-800/80 rounded-xl p-5 flex flex-col justify-between h-36 transition-all hover:border-slate-700/50">
          <span className="text-slate-400 text-xs font-semibold tracking-wide uppercase">Total Tests</span>
          <span className="text-4xl font-bold text-white tracking-tight leading-none mb-1">5</span>
        </div>

        <div className="bg-[#151921] border border-slate-800/80 rounded-xl p-5 flex flex-col justify-between h-36 transition-all hover:border-slate-700/50">
          <span className="text-slate-400 text-xs font-semibold tracking-wide uppercase">Passed</span>
          <span className="text-4xl font-bold text-emerald-500 tracking-tight leading-none mb-1">2</span>
        </div>

        <div className="bg-[#151921] border border-slate-800/80 rounded-xl p-5 flex flex-col justify-between h-36 transition-all hover:border-slate-700/50">
          <span className="text-slate-400 text-xs font-semibold tracking-wide uppercase">Failed</span>
          <span className="text-4xl font-bold text-red-500 tracking-tight leading-none mb-1">2</span>
        </div>

        <div className="bg-[#151921] border border-slate-800/80 rounded-xl p-5 flex flex-col justify-between h-36 transition-all hover:border-slate-700/50">
          <span className="text-slate-400 text-xs font-semibold tracking-wide uppercase">Overall Risk Score</span>
          <span className="text-4xl font-bold text-amber-500 tracking-tight leading-none mb-1">48</span>
        </div>
      </div>

      {/* FILTER CONTROL BAR */}
      <div className="bg-[#151921] border border-slate-800/80 rounded-xl px-6 py-4 flex items-center gap-4 shrink-0">
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
                  ? 'bg-cyan-500 text-slate-950 font-semibold shadow-md shadow-cyan-500/10'
                  : 'bg-[#1a1f29] hover:bg-slate-800 text-slate-400 hover:text-slate-200'
              }`}
            >
              {filter}
            </button>
          ))}
        </div>
      </div>

      {/* DETAILED RESULTS TABLE CONTAINER */}
      <div className="bg-[#151921] border border-slate-800/80 rounded-xl shadow-sm max-w-full overflow-x-auto overflow-y-hidden flex flex-col flex-1 min-h-0">
        
        {/* Table layout wrapper with absolute control over width formatting */}
        <div className="w-full flex flex-col flex-1 min-h-0 min-w-212.5">
          
          {/* FIXED HEADER SEGMENT - Pinned firmly outside of the scroll layer context */}
          <table className="w-full text-left border-collapse table-fixed shrink-0">
            <thead>
              <tr className="text-slate-400 text-xs font-medium border-b border-slate-800/60 bg-[#151921]">
                <th className="w-12 py-4 pl-6 bg-[#151921]"></th>
                <th className="py-4 px-4 font-medium bg-[#151921] w-[15%]">Test ID</th>
                <th className="py-4 px-4 font-medium bg-[#151921] w-[35%]">Category</th>
                <th className="py-4 px-4 font-medium text-center bg-[#151921] w-[15%]">Status</th>
                <th className="py-4 px-4 font-medium text-center bg-[#151921] w-[15%]">Severity</th>
                <th className="py-4 pr-6 pl-4 font-medium bg-[#151921] w-[20%]">Risk Score</th>
              </tr>
            </thead>
          </table>

          {/* INTERNAL DATA INNER LAYER CONTAINER - Vertically scrolls right below the fixed topic columns */}
          <div className="overflow-y-auto custom-scrollbar flex-1 min-h-0 w-full">
            <table className="w-full text-left border-collapse table-fixed">
              <tbody className="divide-y divide-slate-800/40">
                {reportRecords.map((record, index) => (
                  <tr key={`${record.id}-${index}`} className="hover:bg-slate-800/10 transition-colors group">
                    <td className="w-12 py-4 pl-6 text-slate-600 group-hover:text-slate-400 cursor-pointer transition-colors">
                      <ChevronRight size={16} />
                    </td>
                    <td className="py-4 px-4 text-sm font-mono text-cyan-500 cursor-pointer hover:underline w-[15%] truncate">
                      {record.id}
                    </td>
                    <td className="py-4 px-4 text-sm font-medium text-slate-200 w-[35%] truncate">
                      {record.category}
                    </td>
                    <td className="py-4 px-4 text-center w-[15%]">
                      <span className={`inline-block min-w-16 px-2.5 py-1 rounded text-[10px] font-bold uppercase border tracking-wider ${
                        record.status === 'Failed' ? 'bg-red-500/10 text-red-500 border-red-500/20' :
                        record.status === 'Warning' ? 'bg-amber-500/10 text-amber-500 border-amber-500/20' :
                        'bg-emerald-500/10 text-emerald-500 border-emerald-500/20'
                      }`}>{record.status}</span>
                    </td>
                    <td className="py-4 px-4 text-center w-[15%]">
                      <span className={`inline-block min-w-16 px-2.5 py-1 rounded text-[10px] font-bold uppercase tracking-wider ${
                        record.severity === 'Critical' ? 'bg-red-600/20 text-red-400' :
                        record.severity === 'Medium' ? 'bg-blue-600/20 text-blue-400' :
                        'bg-emerald-600/20 text-emerald-400'
                      }`}>{record.severity}</span>
                    </td>
                    <td className="py-4 pr-6 pl-4 w-[20%]">
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

    </div>
  );
};

export default ReportsView;