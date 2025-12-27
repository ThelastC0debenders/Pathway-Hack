from fastapi import FastAPI, Request
from git import Repo, GitCommandError
import os

from pathway_engine.config import (
    WATCH_FOLDER,
    GITHUB_BRANCH,
    GITHUB_REPO_URL,
)


def _ensure_repo_initialized():
    """
    Clone repo once if it does not exist.
    """
    os.makedirs(WATCH_FOLDER, exist_ok=True)

    git_dir = os.path.join(WATCH_FOLDER, ".git")
    if not os.path.exists(git_dir):
        print("🚀 Cloning repository into WATCH_FOLDER")
        Repo.clone_from(
            GITHUB_REPO_URL,
            WATCH_FOLDER,
            branch=GITHUB_BRANCH,
        )
    else:
        print("ℹ️ Repo already present")


def create_github_webhook_app() -> FastAPI:
    app = FastAPI()

    @app.post("/github-webhook")
    async def github_webhook(req: Request):
        try:
            payload = await req.json()
            event = req.headers.get("X-GitHub-Event")

            print("\n🔥 GitHub webhook received:", event)

            # Only repo-changing events
            if event == "push":
                ref = payload.get("ref")
                if ref != f"refs/heads/{GITHUB_BRANCH}":
                    return {"status": "ignored branch"}

            elif event == "pull_request":
                if not payload.get("pull_request", {}).get("merged", False):
                    return {"status": "ignored unmerged PR"}

            elif event not in {"create", "delete", "release"}:
                return {"status": f"ignored event {event}"}

            _ensure_repo_initialized()

            repo = Repo(WATCH_FOLDER)
            repo.remotes.origin.pull()

            print("✅ Repository pulled successfully")
            return {"status": "repo updated"}

        except GitCommandError as e:
            print("❌ Git error:", e)
            return {"error": "git failure"}

        except Exception as e:
            print("❌ Webhook error:", e)
            return {"error": str(e)}

    return app
