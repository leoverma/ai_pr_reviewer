SwiftReview AI - Full MVP (Mock AI)

This project is a ready-to-run MVP of a GitHub App that reviews iOS PRs.
It uses a mock AI pipeline for safe, free testing of GitHub integration.

Setup:
1. Copy .env.example to .env and set values (WEBHOOK_SECRET, GITHUB_APP_ID, GITHUB_PRIVATE_KEY_PATH)
2. Place your GitHub App private key PEM at the path referenced in .env
3. Create a Python virtualenv and install requirements:
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
4. Run the server:
   uvicorn app:app --reload --port 8000
5. Expose via ngrok for GitHub: ngrok http 8000
6. Configure GitHub App webhook URL to https://<ngrok-id>.ngrok.io/webhook/github
7. Install the GitHub App on a repo and create a PR with Swift changes to test.
