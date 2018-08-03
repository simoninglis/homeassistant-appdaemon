import appdaemon.plugins.hass.hassapi as hass
import time


class SwitchSensor(hass.Hass):
    def initialize(self):
        self.listen_state(self.sensor_update, "sensor.nodemanager_7_2")
        self.threshold_upper = 10
        self.threshold_lower = 5


    def sensor_update(self, entity, attribute, old, new, kwargs):
        bom_humidity = float(self.get_state("sensor.nodemanager_11_2"))
        self.log("Reference sensor humidity {0}".format(bom_humidity))
        on_threshold = bom_humidity + self.threshold_upper
        self.log("On threshold {0}".format(on_threshold))
        off_threshold = bom_humidity + self.threshold_lower
        self.log("Off threshold {0}".format(off_threshold))

        new = float(new)
        if new >= on_threshold:
            self.log("Sensor {0} > {1}. Switching fan on".format(new, on_threshold))
            self.turn_on("switch.bathroom_relay_switch_2")
        elif new <= off_threshold:
            self.log("Sensor {0} < {1}.  Switching fan off".format(new, off_threshold))
            self.turn_off("switch.bathroom_relay_switch_2")
        else:
            self.log("No change".format(off_threshold))








