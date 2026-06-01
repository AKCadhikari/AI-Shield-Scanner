import reflex as rx
from .pages.dashboard import dashboard_page
from .pages.reports import reports_page
from .pages.scan_config import scan_config_page
from .pages.settings import settings_page
from .pages.test_runs import test_runs_page

# Initialize the App
app = rx.App()

# Register the routes/pages
app.add_page(dashboard_page, route="/")
app.add_page(reports_page, route="/reports")
app.add_page(scan_config_page, route="/scan-config")
app.add_page(settings_page, route="/settings")
app.add_page(test_runs_page, route="/test-runs")