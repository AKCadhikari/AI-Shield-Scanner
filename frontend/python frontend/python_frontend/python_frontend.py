import reflex as rx
from .components.sidebar import sidebar
from .pages.dashboard import dashboard_page
from .pages.reports import reports_page
from .pages.scan_config import scan_config_page
from .pages.settings import settings_page
from .pages.test_runs import test_runs_page
from .state import State

def index() -> rx.Component:
    """The master routing shell that displays views dynamically based on State."""
    return rx.box(
        sidebar(),
        
        rx.box(
            rx.box(
                rx.cond(State.active_tab == "Dashboard", dashboard_page()),
                rx.cond(State.active_tab == "Scan Configurations", scan_config_page()),
                rx.cond(State.active_tab == "Test Runs", test_runs_page()),
                rx.cond(State.active_tab == "Reports", reports_page()),
                rx.cond(State.active_tab == "Settings", settings_page()),
                class_name="flex-1 overflow-y-auto p-10 h-full"
            ),
            class_name="flex-1 flex flex-col overflow-hidden"
        ),
        class_name="flex h-screen bg-[#0b0e14] text-slate-300 font-sans overflow-hidden w-full"
    )

app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
    ]
)
app.add_page(index, route="/")