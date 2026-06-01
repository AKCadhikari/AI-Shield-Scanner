import reflex as rx
from ..state import State

def menu_button(name: str, icon_tag: str) -> rx.Component:
    """Renders a single reactive navigation sidebar button element."""
    is_active = (State.active_tab == name)
    return rx.button(
        rx.hstack(
            rx.icon(tag=icon_tag, size=20),
            rx.text(name, class_name="text-sm font-medium"),
            spacing="3",
            align="center",
        ),
        rx.cond(
            is_active,
            rx.icon(tag="chevron-right", size=16)
        ),
        on_click=lambda: State.set_active_tab(name),
        class_name=rx.cond(
            is_active,
            "w-full flex items-center justify-between px-4 py-3 rounded-lg transition-all bg-cyan-500 text-white shadow-[0_0_15px_rgba(6,182,212,0.4)] border-none cursor-pointer",
            "w-full flex items-center justify-between px-4 py-3 rounded-lg transition-all text-slate-400 hover:bg-slate-800/50 hover:text-slate-200 bg-transparent border-none cursor-pointer"
        ),
    )

def sidebar() -> rx.Component:
    """The master frontend left column sidebar menu structure."""
    return rx.box(
        rx.center(
            rx.image(
                src="/logo.png",
                alt="AI Shield Logo",
                class_name="w-40 h-auto object-contain filter drop-shadow-[0_0_8px_rgba(6,182,212,0.3)]"
            ),
            class_name="p-8"
        ),
        
        rx.vstack(
            menu_button("Dashboard", "layout-dashboard"),
            menu_button("Scan Configurations", "shield-alert"),
            menu_button("Test Runs", "circle-play"), # Fixed: Changed 'play-circle' to 'circle-play' to comply with Reflex specifications
            menu_button("Reports", "file-text"),
            menu_button("Settings", "settings"),
            class_name="flex-1 px-4 space-y-2 w-full",
        ),
        
        rx.box(
            rx.box(class_name="border-t border-slate-800/60 mb-6 mr-2"),
            rx.hstack(
                rx.hstack(
                    rx.box(
                        rx.icon(tag="user", size=22),
                        class_name="shrink-0 w-11 h-11 rounded-full bg-slate-800 flex items-center justify-center text-cyan-500 border border-slate-700"
                    ),
                    rx.vstack(
                        rx.text("Admin User", class_name="text-sm font-bold text-white"),
                        rx.text("Security Lead", class_name="text-[11px] text-slate-500 uppercase tracking-tighter"),
                        class_name="leading-tight space-y-0"
                    ),
                    class_name="flex items-center gap-3 cursor-pointer overflow-hidden min-w-0"
                ),
                rx.button(
                    rx.icon(tag="log-out", size=20),
                    title="Logout",
                    class_name="p-1.5 rounded-lg text-slate-500 hover:bg-red-500/10 hover:text-red-500 transition-all shrink-0 ml-auto pr-2 bg-transparent border-none cursor-pointer"
                ),
                class_name="flex items-center justify-between w-full group"
            ),
            class_name="mt-auto p-4 pl-6 pb-6 w-full"
        ),
        class_name="w-64 flex flex-col h-full border-r border-slate-800/40 shrink-0 bg-[#0b0e14]"
    )