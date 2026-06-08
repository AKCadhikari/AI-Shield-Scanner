import React, { useState, useRef, useEffect } from 'react';
import { 
  Lock, FlaskConical, FileCode2, 
  ShieldAlert, Play, Save, ChevronDown 
} from 'lucide-react';

const ScanConfigView = () => {
  const [intensity, setIntensity] = useState('Medium');
  const [toggles, setToggles] = useState({ pii: true, apiKey: true, credentials: false });
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [authMethod, setAuthMethod] = useState('None');
  const dropdownRef = useRef(null);
  
  const authOptions = ['None', 'API Key', 'Bearer Token', 'OAuth 2.0'];

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
    <div className="w-full space-y-6 md:space-y-8 pb-4 max-w-full">
      <div>
        <h1 className="text-2xl md:text-3xl font-bold text-white tracking-tight">Create New Scan</h1>
        <p className="text-sm text-slate-400 mt-1">Configure security testing for your AI chatbot</p>
      </div>

      {/* 1. CHATBOT TARGET CONFIGURATION */}
      <div className="bg-[#151921] border border-slate-800 rounded-xl p-5 md:p-8 space-y-6 shadow-sm">
        <h3 className="flex items-center gap-3 text-white font-semibold text-base md:text-lg">
          <div className="p-1.5 rounded border border-blue-500/30 bg-blue-500/10 shrink-0">
            <Lock className="text-blue-400" size={18}/>
          </div>
          Chatbot Target Configuration
        </h3>
        <div className="space-y-5">
          <div>
            <label className="block text-xs md:text-sm font-medium text-slate-200 mb-2">Chatbot API Endpoint URL</label>
            <input className="w-full bg-[#0b0e14] border border-slate-800 rounded-lg p-3 text-sm text-white placeholder-slate-500 outline-none focus:border-cyan-500 transition-colors" placeholder="https://api.example.com/v1/chat" defaultValue="https://api.example.com/v1/chat" />
            <p className="text-[11px] text-slate-500 mt-2">Enter the full URL of your chatbot API endpoint</p>
          </div>
          <div className="relative" ref={dropdownRef}>
            <label className="block text-xs md:text-sm font-medium text-slate-200 mb-2">Authentication Method</label>
            <button onClick={() => setIsDropdownOpen(!isDropdownOpen)} className={`w-full bg-[#0b0e14] border rounded-lg p-3 text-xs md:text-sm text-white flex items-center justify-between transition-all duration-200 ${isDropdownOpen ? 'border-cyan-500 ring-1 ring-cyan-500/20' : 'border-slate-800'}`}>
              <span>{authMethod}</span>
              <ChevronDown className={`text-slate-500 transition-transform duration-200 ${isDropdownOpen ? 'rotate-180' : ''}`} size={16} />
            </button>
            {isDropdownOpen && (
              <div className="absolute top-full left-0 w-full mt-2 bg-[#0b0e14] border border-slate-800 rounded-lg shadow-2xl z-100 overflow-hidden">
                {authOptions.map((option) => (
                  <div key={option} onClick={() => { setAuthMethod(option); setIsDropdownOpen(false); }} className={`px-4 py-2.5 text-xs md:text-sm cursor-pointer transition-colors ${authMethod === option ? 'bg-cyan-500 text-slate-950 font-bold' : 'text-slate-300 hover:bg-slate-800'}`}>
                    {option}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* 2. TEST PROFILE */}
      <div className="bg-[#151921] border border-slate-800 rounded-xl p-5 md:p-8 space-y-6 shadow-sm">
        <h3 className="flex items-center gap-3 text-white font-semibold text-base md:text-lg">
          <div className="p-1.5 rounded border border-emerald-500/30 bg-emerald-500/10 shrink-0">
            <FlaskConical className="text-emerald-400" size={18}/>
          </div>
          Test Profile
        </h3>
        <div className="space-y-4">
          <label className="block text-xs md:text-sm font-medium text-slate-200 mb-1">Test Categories</label>
          <div className="space-y-3">
            {['Prompt Injection Testing', 'Data Leakage Testing', 'Social Engineering Tests'].map((test, index) => (
              <label key={test} className="flex items-start justify-between p-4 md:p-5 bg-[#0b0e14] rounded-xl border border-slate-800 cursor-pointer hover:border-slate-700 transition-colors gap-3">
                <div className="min-w-0">
                  <p className="text-sm font-semibold text-white truncate">{test}</p>
                  <p className="text-xs text-slate-500 mt-1 leading-normal">
                    {index === 0 && 'Test for malicious prompt injections'}
                    {index === 1 && 'Detect potential data exposure vulnerabilities'}
                    {index === 2 && 'Test resistance to social engineering attacks'}
                  </p>
                </div>
                <input type="checkbox" className="w-5 h-5 mt-0.5 rounded bg-slate-800 border-slate-700 accent-cyan-500 cursor-pointer shrink-0" defaultChecked={index !== 2} />
              </label>
            ))}
          </div>
        </div>
        <div className="space-y-2">
          <label className="block text-xs md:text-sm font-medium text-slate-200 mb-2">Test Intensity</label>
          <div className="flex gap-3 md:gap-4">
            {['Low', 'Medium', 'High'].map(lvl => (
              <button key={lvl} onClick={() => setIntensity(lvl)} className={`flex-1 py-3 rounded-xl border text-xs md:text-sm font-semibold transition-all duration-200 ${intensity === lvl ? 'bg-cyan-500 border-cyan-500 text-slate-950 shadow-[0_0_15px_rgba(6,182,212,0.3)]' : 'bg-[#0b0e14] border-slate-800 text-slate-300 hover:border-slate-600'}`}>
                {lvl}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* 3. CUSTOM PROMPTS */}
      <div className="bg-[#151921] border border-slate-800 rounded-xl p-5 md:p-8 space-y-4 shadow-sm">
        <h3 className="flex items-center gap-3 text-white font-semibold text-base md:text-lg">
          <div className="p-1.5 rounded border border-purple-500/30 bg-purple-500/10 shrink-0">
            <FileCode2 className="text-purple-400" size={18}/>
          </div>
          Custom Test Prompts
        </h3>
        <textarea className="w-full bg-[#0b0e14] border border-slate-800 rounded-xl p-4 text-xs md:text-sm text-white placeholder-slate-600 outline-none h-36 resize-none custom-scrollbar" placeholder="Enter custom test prompts, one per line..." />
      </div>

      {/* 4. DETECTION RULES */}
      <div className="bg-[#151921] border border-slate-800 rounded-xl p-5 md:p-8 space-y-4 shadow-sm">
        <h3 className="flex items-center gap-3 text-white font-semibold text-base md:text-lg">
          <div className="p-1.5 rounded border border-orange-500/30 bg-amber-500/10 shrink-0">
            <ShieldAlert className="text-orange-400" size={18}/>
          </div>
          Detection Rules
        </h3>
        <div className="flex flex-col">
          {Object.entries({
            pii: ['PII Detection', 'Detect personally identifiable information in responses'],
            apiKey: ['API Key Detection', 'Identify exposed API keys or tokens'],
            credentials: ['Credential Detection', 'Detect leaked usernames, passwords, or secrets']
          }).map(([key, [label, sub]], index, arr) => (
            <div key={key} className={`flex items-center justify-between py-4 gap-4 ${index !== arr.length - 1 ? 'border-b border-slate-800/60' : ''}`}>
              <div className="min-w-0">
                <p className="text-sm font-semibold text-white truncate">{label}</p>
                <p className="text-xs text-slate-500 mt-1 leading-normal">{sub}</p>
              </div>
              <button onClick={() => setToggles({...toggles, [key]: !toggles[key]})} className={`w-12 h-6 rounded-full relative transition-colors duration-200 shrink-0 ${toggles[key] ? 'bg-cyan-500' : 'bg-[#0b0e14] border border-slate-700'}`}>
                <div className={`absolute top-0.5 left-0.5 w-5 h-5 rounded-full bg-white transition-transform duration-200 ${toggles[key] ? 'translate-x-6' : 'translate-x-0'}`} />
              </button>
            </div>
          ))}
        </div>
      </div>

      <div className="flex flex-col sm:flex-row gap-4 pt-2 w-full">
        <button className="w-full sm:flex-1 flex items-center justify-center gap-2 bg-cyan-500 hover:bg-cyan-400 text-slate-900 font-bold py-3.5 md:py-4 px-6 rounded-xl transition-colors text-sm md:text-base">
          <Play size={18} fill="currentColor" /> Start Scan
        </button>
        <button className="w-full sm:flex-1 flex items-center justify-center gap-2 bg-[#151921] hover:bg-slate-800 border border-slate-700 text-white font-medium py-3.5 md:py-4 px-6 rounded-xl transition-colors text-sm md:text-base">
          <Save size={18} /> Save Configuration
        </button>
      </div>
    </div>
  );
};

export default ScanConfigView;