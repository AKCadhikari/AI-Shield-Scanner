import reflex as rx
from ..state import State

def report_stat_card(title: str, val: str, color_class: str = "text-white") -> rx.Component:
    """Generates smaller visual reports counter block boxes."""
    return rx.box(
        rx.text(title, class_name="text-slate-400 text-xs font-semibold tracking-wide uppercase"),
        rx.text(val, class_name=f"text-4xl font-bold tracking-tight leading-none mb-1 {color_class}"),
        class_name="bg-[#151921] border border-slate-800/80 rounded-xl p-5 flex flex-col justify-between h-36 transition-all hover:border-slate-700/50"
    )

def report_row(rec_id: str, cat: str, stat: str, sev: str, score: int, fill_color: str) -> rx.Component:
    """Renders a single row item entry inside the central reports sheet."""
    stat_classes = rx.cond(
        stat == "Failed", "bg-red-500/10 text-red-500 border-red-500/20",
        rx.cond(stat == "Warning", "bg-amber-500/10 text-amber-500 border-amber-500/20", "bg-emerald-500/10 text-emerald-500 border-emerald-500/20")
    )
    sev_classes = rx.cond(
        sev == "Critical", "bg-red-600/20 text-red-400",
        rx.cond(sev == "Medium", "bg-blue-600/20 text-blue-400", "bg-emerald-600/20 text-emerald-400")
    )
    return rx.el.tr(
        rx.el.td(rx.icon(tag="chevron-right", size=16), class_name="w-12 py-4 pl-6 text-slate-600 group-hover:text-slate-400 cursor-pointer transition-colors"),
        rx.el.td(rec_id, class_name="py-4 px-4 text-sm font-mono text-cyan-500 cursor-pointer hover:underline w-[15%] truncate"),
        rx.el.td(cat, class_name="py-4 px-4 text-sm font-medium text-slate-200 w-[35%] truncate"),
        rx.el.td(rx.text(stat, class_name=f"inline-block min-w-16 px-2.5 py-1 rounded text-[10px] font-bold uppercase border tracking-wider {stat_classes}"), class_name="py-4 px-4 text-center w-[15%]"),
        rx.el.td(rx.text(sev, class_name=f"inline-block min-w-16 px-2.5 py-1 rounded text-[10px] font-bold uppercase tracking-wider {sev_classes}"), class_name="py-4 px-4 text-center w-[15%]"),
        rx.el.td(
            rx.hstack(
                rx.text(str(score), class_name="text-sm font-semibold font-mono text-white min-w-5 text-right"),
                rx.box(
                    rx.box(class_name=f"h-full rounded-full {fill_color}", style={"width": f"{score}%"}),
                    class_name="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden max-w-30"
                ),
                class_name="flex items-center gap-3 w-full"
            ),
            class_name="py-4 pr-6 pl-4 w-[20%]"
        ),
        class_name="hover:bg-slate-800/10 transition-colors group border-b border-slate-800/40"
    )

def reports_page() -> rx.Component:
    """The master compliance reports page."""
    records = [
        ("TST-1234", "Prompt Injection", "Failed", "Critical", 95, "bg-red-500"),
        ("TST-1235", "Prompt Injection", "Failed", "Critical", 95, "bg-red-500"),
        ("TST-1236", "Data Leakage", "Warning", "Medium", 45, "bg-orange-500"),
        ("TST-1237", "Data Leakage", "Warning", "Medium", 45, "bg-orange-500"),
        ("TST-1238", "Data Leakage", "Warning", "Medium", 45, "bg-orange-500"),
    ]
    filters_list = ["all", "Critical", "High", "Medium", "Low"]
    
    return rx.vstack(
        rx.hstack(
            rx.box(
                rx.heading("Scan Results", class_name="text-3xl font-bold text-white mb-1"),
                rx.text("Detailed analysis of security test results", class_name="text-sm text-slate-400")
            ),
            rx.hstack(
                rx.box(
                    rx.select(
                        ["TST-2026-001", "TST-2026-002"],
                        placeholder="TST-2026-001",
                        class_name="bg-[#1a1f29] border border-slate-800 text-slate-300 text-sm rounded-lg px-4 py-2.5 outline-none cursor-pointer focus:border-slate-700"
                    ),
                    class_name="relative"
                ),
                rx.button(
                    rx.icon(tag="download", size=16),
                    rx.text("Export Report", class_name="font-semibold text-sm"),
                    class_name="flex items-center gap-2 bg-cyan-500 hover:bg-cyan-400 text-slate-900 px-4 py-2.5 rounded-lg transition-colors border-none cursor-pointer"
                ),
                class_name="flex items-center gap-3"
            ),
            class_name="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 w-full shrink-0"
        ),
        
        rx.grid(
            report_stat_card("Total Tests", "5"),
            report_stat_card("Passed", "2", "text-emerald-500"),
            report_stat_card("Failed", "2", "text-red-500"),
            report_stat_card("Overall Risk Score", "48", "text-amber-500"),
            class_name="w-full grid grid-cols-1 md:grid-cols-4 gap-6 shrink-0"
        ),
        
        rx.box(
            rx.hstack(
                rx.icon(tag="sliders-horizontal", size=14),
                rx.text("Filter by severity:", class_name="text-slate-400 text-xs font-medium"),
                class_name="flex items-center gap-2"
            ),
            rx.hstack(
                *[rx.button(
                    f.capitalize(),
                    class_name="px-3 py-1.5 rounded-lg text-xs font-medium bg-[#1a1f29] text-slate-400 hover:bg-slate-800 border-none cursor-pointer"
                  ) for f in filters_list],
                class_name="flex flex-wrap gap-2"
            ),
            class_name="bg-[#151921] border border-slate-800/80 rounded-xl px-6 py-4 flex items-center gap-4 w-full shrink-0"
        ),
        
        rx.box(
            rx.box(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th(class_name="w-12 py-4 pl-6"),
                            rx.el.th("Test ID", class_name="py-4 px-4 font-medium w-[15%]"),
                            rx.el.th("Category", class_name="py-4 px-4 font-medium w-[35%]"),
                            rx.el.th("Status", class_name="py-4 px-4 font-medium text-center w-[15%]"),
                            rx.el.th("Severity", class_name="py-4 px-4 font-medium text-center w-[15%]"),
                            rx.el.th("Risk Score", class_name="py-4 pr-6 pl-4 font-medium w-[20%]"),
                            class_name="text-slate-400 text-xs font-medium border-b border-slate-800/60 bg-[#151921] text-left"
                        )
                    ),
                    class_name="w-full border-collapse table-fixed"
                ),
                class_name="w-full shrink-0"
            ),
            rx.box(
                rx.el.table(
                    rx.el.tbody(
                        *[report_row(*row) for row in records]
                    ),
                    class_name="w-full border-collapse table-fixed"
                ),
                class_name="overflow-y-auto flex-1 min-h-0 w-full"
            ),
            class_name="bg-[#151921] border border-slate-800/80 rounded-xl max-w-full flex flex-col flex-1 min-h-0 w-full overflow-hidden"
        ),
        class_name="w-full flex flex-col space-y-6 h-full",
        align_items="stretch"
    )