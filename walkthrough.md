# Project Walkthrough: Autonomous Developer Agent

## Overview
This agent automates the flow from **Jira Ticket** to **Merged Code**.

## Workflow Demo

1.  **Trigger**: User moves a Jira Story (e.g., `SCRUM-3`) to **"In Progress"**.
    -   *Agent detects the webhook event.*
2.  **Planning**: Agent analyzes the story description and creates an implementation plan.
3.  **Coding**:
    -   Agent creates a feature branch (e.g., `feature/SCRUM-3-add-login-1707...`).
    -   Agent writes code and commits it to GitHub.
4.  **PR Creation**:
    -   Agent creates a Pull Request on GitHub.
    -   Agent updates Jira ticket to **"Ready for Test"**.
5.  **Review & Merge**:
    -   User reviews the PR on GitHub and clicks **Merge**.
6.  **Completion**:
    -   Agent detects the merge.
    -   Agent updates Jira ticket to **"Done"**.

## recent Fixes & Improvements

-   **Infinite Loop Prevention**: Agent strictly checks status ("In Progress") and won't re-trigger on its own updates.
-   **Idempotency**: Branch names include timestamps to prevent collisions with old runs.
-   **Robust Error Handling**:
    -   Stops immediately if Code Generation fails (no empty PRs).
    -   Stops if PR creation fails (no premature Jira updates).
-   **Rate Limit Awareness**: Verified GitHub API usage.

## Artifacts
-   `src/agent/workflow.py`: Main LangGraph logic.
-   `src/tools/`: Integration tools for Jira/GitHub.
-   `scripts/debug/`: Collection of verification scripts.
