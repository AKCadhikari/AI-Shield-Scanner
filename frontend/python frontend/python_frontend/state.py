import reflex as rx

class State(rx.State):
    """The global application reactive state controller."""
    active_tab: str = "Dashboard"
    
    auth_dropdown_open: bool = False
    auth_method: str = "None"
    
    retention_dropdown_open: bool = False
    retention_policy: str = "90 Days"
    
    intensity: str = "Medium"
    toggle_pii: bool = True
    toggle_api_key: bool = True
    toggle_credentials: bool = False

    def set_active_tab(self, tab_name: str):
        self.active_tab = tab_name

    def toggle_auth_dropdown(self):
        self.auth_dropdown_open = not self.auth_dropdown_open

    def change_auth_method(self, method: str):
        self.auth_method = method
        self.auth_dropdown_open = False

    def toggle_retention_dropdown(self):
        self.retention_dropdown_open = not self.retention_dropdown_open

    def change_retention_policy(self, policy: str):
        self.retention_policy = policy
        self.retention_dropdown_open = False

    def change_intensity(self, level: str):
        self.intensity = level

    def toggle_rule(self, rule_key: str):
        if rule_key == "pii":
            self.toggle_pii = not self.toggle_pii
        elif rule_key == "api_key":
            self.toggle_api_key = not self.toggle_api_key
        elif rule_key == "credentials":
            self.toggle_credentials = not self.toggle_credentials