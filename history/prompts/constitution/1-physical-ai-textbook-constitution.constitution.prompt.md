---
id: 1
title: physical-ai-textbook-constitution
stage: constitution
date: 2025-12-10
surface: agent
model: qwen
feature: Physical AI & Humanoid Robotics — Essentials
branch: main
user: Administrator
command: /sp.constitution
labels: [constitution, textbook, ai, robotics]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

Create full constitution.

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


/sp.constitution /sp.constitution

Project Name: Physical AI & Humanoid Robotics — Essentials

Purpose:
Create a short, clean, professional AI-Native textbook based on the Physical AI & Humanoid Robotics course. 
The book must serve as a fast, simple, high-quality learning resource built with a modern Docusaurus UI 
and a fully integrated free-tier RAG chatbot.

Scope:
- 6 short chapters:
  1. Introduction to Physical AI  
  2. Basics of Humanoid Robotics  
  3. ROS 2 Fundamentals  
  4. Digital Twin Simulation (Gazebo + Isaac)  
  5. Vision-Language-Action Systems  
  6. Capstone: Simple AI-Robot Pipeline  
- Clean UI
- Free-tier friendly
- Lightweight embeddings

Core Principles:
- Simplicity  
- Accuracy  
- Minimalism  
- Fast builds  
- Free-tier architecture
- RAG answers ONLY from book text

Key Features:
- Docusaurus textbook  
- RAG chatbot (Qdrant + Neon + FastAPI)  
- Select-text → Ask AI  
- Optional Urdu / Personalize features

Constraints:
- No heavy GPU usage  
- Minimal embeddings  

Success Criteria:
- Build success  
- Accurate chatbot  
- Clean UI  
- Smooth GitHub Pages deployment  

Generate full constitution.

## Response snapshot

The constitution document has been successfully created for the Physical AI & Humanoid Robotics textbook project with the following core principles:
1. Simplicity
2. Accuracy
3. Minimalism
4. Fast Builds
5. Free-tier Architecture
6. RAG Answers from Book Text Only

It also includes Technical Constraints, Development Workflow, and Governance sections specific to this project. The document follows version 1.0.0 and is located at .specify/memory/constitution.md.

## Outcome

- ✅ Impact: Created initial project constitution with 6 core principles tailored to Physical AI & Humanoid Robotics textbook project
- 🧪 Tests: none
- 📁 Files: Updated .specify/memory/constitution.md with complete constitution document
- 🔁 Next prompts: Implementation planning and specification creation for textbook chapters
- 🧠 Reflection: The constitution effectively captures the project's core values and constraints in a clear, testable format

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A