import reflex as rx
from ..state import State

def auth_tile(label: str, value: str, icon_tag: str) -> rx.Component:
    """Renders a sleek, state-aware authentication selection tile container."""
    is_selected = (State.auth_method == value)
    
    return rx.el.button(
        rx.el.div(
            rx.icon(
                tag=icon_tag, 
                size=16, 
                class_name=rx.cond(is_selected, "text-cyan-400", "text-slate-500")
            ),
            rx.text(label, class_name="text-sm font-semibold tracking-wide"),
            class_name="flex items-center gap-3 justify-center"
        ),
        on_click=lambda: State.set_auth_method(value),
        type="button",
        class_name=rx.cond(
            is_selected,
            "flex-1 bg-cyan-500/10 text-cyan-400 border border-cyan-500/40 py-3.5 px-4 rounded-xl transition-all shadow-[0_0_15px_rgba(6,182,212,0.15)] font-bold cursor-pointer text-center",
            "flex-1 bg-[#0d1117] text-slate-400 border border-slate-800/80 hover:border-slate-700/80 hover:text-slate-200 py-3.5 px-4 rounded-xl transition-all font-semibold cursor-pointer text-center"
        )
    )

def section_card_header(icon_tag: str, title: str, color_class: str = "text-cyan-500") -> rx.Component:
    """Helper for card header categories matching your design."""
    return rx.el.div(
        rx.icon(tag=icon_tag, size=18, class_name=color_class),
        rx.heading(title, class_name="text-sm font-semibold text-white tracking-wide"),
        class_name="flex items-center gap-3 mb-6 border-b border-slate-800/40 pb-4 w-full"
    )

def test_category_row(title: str, description: str, checked_default: bool = True) -> rx.Component:
    """Renders a selectable test checkbox row container element."""
    return rx.el.div(
        rx.el.div(
            rx.text(title, class_name="text-sm font-semibold text-slate-200 mb-1"),
            rx.text(description, class_name="text-xs text-slate-500"),
            class_name="flex flex-col"
        ),
        rx.el.input(
            type="checkbox",
            default_checked=checked_default,
            class_name="w-4 h-4 rounded border-slate-700 bg-slate-800 text-cyan-500 focus:ring-cyan-500 focus:ring-offset-slate-900 accent-cyan-500 cursor-pointer"
        ),
        class_name="flex items-center justify-between p-4 bg-[#0d1117] rounded-lg border border-slate-800/60 w-full"
    )

def detection_rule_row(title: str, description: str, active_default: bool = True) -> rx.Component:
    """Renders an interactive switch toggle item row matching your screenshot."""
    return rx.el.div(
        rx.el.div(
            rx.text(title, class_name="text-sm font-medium text-slate-300 mb-0.5"),
            rx.text(description, class_name="text-xs text-slate-500"),
            class_name="flex flex-col"
        ),
        rx.el.label(
            rx.el.input(
                type="checkbox",
                default_checked=active_default,
                class_name="sr-only peer"
            ),
            rx.el.div(
                class_name="w-9 h-5 bg-slate-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-cyan-500"
            ),
            class_name="relative inline-flex items-center cursor-pointer"
        ),
        class_name="flex items-center justify-between py-4 border-b border-slate-800/40 w-full last:border-none"
    )

def scan_config_page() -> rx.Component:
    """The complete Scan Configuration view with dynamic auth method selector tiles."""
    return rx.el.div(
        # Page Title Segment
        rx.el.div(
            rx.heading("Create New Scan", class_name="text-3xl font-bold text-white text-left"),
            rx.text("Configure security testing for your AI chatbot", class_name="text-slate-500 mt-1 text-left"),
            class_name="mb-8 w-full"
        ),
        
        # Core Parameters Form Stack
        rx.el.div(
            # 1. Chatbot Target Configuration Card
            rx.el.div(
                section_card_header("lock", "Chatbot Target Configuration"),
                rx.el.div(
                    rx.el.label("Chatbot API Endpoint URL", class_name="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2"),
                    rx.el.input(
                        type="text",
                        placeholder="https://api.example.com/v1/chat",
                        value="https://api.example.com/v1/chat",
                        class_name="w-full bg-[#0d1117] border border-slate-800 rounded-lg px-4 py-3 text-slate-300 text-sm focus:outline-none focus:border-cyan-500/80 transition-colors placeholder-slate-600"
                    ),
                    rx.text("Enter the full URL of your chatbot API endpoint", class_name="text-xs text-slate-600 mt-1.5"),
                    class_name="mb-6 w-full text-left"
                ),
                
                # Dynamic Auth Option Row Container
                rx.el.div(
                    rx.el.label("Authentication Method", class_name="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3"),
                    rx.el.div(
                        auth_tile("None", "none", "ban"),
                        auth_tile("Bearer Token", "bearer", "key-round"),
                        auth_tile("API Key", "apikey", "fingerprint"),
                        class_name="flex flex-row items-center gap-4 w-full"
                    ),
                    class_name="w-full text-left"
                ),
                class_name="bg-[#151921] p-6 rounded-xl border border-slate-800 w-full flex flex-col items-start"
            ),
            
            # 2. Test Profile Selection Card
            rx.el.div(
                section_card_header("flask-conical", "Test Profile", color_class="text-emerald-500"),
                rx.el.div(
                    rx.el.label("Test Categories", class_name="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3"),
                    rx.el.div(
                        test_category_row("Prompt Injection Testing", "Test for malicious prompt injections", checked_default=True),
                        test_category_row("Data Leakage Testing", "Detect potential data exposure vulnerabilities", checked_default=True),
                        test_category_row("Social Engineering Tests", "Test resistance to social engineering attacks", checked_default=False),
                        class_name="space-y-3 w-full"
                    ),
                    class_name="w-full text-left"
                ),
                class_name="bg-[#151921] p-6 rounded-xl border border-slate-800 w-full flex flex-col items-start"
            ),
            
            # 3. Custom Test Prompts Card
            rx.el.div(
                section_card_header("text-cursor-input", "Custom Test Prompts", color_class="text-purple-500"),
                rx.el.div(
                    rx.el.label("Add Custom Prompts (Optional)", class_name="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2"),
                    rx.el.textarea(
                        placeholder="Enter custom test prompts, one per line...",
                        class_name="w-full h-28 bg-[#0d1117] border border-slate-800 rounded-lg p-4 text-slate-300 text-sm focus:outline-none focus:border-cyan-500/80 transition-colors placeholder-slate-600 resize-none"
                    ),
                    class_name="w-full text-left"
                ),
                class_name="bg-[#151921] p-6 rounded-xl border border-slate-800 w-full flex flex-col items-start"
            ),
            
            # 4. Detection Rules Toggle Switches Card
            rx.el.div(
                section_card_header("shield-check", "Detection Rules", color_class="text-amber-500"),
                rx.el.div(
                    detection_rule_row("PII Detection", "Detect personally identifiable information in responses", active_default=True),
                    detection_rule_row("API Key Detection", "Identify exposed API keys or tokens", active_default=True),
                    detection_rule_row("Credential Detection", "Detect leaked usernames, passwords, or secrets", active_default=False),
                    class_name="w-full"
                ),
                class_name="bg-[#151921] p-6 rounded-xl border border-slate-800 w-full flex flex-col items-start"
            ),
            
            # Bottom Action Buttons
            rx.el.div(
                rx.el.button(
                    rx.el.div(
                        rx.icon(tag="play", size=16),
                        rx.text("Start Scan", class_name="font-bold text-sm text-[#0b0e14]"),
                        class_name="flex items-center justify-center gap-2"
                    ),
                    class_name="flex-1 bg-cyan-400 hover:bg-cyan-300 text-[#0b0e14] py-3.5 px-6 rounded-xl transition-all shadow-[0_0_20px_rgba(34,211,238,0.3)] border-none font-bold cursor-pointer"
                ),
                rx.el.button(
                    rx.el.div(
                        rx.icon(tag="save", size=16),
                        rx.text("Save Configuration", class_name="font-semibold text-sm text-slate-300"),
                        class_name="flex items-center justify-center gap-2"
                    ),
                    class_name="bg-transparent hover:bg-slate-800/40 text-slate-300 py-3.5 px-6 rounded-xl border border-slate-800 font-semibold cursor-pointer transition-colors"
                ),
                class_name="flex items-center gap-4 w-full mt-2"
            ),
            class_name="space-y-6 w-full flex flex-col"
        ),
        class_name="w-full h-screen flex flex-col p-10 overflow-y-auto"
    )