import reflex as rx

def test_runs_page() -> rx.Component:
    return rx.vstack(
        rx.heading("Test Runs", size="8"),
        rx.text("View and manage your test runs here."),
        padding="2em",
    )