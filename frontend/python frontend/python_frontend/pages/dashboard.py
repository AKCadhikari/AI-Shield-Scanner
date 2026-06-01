import reflex as rx

def dashboard_page() -> rx.Component:
    return rx.vstack(
        rx.heading("Dashboard View", size="8"),
        rx.text("Welcome to your AI-Shield Scanner Dashboard!"),
        padding="2em",
    )