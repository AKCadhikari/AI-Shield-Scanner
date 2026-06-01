import reflex as rx

def metric_card(title: str, value: str, change: str = "", trend: str = "up", is_progress: bool = False) -> rx.Component:
    """Generates standard responsive visual information summary boxes."""
    return rx.box(
        rx.text(title, class_name="text-slate-400 text-sm mb-2"),
        rx.heading(value, class_name="text-3xl font-bold text-white mb-2"),
        rx.cond(
            is_progress,
            rx.box(
                rx.box(class_name="bg-cyan-500 h-full rounded-full w-[28%] shadow-[0_0_10px_#06b6d4]"),
                class_name="w-full bg-slate-800 h-2 rounded-full mt-4 overflow-hidden"
            ),
            rx.text(
                f"{change} from last week",
                class_name=rx.cond(trend == "up", "text-xs text-green-400", "text-xs text-red-400")
            )
        ),
        class_name="bg-[#151921] p-6 rounded-xl border border-slate-800"
    )

def table_row(test_id: str, category: str, status: str, severity: str, timestamp: str) -> rx.Component:
    """Renders a single row inside the Recent Scan Results table."""
    status_colors = rx.cond(
        status == "Failed", "bg-red-500/10 text-red-500 border-red-500/20",
        rx.cond(status == "Warning", "bg-orange-500/10 text-orange-500 border-orange-500/20", "bg-green-500/10 text-green-500 border-green-500/20")
    )
    severity_colors = rx.cond(
        severity == "Critical", "bg-red-600/20 text-red-400",
        rx.cond(severity == "High", "bg-orange-600/20 text-orange-400", rx.cond(severity == "Medium", "bg-blue-600/20 text-blue-400", "bg-slate-700/50 text-slate-400"))
    )
    return rx.el.tr(
        rx.el.td(test_id, class_name="px-6 py-4 text-cyan-500 font-mono text-xs"),
        rx.el.td(category, class_name="px-6 py-4 text-slate-300"),
        rx.el.td(rx.text(status, class_name=f"inline-block px-2.5 py-0.5 rounded text-[10px] font-bold uppercase border {status_colors}"), class_name="px-6 py-4"),
        rx.el.td(rx.text(severity, class_name=f"inline-block px-2.5 py-0.5 rounded text-[10px] font-bold uppercase {severity_colors}"), class_name="px-6 py-4"),
        rx.el.td(timestamp, class_name="px-6 py-4 text-slate-500 text-xs"),
        class_name="hover:bg-slate-800/30 transition-colors text-sm border-b border-slate-800/50"
    )

def dashboard_page() -> rx.Component:
    """The master landing dashboard view component."""
    scan_results = [
        ("TST-1234", "Prompt Injection", "Failed", "Critical", "2026-02-27 14:32"),
        ("TST-1235", "Data Leakage", "Passed", "Low", "2026-02-27 14:28"),
        ("TST-1236", "Prompt Injection", "Failed", "High", "2026-02-27 14:15"),
        ("TST-1237", "Data Leakage", "Warning", "Medium", "2026-02-27 13:58"),
        ("TST-1238", "Data Leakage", "Passed", "Low", "2026-02-27 13:45"),
    ]
    
    return rx.vstack(
        rx.box(
            rx.heading("Security Dashboard", class_name="text-3xl font-bold text-white"),
            rx.text("Monitor AI chatbot security testing results", class_name="text-slate-500 mt-1")
        ),
        
        rx.grid(
            metric_card("Total Tests Run", "1,247", "+12.5%", "up"),
            metric_card("Failed Tests", "143", "-8.2%", "down"),
            metric_card("Critical Vulnerabilities", "40", "-15.3%", "down"),
            metric_card("Risk Score", "28", is_progress=True),
            class_name="w-full grid grid-cols-1 md:grid-cols-4 gap-6"
        ),
        
        rx.grid(
            rx.box(
                rx.heading("Risk Score Trend", class_name="font-semibold mb-6 text-white text-base"),
                rx.hstack(
                    rx.vstack(
                        rx.text("80"), rx.text("60"), rx.text("40"), rx.text("20"), rx.text("0"),
                        class_name="text-[10px] text-slate-500 h-48 justify-between pr-3 pb-1 space-y-0"
                    ),
                    rx.box(
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
                    class_name="w-full flex items-start"
                ),
                rx.box(
                    rx.html("""<div class="flex justify-between text-[10px] text-slate-500 pl-8 pr-1 mt-4"><span>Feb 20</span><span>Feb 21</span><span>Feb 22</span><span>Feb 23</span><span>Feb 24</span><span>Feb 25</span><span>Feb 26</span><span>Feb 27</span></div>"""),
                    class_name="w-full"
                ),
                class_name="bg-[#151921] p-6 rounded-xl border border-slate-800 h-80 flex flex-col"
            ),
            
            rx.box(
                rx.heading("Vulnerability Distribution", class_name="font-semibold mb-6 text-white text-base"),
                rx.hstack(
                    rx.vstack(
                        rx.text("20"), rx.text("15"), rx.text("10"), rx.text("5"), rx.text("0"),
                        class_name="text-[10px] text-slate-500 h-48 justify-between pr-4 pb-1 space-y-0"
                    ),
                    rx.hstack(
                        rx.box(class_name="w-12 bg-cyan-500/30 rounded-t h-[55%] relative group transition-all hover:bg-cyan-500/50"),
                        rx.box(class_name="w-12 bg-cyan-500 rounded-t h-[90%] relative group transition-all hover:bg-cyan-400"),
                        rx.box(class_name="w-12 bg-cyan-500/50 rounded-t h-[35%] relative group transition-all hover:bg-cyan-500/70"),
                        rx.box(class_name="w-12 bg-cyan-500/20 rounded-t h-[15%] relative group transition-all hover:bg-cyan-500/40"),
                        class_name="flex-1 h-48 border-l border-b border-slate-800/50 flex items-end justify-around px-4"
                    ),
                    class_name="w-full flex items-start"
                ),
                rx.box(
                    rx.html("""<div class="flex justify-around text-[10px] text-slate-500 pl-10 mt-4"><span>Low</span><span>Medium</span><span>High</span><span>Critical</span></div>"""),
                    class_name="w-full"
                ),
                class_name="bg-[#151921] p-6 rounded-xl border border-slate-800 h-80 flex flex-col"
            ),
            class_name="w-full grid grid-cols-1 md:grid-cols-2 gap-6"
        ),
        
        rx.box(
            rx.hstack(
                rx.heading("Recent Scan Results", class_name="font-semibold text-white text-lg"),
                rx.button("View All", class_name="text-cyan-500 text-sm font-medium hover:text-cyan-400 bg-transparent border-none cursor-pointer"),
                class_name="p-6 flex justify-between items-center border-b border-slate-800/50 w-full"
            ),
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th("Test ID", class_name="px-6 py-4 font-semibold"),
                        rx.el.th("Category", class_name="px-6 py-4 font-semibold"),
                        rx.el.th("Status", class_name="px-6 py-4 font-semibold"),
                        rx.el.th("Severity", class_name="px-6 py-4 font-semibold"),
                        rx.el.th("Timestamp", class_name="px-6 py-4 font-semibold"),
                        class_name="text-slate-500 text-[10px] uppercase tracking-widest bg-slate-800/10 text-left border-b border-slate-800"
                    )
                ),
                rx.el.tbody(
                    *[table_row(*row) for row in scan_results]
                ),
                class_name="w-full text-left"
            ),
            class_name="bg-[#151921] rounded-xl border border-slate-800 overflow-hidden w-full"
        ),
        class_name="space-y-8 w-full",
        align_items="stretch"
    )