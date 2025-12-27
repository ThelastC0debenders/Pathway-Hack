import pathway as pw
import threading
import signal
import sys
import uvicorn

from pathway_engine.ingestion.local_source import watch_local_folder
from pathway_engine.ingestion.github_source import create_github_webhook_app
from pathway_engine.config import WATCH_FOLDER
from pathway_engine.state.version_tracker import VersionTracker


class PathwayEngine:
    def __init__(self, folder_path: str):
        self.folder_path = folder_path
        self.table = None
        self.version_tracker = VersionTracker()

    def start(self):
        # Start Pathway filesystem watcher
        self.table = watch_local_folder(self.folder_path)
        print("Pathway live engine initialized")

        # Persist output (debug / proof)
        pw.io.csv.write(self.table, "pathway_output")

        # Start GitHub webhook server
        webhook_app = create_github_webhook_app()
        threading.Thread(
            target=lambda: uvicorn.run(
                webhook_app,
                host="0.0.0.0",
                port=8000,
                log_level="warning",
            ),
            daemon=True,
        ).start()

        print("GitHub webhook server running")

    # -------- APIs for Person 2 / 3 --------
    def get_live_table(self):
        return self.table

    def get_latest_version(self, content: str):
        self.version_tracker.update(content)
        return self.version_tracker.get_version()


# 🔥 SINGLETON ENGINE (IMPORTANT)
engine = PathwayEngine(WATCH_FOLDER)


def _graceful_shutdown(signum, frame):
    print("Pathway Engine Shutdown")
    sys.exit(0)


def run_engine():
    signal.signal(signal.SIGINT, _graceful_shutdown)
    signal.signal(signal.SIGTERM, _graceful_shutdown)

    print("🚀 Pathway Engine Started")
    engine.start()
    pw.run(monitoring_level=pw.MonitoringLevel.NONE)

engine=None
if __name__ == "__main__":
    engine = PathwayEngine(WATCH_FOLDER)
    engine.start()
    pw.run(monitoring_level=pw.MonitoringLevel.NONE)