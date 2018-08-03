import appdaemon.plugins.hass.hassapi as hass


class SceneSonosJoin(hass.Hass):
    def initialize(self):
        self.listen_state(self.do_it, "input_boolean.scene_sonos_join")
        self.device_entity_ids = [ "media_player.living_room", "media_player.kitchen", "media_player.office"]
        self.master_entity_id = "media_player.living_room"

    def do_it(self, entity, attribute, old, new, kwargs):
        if new == "on":
            self.log("Joining")
            self.call_service("media_player/sonos_join", data = {"master": master_entity_id}, entity_id = device_entity_ids)
        else:
            self.log("Splitting")
            self.call_service("media_player/sonos_unjoin", device_entity_ids)
