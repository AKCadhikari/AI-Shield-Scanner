import reflex as rx
from ..state import State

def configuration_rule_row(rule_id: str, title: str, subtitle: str, state_val: bool) -> rx.Component:
    """Generates rule activation toggle switch blocks."""
    return rx.hstack(
        rx.vstack(
            rx.text(title, class_name="text-sm font-semibold text-white"),
            rx.text(subtitle, class_name="text-xs text-slate-500 mt-1"),
            class_name="space-y-0"
        ),
        rx.button(
            rx.box(
                class_name=rx.cond(state_val, "absolute top-0.5 left-0.5 w-5 h-5 rounded-full bg-white translate-x-6 transition-transform duration-200", "absolute top-0.5 left-0.5 w-5 h-5 rounded-full bg-white translate-x-0 transition-transform duration-200")
            ),
            on_click=lambda: State.toggle_rule(rule_id),
            class_name=rx.cond(
                state_val,
                "w-12 h-6 rounded-full relative transition-colors duration-200 ease-in-out bg-cyan-500 border-none cursor-pointer shrink-0",
                "w-12 h-6 rounded-full relative transition-colors duration-200 ease-in-out bg-[#0b0e14] border border-slate-700 cursor-pointer shrink-0"
            )
        ),
        class_name="flex items-center justify-between py-4 border-b border-slate-800/60 w-full"
    )

def scan_config_page() -> rx.Component:
    """The landing profile settings configuration scan component views."""
    return rx.vstack(
        rx.box(
            rx.heading("Create New Scan", class_name="text-3xl font-bold text-white mb-2"),
            rx.text("Configure security testing for your AI chatbot", class_name="text-sm text-slate-400")
        ),
        
        rx.box(
            rx.heading(
                rx.hstack(
                    rx.box(rx.icon(tag="lock", size=18, class_name="text-blue-400"), class_name="p-1.5 rounded border border-blue-500/30 bg-blue-500/10"),
                    rx.text("Chatbot Target Configuration"),
                    align="center", spacing="3"
                ),
                class_name="text-white font-semibold text-lg mb-6"
            ),
            rx.vstack(
                rx.box(
                    rx.text("Chatbot API Endpoint URL", class_name="block text-sm font-medium text-slate-200 mb-2"),
                    rx.input(value="https://api.example.com/v1/chat", class_name="w-full bg-[#0b0e14] border border-slate-800 rounded-lg p-3.5 text-sm text-white focus:border-cyan-500 outline-none"),
                    rx.text("Enter the full URL of your chatbot API endpoint", class_name="text-xs text-slate-500 mt-2"),
                    class_name="w-full"
                ),
                
                rx.box(
                    rx.text("Authentication Method", class_name="block text-sm font-medium text-slate-200 mb-2"),
                    rx.button(
                        rx.text(State.auth_method),
                        rx.icon(tag="chevron-down", size=18, class_name="text-slate-500"),
                        on_click=State.toggle_auth_dropdown,
                        class_name="w-full bg-[#0b0e14] border border-slate-800 rounded-lg p-3.5 text-sm text-white flex items-center justify-between cursor-pointer"
                    ),
                    rx.cond(
                        State.auth_dropdown_open,
                        rx.box(
                            *[rx.box(
                                opt,
                                on_click=lambda o=opt: State.change_auth_method(o),
                                class_name="px-4 py-3 text-sm cursor-pointer text-slate-300 hover:bg-slate-800 hover:text-white transition-colors"
                              ) for opt in ['None', 'API Key', 'Bearer Token', 'OAuth 2.0']],
                            class_name="absolute w-full mt-2 bg-[#0b0e14] border border-slate-800 rounded-lg shadow-2xl z-50 overflow-hidden"
                        )
                    ),
                    class_name="w-full relative"
                ),
                class_name="space-y-6 w-full"
            ),
            class_name="bg-[#151921] border border-slate-800 rounded-xl p-8 w-full"
        ),
        
        rx.box(
            rx.heading(
                rx.hstack(
                    rx.box(rx.icon(tag="flask-conical", size=18, class_name="text-emerald-400"), class_name="p-1.5 rounded border border-emerald-500/30 bg-emerald-500/10"),
                    rx.text("Test Profile"), align="center", spacing="3"
                ),
                class_name="text-white font-semibold text-lg mb-6"
            ),
            rx.vstack(
                rx.text("Test Intensity", class_name="block text-sm font-medium text-slate-200 mb-3"),
                rx.hstack(
                    *[rx.button(
                        lvl,
                        on_click=lambda l=lvl: State.change_intensity(l),
                        class_name=rx.cond(
                            State.intensity == lvl,
                            "flex-1 py-3 rounded-xl border-none text-sm font-medium transition-all bg-cyan-500 text-white shadow-[0_0_15px_rgba(6,182,212,0.3)] cursor-pointer",
                            "flex-1 py-3 rounded-xl border border-slate-800 text-slate-300 bg-[#0b0e14] hover:bg-slate-800/50 cursor-pointer"
                        )
                      ) for lvl in ['Low', 'Medium', 'High']],
                    class_name="w-full flex gap-4"
                ),
                class_name="w-full"
            ),
            class_name="bg-[#151921] border border-slate-800 rounded-xl p-8 w-full"
        ),
        
        rx.box(
            rx.heading(
                rx.hstack(
                    rx.box(rx.icon(tag="shield-alert", size=18, class_name="text-orange-400"), class_name="p-1.5 rounded border border-orange-500/30 bg-orange-500/10"),
                    rx.text("Detection Rules"), align="center", spacing="3"
                ),
                class_name="text-white font-semibold text-lg mb-6"
            ),
            rx.vstack(
                configuration_rule_row("pii", "PII Detection", "Detect personally identifiable information in responses", State.toggle_pii),
                configuration_rule_row("api_key", "API Key Detection", "Identify exposed API keys or tokens", State.toggle_api_key),
                configuration_rule_row("credentials", "Credential Detection", "Detect leaked usernames, passwords, or secrets", State.toggle_credentials),
                class_name="w-full"
            ),
            class_name="bg-[#151921] border border-slate-800 rounded-xl p-8 w-full"
        ),
        
        rx.hstack(
            rx.button(rx.icon(tag="play", size=20), rx.text("Start Scan"), class_name="flex-1 flex items-center justify-center gap-2 bg-cyan-500 hover:bg-cyan-400 text-slate-900 font-bold py-4 px-6 rounded-xl border-none cursor-pointer"),
            rx.button(rx.icon(tag="save", size=20), rx.text("Save Configuration"), class_name="flex-1 flex items-center justify-center gap-2 bg-[#151921] hover:bg-slate-800 border border-slate-700 text-white font-medium py-4 px-6 rounded-xl cursor-pointer"),
            class_name="w-full flex flex-row gap-4 pt-2"
        ),
        class_name="w-full space-y-8 h-full",
        align_items="stretch"
    )