from fastapi import FastAPI, Request
from git import Repo
from pathway_engine.config import WATCH_FOLDER, GITHUB_BRANCH
import os

def create_github_webhook_app():
    """
    Returns a FastAPI app handling GitHub webhooks.
    """

    app = FastAPI()

    @app.post("/github-webhook")
    async def github_webhook(req: Request):
        payload = await req.json()

        # Only respond to pushes on main branch
        if payload.get("ref") != f"refs/heads/{GITHUB_BRANCH}":
            return {"status": "ignored"}

        git_dir = os.path.join(WATCH_FOLDER, ".git")
        if not os.path.exists(git_dir):
            return {"error": "Repo not initialized in WATCH_FOLDER"}

        try:
            repo = Repo(WATCH_FOLDER)
            repo.remotes.origin.pull()
            return {"status": "repo updated"}
        except Exception as e:
            return {"error": str(e)}

    return app
