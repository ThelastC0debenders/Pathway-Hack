from fastapi import FastAPI, Request
from git import Repo
import os

from pathway_engine.config import (
    WATCH_FOLDER,
    GITHUB_BRANCH,
    GITHUB_REPO_URL,
)


def _ensure_repo_initialized():
    """
    Clone the repository if it does not exist.
    Runs ONLY once on the first valid webhook event.
    """
    git_dir = os.path.join(WATCH_FOLDER, ".git")

    print("🔍 Checking repository state")
    print("   WATCH_FOLDER:", os.path.abspath(WATCH_FOLDER))
    print("   GITHUB_REPO_URL:", GITHUB_REPO_URL)
    print("   GITHUB_BRANCH:", GITHUB_BRANCH)

    if not os.path.exists(git_dir):
        print("🚀 Repository not found. Cloning now...")
        Repo.clone_from(
            GITHUB_REPO_URL,
            WATCH_FOLDER,
            branch=GITHUB_BRANCH,
        )
        print("✅ Repository cloned successfully")
    else:
        print("ℹ️ Repository already exists")


def create_github_webhook_app() -> FastAPI:
    """
    Creates a FastAPI app that listens to GitHub webhooks.
    """
    app = FastAPI()

    @app.post("/github-webhook")
    async def github_webhook(req: Request):
        print("\n🔥 GitHub webhook received")

        payload = await req.json()
        event_type = req.headers.get("X-GitHub-Event")

        print("   Event type:", event_type)

        # ----------------------------
        # Decide whether to act
        # ----------------------------

        if event_type == "push":
            ref = payload.get("ref")
            print("   Push ref:", ref)

            if ref != f"refs/heads/{GITHUB_BRANCH}":
                print("   ❌ Ignored: wrong branch")
                return {"status": "ignored branch"}

        elif event_type == "pull_request":
            merged = payload.get("pull_request", {}).get("merged", False)
            print("   PR merged:", merged)

            if not merged:
                print("   ❌ Ignored: PR not merged")
                return {"status": "ignored non-merged PR"}

        elif event_type in {"create", "delete", "release"}:
            print("   Repo structure change event")

        else:
            print("   ❌ Ignored: non repo-mutating event")
            return {"status": f"ignored event {event_type}"}

        # ----------------------------
        # Clone or pull repo
        # ----------------------------

        try:
            _ensure_repo_initialized()

            repo = Repo(WATCH_FOLDER)
            repo.remotes.origin.pull()

            print("✅ Repository pulled successfully")
            return {"status": f"repo updated via {event_type}"}

        except Exception as e:
            print("❌ Git operation failed:", e)
            return {"error": str(e)}

    return app
