# Implementation Plan - Autonomous Agentic SDLC Platform

## Goal Description
Build an end-to-end Autonomous Agentic System that automates the software development lifecycle triggered by Jira ticket status changes.
**Flow:** Jira Task "In Progress" -> Agent Plans -> Codes -> Tests -> PR -> Review -> Merge -> Jira "Done".
**Reference:** This plan is aligned with `Guide_Azure_Platform_Setup.md`.

## User Review Required
> [!NOTE]
> **Azure Guide Found**: I have aligned this plan with the provided `Guide_Azure_Platform_Setup.md`.
> **Prerequisites**: Please ensure you have your Azure OpenAI Endpoint, Jira API Token, and GitHub Token ready for the `.env` file configuration.

## Proposed Architecture
We will use **LangGraph** for orchestration as defined in the guide.
**Stack**: Python 3.11, LangGraph, LangChain, Jira API, PyGithub, Azure OpenAI (GPT-4o).

### Agent Workflow (DAG)
1.  **Trigger**: Jira Webhook/Polling detects "In Progress".
2.  **Analysis**: Fetch Story, AC, and gather Codebase Context (RAG).
3.  **Planning**: Generate detailed implementation plan.
4.  **Development**:
    - Create Feature Branch.
    - Generate Code & Design Doc.
    - Generate Unit Tests.
5.  **Validation**:
    - Run Unit Tests.
    - Run SonarLint/SonarQube (Optional Phase 1).
    - **Loop**: Fix errors if validation fails.
6.  **Review**:
    - Create Pull Request.
    - Handle Reviewer Comments (Simulated or Human).
7.  **Completion**:
    - Merge PR.
    - Update Jira to "Done".

## Proposed Changes

### Project Structure (Matched to Guide)
#### [NEW] [scaffolding](file:///C:/Users/nikhi/OneDrive/Documents/AutnomousAgenticDevelopment/src)
- `src/main.py`: Entry point.
- `src/agent/`:
    - `state.py`: `DevelopmentState` definition.
    - `workflow.py`: LangGraph StateMachine.
    - `nodes/`: `trigger.py`, `planning.py`, `coding.py`, `testing.py`, `pr.py`.
    - `edges/`: `conditions.py`.
- `src/tools/`: `jira_tools.py`, `github_tools.py`, `llm_tools.py`.
- `src/config/`: `settings.py` (Env vars).
- `src/utils/`: `logger.py`, `helpers.py`.

### Configuration
#### [NEW] [.env.example](file:///C:/Users/nikhi/OneDrive/Documents/AutnomousAgenticDevelopment/.env.example)
- Standard Azure/Jira/GitHub credentials template.

## Verification Plan

### Automated Tests
- `tests/unit/test_state.py`: Verify State transitions.
- `tests/unit/test_tools.py`: Mock API calls for Jira/GitHub.
- `tests/integration/test_workflow.py`: End-to-end flow simulation (Dry Run).

### Manual Verification
1.  **Setup Check**: Verify `.env` loads correctly.
2.  **Dry Run**: Execute `main.py` with a dummy Jira Story ID.
3.  **Output Check**:
    - Console logs showing "Trigger received", "Plan created", "Code generated".
    - GitHub: Verify feature branch creation (if credentials provided).
