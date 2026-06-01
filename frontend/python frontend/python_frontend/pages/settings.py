import reflex as rx

def settings_page() -> rx.Component:
    """Renders a sleek cybersecurity-themed Under Construction view for Settings."""
    return rx.el.div(
        # Page Title Segment
        rx.el.div(
            rx.heading("Settings", class_name="text-3xl font-bold text-white text-left"),
            rx.text("Manage administrative matrix controls and token access criteria", class_name="text-slate-500 mt-1 text-left text-xs"),
            class_name="mb-8 w-full shrink-0"
        ),
        
        # Central Splash Block
        rx.el.div(
            rx.el.div(
                # Glowing Icon Core
                rx.el.div(
                    rx.icon(tag="sliders", size=32, class_name="text-amber-400 animate-pulse"),
                    class_name="w-16 h-16 rounded-2xl bg-amber-500/10 border border-amber-500/20 flex items-center justify-center mb-6 shadow-[0_0_30px_rgba(245,158,11,0.15)]"
                ),
                # Message
                rx.heading("Control Panel Locked", class_name="text-xl font-bold text-white mb-2"),
                rx.text(
                    "Global policy parameters, administrative roles, and rule verification switches are currently being mapped.", 
                    class_name="text-slate-400 text-sm max-w-sm"
                ),
                # Tech Spec Badge
                rx.el.div(
                    rx.icon(tag="sliders", size=12, class_name="text-amber-500"),
                    rx.text(" CONFIG_STATUS: MAPPING_POLICIES ", class_name="text-[10px] font-mono text-amber-400 tracking-wider font-bold"),
                    class_name="mt-6 flex items-center gap-2 bg-amber-500/5 border border-amber-500/20 px-3 py-1 rounded-md"
                ),
                class_name="flex flex-col items-center justify-center text-center max-w-md"
            ),
            class_name="bg-[#151921] rounded-xl border border-slate-800 flex-1 flex items-center justify-center w-full min-h-0"
        ),
        class_name="w-full h-screen flex flex-col p-10 overflow-hidden"
    )