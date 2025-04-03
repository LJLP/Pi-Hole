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

class ToggleState(HoleActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def on_ready(self) -> None:
        self.show()

    def on_tick(self):
        self.show()
        
    def on_key_down(self):
        if self.plugin_base.ph.get_enabled():
            self.plugin_base.ph.disable(0)
        else:
            self.plugin_base.ph.enable(0)

        self.show()