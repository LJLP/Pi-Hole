# Import StreamController modules
from src.backend.PluginManager.ActionBase import ActionBase
from src.backend.DeckManagement.DeckController import DeckController
from src.backend.PageManagement.Page import Page
from src.backend.PluginManager.PluginBase import PluginBase

# Import python modules
import os

# Import gtk modules - used for the config rows
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

from ..HoleActionBase import HoleActionBase

class Disable(HoleActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def get_config_rows(self) -> list:
        super_rows = super().get_config_rows()

        self.time_spinner = Adw.SpinRow.new_with_range(0, 60*60, 1)
        self.time_spinner.set_title(self.plugin_base.lm.get("actions.disable.time.label"))
        self.time_spinner.set_subtitle(self.plugin_base.lm.get("actions.disable.time.subtitle"))

        self._load_config_defaults()

        # Connect signals
        self.time_spinner.connect("notify::value", self.on_time_changed)

        super_rows.append(self.time_spinner)
        return super_rows

    def _load_config_defaults(self):
        settings = self.plugin_base.get_settings()
        self.time_spinner.set_value(round(settings.get("time", 0)))

    def on_time_changed(self, *args):
        settings = self.plugin_base.get_settings()
        settings["time"] = self.time_spinner.get_value()
        self.plugin_base.set_settings(settings)


        
    def on_ready(self) -> None:
        self.show()

    def on_tick(self):
        self.show()
        
    def on_key_down(self):
        settings = self.plugin_base.get_settings()

        self.plugin_base.ph.disable(settings.get("time", 0))

        self.show()