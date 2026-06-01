import reflex as rx

def metric_card(title: str, value: str, change: str = "", trend: str = "up", is_progress: bool = False) -> rx.Component:
    """Generates standalone informational summary metric cards."""
    return rx.el.div(
        rx.text(title, class_name="text-slate-400 text-sm mb-2"),
        rx.heading(value, class_name="text-3xl font-bold text-white mb-2"),
        rx.cond(
            is_progress,
            rx.el.div(
                rx.el.div(class_name="bg-cyan-500 h-full rounded-full w-[28%] shadow-[0_0_10px_#06b6d4]"),
                class_name="w-full bg-slate-800 h-2 rounded-full mt-4 overflow-hidden"
            ),
            rx.text(
                f"{change} from last week",
                class_name=rx.cond(trend == "up", "text-xs text-green-400", "text-xs text-red-400")
            )
        ),
        class_name="bg-[#151921] p-6 rounded-xl border border-slate-800 w-full flex flex-col justify-between"
    )

def table_row(test_id: str, category: str, status: str, severity: str, timestamp: str) -> rx.Component:
    """Renders a single row item entry inside the Recent Scan Results table grid."""
    status_class = rx.cond(
        status == "Failed", 
        "inline-block px-2.5 py-0.5 rounded text-[10px] font-bold uppercase border bg-red-500/10 text-red-500 border-red-500/20",
        rx.cond(
            status == "Warning",
            "inline-block px-2.5 py-0.5 rounded text-[10px] font-bold uppercase border bg-orange-500/10 text-orange-500 border-orange-500/20",
            "inline-block px-2.5 py-0.5 rounded text-[10px] font-bold uppercase border bg-green-500/10 text-green-500 border-green-500/20"
        )
    )
    
    severity_class = rx.cond(
        severity == "Critical", "inline-block px-2.5 py-0.5 rounded text-[10px] font-bold uppercase bg-red-600/20 text-red-400",
        rx.cond(
            severity == "High", "inline-block px-2.5 py-0.5 rounded text-[10px] font-bold uppercase bg-orange-600/20 text-orange-400", 
            rx.cond(
                severity == "Medium", "inline-block px-2.5 py-0.5 rounded text-[10px] font-bold uppercase bg-blue-600/20 text-blue-400", 
                "inline-block px-2.5 py-0.5 rounded text-[10px] font-bold uppercase bg-slate-700/50 text-slate-400"
            )
        )
    )
    
    return rx.el.tr(
        rx.el.td(test_id, class_name="px-6 py-4 text-cyan-400 font-mono text-xs font-semibold"),
        rx.el.td(category, class_name="px-6 py-4 text-slate-300 font-medium"),
        rx.el.td(rx.text(status, class_name=status_class), class_name="px-6 py-4"),
        rx.el.td(rx.text(severity, class_name=severity_class), class_name="px-6 py-4"),
        rx.el.td(timestamp, class_name="px-6 py-4 text-slate-500 font-mono text-xs"),
        class_name="hover:bg-slate-800/20 transition-colors text-sm border-b border-slate-800/40"
    )

def dashboard_page() -> rx.Component:
    """The core structural layout container view mapping metrics with whole page scrolling configuration."""
    scan_results = [
        ("TST-1234", "Prompt Injection", "Failed", "Critical", "2026-02-27 14:32"),
        ("TST-1235", "Data Leakage", "Passed", "Low", "2026-02-27 14:28"),
        ("TST-1236", "Prompt Injection", "Failed", "High", "2026-02-27 14:15"),
        ("TST-1237", "Data Leakage", "Warning", "Medium", "2026-02-27 13:58"),
        ("TST-1238", "Prompt Injection", "Passed", "Low", "2026-02-27 13:45"),
        ("TST-1239", "System DoS", "Passed", "Low", "2026-02-27 13:12"),
        ("TST-1240", "PII Exposure", "Failed", "Critical", "2026-02-27 12:55"),
        ("TST-1241", "Prompt Injection", "Warning", "High", "2026-02-27 11:40"),
        ("TST-1242", "Credential Leak", "Passed", "Low", "2026-02-27 10:14"),
        ("TST-1243", "Context Hijacking", "Warning", "Medium", "2026-02-27 09:32"),
        ("TST-1244", "Prompt Injection", "Failed", "Critical", "2026-02-27 08:15"),
        ("TST-1245", "Data Leakage", "Passed", "Low", "2026-02-27 07:44"),
    ]
    
    return rx.el.div(
        # Page Header
        rx.el.div(
            rx.heading("Security Dashboard", class_name="text-3xl font-bold text-white text-left"),
            rx.text("Monitor AI chatbot security testing results", class_name="text-slate-500 mt-1 text-left"),
            class_name="w-full text-left mb-8"
        ),
        
        # Grid Metric Cards
        rx.el.div(
            metric_card("Total Tests Run", "1,247", "+12.5%", "up"),
            metric_card("Failed Tests", "143", "-8.2%", "down"),
            metric_card("Critical Vulnerabilities", "40", "-15.3%", "down"),
            metric_card("Risk Score", "28", is_progress=True),
            class_name="grid grid-cols-1 md:grid-cols-4 gap-6 w-full mb-8"
        ),
        
        # Charts Row Split
        rx.el.div(
            # Risk Score Trend Graph Panel
            rx.el.div(
                rx.heading("Risk Score Trend", class_name="font-semibold mb-6 text-white text-base"),
                rx.el.div(
                    rx.el.div(
                        rx.text("80"), rx.text("60"), rx.text("40"), rx.text("20"), rx.text("0"),
                        class_name="flex flex-col justify-between text-[10px] text-slate-500 pr-3 pb-1 h-48 space-y-0"
                    ),
                    rx.el.div(
                        rx.html("""
                            <svg class="w-full h-full" viewBox="0 0 400 150" preserveAspectRatio="none" style="height: 12rem;">
                              <defs>
                                <linearGradient id="neonGradient" x1="0" y1="0" x2="0" y2="1">
                                  <stop offset="0%" stop-color="#06b6d4" stop-opacity="0.4" />
                                  <stop offset="100%" stop-color="#06b6d4" stop-opacity="0" />
                                </linearGradient>
                              </defs>
                              <path d="M5,90 L66,75 L133,105 L200,55 L266,65 L333,95 L395,115 L395,150 L5,150 Z" fill="url(#neonGradient)" />
                              <polyline fill="none" stroke="#06b6d4" stroke-width="3" points="5,90 66,75 133,105 200,55 266,65 333,95 395,115" />
                              <circle cx="5" cy="90" r="4" fill="#06b6d4" /><circle cx="66" cy="75" r="4" fill="#06b6d4" />
                              <circle cx="133" cy="105" r="4" fill="#06b6d4" /><circle cx="200" cy="55" r="4" fill="#06b6d4" />
                              <circle cx="266" cy="65" r="4" fill="#06b6d4" /><circle cx="333" cy="95" r="4" fill="#06b6d4" />
                              <circle cx="395" cy="115" r="4" fill="#06b6d4" />
                            </svg>
                        """),
                        class_name="flex-1 relative border-l border-b border-slate-800/50"
                    ),
                    class_name="flex h-48 w-full"
                ),
                rx.html("""<div class="flex justify-between text-[10px] text-slate-500 pl-8 pr-1 mt-4"><span>Feb 20</span><span>Feb 21</span><span>Feb 22</span><span>Feb 23</span><span>Feb 24</span><span>Feb 25</span><span>Feb 26</span><span>Feb 27</span></div>"""),
                class_name="bg-[#151921] p-6 rounded-xl border border-slate-800 h-80 flex flex-col w-full text-left"
            ),
            
            # Vulnerability Distribution Bars Panel
            rx.el.div(
                rx.heading("Vulnerability Distribution", class_name="font-semibold mb-6 text-white text-base"),
                rx.el.div(
                    rx.el.div(
                        rx.text("20"), rx.text("15"), rx.text("10"), rx.text("5"), rx.text("0"),
                        class_name="flex flex-col justify-between text-[10px] text-slate-500 pr-4 pb-1 h-48 space-y-0"
                    ),
                    rx.el.div(
                        rx.el.div(class_name="w-12 bg-cyan-500/30 rounded-t h-[55%] relative group transition-all hover:bg-cyan-500/50"),
                        rx.el.div(class_name="w-12 bg-cyan-500 rounded-t h-[90%] relative group transition-all hover:bg-cyan-400"),
                        rx.el.div(class_name="w-12 bg-cyan-500/50 rounded-t h-[35%] relative group transition-all hover:bg-cyan-500/70"),
                        rx.el.div(class_name="w-12 bg-cyan-500/20 rounded-t h-[15%] relative group transition-all hover:bg-cyan-500/40"),
                        class_name="flex-1 h-48 border-l border-b border-slate-800/50 flex items-end justify-around px-4"
                    ),
                    class_name="flex h-48 w-full"
                ),
                rx.html("""<div class="flex justify-around text-[10px] text-slate-500 pl-10 mt-4"><span>Low</span><span>Medium</span><span>High</span><span>Critical</span></div>"""),
                class_name="bg-[#151921] p-6 rounded-xl border border-slate-800 h-80 flex flex-col w-full text-left"
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 gap-6 w-full mb-8"
        ),
        
        # Recent Scan Results Table Box Container Frame
        rx.el.div(
            rx.el.div(
                rx.heading("Recent Scan Results", class_name="font-semibold text-white text-lg"),
                rx.button("View All", class_name="text-cyan-500 text-sm font-medium hover:text-cyan-400 bg-transparent border-none cursor-pointer"),
                class_name="p-6 flex justify-between items-center border-b border-slate-800/50 w-full"
            ),
            # WHOLE PAGE SCROLL CHANGE: Removed strict inner height limits so it prints inline completely
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th("Test ID", class_name="px-6 py-4 font-semibold text-left text-slate-500 text-[10px] uppercase tracking-wider"),
                            rx.el.th("Category", class_name="px-6 py-4 font-semibold text-left text-slate-500 text-[10px] uppercase tracking-wider"),
                            rx.el.th("Status", class_name="px-6 py-4 font-semibold text-left text-slate-500 text-[10px] uppercase tracking-wider"),
                            rx.el.th("Severity", class_name="px-6 py-4 font-semibold text-left text-slate-500 text-[10px] uppercase tracking-wider"),
                            rx.el.th("Timestamp", class_name="px-6 py-4 font-semibold text-left text-slate-500 text-[10px] uppercase tracking-wider"),
                        )
                    ),
                    rx.el.tbody(
                        *[table_row(*row) for row in scan_results]
                    ),
                    class_name="w-full text-left border-collapse"
                ),
                class_name="w-full"
            ),
            class_name="bg-[#151921] rounded-xl border border-slate-800 overflow-hidden w-full text-left"
        ),
        class_name="w-full min-h-screen flex flex-col p-10 overflow-y-auto" # CHANGED: min-h-screen allows global scrolling
    )