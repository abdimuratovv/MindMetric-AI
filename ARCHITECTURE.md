# MindMetric AI — System Architecture

> **Constraint honored throughout:** `MindMetric AI.dc.html` and `support.js` are left byte-for-byte
> untouched. This document and the `backend/` / `frontend/` trees describe how the *existing* UI
> (layout, copy, styling, component names, state shape) is served by a real system. No layout,
> component, or style was changed, renamed, or added.

The existing file is a single self-contained mockup: a custom `<x-dc>` component (`support.js`
runtime) whose `Component` class holds all UI state (`this.state`) and computes every `{{ binding }}`
in `renderVals()`. Everything the HTML displays — student names, question text, scores, KPIs — is
currently a hardcoded JS constant (`COGNITIVE_QUESTIONS`, `CODING_PROBLEM`, `BEHAVIORAL_GROUPS`,
`STUDENTS`, the indicator math in `renderVals()`) or purely client-side state (`cqTimeLeft`,
`behavioralAnswers`, `completed`). The job of this architecture is to replace every one of those
hardcoded constants / client-only computations with a real API call to a real backend, while the
markup that consumes them (`{{ }}`, `sc-if`, `sc-for`, `onClick`) stays exactly as-is.

---

## 1. Folder Structure

```
MindMetric AI/
├── MindMetric AI.dc.html          # UNCHANGED — the mockup / source of truth for markup & styling
├── support.js                      # UNCHANGED — the <x-dc> runtime
├── ARCHITECTURE.md                 # this document
│
├── backend/                        # Django + Django REST Framework
│   ├── manage.py
│   ├── requirements.txt
│   ├── mindmetric/                 # project config
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   └── urls.py
│   └── apps/
│       ├── accounts/                # auth, users, roles
│       │   ├── models.py            # User, StudentProfile, TeacherProfile
│       │   ├── serializers.py
│       │   ├── permissions.py       # IsStudent / IsTeacher / IsAdmin
│       │   ├── views.py             # LoginView, LogoutView, MeView
│       │   └── urls.py
│       ├── assessments/             # test content + student attempts/answers
│       │   ├── models.py            # CognitiveQuestion, CodingProblem, BehavioralCategory,
│       │   │                        # BehavioralItem, AssessmentAttempt, CognitiveResponse,
│       │   │                        # CodingSubmission, BehavioralResponse
│       │   ├── content.py           # seed data ported from COGNITIVE_QUESTIONS / CODING_PROBLEM /
│       │   │                        # BEHAVIORAL_GROUPS (loaded by a migration / management command)
│       │   ├── serializers.py
│       │   ├── views.py             # status, cognitive question/answer, coding run/submit,
│       │   │                        # behavioral items/submit
│       │   └── urls.py
│       ├── scoring/                 # adaptive engine, indicator/overall scoring, resumable state
│       │   ├── models.py            # StudentAbilityEstimate, IndicatorScore, OverallScore
│       │   ├── calculators.py       # tierFor()/bandFor() ported 1:1 from the HTML's JS
│       │   ├── engine.py            # AdaptiveTestingEngine (item selection + ability update)
│       │   ├── state_tracker.py     # StudentStateTracker (resumable session state)
│       │   ├── views.py             # results summary, detailed analytics
│       │   └── urls.py
│       ├── reviews/                 # faculty review queue
│       │   ├── models.py            # TeacherReview
│       │   ├── serializers.py
│       │   ├── views.py             # student queue, student detail, submit review
│       │   └── urls.py
│       └── analytics/               # admin/institution dashboards
│           ├── views.py             # KPIs, cohort distribution, faculty activity, student table
│           └── urls.py
│
└── frontend/                        # React (production implementation of the mockup)
    ├── package.json
    ├── index.html
    └── src/
        ├── main.jsx
        ├── App.jsx                  # screen/role state machine — mirrors Component.state.screen
        ├── api/
        │   ├── client.js            # fetch wrapper (auth header, JSON, error normalization)
        │   ├── auth.js
        │   ├── assessments.js
        │   ├── results.js
        │   ├── teacher.js
        │   └── admin.js
        ├── state/
        │   └── useAppState.js       # the client-side state shape (role, completed{}, cqIndex, …)
        ├── theme/
        │   └── tokens.js            # colorTokens / spacingScale, copied verbatim from the HTML
        ├── pages/
        │   ├── Welcome.jsx          # isWelcome
        │   ├── Auth.jsx             # isAuth
        │   ├── Shell/
        │   │   ├── AppShell.jsx     # showShell — sidebar + nav (<aside>)
        │   │   ├── StudentSelection.jsx   # isSelection
        │   │   ├── Results.jsx            # isResults
        │   │   ├── Analytics.jsx          # isAnalytics
        │   │   ├── TeacherReview.jsx      # isTeacherReview
        │   │   ├── AdminOverview.jsx      # isAdmin
        │   │   └── DesignSystemReference.jsx  # isDesignSystem
        │   └── FocusedTest/
        │       ├── FocusedTestShell.jsx   # isFocusedTest header/timer/progress
        │       ├── Cognitive.jsx          # isCognitive
        │       ├── Coding.jsx             # isCoding
        │       └── Behavioral.jsx         # isBehavioral
```

---

## 2. UI Element → Backend Mapping

Every row below is one `{{ }}` binding group or `onClick` handler from `MindMetric AI.dc.html`,
mapped to the endpoint that produces it and the model(s) behind that endpoint.

### 2.1 Welcome (`isWelcome`, lines 29–70)

| UI element | Data / action | Endpoint | Model |
|---|---|---|---|
| `welcomeStats` (`sc-for`) | 4 marketing stat tiles | `GET /api/public/stats/` | aggregate query over `AssessmentAttempt`, `TeacherReview` (cached) |
| "Sign in" / "Get started" buttons | `goAuth` — pure client nav | — | — |

### 2.2 Auth (`isAuth`, lines 72–109)

| UI element | Data / action | Endpoint | Model |
|---|---|---|---|
| `authTabs` (student/teacher/admin) | client-side tab state | — | — |
| University email / Password inputs | form state | — | — |
| `doLogin` button | credential submit | `POST /api/auth/login/` `{email, password, role}` | `accounts.User` |
| `loginError` | validation / auth failure message | (response of the above) | — |

### 2.3 Shell nav (`showShell`, lines 111–136)

| UI element | Data / action | Endpoint | Model |
|---|---|---|---|
| `navItems` | role-specific nav list | derived client-side from `role` (no fetch) | — |
| `userInitial` / `userName` / `role` | signed-in identity | `GET /api/accounts/me/` | `accounts.User` |
| `logout` | end session | `POST /api/auth/logout/` | — |

### 2.4 Student → Assessments (`isSelection`, lines 140–169)

| UI element | Data / action | Endpoint | Model |
|---|---|---|---|
| `assessments` cards (status/duration/CTA) | per-type completion state | `GET /api/assessments/status/` | `assessments.AssessmentAttempt` |
| `a.onStart` → cognitive | start/resume test | `POST /api/assessments/cognitive/start/` | `AssessmentAttempt`, `scoring.StudentAbilityEstimate` |
| `a.onStart` → coding | start/resume test | `POST /api/assessments/coding/start/` | `AssessmentAttempt` |
| `a.onStart` → behavioral | start/resume test | `POST /api/assessments/behavioral/start/` | `AssessmentAttempt` |
| "View my results" (`viewResults`) | gated on `anyCompleted` | client nav, guarded by `/api/assessments/status/` result | — |

### 2.5 Focused test shell (`isFocusedTest`, lines 518–526)

| UI element | Data / action | Endpoint | Model |
|---|---|---|---|
| `focusedTitle`, `timerLabel`, `timerColor` | resumed session timer | `GET /api/assessments/cognitive/state/` (poll-free — server returns `time_remaining_seconds`, client ticks locally, reconciles on each answer) | `AssessmentAttempt.time_remaining_seconds` |
| `focusedProgressPct` | progress within attempt | derived from `cqIndex` / answered-count already returned by the question/answer endpoints | — |
| `exitTest` (Save & exit) | persist partial progress | `POST /api/assessments/{type}/pause/` | `StudentStateTracker` |

### 2.6 Cognitive test (`isCognitive`, lines 527–543)

| UI element | Data / action | Endpoint | Model |
|---|---|---|---|
| `cqNumber`/`cqTotal`/`cqCategory`/`cqPrompt`/`cqOptions` | current adaptively-selected question | `GET /api/assessments/cognitive/next-question/` | `AdaptiveTestingEngine.select_next_question()` → `assessments.CognitiveQuestion` |
| `opt.onSelect` → `nextCognitive` | submit answer, advance | `POST /api/assessments/cognitive/answer/` `{question_id, selected_index}` | `assessments.CognitiveResponse`, updates `scoring.StudentAbilityEstimate` via `AdaptiveTestingEngine.update_ability()` |
| `prevCognitive` | review previous answer (read-only; adaptive tests don't rescroe on back-nav) | `GET /api/assessments/cognitive/history/{n}/` | `CognitiveResponse` |
| final `nextCognitive` (last question) | finalize attempt | `POST /api/assessments/cognitive/submit/` | marks `AssessmentAttempt.status='completed'`, triggers `scoring.engine` to compute `IndicatorScore` for logic/pattern/decomp |

### 2.7 Coding test (`isCoding`, lines 545–585)

| UI element | Data / action | Endpoint | Model |
|---|---|---|---|
| `codingProblem.*` | problem statement/example/constraints | `GET /api/assessments/coding/problem/` | `assessments.CodingProblem` |
| `code` / `setCode` | editor buffer | client state only (optionally autosaved: `PATCH /api/assessments/coding/draft/`) | `CodingSubmission.code` (draft row) |
| `runCode` → `testResults` | run against sample tests | `POST /api/assessments/coding/run/` `{code}` | sandboxed execution service; result written to `CodingSubmission.test_results` |
| `submitCoding` | final submit | `POST /api/assessments/coding/submit/` `{code}` | `assessments.CodingSubmission` (full hidden test suite) → `scoring.IndicatorScore` (fluency) |

### 2.8 Behavioral evaluation (`isBehavioral`, lines 587–618)

| UI element | Data / action | Endpoint | Model |
|---|---|---|---|
| `behavioralGroups` (`sc-for` × `sc-for`) | categories + Likert items | `GET /api/assessments/behavioral/items/` | `assessments.BehavioralCategory`, `BehavioralItem` |
| `opt.onClick` → `setBehavioralAnswer` | per-item scale value | `PATCH /api/assessments/behavioral/answer/` `{item_id, value}` (autosave, mirrors `state.behavioralAnswers`) | `assessments.BehavioralResponse` |
| `behavioralError` | client-side completeness check before submit | — | — |
| `submitBehavioral` | finalize | `POST /api/assessments/behavioral/submit/` | marks attempt complete → `scoring.IndicatorScore` (persistence, attention) |

### 2.9 Results summary (`isResults`, lines 171–234)

| UI element | Data / action | Endpoint | Model |
|---|---|---|---|
| `overallScore`, `band`, `bandExplanation` | headline score | `GET /api/results/summary/` | `scoring.OverallScore`, `calculators.bandFor()` |
| `radarPoints`/`radarAxes`/`radarRings`/`radarDots` | radar chart geometry (computed client-side from `indicators`, same `polar()` helper ported to the frontend) | (same endpoint as `indicators`) | — |
| `indicators` (score + tier per axis) | 6-indicator breakdown | `GET /api/results/summary/` | `scoring.IndicatorScore` × 6, `calculators.tierFor()` |
| `viewAnalytics` | nav to detail | client nav | — |

### 2.10 Detailed analytics (`isAnalytics`, lines 236–273)

| UI element | Data / action | Endpoint | Model |
|---|---|---|---|
| `indicatorsDetail` (score, cohort avg, percentile, explanation) | per-indicator detail vs. cohort | `GET /api/results/analytics/` | `scoring.IndicatorScore` joined against a cohort aggregate query |
| `backToResults` | nav | client nav | — |

### 2.11 Teacher review queue (`isTeacherReview`, lines 275–370)

| UI element | Data / action | Endpoint | Model |
|---|---|---|---|
| `teacherLoading`/`teacherLoaded` skeleton | initial fetch in flight | (loading state around the call below) | — |
| `teacherSearch` → `teacherStudents` | searchable roster with score/status | `GET /api/teacher/students/?search=` | `accounts.User` (students) joined to `scoring.OverallScore`, `reviews.TeacherReview.status` |
| `s.onSelect` → `selectedStudent` | student detail + `indicatorTags` | `GET /api/teacher/students/{id}/` | `scoring.IndicatorScore`, `assessments.AssessmentAttempt` |
| `rubricItems` / `opt.onClick` → `setRubric` | pedagogical rubric (4 labels × 1–5) | client state, submitted with the review | `reviews.TeacherReview.rubric_scores` (JSON) |
| `reviewComment` / `setReviewComment` | free text | client state | `reviews.TeacherReview.comment` |
| `submitReview` | finalize | `POST /api/teacher/students/{id}/review/` `{rubric_scores, comment}` | `reviews.TeacherReview` |

### 2.12 Admin overview (`isAdmin`, lines 372–444)

| UI element | Data / action | Endpoint | Model |
|---|---|---|---|
| `adminLoading`/`adminLoaded` skeleton | initial fetch in flight | — | — |
| `adminKpis` | 4 headline KPIs + deltas | `GET /api/admin/kpis/` | aggregate over `AssessmentAttempt`, `OverallScore`, `TeacherReview` (delta vs. prior term, cached/materialized) |
| `distributionBars` | cohort score-band histogram | `GET /api/admin/distribution/` | `scoring.OverallScore` grouped by `calculators.bandFor()` |
| `facultyActivity` | reviews-per-faculty | `GET /api/admin/faculty-activity/` | `reviews.TeacherReview` grouped by `reviewer` |
| `adminSearch` → `adminStudents` table | recent assessments table | `GET /api/admin/students/?search=` | `accounts.User` joined to `OverallScore`, `TeacherReview.status` |

### 2.13 Design system reference (`isDesignSystem`, lines 446–512)

| UI element | Data / action | Endpoint | Model |
|---|---|---|---|
| `colorTokens`, `spacingScale`, buttons/inputs/badges/states | static design tokens | none — lives in `frontend/src/theme/tokens.js`, copied verbatim from the HTML's `colorTokens`/`spacingScale` arrays | — |

---

## 3. Data Flow (step-by-step)

### 3.1 Sign-in

1. Student opens the app → `Welcome` renders (`isWelcome`), no backend call.
2. Clicks "Sign in" → `Auth` screen; picks a role tab (client-only), types email/password.
3. `doLogin` → `POST /api/auth/login/`. `accounts.views.LoginView` authenticates against
   `accounts.User`, checks `role` matches the requested tab, returns `{token, role, user}`.
4. Frontend stores the token, calls `GET /api/accounts/me/` to hydrate `userName`/`userInitial`,
   sets `App.jsx` state to `showShell = true` and routes to the role's default screen
   (`selection` / `teacherReview` / `admin` — identical to `doLogin`'s `goTo(...)` in the mockup).

### 3.2 Taking the cognitive test (adaptive)

1. Student clicks "Start assessment" on the Cognitive card → `POST /api/assessments/cognitive/start/`.
   `assessments.views` creates (or resumes) an `AssessmentAttempt(type='cognitive', status='in_progress')`
   and a `scoring.StudentAbilityEstimate` per indicator (`logic`, `pattern`, `decomp`), seeded at
   `theta=0`, if one doesn't already exist for this student.
2. Frontend requests `GET /api/assessments/cognitive/next-question/`. `scoring.engine.AdaptiveTestingEngine.select_next_question()`
   picks the unanswered `CognitiveQuestion` in the active indicator pool whose `difficulty` is
   closest to the student's current `theta` for that indicator (see §4). Question + options returned;
   `cqNumber`/`cqTotal`/`cqCategory`/`cqPrompt`/`cqOptions` render exactly as before.
3. Student selects an option → `POST /api/assessments/cognitive/answer/ {question_id, selected_index}`.
   Server records `CognitiveResponse`, scores it against `correct_index`, calls
   `AdaptiveTestingEngine.update_ability()` to move `theta` toward/away from the question's difficulty,
   and returns whether more questions remain (drives `cqNextLabel`: "Next" vs. "Submit test").
4. Client-side timer (`cqTimeLeft`) ticks locally starting from the `time_remaining_seconds` the
   `start` call returned; each `answer` response includes the authoritative remaining time so client
   and server can't drift. If the timer hits 0, the client auto-calls `submit/`.
5. After the last question, `POST /api/assessments/cognitive/submit/` marks the attempt `completed`,
   `scoring` computes final `IndicatorScore` rows for `logic`/`pattern`/`decomp` from the accumulated
   `theta` values, and the client returns to `selection` with that assessment's status flipped to
   "Completed" (next `GET /api/assessments/status/` reflects it).

### 3.3 Taking the coding test

1. "Start assessment" (coding) → `POST /api/assessments/coding/start/` creates the `AssessmentAttempt`.
2. `GET /api/assessments/coding/problem/` returns the single `CodingProblem` row (title, statement,
   example, constraints, starter code) — this is the same content as `CODING_PROBLEM` in the mockup,
   now database-backed via `assessments/content.py` seed data.
3. `runCode` → `POST /api/assessments/coding/run/ {code}` executes the code against the problem's
   *sample* `test_cases` in a sandboxed runner and returns pass/fail per case (`testResults`).
4. `submitCoding` → `POST /api/assessments/coding/submit/ {code}` runs the *full* hidden test suite,
   persists a `CodingSubmission`, marks the attempt complete, and `scoring` derives the `fluency`
   `IndicatorScore` from pass rate + code-quality heuristics.

### 3.4 Taking the behavioral evaluation

1. "Start assessment" (behavioral) → `POST /api/assessments/behavioral/start/`.
2. `GET /api/assessments/behavioral/items/` returns `BehavioralCategory` → `BehavioralItem` (the
   same 4 categories × 2 items as `BEHAVIORAL_GROUPS`).
3. Each Likert click → `PATCH /api/assessments/behavioral/answer/ {item_id, value}` upserts a
   `BehavioralResponse` (autosave, so `behavioralAnswers` survives a refresh — same intent as the
   in-memory `state.behavioralAnswers`).
4. `submitBehavioral` checks all items answered client-side (`behavioralError`, unchanged), then
   `POST /api/assessments/behavioral/submit/` marks the attempt complete; `scoring` derives
   `persistence`/`attention` `IndicatorScore` from the (reverse-scored where applicable) responses.

### 3.5 Viewing results

1. `viewResults` (enabled once any attempt is completed) → `GET /api/results/summary/`.
2. `scoring.views` reads the student's `IndicatorScore` rows, computes `overallScore` (mean, same as
   the mockup's `renderVals()`), calls `calculators.bandFor()`/`tierFor()` for the band and per-axis
   tiers, and returns `{overallScore, band, bandExplanation, indicators}`.
3. The frontend computes `radarPoints`/`radarAxes`/`radarRings`/`radarDots` client-side from
   `indicators` using the same `polar()` geometry helper (pure presentation, no need to compute
   server-side).
4. "View detailed analytics" → `GET /api/results/analytics/`, which joins the same `IndicatorScore`
   rows against a cohort aggregate (avg + percentile) and returns per-indicator `explanation` text.

### 3.6 Faculty review

1. Teacher signs in → lands on `teacherReview`. `GET /api/teacher/students/` (empty search) fills
   `teacherStudents` (name, program, automated score, review status) — mirrors `teacherLoading` →
   `teacherLoaded` skeleton timing.
2. Typing in the search box calls the same endpoint with `?search=` (debounced), matching the
   mockup's client-side `.filter()` on `teacherSearch`.
3. Selecting a student → `GET /api/teacher/students/{id}/` returns `selectedStudent` (profile +
   `indicatorTags`, the first 4 `IndicatorScore` rows).
4. Teacher sets the 4 rubric scores and a comment (client state) → `submitReview` →
   `POST /api/teacher/students/{id}/review/` persists `reviews.TeacherReview` and flips
   `reviewSubmitted`.

### 3.7 Admin overview

1. Admin signs in → lands on `admin`. Four parallel `GET` calls populate the dashboard:
   `/api/admin/kpis/`, `/api/admin/distribution/`, `/api/admin/faculty-activity/`,
   `/api/admin/students/` — matching `adminLoading` → `adminLoaded` skeleton timing.
2. The student table's search box re-calls `/api/admin/students/?search=` (server-side filter,
   replacing the mockup's client-side `.filter()` over the hardcoded `STUDENTS` array).

---

## 4. Adaptive Testing Engine (`backend/apps/scoring/engine.py`)

The mockup's cognitive test is a **fixed** sequence (`COGNITIVE_QUESTIONS[cqIndex]`, `cqIndex` just
increments). The architecture replaces item *order* with adaptive selection while leaving the UI
(`cqNumber`, `cqTotal`, `cqPrompt`, `cqOptions`, Next/Previous) untouched:

- Each `CognitiveQuestion` carries a `difficulty` (float) and an `indicator_key` (`logic` / `pattern`
  / `decomp`) tying it to one of the 6 result-screen indicators.
- Each student has a `StudentAbilityEstimate.theta` per indicator (starts at 0).
- `select_next_question(attempt)`: among unanswered questions in the active indicator pool, pick the
  one whose `difficulty` is closest to the student's current `theta` (classic maximum-information
  item selection, simplified from full IRT).
- `update_ability(theta, difficulty, correct)`: a 1-parameter logistic step —
  `expected = 1 / (1 + e^-(theta - difficulty))`; `theta += K * (correct - expected)` (K≈0.5) — moves
  the estimate up on a correct answer to a hard item, down on a miss on an easy item, with diminishing
  swings as more items are answered.
- `cqTotal` becomes "however many items this student's adaptive run consumes" (a configurable cap,
  e.g. 6, matching the mockup's fixed count) rather than `COGNITIVE_QUESTIONS.length`.

## 5. Student State Tracking (`backend/apps/scoring/state_tracker.py`)

The mockup keeps all progress in `Component.state` (`completed{}`, `cqIndex`, `cqAnswers`,
`cqTimeLeft`, `coding.code`, `coding.hasRun`, `behavioralAnswers`) — it vanishes on refresh.
`StudentStateTracker` gives that same state shape a server-side home so a session survives a reload,
a lost connection, or a teacher wanting to see "how far along" a student is:

- `get_or_create_attempt(student, assessment_type)` — one active `AssessmentAttempt` per
  student/type; `status` transitions `not_started → in_progress → completed`, mirroring
  `state.completed[type]`.
- `record_progress(attempt, **fields)` — persists the equivalent of `cqIndex`/`cqAnswers`
  (via `CognitiveResponse` rows already being the per-question record), `time_remaining_seconds`,
  and `coding.hasRun` (`CodingSubmission.test_results IS NOT NULL`).
- `get_resume_state(student)` — returns, per assessment type, exactly the shape
  `GET /api/assessments/status/` needs to redraw the `selection` screen's status badges
  ("Available" / "Completed") and to let a focused-test screen resume mid-attempt instead of
  restarting, closing the biggest behavioral gap versus the current in-memory-only mockup.
