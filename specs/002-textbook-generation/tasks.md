---

description: "Task list for AI-Native Textbook with RAG Chatbot implementation"
---

# Tasks: AI-Native Textbook with RAG Chatbot

**Input**: Design documents from `/specs/002-textbook-generation/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure per implementation plan with backend, frontend, and docs directories
- [x] T002 [P] Initialize backend Python project with FastAPI dependencies in backend/
- [x] T003 [P] Initialize frontend Docusaurus project with required dependencies in frontend/
- [x] T004 [P] Configure linting and formatting for Python (flake8, black) in backend/
- [x] T005 [P] Configure linting and formatting for JavaScript (ESLint, Prettier) in frontend/
- [x] T006 Set up environment configuration management with .env files in both projects

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T007 Setup database schema and migrations framework for PostgreSQL in backend/src/
- [x] T008 [P] Install and configure Qdrant client library in backend/src/
- [x] T009 [P] Setup API routing and middleware structure in backend/src/api/
- [x] T010 Create base models/entities that all stories depend on in backend/src/models/
- [x] T011 Configure error handling and logging infrastructure in backend/src/
- [x] T012 Setup connection to Neon PostgreSQL database in backend/src/config/
- [x] T013 Create basic Docusaurus config and initial pages in frontend/

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Generate Complete Textbook with Auto Navigation (Priority: P1) 🎯 MVP

**Goal**: Create a complete AI-native textbook with 6 chapters using Docusaurus with auto-generated navigation

**Independent Test**: Can generate a textbook with all 6 specified chapters (Introduction to Physical AI, Basics of Humanoid Robotics, ROS 2 Fundamentals, Digital Twin Simulation (Gazebo + Isaac), Vision-Language-Action Systems, and Capstone) with proper navigation and clean UI.

### Implementation for User Story 1

- [x] T014 [P] [US1] Create Textbook model in backend/src/models/textbook.py
- [x] T015 [P] [US1] Create Chapter model in backend/src/models/chapter.py
- [x] T016 [P] [US1] Create User model in backend/src/models/user.py
- [x] T017 [US1] Create TextbookService in backend/src/services/textbook_service.py
- [x] T018 [US1] Create ChapterService in backend/src/services/chapter_service.py
- [x] T019 [US1] Create API endpoint to get textbook chapters in backend/src/api/textbook.py
- [x] T020 [US1] Add validation for textbook content in backend/src/models/textbook.py
- [x] T021 [US1] Create Docusaurus markdown files for all 6 textbook chapters in docs/
- [x] T022 [US1] Configure automatic sidebar navigation for textbook in docusaurus.config.js
- [x] T023 [US1] Implement textbook generation script that creates Docusaurus structure from database content
- [x] T024 [US1] Add responsive design and clean UI styling in frontend/

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Integrate RAG Chatbot (Priority: P1)

**Goal**: Integrate a RAG (Retrieval-Augmented Generation) chatbot that only uses textbook content to provide answers

**Independent Test**: Can ask the RAG chatbot questions about the textbook content and receive accurate responses that reference only the textbook material with no external knowledge.

### Implementation for User Story 2

- [x] T025 [P] [US2] Create RAGIndex model in backend/src/models/rag_index.py
- [x] T026 [US2] Install and configure LangChain for RAG implementation in backend/src/
- [x] T027 [US2] Create RAGService for processing textbook content into embeddings in backend/src/services/rag_service.py
- [x] T028 [US2] Implement RAGIndex creation endpoint in backend/src/api/rag.py
- [x] T029 [US2] Create query endpoint for RAG chatbot in backend/src/api/rag.py
- [x] T030 [US2] Implement embedding generation using free-tier compatible model in backend/src/services/rag_service.py
- [x] T031 [US2] Create RAG response validation to ensure answers only come from textbook content in backend/src/services/rag_service.py
- [x] T032 [US2] Add frontend UI component for RAG chatbot in frontend/src/components/
- [x] T033 [US2] Integrate frontend with RAG API endpoints in frontend/src/services/

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Enable Free-tier Operation (Priority: P2)

**Goal**: Ensure all functionality operates within free-tier cost constraints

**Independent Test**: The embedding process completes successfully using free-tier services and the resulting chatbot functions as expected.

### Implementation for User Story 3

- [x] T034 [US3] Implement embedding size optimization to stay within free-tier limits in backend/src/services/rag_service.py
- [x] T035 [US3] Add caching mechanism for embeddings to reduce API calls in backend/src/services/rag_service.py
- [x] T036 [US3] Optimize database queries for cost efficiency in backend/src/services/textbook_service.py
- [x] T037 [US3] Add monitoring and limits for API usage to prevent exceeding free-tier in backend/src/
- [x] T038 [US3] Optimize build times to meet "Fast Builds" constitutional requirement in frontend/

**Checkpoint**: At this point, all user stories 1, 2, and 3 should work independently

---

## Phase 6: User Story 4 - Enable Chapter Personalization (Priority: P3)

**Goal**: Allow students to personalize their learning experience by selecting focus chapters

**Independent Test**: Students can select which chapters they want to focus on, and the system adapts the content or navigation accordingly.

### Implementation for User Story 4

- [x] T039 [P] [US4] Create UserPreference model in backend/src/models/user_preference.py
- [x] T040 [US4] Create UserPreferenceService in backend/src/services/user_preference_service.py
- [x] T041 [US4] Add API endpoint for managing chapter preferences in backend/src/api/user_preferences.py
- [x] T042 [US4] Update frontend to allow chapter selection in frontend/src/components/
- [x] T043 [US4] Implement UI adaptation based on user preferences in frontend/src/components/
- [x] T044 [US4] Add logic to adjust navigation based on selected chapters in frontend/src/

**Checkpoint**: All user stories should now be independently functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T045 [P] Add documentation updates based on quickstart.md in docs/
- [x] T046 Code cleanup and refactoring across both backend and frontend
- [x] T047 Performance optimization for RAG response time to meet <3 seconds requirement
- [x] T048 [P] Add unit tests for backend services in backend/tests/
- [x] T049 [P] Add integration tests for API endpoints in backend/tests/
- [x] T050 Security hardening for API endpoints in backend/src/api/
- [x] T051 Run quickstart.md validation and update if needed

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Depends on Textbook/Chapter models from US1
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US2 components
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Depends on User model from US1

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all models for User Story 1 together:
Task: "Create Textbook model in backend/src/models/textbook.py"
Task: "Create Chapter model in backend/src/models/chapter.py"
Task: "Create User model in backend/src/models/user.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Textbook generation)
   - Developer B: User Story 2 (RAG integration)
   - Developer C: User Story 3 (Free-tier optimization)
   - Developer D: User Story 4 (Personalization)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence