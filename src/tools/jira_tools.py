"""
Jira Tools
Wrappers for Atlassian Jira interactions
"""
import os
import logging
from atlassian import Jira
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

def get_jira_client():
    """Get authenticated Jira client"""
    url = os.getenv("JIRA_SERVER_URL")
    username = os.getenv("JIRA_USERNAME")
    token = os.getenv("JIRA_API_TOKEN")
    
    if not url or not username or not token:
        logger.warning("Jira credentials missing! Using mock mode.")
        return None
        
    return Jira(
        url=url,
        username=username,
        password=token,
        cloud=True
    )

def get_story_details(story_id: str) -> dict:
    """Fetch story details from Jira"""
    jira = get_jira_client()
    if not jira:
        # Mock fallback
        return {
            "key": story_id,
            "fields": {
                "summary": "Mock Story: Add Login",
                "description": "As a user I want to login...",
                "customfield_12345": ["Acceptance Criteria 1", "AC 2"] # Example field
            }
        }
        
    try:
        issue = jira.issue(story_id)
        return issue
    except Exception as e:
        logger.error(f"Failed to fetch Jira issue {story_id}: {e}")
        raise

def transition_issue(story_id: str, transition_name: str) -> bool:
    """
    Transition an issue to a new status (e.g., 'Done', 'In Progress')
    """
    jira = get_jira_client()
    if not jira:
        logger.info(f"[MOCK] Transitioned {story_id} to {transition_name}")
        return True
        
    try:
        # Simply use the high-level method
        jira.set_issue_status(story_id, transition_name)
        logger.info(f"✅ Transitioned {story_id} to {transition_name}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to transition {story_id} to {transition_name}: {e}")
        return False
    except Exception as e:
        logger.error(f"Failed to transition {story_id} to {transition_name}: {e}")
        return False

def should_process_story(story_id: str) -> bool:
    """
    Check if story is in a valid state to start processing.
    Strictly enforces 'In Progress' status.
    """
    try:
        issue = get_story_details(story_id)
        if not issue:
            return False
            
        status = issue.get('fields', {}).get('status', {}).get('name', 'Unknown')
        logger.info(f"Story {story_id} is currently in status: '{status}'")
        
        # STRICT RULE: Only start if status is 'In Progress'
        # This prevents running on 'To Do', 'Ready for Test', 'Done', etc.
        allowed_statuses = ["In Progress"]
        
        if status not in allowed_statuses:
            logger.info(f"🛑 Skipping {story_id}: Status '{status}' is not in allowed triggers {allowed_statuses}")
            return False
            
        logger.info(f"✅ Status '{status}' is valid. Starting agent.")
        return True
    except Exception as e:
        logger.error(f"Error checking status for {story_id}: {e}")
        return False
