from fastapi import FastAPI, Request
from git import Repo
import os

from pathway_engine.config import WATCH_FOLDER, GITHUB_BRANCH, GITHUB_REPO_URL


def _ensure_repo_initialized():
    if not os.path.exists(os.path.join(WATCH_FOLDER, ".git")):
        Repo.clone_from(
            GITHUB_REPO_URL,
            WATCH_FOLDER,
            branch=GITHUB_BRANCH,
        )


def create_github_webhook_app() -> FastAPI:
    app = FastAPI()

    @app.post("/github-webhook")
    async def github_webhook(req: Request):
        payload = await req.json()
        event_type = req.headers.get("X-GitHub-Event")

        # Only events that MAY change repo state
        if event_type == "push":
            ref = payload.get("ref")
            if ref != f"refs/heads/{GITHUB_BRANCH}":
                return {"status": "ignored branch"}

        elif event_type == "pull_request":
            # Only react if PR is merged
            if not payload.get("pull_request", {}).get("merged", False):
                return {"status": "ignored non-merged PR"}

        elif event_type in {"create", "delete", "release"}:
            pass  # valid repo-changing events

        else:
            return {"status": f"ignored event {event_type}"}

        try:
            _ensure_repo_initialized()
            repo = Repo(WATCH_FOLDER)
            repo.remotes.origin.pull()
            return {"status": f"repo updated via {event_type}"}

        except Exception as e:
            return {"error": str(e)}

    return app
