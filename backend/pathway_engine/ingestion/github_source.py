@ app.post("/github-webhook")
async def github_webhook(req: Request):
    payload = await req.json()
    event_type = req.headers.get("X-GitHub-Event")

    # Events that actually change repo content
    REPO_MUTATING_EVENTS = {
        "push",
        "pull_request",
        "create",        # branch created
        "delete",        # branch deleted
        "release",
    }

    if event_type not in REPO_MUTATING_EVENTS:
        return {"status": f"ignored event {event_type}"}

    # For push & PR merge, check branch
    ref = payload.get("ref")
    if ref and ref != f"refs/heads/{GITHUB_BRANCH}":
        return {"status": "ignored branch"}

    try:
        _ensure_repo_initialized()
        repo = Repo(WATCH_FOLDER)
        repo.remotes.origin.pull()
        return {"status": f"repo updated via {event_type}"}

    except Exception as e:
        return {"error": str(e)}
