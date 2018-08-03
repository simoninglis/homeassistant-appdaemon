import appdaemon.plugins.hass.hassapi as hass
import time


class SceneNight(hass.Hass):
    def initialize(self):
        self.listen_state(self.sleep_timer, "input_boolean.scene_night")
        self.timer_handle = None


    def sleep_timer(self, entity, attribute, old, new, kwargs):
        if new == "on":
            self.log("Timer started")
            timer_duration = 2 * 60
            self.timer_handle = self.run_in(self.time_up, timer_duration)
        else:
            self.log("Timer cancelled")
            if self.timer_handle is not None:
                self.cancel_timer(self.timer_handle)
                self.timer_handle = None


    def time_up(self, kwargs):
        self.log("Timer up")
        self.turn_off("media_player.apple_tv")
        self.turn_off("switch.lounge_entertainment_switch")
        self.turn_off("light.lounge-dimmer_1")
        self.turn_off("light.lounge-dimmer_2")
        self.turn_off("switch.kitchen_relay_switch")
        self.turn_off("switch.kitchen_relay_switch_2")
        self.turn_off("switch.laundry_relay_switch")
        self.turn_off("switch.laundry_relay_switch_2")
        self.turn_off("switch.bathroom_relay_switch")
        self.turn_on("lock.front_door_locked")
        self.turn_off("input_boolean.scene_night")
        self.timer_handle = None
