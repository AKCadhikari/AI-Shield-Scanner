import reflex as rx
from ..state import State

def permission_dot(allowed: bool) -> rx.Component:
    """Generates green verification verification check elements for specific role grids."""
    return rx.center(
        rx.cond(
            allowed,
            rx.box(
                rx.box(class_name="w-1.5 h-1.5 rounded-full bg-emerald-500 shadow-[0_0_8px_#10b981]"),
                class_name="w-5 h-5 rounded-full bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center"
            ),
            rx.box(class_name="w-5 h-5 rounded-full bg-[#0b0e14] border border-slate-800/60")
        ),
        class_name="w-full text-center"
    )

def settings_page() -> rx.Component:
    """The systemic application permissions setup interface window panel view."""
    permissions = [
        ("View Dashboard", True, True, True), ("Run Security Scans", True, True, False),
        ("Configure Scans", True, True, False), ("View Reports", True, True, True),
        ("Generate Reports", True, True, False), ("Manage Users", True, False, False),
    ]
    
    return rx.vstack(
        rx.box(
            rx.heading("Settings", class_name="text-3xl font-bold text-white mb-1"),
            rx.text("Manage application permissions and global security rules", class_name="text-sm text-slate-400")
        ),
        
        rx.box(
            rx.heading(
                rx.hstack(
                    rx.box(rx.icon(tag="shield", size=18, class_name="text-purple-400"), class_name="p-1.5 rounded border border-purple-500/30 bg-purple-500/10"),
                    rx.vstack(rx.text("Role Permissions"), rx.text("Define what each role can do", class_name="text-xs text-slate-500 font-normal mt-0.5"), class_name="space-y-0"),
                    align="center", spacing="3"
                ),
                class_name="text-white font-semibold text-lg mb-6"
            ),
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th("Permission", class_name="pb-4 font-semibold text-left w-1/2"),
                        rx.el.th("Admin", class_name="pb-4 font-semibold text-center w-1/6"),
                        rx.el.th("Tester", class_name="pb-4 font-semibold text-center w-1/6"),
                        rx.el.th("Viewer", class_name="pb-4 font-semibold text-center w-1/6"),
                        class_name="text-slate-400 text-xs font-semibold border-b border-slate-800/60"
                    )
                ),
                rx.el.tbody(
                    *[rx.el.tr(
                        rx.el.td(p[0], class_name="py-4 text-slate-200 text-left"),
                        rx.el.td(permission_dot(p[1]), class_name="py-4"),
                        rx.el.td(permission_dot(p[2]), class_name="py-4"),
                        rx.el.td(permission_dot(p[3]), class_name="py-4"),
                        class_name="hover:bg-slate-800/10 transition-colors text-sm font-medium border-b border-slate-800/40"
                      ) for p in permissions]
                ),
                class_name="w-full border-collapse"
            ),
            class_name="bg-[#151921] border border-slate-800/80 rounded-xl p-8 w-full"
        ),
        
        rx.box(
            rx.heading(
                rx.hstack(
                    rx.box(rx.icon(tag="database", size=18, class_name="text-amber-400"), class_name="p-1.5 rounded border border-amber-500/30 bg-amber-500/10"),
                    rx.vstack(rx.text("Security Settings"), rx.text("Configure data retention and encryption", class_name="text-xs text-slate-500 font-normal mt-0.5"), class_name="space-y-0"),
                    align="center", spacing="3"
                ),
                class_name="text-white font-semibold text-lg mb-6"
            ),
            rx.vstack(
                rx.hstack(
                    rx.vstack(rx.text("Data Retention Policy", class_name="text-sm font-semibold text-slate-200"), rx.text("Scan results will be automatically deleted after this period", class_name="text-xs text-slate-500"), class_name="space-y-0.5 text-left"),
                    rx.box(
                        rx.button(rx.text(State.retention_policy), rx.icon(tag="chevron-down", size=14), on_click=State.toggle_retention_dropdown, class_name="w-full bg-[#0b0e14] border border-slate-800 rounded-lg px-4 py-3 text-xs text-slate-200 flex items-center justify-between cursor-pointer"),
                        rx.cond(State.retention_dropdown_open, rx.box(*[rx.box(o, on_click=lambda opt=o: State.change_retention_policy(opt), class_name="px-4 py-3 text-xs cursor-pointer text-slate-300 hover:bg-slate-800 transition-colors") for o in ['30 Days', '60 Days', '90 Days']], class_name="absolute w-full mt-2 bg-[#0b0e14] border border-slate-800 rounded-lg z-50 overflow-hidden")),
                        class_name="w-full sm:w-48 shrink-0 relative"
                    ),
                    class_name="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-5 border-b border-slate-800/60 w-full"
                ),
                rx.hstack(
                    rx.vstack(rx.text("Log Encryption", class_name="text-sm font-semibold text-slate-200"), rx.text("Encrypt all stored test logs and results", class_name="text-xs text-slate-500"), class_name="space-y-0.5 text-left"),
                    rx.box(
                        rx.text(class_name="w-1.5 h-1.5 rounded-full bg-emerald-500 inline-block align-middle mr-1.5"),
                        rx.text("Enabled", class_name="inline-block align-middle"),
                        class_name="flex items-center gap-2 text-xs font-semibold text-emerald-400 bg-emerald-500/5 border border-emerald-500/10 px-2.5 py-1 rounded-md"
                    ),
                    class_name="flex items-center justify-between py-4 border-b border-slate-800/60 w-full"
                ),
                rx.hstack(
                    rx.vstack(rx.text("Two-Factor Authentication", class_name="text-sm font-semibold text-slate-200"), rx.text("Require 2FA for all admin users", class_name="text-xs text-slate-500"), class_name="space-y-0.5 text-left"),
                    rx.box(
                        rx.text(class_name="w-1.5 h-1.5 rounded-full bg-emerald-500 inline-block align-middle mr-1.5"),
                        rx.text("Enabled", class_name="inline-block align-middle"),
                        class_name="flex items-center gap-2 text-xs font-semibold text-emerald-400 bg-emerald-500/5 border border-emerald-500/10 px-2.5 py-1 rounded-md"
                    ),
                    class_name="flex items-center justify-between py-4 w-full"
                ),
                class_name="w-full"
            ),
            class_name="bg-[#151921] border border-slate-800/80 rounded-xl p-8 w-full"
        ),
        class_name="w-full space-y-6 h-full",
        align_items="stretch"
    )