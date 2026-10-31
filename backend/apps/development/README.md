# Development backend foundation

Stages two through four provide versioned content, progress storage, permissions,
read-only Django admin inspection, explicit publication, atomic seed, student
learning APIs and the first React learning flow. Automated skill recommendations
remain a later stage.

## Content

The five deployed manifests are in `content/cluster1/` in this application.
Reviewed copies are in `docs/content/cluster1/` at repository root; offline
checks compare them. No Downloads files are
needed to import. Numeric input accepts bounded exact integers, decimals or
fractions; expressions and executable code are rejected.

From `backend/`, with its virtual environment activated:

```powershell
python manage.py migrate development --plan
python manage.py migrate development
python manage.py seed_development_content --dry-run
python manage.py seed_development_content
python manage.py seed_development_content --all --dry-run
python manage.py seed_development_content --all
```

`--path` accepts an alternative reviewed UTF-8 JSON manifest. Imports remain
draft, never create accounts and never write diagnostic scores. Missing
diagnostic questions cause an error before writes; the command does not seed
demo users to satisfy these references. Validate the target database and take
an appropriate backup before applying migrations to an existing installation.

The default command still imports only arithmetic/algebra. `--all` imports the
latest bundled version of each of the six modules in one atomic transaction,
with prerequisite modules first. Its dry run resolves all cross-module
references without creating any rows. Matrix content intentionally has no
diagnostic links because no matching questions exist in the current bank;
an explicit coverage note is required instead of a fabricated link.

The stage-four authoring source is `docs/content/cluster1/build_stage4_content.py`.
`verify_stage4_content.py` independently checks the new answers/examples,
Boolean equivalence over all assignments, provenance hashes and the full graph.
Browser smoke tests accept `--all-modules` to also verify the six-course catalogue.

Drafts can be reconciled using the same key/version. After publication or
enrollment, changed content requires a new version. Identical imports remain
idempotent. Enrollment pins the student, module version, diagnostic baseline
and recommendation reason. Session questions are pinned; answer rows are
append-only and have unique idempotency and attempt constraints.

## Admin and permissions

Visit the existing `/admin/` with an active Django staff account whose product
role is `admin`, or a superuser. Product role alone does not grant Django staff
access. Models are read-only; use the module action **Publish validated drafts**
to publish explicitly. It revalidates and reconciles the stored manifest.
Application code must use the importer/publication service for content writes;
`QuerySet.update`, bulk writes and raw SQL bypass ordinary model save guards.

The pilot flag `DEVELOPMENT_CLUSTER1_ENABLED` defaults to false; set it to `1`
when opening the pilot. Student APIs at `/api/development/` use
`STUDENT_PERMISSIONS` and owner-filtered querysets. Capabilities intentionally
return an unavailable state when the flag is off. DRF does not run object
permissions on list results. Neither the full manifest, answer keys nor option
feedback is serialized as a live check question. Completed reviews and lessons
are also suppressed during an active check.

The learning sequence is enroll, precheck, study, practice, postcheck and report.
An 80% precheck can skip study/practice. Otherwise lesson completion and four
unaided first answers among the last five practice questions unlock postcheck.
Repeated practice is rehearsal, not an independent growth measurement. Each
enrollment has one precheck and one held-out postcheck set; postcheck cannot be
repeated after its answers have been revealed. Numeric grading is exact. Learning
results never write diagnostic indicator scores or IRT ability estimates.

Session creation locks the student before the enrollment; other writes lock
enrollment before session. Only one session per student may be active, across
all modules. Answer retries use a client UUID and
identical payload; a reused UUID with different content is rejected. Lessons
and session questions resume from the server after refresh. The frontend keeps
only its selection and pending submission in per-user sessionStorage.

## Personal plan and focused lessons (stage five)

`GET /api/development/plan/` returns at most two explainable priorities and the
full published/pinned catalogue. Only completed diagnostic attempts and their
current cycles contribute; a skill needs three distinct mapped questions.
Fewer answers return insufficient evidence, never a zero ability score. Low
aggregate IQ/math alone cannot establish a topic weakness. Missing matrix
diagnostic coverage leads to an optional module precheck.

Completed module checks provide provisional evidence (one item per skill).
Newer checks supersede older diagnostic observations; a later completed
diagnostic with enough mapped responses may update priorities. Practice is
never evidence of independent improvement. Completed modules are optional
unless newer diagnostic evidence warrants review. Enrolling captures an
immutable server-derived reason and policy version; GET requests do not write.

Wrong check skills focus study on their lessons and unresolved local
prerequisites, in prerequisite order. Answered-correctly prerequisites are
skipped; other lessons remain available. With a precheck below 80%, completing
the focused required lessons unlocks practice. An 80% precheck still allows
direct postcheck. Evidenced weak prerequisites in other modules are prioritized
before their dependent module without automatically enrolling or hard locking.

During any active check, evidence details, theory and completed reviews are
hidden across modules; the plan offers resuming that check. The UI includes
module completion totals, skill/source/count labels, focused lesson links,
mobile layouts and Uzbek/Russian interface text. Course content remains Uzbek
with explicit language fallback. Normal grading validation is localized too.

Browser smoke with `--all-modules` uses a disposable database, verifies the
personal plan at mobile width and completes every extra module precheck before
opening the next. It never publishes content into the main configured database.

## Tests

For an authorized production release, `python manage.py activate_development_cluster1`
imports and publishes the six reviewed modules in one transaction. It is
idempotent, creates no accounts/scores and serializes PostgreSQL releases with
an advisory lock. Render requires PostgreSQL; ephemeral SQLite is rejected.
Gunicorn loads `backend/gunicorn.conf.py` automatically from its backend working
directory. Its master startup hook runs this command only when
`DEVELOPMENT_CLUSTER1_PUBLISH_ON_DEPLOY=1`, closing DB connections before workers
fork. Set `DEVELOPMENT_CLUSTER1_ENABLED=1` separately to expose the pilot.
Rollback access by setting the enabled flag to `0`; published content/results
remain stored. Failed publication rolls back all six modules and fails the
new startup, preserving the prior release. Normal startup does not publish.

```powershell
python manage.py test apps.development --settings=apps.development.tests.settings
python manage.py check --settings=apps.development.tests.settings
python manage.py makemigrations --check --dry-run --settings=apps.development.tests.settings
```

The test settings explicitly select an isolated in-memory SQLite database, not
the database configured by `DATABASE_URL`. Tests cover real migrations,
manifest validation, reference integrity, rollback, repeated seed, immutable
versions and snapshots, uniqueness/range constraints, role/owner/profile/flag
permissions, and the actual Django admin publication action. PostgreSQL lock
checks are described below; hosted staging remains a separate environment check.

### PostgreSQL concurrency checks (stage six)

`tests/postgres_settings.py` always connects to `127.0.0.1`, user `stage6test`,
port `55436` (override only with `STAGE6_POSTGRES_PORT`). It never uses a
production `DATABASE_URL`. Provision a disposable local PostgreSQL cluster with
that role and bind it to loopback. The Django runner creates and drops only
`test_mindmetric_stage6`; the base database name is `mindmetric_stage6`.
Never point the runner at an existing user database. Binaries/data are local
test infrastructure under ignored `backups/stage6-postgresql/` in this workspace.

```powershell
backend/venv/Scripts/python.exe backend/manage.py test apps.development --settings=apps.development.tests.postgres_settings --noinput
```

On PostgreSQL, seven additional TransactionTestCase tests send overlapping API
view requests with separate database connections. They verify duplicate enroll,
duplicate start, competing modules, identical answer UUID retries, different
answer UUID races, duplicate finish and simultaneous hint/answer ordering.
They run real migrations and use synthetic content/students only. SQLite skips
these seven tests because its locks cannot establish PostgreSQL behavior.
Production Neon was not used for destructive tests. Separate hosted staging
and real participant observations must be recorded separately from these tests.

## Number theory module 1.4

`number-theory-discrete-mathematics.v1.json` adds five skills, five lessons and
20 questions (10 practice, 5 precheck, 5 postcheck), ordered between sets and
functions. The authored Markdown/Word resource is in `docs/content/cluster1/`.
Its source hash pins the new Markdown, with LF line endings enforced by Git.
It does not pretend a previously supplied 1.4 Word source existed.
No diagnostic links are fabricated; the module begins with its own precheck.
Existing five published manifests and their version hashes stay unchanged.
`test_number_theory.py` checks all 20 answers and five examples independently.

## Russian resources for modules 1.1 and 1.6

`content/translations/*.v1.ru.json` contains complete reviewed Russian overlays
for arithmetic/algebra and matrices. Overlays are bound to the canonical module
key, version and content hash. Frozen manifests, rows and session question
snapshots stay unchanged, so existing v1 enrollments can switch languages too.
The release command validates the overlays before the new process serves traffic.
Missing translations or an incompatible version/hash use the explicit Uzbek
fallback; there are no machine-generated partial translations in responses.

All development endpoints resolve the existing `X-Language`/`lang` request
language. `content_language` identifies the actual resource language, separately
from the interface. Module/skill/lesson titles, theory, examples, live question
text/options, practice hints, feedback and completed reviews are localized on
the server. Full overlays are never sent to the browser during checks. Option
IDs, answer keys, UUID retries, scoring and phase rules do not change.

Worked examples now expose `prompt`, `solution_steps`, `answer`; the legacy
`*_uz` aliases contain the same localized values for older clients. A requested
practice hint may be restored on the current question. `last_feedback` is only
available for practice outside any active check, so switching language can keep
an already open explanation. Frontend locale refresh also preserves the lesson,
expanded example and selected option; a mutation finishing in an older language
triggers a fresh read in the current language.

Authoring source: `docs/content/cluster1/build_russian_resources.py`; reviewed
copies live in `docs/content/cluster1/translations/`. Validation checks complete
coverage, unchanged numerical constants and option IDs, and forbidden check
hints/grading overrides. API tests cover pinned v1 sessions and immutable hashes.
The browser smoke covers RU ↔ UZ in the catalogue, lesson, expanded example,
selected answer, hint, feedback and matrix check, including Uzbek fallback for
other modules.
