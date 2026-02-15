# Autonomous Developer Agent 🤖

This project implements an autonomous AI agent that manages the full software development lifecycle using Jira and GitHub.

## 🌟 Capabilities

-   **Jira Integration**: Detects tickets moving to "In Progress".
-   **Autonomous Coding**: Analyzes requirements, plans implementation, writes code, and runs tests.
-   **GitHub Integration**:
    -   Creates Feature Branches.
    -   Commits Code.
    -   **Creates Pull Requests**.
-   **Workflow Management**:
    -   Moves Jira ticket to **"Ready for Test"** when PR is created.
    -   Waits for **Manual Merge** of the PR.
    -   Moves Jira ticket to **"Done"** after merge is detected.

## 🚀 Getting Started

### Prerequisites

-   Python 3.10+
-   Jira Account (Cloud)
-   GitHub Account
-   [Ngrok](https://ngrok.com/) (for local webhooks)

### Installation

1.  Clone the repository.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Set up environment variables in `.env`:
    ```env
    OPENAI_API_KEY=sk-...
    JIRA_SERVER_URL=https://your-domain.atlassian.net
    JIRA_USERNAME=email@example.com
    JIRA_API_TOKEN=your-token
    GITHUB_TOKEN=your-pat
    GITHUB_REPO_OWNER=username
    GITHUB_REPO_NAME=repo-name
    ```

### Running the Agent

1.  **Start the Agent Server (LangGraph):**
    ```bash
    langgraph dev --port 2025
    ```

2.  **Start the Webhook Shim:**
    ```bash
    python src/webhook_server.py
    ```

3.  **Expose Webhook via Ngrok:**
    ```bash
    ngrok http 8000
    ```
    *Copy the HTTPS URL (e.g., `https://xyz.ngrok-free.app`) and configure it in your Jira System Webhooks settings.*

## 🛠️ Debugging

Debug scripts are located in `scripts/debug/` if you need to verify connections or simulating logic manually.

## 📄 License

MIT
