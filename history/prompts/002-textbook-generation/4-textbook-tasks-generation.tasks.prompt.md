---
id: 4
title: textbook-tasks-generation
stage: tasks
date: 2025-12-10
surface: agent
model: qwen
feature: textbook-generation
branch: 002-textbook-generation
user: Administrator
command: /sp.tasks
labels: [tasks, textbook, ai, rag, docusaurus, qdrant]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - specs/002-textbook-generation/tasks.md
tests:
 - none
---

## Prompt

Feature: textbook-generation Objective: Define a complete, unambiguous specification for building the AI-native textbook with RAG chatbot. Book Structure: 1. Introduction to Physical AI 2. Basics of Humanoid Robotics 3. ROS 2 Fundamentals 4. Digital Twin Simulation (Gazebo + Isaac) 5. Vision-Language-Action Systems 6. Capstone Technical Requirements: - Docusaurus - Auto sidebar - RAG backend (Qdrant + Neon) - Free-tier embeddings Optional: - Urdu translation - Personalize chapter Output: Full specification.

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

1) Determine Stage
   - Stage: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate Title and Determine Routing:
   - Generate Title: 3–7 words (slug for filename)
   - Route is automatically determined by stage:
     - `constitution` → `history/prompts/constitution/`
     - Feature stages → `history/prompts/<feature-name>/` (spec, plan, tasks, red, green, refactor, explainer, misc)
     - `general` → `history/prompts/general/`

3) Create and Fill PHR (Shell first; fallback agent‑native)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Open the file and fill remaining placeholders (YAML + body), embedding full PROMPT_TEXT (verbatim) and concise RESPONSE_TEXT.
   - If the script fails:
     - Read `.specify/templates/phr-template.prompt.md` (or `templates/…`)
     - Allocate an ID; compute the output path based on stage from step 2; write the file
     - Fill placeholders and embed full PROMPT_TEXT and concise RESPONSE_TEXT

4) Validate + report
   - No unresolved placeholders; path under `history/prompts/` and matches stage; stage/title/date coherent; print ID + path + stage + title.
   - On failure: warn, don't block. Skip only for `/sp.phr`.

## Response snapshot

Created comprehensive task list for the AI-Native Textbook with RAG Chatbot feature based on the design documents. The tasks are organized by user story in priority order, with clear dependencies and file paths. The task list includes:
- Phase 1: Setup tasks for project initialization
- Phase 2: Foundational tasks that block user stories
- Phase 3-6: User story tasks organized by priority (P1, P1, P2, P3)
- Final phase: Polish and cross-cutting concerns
All tasks follow the required checklist format with proper IDs, story labels, and file paths.

## Outcome

- ✅ Impact: Complete task breakdown for textbook generation implementation
- 🧪 Tests: none
- 📁 Files: Created specs/002-textbook-generation/tasks.md with 51 tasks
- 🔁 Next prompts: Ready for implementation
- 🧠 Reflection: Tasks organized by user story for independent implementation and testing

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): All tasks follow required format
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A