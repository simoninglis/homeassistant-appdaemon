import appdaemon.plugins.hass.hassapi as hass
import time


class SleepTimer(hass.Hass):
    def initialize(self):
        self.listen_state(self.sleep_timer, "input_boolean.sleep_timer")
        self.timer_handle = None


    def sleep_timer(self, entity, attribute, old, new, kwargs):
        if new == "on":
            self.log("Sleep timer turned on")
            timer_duration = self.get_state("input_select.sleep_timer_duration") * 60
            self.timer_handle = self.run_in(self.time_up, timer_duration)
        else:
            self.log("Sleep timer cancelled")
            if self.timer_handle is not None:
                self.cancel_timer(self.timer_handle)
                self.timer_handle = None


    def time_up(self, kwargs):
        self.log("Time up")
        self.turn_off("media_player.apple_tv")
        self.turn_off("switch.master_entertainment_switch")
        self.turn_off("input_boolean.sleep_timer")
        self.timer_handle = None







