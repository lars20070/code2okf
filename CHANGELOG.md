# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-09-20

First release.

### Added

- **`code2okf`, one command from Markdown to an OKF wiki.** Files or folders
  in, a directory out: `code2okf [-o DIR] [--spec FILE] [-n N] [--fresh]
  [--dry-run] [-q|-v] [FILE|DIR ...]`. stdout carries one TSV row per document
  (`path  iterations  hash-before  hash-after`) and nothing else, diagnostics
  go to stderr, and the exit status is the verdict: 0 every document converged
  (a hash-stable first pass included — that is the idempotent re-run), 1 the
  run failed, 2 usage or environment, decided before any work starts. The
  driver is stdlib-only Python with a pytest suite that fakes the one `sbx`
  seam, so the Ralph loop, the prompts and the event rendering are testable
  without a paid sandbox run.
- **A workbench, so one sandbox serves any input and output.** sbx fixes a
  sandbox's mounts at creation, so runs are staged through
  `$XDG_STATE_HOME/code2okf/work`: inputs copied in, the target wiki mirrored
  in before the run and back out after every iteration, the five mount paths
  never changing. The sandbox is rebuilt only when the kit it was built from
  changes, when the recorded configuration no longer matches, or on `--fresh`
  — and one that cannot be proven to belong to the driver is reported, never
  deleted.
- **The sandbox sees only what the agent needs.** The wiki and the session
  state are mounted read-write, the staged inputs, the helper CLIs and
  `SPEC.md` read-only, and nothing else on the host is visible inside the
  microVM — so the agent's restriction to the wiki is enforced by the
  filesystem rather than by instructions alone. The mount list lives in
  `src/code2okf/workbench.py`. The wiki is the primary mount and therefore the
  working directory inside the VM, which is why the agent's config and the
  `compile-okf` gate address the read-only mounts as `../md/`, `../scripts/`
  and `../SPEC.md`. Pi's native `~/.pi/agent/sessions` tree persists in
  `$XDG_STATE_HOME/code2okf/sessions`, bind-mounted from host state; the guest
  helper reads `CODE2OKF_STATE_DIR`, and the per-user lock sits at
  `/tmp/code2okf-<uid>.lock`, outside the configurable state directory. An
  exported `XDG_STATE_HOME` takes precedence, with `~/.local/state` as the
  fallback; changing it requires rebuilding the sandbox.
- **OKF v0.2 output, gated before the agent finishes.** Every page carries
  `generated: { by, at }` provenance (§5.2) with the actor recorded as
  `pi/<model-id>` (§7), the bundle-root `index.md` declares its `okf_version`,
  and index links are relative — what `okfctl index build` writes. `okfctl`
  (pinned 0.4.0, checksummed release archive) owns the reserved `index.md`
  files, so the agent runs `okfctl index build` instead of writing link lists
  by hand, and a `curate-okf` skill covers it.
- **One gate with two call sites.** `compile-okf/scripts/check-okf.sh` is what
  the agent runs before finishing and what `make check-okf` runs on the host —
  one implementation, not two. It combines `okfctl validate`, a
  dependency-free `frontmatter-guard.py`, `okfctl lint`, `okfctl analyze` for
  links that resolve to nothing, and `okfctl index check`, which fails closed
  on a stale or hand-edited index. Lint defects (`broken-link`, `orphan`,
  `type-hygiene`, `status-lifecycle`, `spec-version`) block; `missing-xref`
  and `coverage-gap` are printed as advice, since they are judgment calls and
  the gate runs unattended inside the compile loop.
- **Publication to PyPI.** `code2okf` is installable with
  `uv tool install code2okf` (or runnable with `uvx code2okf`), with the
  sandbox kit, `SPEC.md` and the four helper CLI projects carried inside the
  wheel, so it compiles without a checkout. A `vX.Y.Z` tag builds the wheel
  and sdist once, publishes them by trusted publishing — OIDC, no stored token
  — and then creates the GitHub Release with those same artifacts attached and
  the matching section of this file as its notes.
- Four helper CLIs that survey the wiki — `inspectmd` (a Markdown heading map),
  `inspectokf` (the wiki tree), `sizeokf` (word counts, excluding frontmatter)
  and `merkleokf` (a hash per file and per directory) — exposed to the agent
  inside the sandbox and installable on the host with `make install-clis`.
  `merkleokf` hashes raw bytes and is what decides convergence; its `--nolog`
  skips the root `log.md` whatever the wiki directory is called, since `-o` can
  name any directory.
- `NOTICE-OKF-SPEC.md` and `LICENSE-OKF-SPEC.txt`, recording that the bundled
  `SPEC.md` is the Open Knowledge Format v0.2 specification, taken verbatim
  from `GoogleCloudPlatform/open-knowledge-format` and licensed Apache-2.0.
  Both ship in the wheel and the sdist beside code2okf's own MIT licence.
  Package metadata carries the README as its long description, an SPDX licence
  expression, project URLs and classifiers, and the sdist leaves out the
  agent-tool directories and their vendored third-party skills.
- A developer task runner and offline suites: `make lint` (markdownlint, jq,
  yamllint, shellcheck, cspell and ruff, plus a `VERSION` ↔ `CHANGELOG.md`
  agreement check), `make validate` for the kit spec, `make dist` for the wheel
  and sdist with a smoke test of the built artifact from outside the checkout,
  and pytest suites for the driver, the `web2md` scraper and the four CLIs. CI
  runs each as its own job, and `make test-sandbox` checks a live sandbox
  against what the kit promises.
- Host requirements are `sbx` (0.43.0 or newer) and `uv`; the kit pins the Pi
  coding agent at 0.85.1. `OPENROUTER_API_KEY` is handed to `sbx secret`, so
  the key stays outside the VM and out of your shell environment.
