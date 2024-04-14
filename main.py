# Import StreamController modules
from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.PluginManager.ActionHolder import ActionHolder

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
            action_id = "dev_core447_Pi-hole::ToggleState",
            action_name = "Toggle State",
        )
        self.add_action_holder(self.disable_holder)

        self.disable_holder = ActionHolder(
            plugin_base = self,
            action_base = Disable,
            action_id = "dev_core447_Pi-hole::Disable",
            action_name = "Disable",
        )
        self.add_action_holder(self.disable_holder)

        self.info_holder = ActionHolder(
            plugin_base = self,
            action_base = Info,
            action_id = "dev_core447_Pi-hole::Info",
            action_name = self.lm.get("actions.info.name")
        )
        self.add_action_holder(self.info_holder)

        # Register plugin
        self.register(
            plugin_name = "Pi-hole",
            github_repo = "https://github.com/StreamController/Pi-hole",
            plugin_version = "1.0.0",
            app_version = "1.1.1-alpha"
        )

    def init_vars(self):
        self.lm = self.locale_manager

        settings = self.get_settings()
        self.ph = PiHole(
            ip_address=settings.get("ip"),
            api_token=settings.get("token")
        )