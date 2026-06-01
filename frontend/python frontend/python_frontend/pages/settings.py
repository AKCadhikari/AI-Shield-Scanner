import reflex as rx

def settings_page() -> rx.Component:
    return rx.vstack(
        rx.heading("Settings", size="8"),
        rx.text("Manage your AI-Shield Scanner settings here."),
        padding="2em",
    )