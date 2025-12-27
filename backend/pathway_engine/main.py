import pathway as pw
import threading
import signal
import sys
import uvicorn

from pathway_engine.ingestion.local_source import watch_local_folder
from pathway_engine.ingestion.github_source import create_github_webhook_app
from pathway_engine.ingestion.github_source import _ensure_repo_initialized
from pathway_engine.state.version_tracker import VersionTracker
from pathway_engine.config import WATCH_FOLDER


class PathwayEngine:
    """
    Long-running Pathway engine.
    Designed to stay alive and react to live data updates.
    """

    def __init__(self, folder_path: str):
        self.folder_path = folder_path
        self.table = None
        self.version_tracker = VersionTracker()

    def start(self):
        self.table = watch_local_folder(self.folder_path)
        print("Pathway live engine initialized")

        pw.io.csv.write(self.table, "pathway_output")


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


    # ---- APIs for Person-2 ----
    def get_live_table(self):
        return self.table

    def get_latest_version(self, content: str):
        self.version_tracker.update(content)
        return self.version_tracker.get_version()


def _graceful_shutdown(signum, frame):
    print("Pathway Engine Shutdown")
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, _graceful_shutdown)
    signal.signal(signal.SIGTERM, _graceful_shutdown)
    print("Pathway Engine Started")

    engine = PathwayEngine(WATCH_FOLDER)

    _ensure_repo_initialized()
    engine.start()
    pw.run()
