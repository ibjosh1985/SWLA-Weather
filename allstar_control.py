import subprocess

class AllStarController:
    def __init__(self, node, logger):
        self.node = node
        self.logger = logger

    def _run(self, cmd):
        try:
            subprocess.run(
                ["asterisk", "-rx", cmd],
                timeout=5,
                check=True
            )
        except Exception as e:
            self.logger.error(f"Asterisk command failed: {e}")

    def courtesy_tone(self, tone):
        self._run(f"rpt tone {self.node} {tone}")

    def play_file(self, path):
        self._run(f"rpt playback {self.node} {path}")

    def say_text(self, text):
        self._run(f'rpt say "{self.node}" "{text}"')
