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
    Clone the repository if it does not exist.
    Runs ONLY once on the first valid repo-mutating event.
    """
    git_dir = os.path.join(WATCH_FOLDER, ".git")

    print("\n🔍 Checking repository state")
    print("📁 WATCH_FOLDER:", os.path.abspath(WATCH_FOLDER))
    print("🌿 Target branch:", GITHUB_BRANCH)

    os.makedirs(WATCH_FOLDER, exist_ok=True)

    if not os.path.exists(git_dir):
        print("🚀 Repository not found — cloning now...")
        try:
            Repo.clone_from(
                GITHUB_REPO_URL,
                WATCH_FOLDER,
                branch=GITHUB_BRANCH,
            )
            print("✅ Repository cloned successfully")
        except Exception as e:
            print("❌ CLONE FAILED")
            print("   Error:", repr(e))
            raise
    else:
        print("ℹ️ Repository already exists — skipping clone")


def create_github_webhook_app() -> FastAPI:
    """
    FastAPI app handling GitHub webhooks.
    Reacts ONLY to repo-mutating events.
    """
    app = FastAPI()

    @app.post("/github-webhook")
    async def github_webhook(req: Request):
        payload = await req.json()
        event_type = req.headers.get("X-GitHub-Event")

        print("\n🔥 GitHub webhook received")
        print("   Event type:", event_type)

        # ----------------------------
        # Decide whether to react
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
        # Clone / Pull repository
        # ----------------------------

        try:
            print("➡️ Ensuring repository state")
            _ensure_repo_initialized()

            repo = Repo(WATCH_FOLDER)
            repo.remotes.origin.pull()

            print("✅ Repository updated successfully")
            return {"status": f"repo updated via {event_type}"}

        except GitCommandError as e:
            print("❌ Git operation failed")
            print("   Error:", e)
            return {"error": "git failure", "details": str(e)}

        except Exception as e:
            print("❌ Internal webhook error")
            print("   Error:", e)
            return {"error": "internal error", "details": str(e)}

    return app
