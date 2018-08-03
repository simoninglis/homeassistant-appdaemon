import appdaemon.plugins.hass.hassapi as hass

class DoorBell(hass.Hass):
    def initialize(self):
        self.listen_state(self.alert, "input_boolean.holidays")
        self.listen_state(self.alert, "binary_sensor.garage_1_line_crossing")
        self.speaker_entities = ["media_player.kitchen", "media_player.living_room"]
        self.master_speaker_entity= "media_player.living_room"
        self.light_entities = ["switch.front_entrance_exterior_switch"]
        self.media_player_entities = ["media_player.apple_tv"]
        self.timer_handles = {}
        self.in_progress = False

    # Play a TTS alert
    # If the current time is between sunset and sunrise and the front exteriod light is already off, 
    #   turn it on for 5 mins and then schedule it to turn off
    def alert(self, entity, attribute, old, new, kwargs):
        if self.in_progress:
            return
        else:
            self.in_progress = True
        self.log("DoorBell alert")
        if self.now_is_between("sunset - 00:45:00", "sunrise + 00:00:45"):
            for entity_id in self.light_entities:
                if self.get_state(entity_id) == "off":
                    self.log("Turn on light {}".format(entity_id))
                    self.turn_on(entity_id)
                    self.log("Schedule turn off light {}".format(entity_id))
                    self.timer_handles[entity_id] = self.run_in(self.light_turn_off, 60 * 5, entity_id=entity_id)
                self.log("Light {} already on.  Ignoring.".format(entity_id))


        for entity_id in self.media_player_entities:
            if self.get_state(entity_id) == "playing":
              self.log("Pause media player {}".format(entity_id))
              self.turn_off(entity_id)
              self.log("Schedule play {}".format(entity_id))
              self.timer_handles[entity_id] = self.run_in(self.media_player_resume, 60 * 5, entity_id=entity_id)
            self.log("Media player {} not playing. Ignoring.".format(entity_id))


        self.log("Save sonos state")
        self.call_service("media_player/sonos_snapshot", with_group="yes")
        self.log("Sonos join {}".format(",".join(self.speaker_entities)))
        self.call_service("media_player/sonos_join", master=self.master_speaker_entity, entity_id=self.speaker_entities)
        self.log("TTS")
        self.call_service("tts/google_say", message= "Someone approaches the front gate")
        self.log("Restore sonos state")
        self.call_service("media_player/sonos_unjoin", entity_id=self.master_speaker_entity)
        self.call_service("media_player/sonos_restore", with_group="yes")
        self.in_progress = False


    def light_turn_off(self, kwargs):
        entity_id = kwargs['entity_id']
        self.log("Turn off light {}".format(entity_id))
        self.turn_off(entity_id)
        self.timer_handles[entity_id] = None

    def media_player_resume(self, kwargs):
        entity_id = kwargs['entity_id']
        self.log("Resume playing media player {}".format(entity_id))
        self.turn_on(entity_id)
        self.timer_handles[entity_id] = None







