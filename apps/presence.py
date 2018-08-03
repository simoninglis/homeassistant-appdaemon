import appdaemon.plugins.hass.hassapi as hass


class Presence(hass.Hass):
    def initialize(self):
        self.log("Initialising")
        self.sensor = "binary_sensor.someone_home"
        self.log("Listening to {0}".format(self.sensor))
        self.listen_state(self.arrival_departure, self.sensor)

    def arrival_departure(self, entity, attribute, old, new, kwargs):
        self.log("Arrival or departure event on sensor {0}. New: {1}.  Old {2}.".format(self.sensor,new,old))
        if new == old:
            self.log("Skipping. Sensor new value == old.")
            return
        if self.now_is_between("sunset - 00:45:00", "sunrise + 00:00:45"):
            self.log("It's after sunset and before sunrise")
            if new == 'on':
                self.log("Somone is home. Runing evening script")
                # self.turn_on("script.evening")
            else:
                self.log("Somone has left. Runing away night script")
                # self.turn_on("script.away_night")
        else:
            self.log("It's after sunrise and before sunset")
            if new == 'on':
                self.log("Somone is home. Runing daytime script")
                # self.turn_on("script.daytime")
            else:
                self.log("Somone has left. Runing away script")
                # self.turn_on("script.away")
