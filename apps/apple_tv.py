import appdaemon.plugins.hass.hassapi as hass
import time


class AbcNews(hass.Hass):
    def initialize(self):
        self.entity_trigger = self.args['entity_trigger']
        self.listen_state(self.do_it, self.entity_trigger)
        self.entity_apple_tv = self.args['entity_apple_tv']


    def do_it(self, entity, attribute, old, new, kwargs):
        if new == "on":
            self.log("Starting")
            self.call_service("remote/send_command", entity_id=self.entity_apple_tv, command="top_menu")
            time.sleep(2)
            self.call_service("remote/send_command", entity_id=self.entity_apple_tv, command="menu")
            time.sleep(1)
            self.call_service("remote/send_command", entity_id=self.entity_apple_tv, command="down")
            time.sleep(1)
            self.call_service("remote/send_command", entity_id=self.entity_apple_tv, command="select")
            time.sleep(5)
            self.call_service("remote/send_command", entity_id=self.entity_apple_tv, command="down")
            for i in range(20):
                self.call_service("remote/send_command", entity_id=self.entity_apple_tv, command="up")
                time.sleep(.2)
            self.call_service("remote/send_command", entity_id=self.entity_apple_tv, command="down")
            time.sleep(.2)
            self.call_service("remote/send_command", entity_id=self.entity_apple_tv, command="down")
            time.sleep(.2)
            self.call_service("remote/send_command", entity_id=self.entity_apple_tv, command="down")
            time.sleep(.2)
            self.call_service("remote/send_command", entity_id=self.entity_apple_tv, command="down")
            time.sleep(.2)
            self.call_service("remote/send_command", entity_id=self.entity_apple_tv, command="select")
            time.sleep(.2)
            self.call_service("remote/send_command", entity_id=self.entity_apple_tv, command="select")
            self.turn_off(entity)
            self.log("Finished")
