# Rename md2okf → code2okf, cut v0.1.0, publish to PyPI

## Context

This repository (`lars20070/code2okf`) currently has only a placeholder
commit on `main` (`# code2okf` in `README.md`). The actual, fully-developed
project sitting in the working tree — driver, sandbox kit, tests, docs, CI —
was built under the name **md2okf**, and a sibling package `md2okf` is
already published on PyPI at v0.2.0 under the same GitHub owner
(`lars20070`). `VERSION` and `CHANGELOG.md` already narrate a `0.1.0`
(2026-09-07) and `0.2.0` (2026-09-20) history, even though nothing has ever
actually been tagged or released from this repo.

The goal: rename every `md2okf` identifier in the codebase to `code2okf`,
land it on `main` as the project's real first commit, cut it as `v0.1.0`,
and publish `code2okf` to PyPI via the trusted-publishing pipeline that
already exists in `.github/workflows/release.yml`.

**Decisions made with the user:**
1. **Version**: squash the existing `0.1.0`/`0.2.0` CHANGELOG sections into a
   single `## [0.1.0]` entry (new date), set `VERSION` = `0.1.0`. This
   becomes code2okf's first-ever tagged release.
2. **Legacy `md2okf` on PyPI** (already live at v0.2.0): left completely
   alone — out of scope.
3. **`master` → `main` mismatch**: `ci.yml`'s `push` trigger
   (`branches: [master]`) and `CONTRIBUTING.md`'s Releasing section both
   still say `master`; fix both to `main` as part of this same change.
4. No backward-compatibility `md2okf` CLI alias is added — nothing has ever
   shipped under the `code2okf` name, so there's no compatibility burden,
   and the project's own convention (AGENTS.md) is no compat shims unless
   asked.
5. **Old local state under the `md2okf` name is left alone, not migrated.**
   Renaming the sandbox name, state-dir env var, and lock path means any
   existing Pi session transcripts and ownership/fingerprint records under
   the old `md2okf` namespace, plus the old `md2okf` sandbox itself, become
   orphaned. This is pre-release dev state, so no migration procedure is
   provided — just documented as intentional. Manual cleanup
   (`sbx rm --force md2okf`, clearing the old state dir) is left to the user
   whenever they want it.
6. **No GitHub `pypi` environment protection rule (no required reviewer).**
   Pushing the `v0.1.0` tag runs straight through to PyPI with no manual
   approval step, matching how `release.yml` already works today.

Repo policy (`AGENTS.md`): **never run `git commit` or `git push`** in this
repo. All git actions below through "stage + draft message" are mine to do;
committing, pushing, opening the PR, merging, and tagging are the user's.
Staging (`git add`) is not commit/push and is used below as part of
verification, per the review this plan was updated against.

---

## Stage 1 — Mechanical rename

Grouped so each group is independently checkable. Directory renames first,
since later edits reference the new paths.

**1a. Directory renames**
- `src/md2okf/` → `src/code2okf/` (`__init__.py`, `cli.py`, `compile.py`,
  `events.py`, `resources.py`, `sandbox.py`, `workbench.py`)
- `kits/md2okf/` → `kits/code2okf/`, including
  `kits/code2okf/files/home/.local/lib/md2okf/` →
  `.../lib/code2okf/` (the `mount-state.sh` directory itself)

**1b. `pyproject.toml`** (read in full and confirmed) — the most
load-bearing file:
- `name = "md2okf"` → `"code2okf"`
- `[project.urls]`: all three `lars20070/md2okf` → `lars20070/code2okf`
  (including the `/blob/master/CHANGELOG.md` Changelog URL — update the
  branch segment to `main` too, per decision 3)
- `[project.scripts]`: `md2okf = "md2okf.cli:main"` →
  `code2okf = "code2okf.cli:main"`
- `[tool.hatch.build.targets.wheel]` `packages = ["src/md2okf"]` →
  `["src/code2okf"]`
- `force-include` table: `"kits/md2okf" = "md2okf/kit"` →
  `"kits/code2okf" = "code2okf/kit"`; `"SPEC.md" = "md2okf/SPEC.md"` →
  `"code2okf/SPEC.md"`; all four `scripts/<cli>/...` → `md2okf/clis/<cli>/...`
  mappings → `code2okf/clis/<cli>/...`
- Prose comments referencing "md2okf's own licence", "an installed md2okf",
  `import md2okf`, `src/md2okf` — reword, not just token-swap, since these
  are full sentences
- `[tool.ruff]` `extend-exclude` comment mentioning `kits/md2okf/files/...`
- `[tool.hatch.build.targets.sdist]` `exclude = [".claude", ".cursor"]` →
  add `".codex"`. Verified: `.codex/config.toml` and
  `.codex/plans/.gitkeep` currently leak into a local `make dist` sdist
  build even though the packaging comment says agent-tool directories are
  deliberately excluded — `.codex` is the same kind of agent-tool config as
  `.claude`/`.cursor` and was simply missed.

**1c. Source literals** in the 7 files now under `src/code2okf/`:
- `cli.py`: `prog="md2okf"` → `"code2okf"`; every `f"md2okf: {exc}"` /
  "another md2okf run" error-prefix string; the assembled
  `MD2OKF_STATE_DIR=` env string → `CODE2OKF_STATE_DIR`;
  `from md2okf import ...` → `from code2okf import ...`
- `workbench.py`: `SANDBOX_NAME = "md2okf"` → `"code2okf"`;
  `LOCK_PATH_TEMPLATE = "/tmp/md2okf-{uid}.lock"` → `/tmp/code2okf-{uid}.lock`;
  the `{"MD2OKF_STATE_DIR": ...}` dict key → `CODE2OKF_STATE_DIR`;
  docstring/comment mentions of `kits/md2okf`, `state_home()/md2okf`
- `sandbox.py`: `OWNER_TOKEN_PATH = "/tmp/md2okf-owner"` →
  `/tmp/code2okf-owner`; `python -m md2okf.sandbox` mentions;
  `from md2okf import workbench`; `f"md2okf.sandbox: {exc}"` /
  "another md2okf run" print strings
- `resources.py`: `files("md2okf")` → `files("code2okf")`;
  `_checkout_path("kits/md2okf", ...)` → `"kits/code2okf"`; docstrings
  mentioning `md2okf/kit`, `md2okf/SPEC.md`, `md2okf/clis`, `uv run md2okf`
- `compile.py`, `events.py`, `__init__.py`: sweep for any residual `md2okf`
  mentions in the same pass (not individually enumerated by the inventory)

**1d. `kits/code2okf/spec.yaml`** — read in full during inventory, uses
`md2okf` in:
- `name: md2okf` → `name: code2okf` (the literal `sbx` sandbox name — must
  match `workbench.SANDBOX_NAME`)
- entrypoint path `$HOME/.local/lib/md2okf/mount-state.sh` →
  `.../lib/code2okf/mount-state.sh` (two occurrences in the file)
- echo message `"md2okf: could not relocate..."` → `"code2okf: ..."`
- entrypoint arg `md2okf-entrypoint` → `code2okf-entrypoint`
- both embedded agent-instruction mentions of `$MD2OKF_STATE_DIR/sessions` →
  `$CODE2OKF_STATE_DIR/sessions`

**1e. `kits/code2okf/README.md`** — 7 occurrences, including example
commands `sbx exec md2okf --` / `sbx secret set-custom --sandbox md2okf` →
`code2okf` equivalents.

**1f. `kits/code2okf/files/home/.local/lib/code2okf/mount-state.sh`** — reads
`MD2OKF_STATE_DIR` → `CODE2OKF_STATE_DIR`. Leave
`kits/code2okf/files/home/.pi/agent/AGENTS.md` and everything under
`skills/` untouched (confirmed zero `md2okf` mentions).

**1g. Tests (`tests/`)**
- `conftest.py`: `from md2okf import sandbox as sandbox_module` /
  `workbench as workbench_module` → `code2okf`; `LOCK_PATH_TEMPLATE` patch
  literal `"md2okf-{uid}.lock"` → `"code2okf-{uid}.lock"`
- `test_sandbox.py`, `test_workbench.py`, `test_compile.py`, `test_cli.py`:
  every hard-coded literal `"md2okf"` (e.g. `sandbox.create("md2okf", ...)`,
  `"sbx run --detached --name md2okf"`, `"sbx exec md2okf --"`,
  `NAME = "md2okf"`) → `"code2okf"`. These are literals, not derived from
  `SANDBOX_NAME`, so plain find/replace per file is safe and complete.
- `test_resources.py`: **not just the import** — re-checked directly and it
  also builds `fake_root = tmp_path / "installed" / "md2okf"` (→
  `"code2okf"`) and asserts
  `resources.kit_dir() == resources._CHECKOUT_ROOT / "kits" / "md2okf"` (→
  `"kits" / "code2okf"`); the latter breaks once the kit directory moves
  unless updated.
- `test_kit.py`, `test_events.py`: import statements →
  `from code2okf import ...`
- `test_package.py`: every asserted wheel path —
  `"md2okf/cli.py"` → `"code2okf/cli.py"`,
  `"md2okf/kit/spec.yaml"` → `"code2okf/kit/spec.yaml"`,
  `"md2okf/kit/files/home/.local/lib/md2okf/mount-state.sh"` →
  `"code2okf/kit/files/home/.local/lib/code2okf/mount-state.sh"`,
  `"md2okf/SPEC.md"` → `"code2okf/SPEC.md"`,
  `"md2okf/clis/merkleokf/..."` → `"code2okf/clis/merkleokf/..."`, and the
  `"md2okf/"` prefix check
- `tests/test-sandbox.sh`: `kit_name="md2okf"` → `"code2okf"` (also fix its
  comment "keyed to `name:` in kits/md2okf/spec.yaml" →
  `kits/code2okf/spec.yaml`); `uv run python -m md2okf.sandbox` →
  `code2okf.sandbox`
- `tests/test-sandbox-guest.sh`: re-checked directly, this file has far more
  than env-var mentions — `check_file "${HOME}/.local/lib/md2okf/mount-state.sh"`
  (path), `.md2okf-sandbox-test-$$` and `.md2okf-write-probe-$$` probe-name
  literals, `MD2OKF_STATE_DIR`/`MISSING MD2OKF_STATE_DIR` (env var + its own
  error message), and a dozen `kits/md2okf/spec.yaml` mentions inside
  comments cross-referencing the spec — all need the `code2okf` rename, not
  just the two env var occurrences originally noted.
- `tests/test-mount-state.sh`: also far more than env vars — `HELPER` path
  `kits/md2okf/files/home/.local/lib/md2okf/mount-state.sh`, `TEST_ROOT`
  prefix `md2okf-state-test`, `MD2OKF_STATE_DIR`/`MD2OKF_REQUIRE_BIND` env
  vars (multiple call sites, not just set/unset), `SPEC="${ROOT}/kits/md2okf/spec.yaml"`,
  `FAKE_HOME}/.local/lib/md2okf` directory creation, the `md2okf-entrypoint`
  argument passed to the fake entrypoint (twice), and a `grep -c
  'lib/md2okf/mount-state\.sh'` assertion against the spec file — every one
  of these needs updating, not just the two env var names.

**1h. Scripts**
- `scripts/validate-spec.sh`: comment + path `kits/md2okf/` →
  `kits/code2okf/`
- `scripts/check-release-tag.sh`, `scripts/release-notes.sh`: no mentions,
  leave alone (confirmed generic)

**1i. Docs**

(Occurrence counts below are indicative only — re-verified counts came out
higher than the original inventory's line-based counts, e.g. README.md is
53 total token matches not 45, AGENTS.md is 26 not 24 — so treat every count
here as "at least this many" and rely on the Stage 1o residual sweep below
as the actual completeness check, not these numbers.)

- `README.md`: title, badge URLs (`.../actions/workflows/ci.yml`,
  `/releases/latest`), Mermaid diagram labels (`~/.local/state/md2okf`,
  `kits/md2okf/spec.yaml`), every command/prose mention,
  `uv tool install git+https://github.com/lars20070/md2okf`
- `AGENTS.md`: repo-map prose, `kits/md2okf/` paths, `make test-md2okf`
  target name, command examples (`sbx exec -it md2okf -- bash`,
  `sbx rm --force md2okf`, `python -m md2okf.sandbox`)
- `CONTRIBUTING.md` (25 occurrences), **plus** the Releasing section's
  "Land that commit on `master`" → `main` (decision 3)
- `.coderabbit.yaml` (1 mention, a comment)
- `NOTICE-OKF-SPEC.md` (confirmed 2 mentions by direct read, correcting the
  earlier "zero mentions" inventory note): "md2okf itself is MIT-licensed"
  and "It is not part of md2okf: it is the format md2okf compiles" — reword
  to `code2okf`; the rest of the file (OKF spec attribution to
  `GoogleCloudPlatform/open-knowledge-format`, Apache-2.0) is unaffected and
  must stay exactly as-is
- `CLAUDE.md`, `SPEC.md` — confirmed zero mentions; `SPEC.md` is the
  vendored verbatim upstream OKF spec, never touch it for any reason
- **`CHANGELOG.md` is handled separately in Stage 2**, not here — squashing
  and renaming in the same edit would make the diff hard to review

**1j. CI/CD workflow files**
- `.github/workflows/ci.yml` (read in full):
  - `on: push: branches: [master]` → `[main]` (decision 3)
  - job id `test-md2okf` → `test-code2okf`, and its step
    `run: make test-md2okf` → `make test-code2okf`
  - `run: make test-shell MD2OKF_REQUIRE_BIND=1` →
    `CODE2OKF_REQUIRE_BIND=1`
  - comments mentioning `md2okf.sandbox`, `kits/md2okf/spec.yaml`
- `.github/workflows/release.yml`: the rename literal —
  `environment.url: https://pypi.org/p/md2okf` → `.../p/code2okf`. **Plus a
  correctness fix unrelated to the rename, confirmed by reading the file in
  full**: the `build` job's `actions/upload-artifact@v7` step (uploading
  `dist/`) has no `overwrite:` key, which defaults to `false`. GitHub's docs
  say a second upload with the same artifact name in the same workflow run
  then fails outright — so re-running the whole workflow after a partial
  failure (e.g. a `publish-pypi` hiccup) would fail again at the `build`
  job's upload step, before ever reaching PyPI, contradicting
  `CONTRIBUTING.md`'s claim that "a re-run is safe". Add `overwrite: true`
  to that step.
- `CONTRIBUTING.md`'s Releasing section (around the "a re-run is safe
  because PyPI treats an upload of a byte-identical file as idempotent"
  line): that claim is true for PyPI itself but incomplete — clarify that
  the artifact-upload step is now also safe to re-run (`overwrite: true`
  above), so a full re-run is safe end-to-end, not just at the PyPI step.

**1k. `Makefile`**
- Header comment `# md2okf — developer task runner.` → `# code2okf — ...`
- `kits/md2okf/` references in comments → `kits/code2okf/`
- `.PHONY` entry and target `test-md2okf` → `test-code2okf` (update its one
  caller in the `test:` target too)
- `dist:` smoke test: `dist/md2okf-*.tar.gz` → `dist/code2okf-*.tar.gz`,
  scratch-dir globs, `md2okf --version` / `md2okf --dry-run -o wiki doc/` →
  `code2okf` equivalents
- `check-okf:` target's script path
  `kits/md2okf/files/home/.pi/agent/skills/compile-okf/scripts/check-okf.sh`
  → `kits/code2okf/...`

**1l. Misc**
- `web2md/src/web2md.py:34`: `UA = "md2okf-web2md/0.1 (+https://github.com/lars20070/md2okf)"`
  → `"code2okf-web2md/0.1 (+https://github.com/lars20070/code2okf)"`

**1m. `uv.lock`** — do not hand-edit the `name = "md2okf"` entry; regenerate
via `uv lock` (or `uv sync`) after `pyproject.toml` and `src/code2okf/` are
renamed.

**1n. Stale build artifacts** — delete `.venv/` and `dist/` (both
gitignored, hold old `md2okf-0.1.0`/`md2okf-0.2.0` output) and regenerate
via `uv sync` / `make dist` rather than hand-editing.

**Explicitly out of scope**: `.claude/plans/interface-plan.md` (internal
planning doc, 96 mentions, unrelated to this rename) —leave untouched.

**1o. Residual sweep — run after 1a–1n, before touching git at all.** The
per-file inventory above is a guide, not a guaranteed-exhaustive edit list —
Stage 1g's original test-file entries already turned out to be incomplete
once checked directly (fixed above). Close that gap with a repository-wide
search and resolve every hit as either renamed or explicitly justified:

```bash
rg -n --hidden -S 'md2okf|MD2OKF' \
  --glob '!.git/**' --glob '!.venv/**' --glob '!dist/**' \
  --glob '!**/__pycache__/**' --glob '!**/*.pyc'
find . -path './.git' -prune -o -path './.venv' -prune -o \
  -iname '*md2okf*' -print
```

Expected surviving hits after a complete rename: only
`.claude/plans/interface-plan.md` (explicitly out of scope, historical) and
this plan file itself. Anything else is a missed rename.

---

## Stage 2 — CHANGELOG/VERSION squash (its own reviewable step)

Done as its own working-tree edit, immediately after Stage 1's residual
sweep comes up clean and before anything is staged, so the wording can be
reviewed on its own merits — as the finished `CHANGELOG.md` content, shown
to the user separately from the mechanical rename, rather than mixed into
one big change to skim past. (Nothing is staged yet at this point, so this
isn't a `git diff` in the traditional sense — nearly the whole tree is new
to git — but it's still worth presenting as its own reviewable unit before
Stage 3 stages everything together.)

1. In `CHANGELOG.md`, merge `## [0.2.0] - 2026-09-20` and
   `## [0.1.0] - 2026-09-07` into one `## [0.1.0]` entry dated today
   (2026-09-20 — when this release is actually cut). Combine the
   `### Added` / `### Changed` / `### Fixed` / `### Removed` subsections;
   where a later entry describes replacing something the earlier entry
   added (e.g. 0.2.0 "Removed: the shell compile path" superseding parts of
   0.1.0), compress rather than list both, since this is internal history
   predating the project's public existence, not a promise to any external
   consumer.
2. Rename every surviving `md2okf` mention inside the squashed entry to
   `code2okf` (deliberately deferred from Stage 1 so the squash and the
   rename are each a clean, separate diff).
3. Set `VERSION` to `0.1.0` (currently `0.2.0`).
4. Keep the `## [Unreleased]` header in place (empty), per Keep a Changelog
   convention.

---

## Stage 3 — Verification checkpoint

**Critical ordering fix, confirmed by reading the `Makefile`'s `lint` target
in full**: every check in `make lint` (markdownlint, JSON, yamllint,
shellcheck, cspell, ruff) is driven off `git ls-files`, which lists only
tracked/staged files, never untracked ones. Right now only `README.md` is
tracked — everything else in this repo is untracked. Running `make lint`
before staging would therefore silently skip nearly the entire project and
give a false-green result. **Stage the renamed tree before the first lint
run.** Staging (`git add`) is not commit/push and is explicitly fine under
`AGENTS.md`'s git policy; nothing is reviewable-diff-broken by this, since
`git diff --cached` still shows the full staged diff for review at any
point, and nothing is committed until the user does so in Stage 4.

1. **Stage everything** (after the Stage 1o residual sweep comes up clean
   and the Stage 2 squash is done — both are on-disk working-tree edits at
   this point, nothing staged yet): `git add -A && git status --short`.
   Skim the status for anything unexpected (stray
   `__pycache__`/`.pytest_cache`/`.ruff_cache`/`.DS_Store` — these should
   already be `.gitignore`d, but verify). Run `git diff --cached --check`
   to catch whitespace errors. Since nearly every file is new to git (only
   `README.md` was previously tracked), there's little a `git diff` would
   show beyond new-file content — the Stage 2 squash is reviewed by reading
   the finished `CHANGELOG.md` section directly (call this out to the user
   explicitly as its own review point before moving on), not via a
   before/after diff.
2. `make lint` — now actually exercises the full staged tree, including the
   VERSION↔CHANGELOG.md agreement check, which by this point should pass
   against the squashed `0.1.0`/`0.1.0`.
3. `make validate` (`scripts/validate-spec.sh`) — static schema check of
   `kits/code2okf/spec.yaml`; no Docker/login needed.
4. `make test-shell` (`tests/test-mount-state.sh`, `tests/test-sandbox-guest.sh`
   is not run by this target) — exercises the renamed `CODE2OKF_STATE_DIR`/
   `CODE2OKF_REQUIRE_BIND` env vars and the other literals fixed in Stage 1g.
5. `make test-web2md` — confirms the `web2md.py` UA string edit didn't break
   anything.
6. `make test-clis` — confirms `pyproject.toml`'s force-include renames
   didn't collaterally break the four helper CLIs.
7. `make test-code2okf` (renamed from `test-md2okf`) — the driver's own
   pytest suite; most directly exercises the Stage 1c/1g renames, including
   the corrected `test_resources.py` and `test_package.py` assertions.
8. `make dist` — builds wheel + sdist, rebuilds the wheel from the sdist in
   a scratch dir, and smoke-tests it (`code2okf --version`,
   `code2okf --dry-run -o wiki doc/`) from outside the checkout.
9. **Inspect the built artifact manifests directly, not just whether install
   succeeds** — this is how the `.codex` sdist leak (fixed in Stage 1b) was
   actually found:
   ```bash
   tar tzf dist/code2okf-0.1.0.tar.gz
   unzip -l dist/code2okf-0.1.0-py3-none-any.whl
   uv tool run twine check dist/*
   ```
   Confirm `.codex` is absent from the sdist listing, and both files
   carry only the intended `code2okf/` (wheel) / project-root (sdist)
   contents.

**Do not run `make test` as a bundle here** — it chains
`test-shell test-web2md test-clis test-code2okf test-sandbox`, and the last
of those needs a live `sbx login` session unavailable in a typical agent
sandbox, making the bundle fail on infrastructure grounds rather than code
grounds. Run steps 4–7 individually instead (as above), then treat
`test-sandbox` as its own required checkpoint:

10. **`make test-sandbox` — required, not optional.** `AGENTS.md` is
    explicit: "If you changed what the sandbox installs or what it carries
    in `kits/md2okf/files/`, also run `sbx rm --force md2okf && make
    test-sandbox`." This rename does exactly that (moves and edits
    `kits/*/files/`), so this check is mandated by repo policy, not a nice-
    to-have. With an active `sbx login` session:
    ```bash
    sbx rm --force code2okf
    make test-sandbox
    ```
    If `sbx login` is unavailable in this environment, this is an
    **outstanding required check**, not a skippable one — hand it to the
    user explicitly as unfinished verification rather than declaring the
    rename complete without it. The old `md2okf` sandbox is left alone
    (decision 5) unless the user chooses to clean it up.
11. `make check-okf` — needs a generated `okf/` wiki plus `okfctl` on PATH;
    validates wiki *content*, unrelated to this rename's correctness — still
    genuinely skippable for this task.

---

## Stage 4 — Git handoff checkpoint

Per `AGENTS.md`, I never run `git commit` or `git push` in this repo. My
part ends at staging and drafting.

1. **Staging already happened in Stage 3** (`git add -A`, before the lint
   pass) — nothing new to stage here. Because the directory renames
   (`src/md2okf/`→`src/code2okf/`, `kits/md2okf/`→`kits/code2okf/`) happen
   on disk before anything is committed, this lands as new files under
   their final paths in one commit — no `git mv` history to preserve.
2. **Draft commit message** for the user, reflecting that this is
   simultaneously a rename and the project's real first commit, e.g.:
   ```
   Rename project to code2okf and cut the v0.1.0 release

   Establish the codebase (previously developed as md2okf) under its
   permanent name, code2okf, with every command, package, sandbox name,
   env var, and doc reference updated to match. Squash the pre-rename
   0.1.0/0.2.0 changelog history into a single v0.1.0 entry, since
   nothing has shipped publicly from this repository before now. Also
   fix ci.yml's push trigger and CONTRIBUTING.md's Releasing section to
   say main instead of the stale master.

   Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
   ```
3. **What I do not do**: `git commit`, `git push`, create/push the `v0.1.0`
   tag, open the PR, or merge it.
4. **What the user does by hand**:
   - Review the staged diff (`git diff --cached`) plus the Stage 2 changelog
     wording and Stage 3 verification output.
   - `git commit` with the drafted message (on a feature branch, e.g.
     `rename-to-code2okf`, or directly on `main` given this predates any
     real release).
   - Push, open a PR (or push straight to `main`), let CI run — the
     `pull_request:` trigger fires regardless of branch name, so this works
     even before the `master`→`main` push-trigger fix lands.
   - Merge to `main`.
   - **Tag safely, not blindly** — a bare `git tag v0.1.0` right after
     merging risks tagging a stale local `HEAD` rather than the actual
     merged `main` (e.g. if the merge was a squash/merge commit on GitHub
     and the local branch never fast-forwarded to it). Update and verify
     `main` first, use an annotated tag, and confirm what it actually
     points at before pushing:
     ```bash
     git fetch origin
     git switch main
     git pull --ff-only origin main
     git status --short          # must be clean
     git tag -a v0.1.0 -m 'code2okf v0.1.0'
     git show --stat v0.1.0      # confirm this is the intended release commit
     git push origin v0.1.0
     ```

---

## Stage 5 — PyPI publication checkpoint

**5a. Manual, before pushing the tag** — register a PyPI **pending
publisher** for `code2okf` (it doesn't exist on PyPI yet — confirmed via a
404 on PyPI's JSON API), at
https://pypi.org/manage/account/publishing/, with these values (derived
directly from `release.yml`'s `publish-pypi` job):

| Field | Value |
|---|---|
| PyPI Project Name | `code2okf` |
| Owner | `lars20070` |
| Repository name | `code2okf` |
| Workflow filename | `release.yml` |
| Environment name | `pypi` |

This is a PyPI web-UI action only — no repo file can do it — and must be in
place before the tag push, or the `publish-pypi` job's OIDC exchange has
nothing to match against.

**Two cautions**, both from PyPI's own trusted-publisher documentation:
- A pending publisher does **not** reserve the `code2okf` name — it only
  pre-authorizes this workflow to claim it on first successful publish.
  Someone else could register `code2okf` on PyPI between now and the tag
  push. Recheck availability (`https://pypi.org/pypi/code2okf/json` should
  still 404) immediately before pushing the tag, and minimize the gap
  between creating the pending publisher and the actual publish.
- Decision 6 (no required-reviewer gate on the GitHub `pypi` environment):
  this means the pending publisher being live is the *only* thing standing
  between a tag push and a real PyPI upload — there is no manual approval
  step in between. Make sure the tag push itself (Stage 4) is the intended,
  reviewed trigger, not a rehearsal.

**5b. What happens automatically once `v0.1.0` is pushed** (existing
`release.yml` pipeline, only needing the Stage 1j `environment.url` fix):
1. `verify` job: `scripts/check-release-tag.sh` confirms the tag matches
   `VERSION` (`0.1.0`); `scripts/release-notes.sh 0.1.0` confirms the
   CHANGELOG section isn't empty; `make lint` re-runs in full.
2. `build` job: `make dist` builds wheel + sdist, uploads as an artifact.
3. `publish-pypi` job: OIDC token, `uv publish --trusted-publishing always
   dist/*.tar.gz dist/*.whl`.
4. `github-release` job: creates the GitHub Release for `v0.1.0`, body from
   `CHANGELOG.md`'s squashed `## [0.1.0]` section, artifacts attached.

**5c. What to check afterward**:
- `https://pypi.org/p/code2okf` shows `0.1.0` as the only/latest release.
- `uvx code2okf --version` (or `uv tool install code2okf`) installs and runs
  from the real published index.
- The GitHub Release for `v0.1.0` exists with the squashed changelog body
  and both `.tar.gz`/`.whl` assets.
- `README.md`'s CI and "latest release" badges render correctly once the
  Stage 1i URL fixes are live and a release exists.
- The old `md2okf` PyPI project (v0.2.0) is untouched — nothing here writes
  to it.

---

## Critical files

- `pyproject.toml` — package name, entry point, wheel layout,
  `sdist.exclude` (`.codex` addition)
- `src/md2okf/workbench.py` → `src/code2okf/workbench.py` — `SANDBOX_NAME`,
  lock path, state-dir env var
- `kits/md2okf/spec.yaml` → `kits/code2okf/spec.yaml` — sandbox name,
  entrypoint paths
- `tests/test_package.py`, `tests/test_resources.py`,
  `tests/test-sandbox-guest.sh`, `tests/test-mount-state.sh` — most exposed
  to the rename; the latter two turned out to need far more than the env-var
  rename originally scoped (see Stage 1g)
- `.github/workflows/ci.yml` — `master`→`main` fix, job/env renames
- `.github/workflows/release.yml` — `environment.url` fix,
  `actions/upload-artifact` `overwrite: true` fix
- `CHANGELOG.md` / `VERSION` — Stage 2 squash
- `Makefile` — target renames, `make dist` smoke test literals

## Verification summary

Order matters: **Stage 1 rename (incl. the 1o residual sweep) → Stage 2
CHANGELOG/VERSION squash → stage everything (`git add -A`) → `make lint` →
`make validate` → `make test-shell` / `make test-web2md` / `make test-clis`
/ `make test-code2okf` individually (not the `make test` bundle) → `make
dist` → manifest/`twine check` inspection → `sbx rm --force code2okf &&
make test-sandbox` (required per `AGENTS.md`, not optional — flag as
outstanding if `sbx login` isn't available in this environment)**. Staging
before linting matters because `make lint` is driven off `git ls-files` and
would otherwise silently skip almost the whole project. `make check-okf` is
the one genuinely optional/skippable check (validates wiki content, not
this rename). Nothing is committed, pushed, tagged, or published without
the user's own action at Stages 4 and 5.
