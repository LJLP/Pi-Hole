# Import StreamController modules
from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.PluginManager.ActionHolder import ActionHolder
from src.backend.DeckManagement.InputIdentifier import Input
from src.backend.PluginManager.ActionInputSupport import ActionInputSupport

# Import actions
from .actions.ToggleState.ToggleState import ToggleState
from .actions.Disable.Disable import Disable
from .actions.Info.Info import Info

from .PiHole import PiHole

class PiHolePlugin(PluginBase):
    def __init__(self):
        super().__init__()

        self.init_vars()

        ## Register actions
        self.disable_holder = ActionHolder(
            plugin_base = self,
            action_base = ToggleState,
            action_id_suffix = "ToggleState",
            action_name = self.lm.get("actions.toggle.name"),
            action_support={
                Input.Key: ActionInputSupport.SUPPORTED,
                Input.Dial: ActionInputSupport.SUPPORTED,
                Input.Touchscreen: ActionInputSupport.UNTESTED
            }
        )
        self.add_action_holder(self.disable_holder)

        self.disable_holder = ActionHolder(
            plugin_base = self,
            action_base = Disable,
            action_id_suffix = "Disable",
            action_name = self.lm.get("actions.disable.name"),
            action_support={
                Input.Key: ActionInputSupport.SUPPORTED,
                Input.Dial: ActionInputSupport.SUPPORTED,
                Input.Touchscreen: ActionInputSupport.UNTESTED
            }
        )
        self.add_action_holder(self.disable_holder)

        self.info_holder = ActionHolder(
            plugin_base = self,
            action_base = Info,
            action_id_suffix = "Info",
            action_name = self.lm.get("actions.info.name"),
            action_support={
                Input.Key: ActionInputSupport.SUPPORTED,
                Input.Dial: ActionInputSupport.SUPPORTED,
                Input.Touchscreen: ActionInputSupport.UNSUPPORTED
            }
        )
        self.add_action_holder(self.info_holder)

        # Register plugin
        self.register(
            plugin_name = self.lm.get("plugin.name"),
            github_repo = "https://github.com/StreamController/Pi-hole",
            plugin_version = "1.0.0",
            app_version = "1.4.10-beta"
        )

    def init_vars(self):
        self.lm = self.locale_manager

        settings = self.get_settings()
        self.ph = PiHole(
            ip_address=settings.get("ip"),
            api_token=settings.get("token")
        )