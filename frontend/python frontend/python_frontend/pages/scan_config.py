import reflex as rx

def scan_config_page() -> rx.Component:
    return rx.vstack(
        rx.heading("Scan Configuration", size="8"),
        rx.text("Configure your AI-Shield Scanner settings here."),
        padding="2em",
    )