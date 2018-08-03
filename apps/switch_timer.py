import appdaemon.plugins.hass.hassapi as hass
import time


class SwitchTimer(hass.Hass):
    def initialize(self):
        self.listen_state(self.switch_timer, "switch.bathroom_relay_switch")
        self.timer_duration = 30 * 60
        self.timer_handle = None


    def switch_timer(self, entity, attribute, old, new, kwargs):
        if self.get_state('switch.bathroom_relay_switch_2') == "on":
            self.log("Switch on - fan on.  Ignore as the fan is already on")
            return
        if new == "on":
            self.log("Switch on - turning fan on")
            self.turn_on("switch.bathroom_relay_switch_2")
        else:
            self.log("Switch off, starting fan timer")
            self.timer_handle = self.run_in(self.time_up, self.timer_duration)


    def time_up(self, kwargs):
        self.log("Fan timer up.  Switching fan off")
        self.turn_off("switch.bathroom_relay_switch_2")
        self.timer_handle = None







