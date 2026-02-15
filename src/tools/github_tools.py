"""
GitHub Tools
Wrappers for PyGithub interactions
"""
import os
import logging
from github import Github, Auth
from github.Repository import Repository
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

def get_repo() -> Repository:
    """Get authenticated GitHub repository"""
    token = os.getenv("GITHUB_TOKEN")
    owner = os.getenv("GITHUB_REPO_OWNER")
    repo_name = os.getenv("GITHUB_REPO_NAME")
    
    if not token or not owner or not repo_name:
        logger.warning("GitHub credentials/config missing! Using mock mode.")
        return None
        
    auth = Auth.Token(token)
    g = Github(auth=auth)
    return g.get_repo(f"{owner}/{repo_name}")

def create_branch(branch_name: str, base: str = "main") -> str:
    """Create a new branch from base"""
    repo = get_repo()
    if not repo:
        logger.info(f"[MOCK] Created branch {branch_name} from {base}")
        return branch_name
        
    try:
        source_branch = repo.get_branch(base)
        repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=source_branch.commit.sha)
        logger.info(f"✅ Created branch {branch_name}")
        return branch_name
    except Exception as e:
        logger.error(f"Failed to create branch: {e}")
        # If branch exists, return it anyway?
        if "Reference already exists" in str(e):
             return branch_name
        raise

def create_pull_request(title: str, body: str, head: str, base: str = "main") -> dict:
    """Create a PR"""
    repo = get_repo()
    if not repo:
        return {
            "number": 101,
            "url": "https://github.com/mock/repo/pull/101",
            "status": "open"
        }
        
    try:
        pr = repo.create_pull(title=title, body=body, head=head, base=base)
        return {
            "number": pr.number,
            "url": pr.html_url,
            "status": pr.state
        }
    except Exception as e:
        logger.error(f"Failed to create PR: {e}")
        raise

def commit_file(branch: str, file_path: str, content: str, message: str) -> str:
    """Commit a file to the branch"""
    repo = get_repo()
    if not repo:
        logger.info(f"[MOCK] Committed {file_path} to {branch}")
        return "sha-mock-123"
        
    try:
        # Check if file exists to deciding create/update
        sha = None
        try:
            contents = repo.get_contents(file_path, ref=branch)
            # File exists -> Update
            res = repo.update_file(contents.path, message, content, contents.sha, branch=branch)
            sha = res['commit'].sha
            logger.info(f"✅ Updated {file_path} (SHA: {sha})")
        except Exception as e:
            # File likely doesn't exist -> Create
            # Note: get_contents raises UnknownObjectException (404) if not found
            logger.info(f"File {file_path} not found on {branch}, creating new...")
            res = repo.create_file(file_path, message, content, branch=branch)
            sha = res['commit'].sha
            logger.info(f"✅ Created {file_path} (SHA: {sha})")
            
        return sha
    except Exception as e:
        logger.error(f"Failed to commit file {file_path}: {e}")
        raise

def merge_pull_request(pr_number: int, merge_method: str = "squash") -> dict:
    """Merge a PR by number"""
    repo = get_repo()
    if not repo:
        logger.info(f"[MOCK] Merged PR #{pr_number}")
        return {"merged": True, "sha": "mock-merge-sha"}
        
    try:
        pr = repo.get_pull(pr_number)
        # merge_method can be 'merge', 'squash', or 'rebase'
        result = pr.merge(merge_method=merge_method)
        logger.info(f"✅ Merged PR #{pr_number}: {result.sha}")
        return {
            "merged": result.merged,
            "sha": result.sha,
            "message": result.message
        }
    except Exception as e:
        logger.error(f"Failed to merge PR #{pr_number}: {e}")
        raise

def is_pr_merged(pr_number: int) -> bool:
    """Check if a PR is merged"""
    repo = get_repo()
    if not repo:
        # Mock assumption: After some time, it is merged
        return True
        
    try:
        pr = repo.get_pull(pr_number)
        return pr.is_merged()
    except Exception as e:
        logger.error(f"Failed to check PR #{pr_number} status: {e}")
        return False

def find_pr_for_branch(branch_name: str) -> dict:
    """Find an existing PR for a branch"""
    repo = get_repo()
    if not repo:
        return None
        
    try:
        # Get all PRs for this branch
        pulls = repo.get_pulls(state='all', head=f"{os.getenv('GITHUB_REPO_OWNER')}:{branch_name}")
        for pr in pulls:
            # If PR is closed and NOT merged, it was closed without merging (abandoned). 
            # We should ignore it and allow a new one to be created.
            if pr.state == 'closed' and not pr.merged:
                continue
                
            return {
                "number": pr.number,
                "url": pr.html_url,
                "status": pr.state, # open, closed
                "merged": pr.merged
            }
        return None
    except Exception as e:
        logger.error(f"Failed to find PR for {branch_name}: {e}")
        return None
