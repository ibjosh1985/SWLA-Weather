import json
import os
from datetime import datetime, timezone

STATE_FILE = "/var/lib/swla/alert_state.json"

class AlertState:
    def __init__(self):
        os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
        self.state = self._load()

    def _load(self):
        if not os.path.exists(STATE_FILE):
            return {}
        with open(STATE_FILE) as f:
            return json.load(f)

    def save(self):
        with open(STATE_FILE, "w") as f:
            json.dump(self.state, f)

    def is_new(self, alert_id):
        return alert_id not in self.state

    def add(self, alert_id, expires):
        self.state[alert_id] = expires
        self.save()

    def expired_alerts(self):
        now = datetime.now(timezone.utc)
        expired = []
        for aid, exp in list(self.state.items()):
            if exp and datetime.fromisoformat(exp.replace("Z","+00:00")) <= now:
                expired.append(aid)
        return expired

    def remove(self, alert_id):
        self.state.pop(alert_id, None)
        self.save()
