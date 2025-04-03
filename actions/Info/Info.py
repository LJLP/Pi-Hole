# Import StreamController modules
import threading
import typing
import six
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

import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

class Info(HoleActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
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

            if isinstance(value, float):
                value = round(value)
            
            label = label.replace("{" + key + "}", str(value))
        return label

    def show(self) -> None:
        settings = self.get_settings()
        def _show(self: "Info"):
            def _construct_key(previous_key, separator, new_key, replace_separators=None):
                """
                Returns the new_key if no previous key exists, otherwise concatenates
                previous key, separator, and new_key
                :param previous_key:
                :param separator:
                :param new_key:
                :param str replace_separators: Replace separators within keys
                :return: a string if previous_key exists and simply passes through the
                new_key otherwise
                """
                if replace_separators is not None:
                    new_key = str(new_key).replace(separator, replace_separators)
                if previous_key:
                    return u"{}{}{}".format(previous_key, separator, new_key)
                else:
                    return new_key

            def flatten(
                        nested_dict,
                        separator="_",
                        root_keys_to_ignore=None,
                        replace_separators=None):
                    """
                    Flattens a dictionary with nested structure to a dictionary with no
                    hierarchy
                    Consider ignoring keys that you are not interested in to prevent
                    unnecessary processing
                    This is specially true for very deep objects

                    :param nested_dict: dictionary we want to flatten
                    :param separator: string to separate dictionary keys by
                    :param root_keys_to_ignore: set of root keys to ignore from flattening
                    :param str replace_separators: Replace separators within keys
                    :return: flattened dictionary
                    """
                    log.debug(f"flatten called with type: {type(nested_dict)}, value: {nested_dict}")
                    
                    assert isinstance(nested_dict, dict), "flatten requires a dictionary input"
                    assert isinstance(separator, six.string_types), "separator must be string"

                    if root_keys_to_ignore is None:
                        root_keys_to_ignore = set()

                    if len(nested_dict) == 0:
                        return {}

                    # This global dictionary stores the flattened keys and values and is
                    # ultimately returned
                    flattened_dict = dict()

                    def _flatten(object_, key):
                        """
                        For dict, list and set objects_ calls itself on the elements and for
                        other types assigns the object_ to
                        the corresponding key in the global flattened_dict
                        :param object_: object to flatten
                        :param key: carries the concatenated key for the object_
                        :return: None
                        """
                        # Empty object can't be iterated, take as is
                        if not object_:
                            flattened_dict[key] = object_
                        # These object types support iteration
                        elif isinstance(object_, dict):
                            for object_key in object_:
                                if not (not key and object_key in root_keys_to_ignore):
                                    _flatten(
                                        object_[object_key],
                                        _construct_key(
                                            key,
                                            separator,
                                            object_key,
                                            replace_separators=replace_separators))
                        elif isinstance(object_, (list, set, tuple)):
                            for index, item in enumerate(object_):
                                _flatten(
                                    item,
                                    _construct_key(
                                        key,
                                        separator,
                                        index,
                                        replace_separators=replace_separators))
                        # Anything left take as is
                        else:
                            flattened_dict[key] = object_

                    _flatten(nested_dict, None)
                    return flattened_dict

            status = self.plugin_base.ph.get_summary()
            if status is None:
                return
            
            status = flatten(status)  # Flatten the nested dictionary

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