import appdaemon.plugins.hass.hassapi as hass
import time


class DelayedSwitchesScene(hass.Hass):
    def initialize(self):
        self.timer_handle = None
        self.timer_duration = self.args['timer_duration']
        self.entities_off = self.args['entities_off']
        self.entites_on = self.args['entities_off']
        if 'entity_trigger' in self.args:
            self.entity_trigger = self.args['entity_trigger']
            self.listen_state(self.sleep_timer, self.entity_trigger)
        else:
            self.entity_trigger = None
            self.sleep_timer(None, None, None, None, None)


    def sleep_timer(self, entity, attribute, old, new, kwargs):
        if new == "on":
            self.log("Timer started")
            self.timer_handle = self.run_in(self.time_up, self.timer_duration)
        else:
            self.log("Timer cancelled")
            if self.timer_handle is not None:
                self.cancel_timer(self.timer_handle)
                self.timer_handle = None


    def time_up(self, kwargs):
        self.log("Timer up")
        for entity in self.entities_off:
            self.turn_off(entity)
        for entity in self.entities_on:
            self.turn_on(entity)
        # turn off the entity we are listening for
        if self.entity_trigger:
            self.turn_off(self.entity_trigger)
        self.timer_handle = None
