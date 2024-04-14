# Import StreamController modules
from src.backend.PluginManager.ActionBase import ActionBase
from src.backend.DeckManagement.DeckController import DeckController
from src.backend.PageManagement.Page import Page
from src.backend.PluginManager.PluginBase import PluginBase

# Import python modules
import os
import threading

# Import gtk modules - used for the config rows
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

class HoleActionBase(ActionBase):
    def __init__(self, action_id: str, action_name: str,
                 deck_controller: DeckController, page: Page, coords: str, plugin_base: PluginBase):
        super().__init__(action_id=action_id, action_name=action_name,
            deck_controller=deck_controller, page=page, coords=coords, plugin_base=plugin_base)
        
        self.HAS_CONFIGURATION = True

    def get_config_rows(self) -> list:
        self.ip_entry = Adw.EntryRow(title=self.plugin_base.lm.get("actions.base.ip.label"))
        self.token_entry = Adw.PasswordEntryRow(title=self.plugin_base.lm.get("actions.base.password.label"))

        self.load_config_defaults()

        # Connect signals
        self.ip_entry.connect("notify::text", self.on_value_changed)
        self.token_entry.connect("notify::text", self.on_value_changed)

        return [self.ip_entry, self.token_entry]

    def load_config_defaults(self):
        settings = self.plugin_base.get_settings()
        ip = settings.setdefault("ip", "localhost")
        token = settings.setdefault("token", "")

        # Update ui
        self.ip_entry.set_text(ip)
        self.token_entry.set_text(token)

        self.plugin_base.set_settings(settings)

    def on_value_changed(self, entry, *args):
        settings = self.plugin_base.get_settings()

        ip = self.ip_entry.get_text()
        token = self.token_entry.get_text()

        settings["ip"] = ip
        settings["token"] = token

        self.plugin_base.set_settings(settings)
        self.plugin_base.ph.ip_address = ip
        self.plugin_base.ph.api_token = token

        self.on_tick()

    def show(self):
        def _show(self: "HoleActionBase"):
            enabled = self.plugin_base.ph.get_enabled()
            if enabled is None:
                self.set_media(media_path=os.path.join(self.plugin_base.PATH, "assets", "no-connection.png"), size=0.85)
            elif enabled:
                self.set_media(media_path=os.path.join(self.plugin_base.PATH, "assets", "active.png"), size=0.85)
            else:
                self.set_media(media_path=os.path.join(self.plugin_base.PATH, "assets", "inactive.png"), size=0.85)

        thread = threading.Thread(target=_show, args=(self,), daemon=True, name="show")
        thread.start()