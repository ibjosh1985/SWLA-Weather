import requests
from alerts.announcer import AlertAnnouncer
from alerts.alert_state import AlertState

NWS_API = "https://api.weather.gov/alerts/active"

class NWSAlertMonitor:
    def __init__(self, config, logger):
        self.logger = logger
        self.states = config["nws"]["states"]
        self.announcer = AlertAnnouncer(config, logger)
        self.state = AlertState()

    def check_alerts(self):
        response = requests.get(
            NWS_API,
            params={"area": ",".join(self.states)},
            timeout=10
        )
        data = response.json()

        for feature in data.get("features", []):
            props = feature["properties"]
            alert_id = feature["id"]
            event = props.get("event", "").title().strip()
            severity = props.get("severity", "")
            expires = props.get("expires")

            if "Warning" not in event or severity not in ("Severe", "Extreme"):
                continue

            if self.state.is_new(alert_id):
                self.logger.warning(f"NEW WARNING: {event}")
                self.announcer.announce(event)
                self.state.add(alert_id, expires)

        for alert_id in self.state.expired_alerts():
            self.logger.info("Alert expired — clearing")
            self.announcer.clear()
            self.state.remove(alert_id)
