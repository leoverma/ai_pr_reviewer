import asyncio
import json
from github_auth import get_installation_token
from download_patch import download_diff
from diff_parser import parse_diff
from ai_pipeline import review_diff
from post_comments import post_summary_comment, post_file_comments

_queue = asyncio.Queue()

async def enqueue_job(job: dict):
    await _queue.put(job)
    return True

async def process_job(job: dict):
    try:
        installation_id = job.get("installation_id")
        if not installation_id:
            print("No installation id available for job", job)
            return
        token = await get_installation_token(installation_id)
        diff_text = await download_diff(job["diff_url"], token)
        swift_files = parse_diff(diff_text)
        all_issues = []
        for f in swift_files:
            res = await review_diff(f["diff"])
            if res.get("status") == "issues_found":
                for iss in res["issues"]:
                    iss["file"] = f["file_path"]
                    all_issues.append(iss)
        owner, repo = job["repo"].split("/")
        if all_issues:
            await post_summary_comment(owner, repo, job["pr_number"], token, all_issues)
            await post_file_comments(owner, repo, job["pr_number"], token, all_issues)
        else:
            await post_summary_comment(owner, repo, job["pr_number"], token, [])
        print(f"Processed PR {job['pr_number']} for {job['repo']}")
    except Exception as e:
        print("Error processing job:", e)

async def worker_loop():
    print("Worker started")
    while True:
        job = await _queue.get()
        try:
            await process_job(job)
        except Exception as e:
            print("worker error:", e)
        finally:
            _queue.task_done()

def start_background_worker(loop):
    loop.create_task(worker_loop())
