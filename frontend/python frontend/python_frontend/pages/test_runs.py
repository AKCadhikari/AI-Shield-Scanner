import reflex as rx

def test_runs_page() -> rx.Component:
    """Renders a sleek cybersecurity-themed Under Construction view for Test Runs."""
    return rx.el.div(
        # Page Title Segment
        rx.el.div(
            rx.heading("Test Runs", class_name="text-3xl font-bold text-white text-left"),
            rx.text("Execute automated security assessment profiles", class_name="text-slate-500 mt-1 text-left text-xs"),
            class_name="mb-8 w-full shrink-0"
        ),
        
        # Central Splash Block
        rx.el.div(
            rx.el.div(
                # Glowing Icon Core
                rx.el.div(
                    rx.icon(tag="shield-alert", size=32, class_name="text-cyan-400 animate-pulse"),
                    class_name="w-16 h-16 rounded-2xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center mb-6 shadow-[0_0_30px_rgba(6,182,212,0.15)]"
                ),
                # Message
                rx.heading("Module Under Construction", class_name="text-xl font-bold text-white mb-2"),
                rx.text(
                    "The automated target scanning terminal engine is currently being integrated into the core pipeline framework.", 
                    class_name="text-slate-400 text-sm max-w-sm"
                ),
                # Tech Spec Badge
                rx.el.div(
                    rx.icon(tag="terminal", size=12, class_name="text-cyan-500"),
                    rx.text(" PIPELINE_STATUS: DEPLOYING_ENGINE ", class_name="text-[10px] font-mono text-cyan-400 tracking-wider font-bold"),
                    class_name="mt-6 flex items-center gap-2 bg-cyan-500/5 border border-cyan-500/20 px-3 py-1 rounded-md"
                ),
                class_name="flex flex-col items-center justify-center text-center max-w-md"
            ),
            class_name="bg-[#151921] rounded-xl border border-slate-800 flex-1 flex items-center justify-center w-full min-h-0"
        ),
        class_name="w-full h-screen flex flex-col p-10 overflow-hidden"
    )