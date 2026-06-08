import React from 'react';

const MetricCard = ({ title, value, change, trend, isProgress }) => (
  <div className="bg-[#151921] p-5 md:p-6 rounded-xl border border-slate-800 flex flex-col justify-between">
    <div>
      <p className="text-slate-400 text-xs md:text-sm mb-2 font-medium">{title}</p>
      <h2 className="text-2xl md:text-3xl font-bold text-white mb-2 font-mono tracking-tight">{value}</h2>
    </div>
    {isProgress ? (
      <div className="w-full bg-slate-800 h-2 rounded-full mt-2 overflow-hidden">
        <div className="bg-cyan-500 h-full rounded-full w-[28%] shadow-[0_0_10px_#06b6d4]"></div>
      </div>
    ) : (
      <p className={`text-[11px] font-medium mt-1 ${trend === 'up' ? 'text-green-400' : 'text-red-400'}`}>
        {change} <span className="text-slate-500 font-normal">from last week</span>
      </p>
    )}
  </div>
);

const DashboardView = () => {
  const scanResults = [
    { id: 'TST-1234', category: 'Prompt Injection', status: 'Failed', severity: 'Critical', time: '2026-02-27 14:32' },
    { id: 'TST-1235', category: 'Data Leakage', status: 'Passed', severity: 'Low', time: '2026-02-27 14:28' },
    { id: 'TST-1236', category: 'Prompt Injection', status: 'Failed', severity: 'High', time: '2026-02-27 14:15' },
    { id: 'TST-1237', category: 'Data Leakage', status: 'Warning', severity: 'Medium', time: '2026-02-27 13:58' },
    { id: 'TST-1238', category: 'Prompt Injection', status: 'Passed', severity: 'Low', time: '2026-02-27 13:45' },
  ];

  return (
    <div className="space-y-6 md:space-y-8 w-full max-w-full">
      <div>
        <h1 className="text-2xl md:text-3xl font-bold text-white tracking-tight">Security Dashboard</h1>
        <p className="text-sm text-slate-500 mt-1">Monitor AI chatbot security testing results</p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6">
        <MetricCard title="Total Tests Run" value="1,247" change="+12.5%" trend="up" />
        <MetricCard title="Failed Tests" value="143" change="-8.2%" trend="down" />
        <MetricCard title="Critical Vulnerabilities" value="40" change="-15.3%" trend="down" />
        <MetricCard title="Risk Score" value="28" isProgress />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-[#151921] p-5 md:p-6 rounded-xl border border-slate-800 h-80 flex flex-col min-w-0">
          <h3 className="font-semibold mb-6 text-white text-sm md:text-base">Risk Score Trend</h3>
          <div className="flex flex-col h-full overflow-hidden flex-1">
            <div className="flex h-44 md:h-48 flex-1 min-w-0">
              <div className="flex flex-col justify-between text-[10px] text-slate-500 pr-2 pb-1 font-mono">
                <span>80</span><span>60</span><span>40</span><span>20</span><span>0</span>
              </div>
              <div className="flex-1 relative border-l border-b border-slate-800/50 min-w-0">
                <div className="absolute inset-0 flex flex-col justify-between pointer-events-none">
                  {[...Array(5)].map((_, i) => (
                    <div key={i} className="w-full border-t border-slate-800/20 border-dashed"></div>
                  ))}
                </div>
                <svg className="w-full h-full" viewBox="0 0 400 150" preserveAspectRatio="none">
                  <defs>
                    <linearGradient id="neonGradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="#06b6d4" stopOpacity="0.4" />
                      <stop offset="100%" stopColor="#06b6d4" stopOpacity="0" />
                    </linearGradient>
                  </defs>
                  <path d="M5,90 L66,75 L133,105 L200,55 L266,65 L333,95 L395,115 L395,150 L5,150 Z" fill="url(#neonGradient)" />
                  <polyline fill="none" stroke="#06b6d4" strokeWidth="3" points="5,90 66,75 133,105 200,55 266,65 333,95 395,115" />
                  {[ {x: 5, y: 90}, {x: 66, y: 75}, {x: 133, y: 105}, {x: 200, y: 55}, {x: 266, y: 65}, {x: 333, y: 95}, {x: 395, y: 115} ].map((p, i) => (
                    <g key={i}>
                      <circle cx={p.x} cy={p.y} r="4" fill="#06b6d4" />
                      <circle cx={p.x} cy={p.y} r="2" fill="#151921" />
                    </g>
                  ))}
                </svg>
              </div>
            </div>
            <div className="overflow-x-auto select-none overflow-y-hidden w-full shrink-0">
              <div className="flex justify-between text-[9px] md:text-[10px] text-slate-500 pl-7 pr-1 mt-3 min-w-70 font-mono">
                <span>Feb 20</span><span>Feb 21</span><span>Feb 22</span><span>Feb 23</span><span>Feb 24</span><span>Feb 25</span><span>Feb 26</span><span>Feb 27</span>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-[#151921] p-5 md:p-6 rounded-xl border border-slate-800 h-80 flex flex-col min-w-0">
          <h3 className="font-semibold mb-6 text-white text-sm md:text-base">Vulnerability Distribution</h3>
          <div className="flex flex-col h-full overflow-hidden flex-1">
            <div className="flex h-44 md:h-48 flex-1 min-w-0">
              <div className="flex flex-col justify-between text-[10px] text-slate-500 pr-3 pb-1 font-mono">
                <span>20</span><span>15</span><span>10</span><span>5</span><span>0</span>
              </div>
              <div className="flex-1 relative border-l border-b border-slate-800/50 flex items-end justify-around px-2 md:px-4 min-w-0">
                <div className="absolute inset-0 flex flex-col justify-between pointer-events-none">
                  {[...Array(5)].map((_, i) => (
                    <div key={i} className="w-full border-t border-slate-800/20 border-dashed"></div>
                  ))}
                </div>
                <div className="w-8 sm:w-12 bg-cyan-500/30 rounded-t h-[55%] relative group">
                  <span className="absolute -top-5 left-1/2 -translate-x-1/2 text-[9px] text-cyan-500 font-bold font-mono">11</span>
                </div>
                <div className="w-8 sm:w-12 bg-cyan-500 rounded-t h-[90%] relative group">
                  <span className="absolute -top-5 left-1/2 -translate-x-1/2 text-[9px] text-cyan-400 font-bold font-mono">18</span>
                </div>
                <div className="w-8 sm:w-12 bg-cyan-500/50 rounded-t h-[35%] relative group">
                  <span className="absolute -top-5 left-1/2 -translate-x-1/2 text-[9px] text-cyan-500 font-bold font-mono">7</span>
                </div>
                <div className="w-8 sm:w-12 bg-cyan-500/20 rounded-t h-[15%] relative group">
                  <span className="absolute -top-5 left-1/2 -translate-x-1/2 text-[9px] text-cyan-500 font-bold font-mono">3</span>
                </div>
              </div>
            </div>
            <div className="flex justify-around text-[10px] text-slate-500 pl-8 mt-3 shrink-0 font-medium">
              <span>Low</span><span>Medium</span><span>High</span><span>Critical</span>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-[#151921] rounded-xl border border-slate-800 overflow-hidden shadow-sm">
        <div className="p-5 flex justify-between items-center border-b border-slate-800/50">
          <h3 className="font-semibold text-white text-base md:text-lg">Recent Scan Results</h3>
        </div>
        <div className="overflow-x-auto w-full custom-scrollbar">
          <table className="w-full text-left border-collapse min-w-175 whitespace-nowrap">
            <thead>
              <tr className="text-slate-500 text-[10px] uppercase tracking-widest bg-slate-800/10 border-b border-slate-800/80">
                <th className="px-6 py-4 font-semibold">Test ID</th>
                <th className="px-6 py-4 font-semibold">Category</th>
                <th className="px-6 py-4 font-semibold">Status</th>
                <th className="px-6 py-4 font-semibold">Severity</th>
                <th className="px-6 py-4 font-semibold">Timestamp</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/40">
              {scanResults.map((result) => (
                <tr key={result.id} className="hover:bg-slate-800/20 transition-colors text-sm">
                  <td className="px-6 py-4 text-cyan-500 font-mono text-xs font-semibold">{result.id}</td>
                  <td className="px-6 py-4 text-slate-300 font-medium">{result.category}</td>
                  <td className="px-6 py-4">
                    <span className={`inline-block min-w-16 text-center px-2.5 py-0.5 rounded text-[10px] font-bold uppercase border tracking-wide ${
                      result.status === 'Failed' ? 'bg-red-500/10 text-red-500 border-red-500/20' : 
                      result.status === 'Warning' ? 'bg-orange-500/10 text-orange-500 border-orange-500/20' : 
                      'bg-green-500/10 text-green-500 border-green-500/20'
                    }`}>{result.status}</span>
                  </td>
                  <td className="px-6 py-4">
                     <span className={`inline-block min-w-16 text-center px-2.5 py-0.5 rounded text-[10px] font-bold uppercase tracking-wide ${
                      result.severity === 'Critical' ? 'bg-red-600/20 text-red-400' :
                      result.severity === 'High' ? 'bg-orange-600/20 text-orange-400' :
                      result.severity === 'Medium' ? 'bg-blue-600/20 text-blue-400' : 'bg-slate-700/50 text-slate-400'
                    }`}>{result.severity}</span>
                  </td>
                  <td className="px-6 py-4 text-slate-500 text-xs font-mono">{result.time}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default DashboardView;