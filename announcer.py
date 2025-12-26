import os
from alerts.allstar_control import AllStarController

class AlertAnnouncer:
    def __init__(self, config, logger):
        self.logger = logger
        self.controller = AllStarController(
            config["allstar"]["node"], logger
        )
        self.audio_path = config["audio"]["path"]
        self.tones = config.get("tones", {})

    def _get_tones(self, event):
        default = self.tones.get("default", {"start": 3, "end": 3})
        event_tones = self.tones.get(event, {})
        return (
            event_tones.get("start", default["start"]),
            event_tones.get("end", default["end"])
        )

    def announce(self, event):
        start, end = self._get_tones(event)
        self.controller.courtesy_tone(start)

        wav = f"alert_{event.lower().replace(' ', '_')}.wav"
        path = os.path.join(self.audio_path, wav)

        if os.path.exists(path):
            self.controller.play_file(path)
        else:
            self.controller.say_text(event)

        self.controller.courtesy_tone(end)

    def clear(self):
        self.controller.courtesy_tone(2)
        self.controller.say_text("Weather alert cleared")
