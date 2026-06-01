import reflex as rx

class State(rx.State):
    """The global application reactive state controller."""
    active_tab: str = "Dashboard"
    
    # Report Page Custom Dropdown Controls
    report_dropdown_open: bool = False
    selected_report: str = "TST-2026-001"
    
    # Scan Configuration Settings
    auth_method: str = "none"            
    retention_policy: str = "90 Days"    
    intensity: str = "Medium"            
    
    # Active Detection Rule Toggles
    toggle_pii: bool = True
    toggle_api_key: bool = True
    toggle_credentials: bool = False

    def set_active_tab(self, tab_name: str):
        self.active_tab = tab_name

    def toggle_report_dropdown(self):
        """Flips the display visibility of the high-tech reports selector."""
        self.report_dropdown_open = not self.report_dropdown_open

    def select_report(self, report_id: str):
        """Sets the active historical scan data session tracking identifier code."""
        self.selected_report = report_id
        self.report_dropdown_open = False

    def set_auth_method(self, method: str):
        self.auth_method = method

    def change_retention_policy(self, policy: str):
        self.retention_policy = policy

    def change_intensity(self, level: str):
        self.intensity = level

    def toggle_rule(self, rule_key: str):
        if rule_key == "pii":
            self.toggle_pii = not self.toggle_pii
        elif rule_key == "api_key":
            self.toggle_api_key = not self.toggle_api_key
        elif rule_key == "credentials":
            self.toggle_credentials = not self.toggle_credentials