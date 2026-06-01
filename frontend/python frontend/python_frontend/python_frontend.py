import reflex as rx
from .components.sidebar import sidebar
from .pages.dashboard import dashboard_page
from .pages.reports import reports_page
from .pages.scan_config import scan_config_page
from .pages.settings import settings_page
from .pages.test_runs import test_runs_page  # Ensure this import name matches!
from .state import State

def main_content_area() -> rx.Component:
    """Routes the internal layout panel view while permitting native page-level scrolling."""
    return rx.el.div(
        rx.match(
            State.active_tab,
            ("Dashboard", dashboard_page()),
            ("Scan Configurations", scan_config_page()),
            ("Test Runs", test_runs_page()),
            ("Reports", reports_page()),
            ("Settings", settings_page()),
            rx.el.div(
                rx.text(f"{State.active_tab} View is under development", class_name="text-slate-500 italic"),
                class_name="h-full flex items-center justify-center w-full"
            )
        ),
        # FIXED: Changed overflow-hidden to overflow-y-auto in classes and styles
        class_name="flex-1 h-full bg-[#0b0e14] overflow-y-auto",
        style={"flex": "1 1 0%", "overflowY": "auto", "height": "100%", "width": "100%"}
    )

def index() -> rx.Component:
    """The root layout container forcing side-by-side alignment parameters."""
    return rx.el.div(
        sidebar(),
        main_content_area(),
        class_name="w-screen h-screen bg-[#0b0e14] text-slate-300 font-sans overflow-hidden",
        style={
            "display": "flex",
            "flexDirection": "row",
            "width": "100vw",
            "height": "100vh",
            "overflow": "hidden",
            "backgroundColor": "#0b0e14"
        }
    )

app = rx.App(
    theme=None,
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
    ],
    head_components=[
        rx.el.script(src="https://cdn.tailwindcss.com"),
    ]
)
app.add_page(index, route="/")