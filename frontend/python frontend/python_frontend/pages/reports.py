import reflex as rx

def reports_page() -> rx.Component:
    return rx.vstack(
        rx.heading("Reports", size="8"),
        rx.text("View your generated reports here."),
        padding="2em",
    )