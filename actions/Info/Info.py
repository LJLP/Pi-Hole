# Import StreamController modules
import threading
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

class Info(HoleActionBase):
    def __init__(self, action_id: str, action_name: str,
                 deck_controller: DeckController, page: Page, coords: str, plugin_base: PluginBase):
        super().__init__(action_id=action_id, action_name=action_name,
            deck_controller=deck_controller, page=page, coords=coords, plugin_base=plugin_base)
        
    def get_config_rows(self) -> list:
        super_rows = super().get_config_rows()

        self.top_label_row = Adw.EntryRow(title=self.plugin_base.lm.get("actions.info.top-label.title"))
        self.center_label_row = Adw.EntryRow(title=self.plugin_base.lm.get("actions.info.center-label.title"))
        self.bottom_label_row = Adw.EntryRow(title=self.plugin_base.lm.get("actions.info.bottom-label.title"))

        self._load_config_defaults()

        # Connect signals
        self.top_label_row.connect("notify::text", self.on_label_row_changed)
        self.center_label_row.connect("notify::text", self.on_label_row_changed)
        self.bottom_label_row.connect("notify::text", self.on_label_row_changed)

        super_rows.append(self.top_label_row)
        super_rows.append(self.center_label_row)
        super_rows.append(self.bottom_label_row)
        return super_rows

    def _load_config_defaults(self):
        settings = self.get_settings()
        top = settings.get("labels", {}).get("top", "")
        center = settings.get("labels", {}).get("center", "")
        bottom = settings.get("labels", {}).get("bottom", "")

        self.top_label_row.set_text(top)
        self.center_label_row.set_text(center)
        self.bottom_label_row.set_text(bottom)

    def on_label_row_changed(self, entry, *args):
        settings = self.get_settings()
        settings.setdefault("labels", {})
        settings["labels"]["top"] = self.top_label_row.get_text()
        settings["labels"]["center"] = self.center_label_row.get_text()
        settings["labels"]["bottom"] = self.bottom_label_row.get_text()

        self.set_settings(settings)
        self.show()

    def on_ready(self) -> None:
        self.show()

    def on_tick(self):
        self.show()
        
    def on_key_down(self):
        settings = self.plugin_base.get_settings()

        self.plugin_base.ph.disable(settings.get("time", 0))

        self.show()

    def inject_data(self, label: str, data: dict) -> str:
        for key in data:
            value = data[key]
            if key in ["gravity_last_updated"]:
                continue

            if isinstance(value, float):
                value = round(value)
            
            label = label.replace("{" + key + "}", str(value))
        return label

    def show(self) -> None:
        settings = self.get_settings()
        def _show(self: "Info"):
            status = self.plugin_base.ph.get_summary()
            if status is None:
                return

            if status.get("status") is None:
                self.set_media(media_path=os.path.join(self.plugin_base.PATH, "assets", "no-connection.png"), size=0.85)
            elif status.get("status") == "enabled":
                self.set_media(media_path=os.path.join(self.plugin_base.PATH, "assets", "active.png"), size=0.85)
            else:
                self.set_media(media_path=os.path.join(self.plugin_base.PATH, "assets", "inactive.png"), size=0.85)

            top = self.inject_data(settings.get("labels", {}).get("top", ""), status)
            center = self.inject_data(settings.get("labels", {}).get("center", ""), status)
            bottom = self.inject_data(settings.get("labels", {}).get("bottom", ""), status)

            self.set_top_label(top, font_size=14)
            self.set_center_label(center, font_size=14)
            self.set_bottom_label(bottom, font_size=14)

        thread = threading.Thread(target=_show, args=(self,), daemon=True, name="show")
        thread.start()

    def get_custom_config_area(self):
        label = Gtk.Label(
            use_markup=True,
            label = f"{self.plugin_base.lm.get('actions.info.link.label')} <a href=\"https://github.com/StreamController/Pi-Hole\">{self.plugin_base.lm.get('actions.info.link.text')}</a>"        )
        return label