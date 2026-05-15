import React from 'react';

const MetricCard = ({ title, value, change, trend, isProgress }) => (
  <div className="bg-[#151921] p-6 rounded-xl border border-slate-800">
    <p className="text-slate-400 text-sm mb-2">{title}</p>
    <h2 className="text-3xl font-bold text-white mb-2">{value}</h2>
    {isProgress ? (
      <div className="w-full bg-slate-800 h-2 rounded-full mt-4 overflow-hidden">
        <div className="bg-cyan-500 h-full rounded-full w-[28%] shadow-[0_0_10px_#06b6d4]"></div>
      </div>
    ) : (
      <p className={`text-xs ${trend === 'up' ? 'text-green-400' : 'text-red-400'}`}>
        {change} from last week
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
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-white">Security Dashboard</h1>
        <p className="text-slate-500 mt-1">Monitor AI chatbot security testing results</p>
      </div>

      <div className="grid grid-cols-4 gap-6">
        <MetricCard title="Total Tests Run" value="1,247" change="+12.5%" trend="up" />
        <MetricCard title="Failed Tests" value="143" change="-8.2%" trend="down" />
        <MetricCard title="Critical Vulnerabilities" value="40" change="-15.3%" trend="down" />
        <MetricCard title="Risk Score" value="28" isProgress />
      </div>

      <div className="grid grid-cols-2 gap-6">
        
        {/* Risk Score Trend */}
        <div className="bg-[#151921] p-6 rounded-xl border border-slate-800 h-80 flex flex-col">
          <h3 className="font-semibold mb-6 text-white">Risk Score Trend</h3>
          <div className="flex flex-col h-full overflow-hidden">
            <div className="flex h-48">
              {/* Y-Axis */}
              <div className="flex flex-col justify-between text-[10px] text-slate-500 pr-3 pb-1">
                <span>80</span><span>60</span><span>40</span><span>20</span><span>0</span>
              </div>
              
              <div className="flex-1 relative border-l border-b border-slate-800/50">
                {/* Dashed Grid Lines */}
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
                    <filter id="lineGlow" x="-20%" y="-20%" width="140%" height="140%">
                      <feGaussianBlur stdDeviation="3" result="blur" />
                      <feComposite in="SourceGraphic" in2="blur" operator="over" />
                    </filter>
                  </defs>
                  <path d="M5,90 L66,75 L133,105 L200,55 L266,65 L333,95 L395,115 L395,150 L5,150 Z" fill="url(#neonGradient)" />
                  <polyline fill="none" stroke="#06b6d4" strokeWidth="3" points="5,90 66,75 133,105 200,55 266,65 333,95 395,115" filter="url(#lineGlow)" />
                  {/* High Detail Data Points */}
                  {[ {x: 5, y: 90}, {x: 66, y: 75}, {x: 133, y: 105}, {x: 200, y: 55}, {x: 266, y: 65}, {x: 333, y: 95}, {x: 395, y: 115} ].map((p, i) => (
                    <g key={i}>
                      <circle cx={p.x} cy={p.y} r="5" fill="#06b6d4" />
                      <circle cx={p.x} cy={p.y} r="3" fill="#151921" />
                    </g>
                  ))}
                </svg>
              </div>
            </div>
            <div className="flex justify-between text-[10px] text-slate-500 pl-8 pr-1 mt-4">
              <span>Feb 20</span><span>Feb 21</span><span>Feb 22</span><span>Feb 23</span><span>Feb 24</span><span>Feb 25</span><span>Feb 26</span><span>Feb 27</span>
            </div>
          </div>
        </div>

        {/* Vulnerability Distribution */}
        <div className="bg-[#151921] p-6 rounded-xl border border-slate-800 h-80 flex flex-col">
          <h3 className="font-semibold mb-6 text-white">Vulnerability Distribution</h3>
          <div className="flex flex-col h-full overflow-hidden">
            <div className="flex h-48">
              <div className="flex flex-col justify-between text-[10px] text-slate-500 pr-4 pb-1">
                <span>20</span><span>15</span><span>10</span><span>5</span><span>0</span>
              </div>

              <div className="flex-1 relative border-l border-b border-slate-800/50 flex items-end justify-around px-4">
                <div className="absolute inset-0 flex flex-col justify-between pointer-events-none">
                  {[...Array(5)].map((_, i) => (
                    <div key={i} className="w-full border-t border-slate-800/20 border-dashed"></div>
                  ))}
                </div>
                {/* Bars - Adjusted to w-12 for better visual balance */}
                <div className="w-35 bg-cyan-500/30 rounded-t h-[55%] z-10 transition-all hover:bg-cyan-500/50 relative group">
                    <span className="absolute -top-6 left-1/2 -translate-x-1/2 text-[10px] text-cyan-500 opacity-0 group-hover:opacity-100 font-bold">11</span>
                </div>
                <div className="w-35 bg-cyan-500 rounded-t h-[90%] z-10 transition-all hover:bg-cyan-400 relative group">
                    <span className="absolute -top-6 left-1/2 -translate-x-1/2 text-[10px] text-cyan-500 opacity-0 group-hover:opacity-100 font-bold">18</span>
                </div>
                <div className="w-35 bg-cyan-500/50 rounded-t h-[35%] z-10 transition-all hover:bg-cyan-500/70 relative group">
                    <span className="absolute -top-6 left-1/2 -translate-x-1/2 text-[10px] text-cyan-500 opacity-0 group-hover:opacity-100 font-bold">7</span>
                </div>
                <div className="w-35 bg-cyan-500/20 rounded-t h-[15%] z-10 transition-all hover:bg-cyan-500/40 relative group">
                    <span className="absolute -top-6 left-1/2 -translate-x-1/2 text-[10px] text-cyan-500 opacity-0 group-hover:opacity-100 font-bold">3</span>
                </div>
              </div>
            </div>
            <div className="flex justify-around text-[10px] text-slate-500 pl-10 mt-4">
              <span>Low</span><span>Medium</span><span>High</span><span>Critical</span>
            </div>
          </div>
        </div>
      </div>

      {/* Table Section */}
      <div className="bg-[#151921] rounded-xl border border-slate-800 overflow-hidden">
        <div className="p-6 flex justify-between items-center border-b border-slate-800/50">
          <h3 className="font-semibold text-white text-lg">Recent Scan Results</h3>
          <button className="text-cyan-500 text-sm font-medium hover:text-cyan-400">View All</button>
        </div>
        <table className="w-full text-left">
          <thead>
            <tr className="text-slate-500 text-[10px] uppercase tracking-widest bg-slate-800/10 border-b border-slate-800">
              <th className="px-6 py-4 font-semibold">Test ID</th>
              <th className="px-6 py-4 font-semibold">Category</th>
              <th className="px-6 py-4 font-semibold">Status</th>
              <th className="px-6 py-4 font-semibold">Severity</th>
              <th className="px-6 py-4 font-semibold">Timestamp</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/50">
            {scanResults.map((result) => (
              <tr key={result.id} className="hover:bg-slate-800/30 transition-colors text-sm">
                <td className="px-6 py-4 text-cyan-500 font-mono text-xs">{result.id}</td>
                <td className="px-6 py-4 text-slate-300">{result.category}</td>
                <td className="px-6 py-4">
                  <span className={`px-2.5 py-0.5 rounded text-[10px] font-bold uppercase border ${
                    result.status === 'Failed' ? 'bg-red-500/10 text-red-500 border-red-500/20' : 
                    result.status === 'Warning' ? 'bg-orange-500/10 text-orange-500 border-orange-500/20' : 
                    'bg-green-500/10 text-green-500 border-green-500/20'
                  }`}>
                    {result.status}
                  </span>
                </td>
                <td className="px-6 py-4">
                   <span className={`px-2.5 py-0.5 rounded text-[10px] font-bold uppercase ${
                    result.severity === 'Critical' ? 'bg-red-600/20 text-red-400' :
                    result.severity === 'High' ? 'bg-orange-600/20 text-orange-400' :
                    result.severity === 'Medium' ? 'bg-blue-600/20 text-blue-400' :
                    'bg-slate-700/50 text-slate-400'
                  }`}>
                    {result.severity}
                  </span>
                </td>
                <td className="px-6 py-4 text-slate-500 text-xs">{result.time}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default DashboardView;