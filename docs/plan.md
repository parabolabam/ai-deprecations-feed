# AI Deprecations Feed — Stage 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development (recommended) or superpowers:executing-plans. Steps use `- [ ]`.
> **Owner rules (from ~/.claude/CLAUDE.md):** every implementing agent runs with `model: "sonnet"`, has the `Skill` tool (`general-purpose` type, not `code-writer`), invokes the `ponytail` skill before writing code, and pastes the verify command + its real output. The main session re-runs every verify command before marking a task done, and reviews `git diff --staged` before each commit.

## Context

The owner needs a readable RSS feed of AI-provider model/API deprecations. OpenAI has no official subscription. `deprecations.info` (open-source `deprecations/deprecations-rss`) has had 0 OpenAI and 0 Bedrock entries for weeks while every scrape run reports "success": both pages were restructured (OpenAI moved from dated sections to big tables; Bedrock moved its list to `model-lifecycle-legacy`), and its health check only fires when a provider *had* entries before. This plan builds Stage 1 of the approved design: skeleton, OpenAI parser, diff fallback for the other 8 sources, feeds, Pages, health checks, issues. Stage 2 parsers get their own plans.

**Goal:** Daily RSS + JSON feed of deprecation announcements for 9 sources on GitHub Pages, that never goes silently stale and never loses records.

**Architecture:** Python package `depfeed`, run daily by GitHub Actions. Per source: fetch markdown → normalize → compare with last snapshot → extractor (parser or diff fallback) → sanity check → merge into archive → rebuild feeds. Code on `main`, state on branch `data`, site via `actions/deploy-pages`. Extractor = plain function per source, so an LLM extractor can replace it later without other changes.

**Tech Stack:** Python ≥3.12 (Actions pins 3.12; local 3.14 is fine), `uv`, stdlib only at runtime (`urllib.request`, `difflib`, `xml.etree.ElementTree`, `json`, `hashlib`, `html`), `pytest` for dev. No BeautifulSoup: every source has a markdown endpoint (research below).

**Spec:** design doc «Лента депрекаций AI-провайдеров — дизайн» (2026-11-22). Task 0 commits it as `docs/design.md` and this plan as `docs/plan.md`.

**Repo:** `github.com/parabolabam/ai-deprecations-feed`, public, local `~/github/ai-deprecations-feed`. Feed: `https://parabolabam.github.io/ai-deprecations-feed/feed.xml` (+ `feed.json`, `deprecations.json`, `status.json`). `parabolabam` = output of `gh api user --jq .login` after the owner logs in.

## Global Constraints

- Sources (9): OpenAI, Anthropic, Google AI (Gemini), Google Vertex AI, AWS Bedrock, Cohere, Groq, xAI, Azure AI Foundry. Stage 1: parser for OpenAI only; the other 8 use the diff extractor.
- Daily cron + `workflow_dispatch`. No secrets; only `GITHUB_TOKEN`.
- Workflow permissions: `contents: write`, `issues: write`, `pages: write`, `id-token: write`, `actions: write` (keepalive only). Nothing else.
- Code on `main`; data on `data`. Commit to `data` only when a file changed. Weekly heartbeat forces one change.
- Retention: snapshot = latest only per source; parsed records = forever in `deprecations.json`; feed items = last 6 months (`WINDOW_DAYS = 183`); raw diff and health records = 90 days (`RAW_DAYS = 90`); status = current only.
- Feed date of a record = `announced` if set, else `first_seen`. The 6-month window uses it, so the first OpenAI run does not push 2023 history to readers. If Task 4 shows OpenAI rows without a notice date, the rule becomes `announced or min(shutdown, first_seen) or first_seen` (a past shutdown keeps the row out; a future shutdown never makes a future `pubDate`).
- Reset of a broken source (a legitimate big change, e.g. a page split): delete `snapshots/<id>.md` and `sources.<id>` from `status.json` on branch `data`; the next run treats the source as new. Written in README and in every auto-issue body.
- All dates UTC, ISO `YYYY-MM-DD`.
- Monthly: squash `data` to one commit (orphan + force-push).
- Both workflows use `concurrency: {group: data-branch, cancel-in-progress: false}` so the squash never races a daily push.
- HTTP: `User-Agent: ai-deprecations-feed (+https://github.com/parabolabam/ai-deprecations-feed)` (non-browser on purpose: Gemini serves markdown only to non-browser UAs), `Accept: text/markdown, text/plain;q=0.9`, timeout 30 s, 1 retry on network error / 429 / 5xx.
- The run exits 0 when a source is broken (data and site must still update; the issue is the signal). It exits non-zero only on a bug outside per-source processing.

## Decisions the spec left to the executor

**Sources** (verified by research 2026-11-22: all return 200 to plain GET, no bot challenge, all serve markdown):

| id | name | fetch URLs (joined with `\n`) | link | extractor |
|---|---|---|---|---|
| openai | OpenAI | `https://developers.openai.com/api/docs/deprecations.md` | `https://developers.openai.com/api/docs/deprecations` | `parsers.openai.parse` |
| anthropic | Anthropic | `https://platform.claude.com/docs/en/about-claude/model-deprecations.md` | same without `.md` | diff |
| gemini | Google AI (Gemini) | `https://aistudio.google.com/docs/deprecations.md` | `https://aistudio.google.com/docs/deprecations` | diff |
| vertex | Google Vertex AI | `https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/model-versions.md.txt`, `https://docs.cloud.google.com/vertex-ai/generative-ai/docs/deprecations.md.txt`, `https://docs.cloud.google.com/vertex-ai/generative-ai/docs/deprecations/partner-models.md.txt` | `https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/model-versions` | diff |
| bedrock | AWS Bedrock | `https://docs.aws.amazon.com/bedrock/latest/userguide/model-lifecycle-legacy.md`, `https://docs.aws.amazon.com/bedrock/latest/userguide/model-lifecycle.md` | `.../model-lifecycle-legacy.html` | diff |
| cohere | Cohere | `https://docs.cohere.com/docs/deprecations.md` | without `.md` | diff |
| groq | Groq | `https://console.groq.com/docs/deprecations.md` | without `.md` | diff |
| xai | xAI | `https://docs.x.ai/developers/release-notes.md` (xAI has no deprecations page) | without `.md` | diff, `keep=r"(?i)end of life\|deprecat\|retire\|sunset\|shut ?down"` |
| azure | Azure AI Foundry | `https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/model-retirement-schedule?accept=text/markdown` | without query | diff |

Traps found: the old Vertex path `.../vertex-ai/generative-ai/docs/learn/model-versions.md.txt` returns 200 but is a stale copy — never use it. The Vertex partner-models `.md.txt` URL is not verified; if the Task 1 live test shows non-200, remove it and note it in README.

**Normalization** (`normalize`): `html.unescape` repeated until the text stops changing (Gemini sometimes double-encodes, e.g. `&amp;quot;`) → drop a leading YAML front-matter block (`---` … `---`) → strip each line, collapse inner whitespace runs to one space → drop blank lines → drop lines that match a per-source `ignore` regex. Idempotent. No HTML step.

**Junk detection** (source "silently stopped"): `fetch_broken` when HTTP fails after retry, OR the body starts with `<!doctype`/`<html` (case-insensitive), OR content-type is `text/html`, OR normalized text < 500 chars, OR < 50% of the last snapshot's length. Snapshot and records stay unchanged.

**Merge rule for edited records:** `id = sha1("|".join(parts))[:16]`; parsed: parts = `(source, announced or shutdown or "", affected[0] or title)`; raw: `(source, first_seen, text)`; health: `(source, first_seen, title)`. Same id → replace changed fields, keep `first_seen`, set `updated = today`. Feed item keeps its guid and gets `date_modified`. A record that disappears from the page stays in the archive.

**OpenAI record unit:** one record per table row (the page is now tables `## Upcoming deprecations`, `## Feature and endpoint deprecations`, `## Past deprecations`; columns e.g. `Shutdown date | Affected model | Status | Recommended replacement | Notice date`). `announced` = Notice date, `shutdown` = Shutdown date, `affected` = backticked IDs in the affected cell (else comma-split cell text), `replacement` = replacement cell (`—`/empty → None), `title` = `"<affected cell text> — shutdown <shutdown>"`.

## Data layout

Branch `data` (checked out at `./data` locally and in CI; `data/` and `site/` are in `.gitignore` on `main`):
```
snapshots/<source_id>.md     latest normalized text
deprecations.json            {"records": [Record, ...]}  (archive)
status.json                  {"heartbeat": "YYYY-MM-DD"|null, "sources": {id: Status}}
```
`Status = {"state": "ok"|"diff"|"parser_broken"|"fetch_broken", "since": date, "changed": date|null, "count": int, "error": str|null}`.
Site (`./site`, built each run, deployed, not committed): `feed.xml`, `feed.json`, `deprecations.json`, `status.json`.

## Review Focus

1. **Source returns 200 with junk** (HTML shell, challenge page, Gemini UA switch, truncated page) → `fetch_broken`, snapshot not overwritten, health record + issue. Tests: Task 1 (`fetch` rejects HTML), Task 5 (shrink >50%).
2. **First run of a diff source** (no snapshot) → snapshot stored, no record. Test: Task 3.
3. **Parser breaks after a redesign** (the deprecations.info failure) → 0 records, drop >50%, or a record with neither `announced` nor `shutdown` → old records kept, raw diff record, health record only on transition into broken (not daily), one open issue per source. Tests: Task 5, Task 7.
4. **Announcement edited on the page** → one record updated in place, no duplicate. Test: Task 2.
5. **Huge diff** (restructure moves every line) → text capped at `MAX_DIFF_CHARS = 4000` + `"\n…(truncated)"`. Test: Task 3.

---

### Task 0: Bootstrap repo

**Files:** Create `pyproject.toml`, `.gitignore`, `README.md`, `depfeed/__init__.py`, `depfeed/parsers/__init__.py`, `tests/test_smoke.py`, `docs/design.md`, `docs/plan.md`.

- [ ] **Step 1: Owner logs in** — owner runs `gh auth login` (not the agent). Verify: `gh api user --jq .login` prints a login.
- [ ] **Step 2: Create repo** — `mkdir -p ~/github && cd ~/github && gh repo create ai-deprecations-feed --public --clone`.
- [ ] **Step 3: Skeleton** — `pyproject.toml`: name `depfeed`, `requires-python = ">=3.12"`, no runtime deps, dev group `pytest`; `uv lock`. `.gitignore`: `data/`, `site/`, `.venv/`, `__pycache__/`. README: one paragraph + feed URLs. Copy the design doc (owner's pasted text) to `docs/design.md` and this plan to `docs/plan.md`. `tests/test_smoke.py`: `import depfeed`.
- [ ] **Step 4: Verify** — `uv run pytest -q` → `1 passed`.
- [ ] **Step 5: Commit + push main.**
- [ ] **Step 6: Data branch** — `git switch --orphan data && echo "State branch, written by CI." > README.md && git add README.md && git commit -m "data: init" && git push -u origin data && git switch main`.
- [ ] **Step 7: Pages** — `gh api -X POST repos/{owner}/ai-deprecations-feed/pages -f build_type=workflow`. Verify: `gh api repos/{owner}/ai-deprecations-feed/pages --jq .build_type` → `workflow`.

### Task 1: Sources, fetch, normalize

**Files:** Create `depfeed/sources.py`, `depfeed/fetch.py`, `tests/test_fetch.py`.

**Interfaces — Produces:**
- `@dataclass(frozen=True) class Source: id: str; name: str; urls: tuple[str, ...]; link: str; parser: Callable[[str, str], list[Record]] | None = None; keep: str | None = None; ignore: tuple[str, ...] = ()` — `SOURCES: list[Source]` = the table above (openai's `parser` wired in Task 4; until then `None`).
- `class FetchError(Exception)`; `fetch(url: str) -> str`; `normalize(text: str, ignore: tuple[str, ...] = ()) -> str`; `fetch_source(src: Source) -> str` = `normalize("\n".join(fetch(u) for u in src.urls), src.ignore)`.

- [ ] **Step 1: Tests**
  - `test_normalize_idempotent`: `normalize(normalize(s)) == normalize(s)` for a sample with tabs, blank lines, `&amp;quot;`.
  - `test_normalize_strips_front_matter_and_whitespace`: `"---\nms.date: 1\n---\n  a   b \n\n c"` → `"a b\nc"`.
  - `test_normalize_ignore`: `normalize("x\nLast updated 2026\ny", (r"^Last updated",))` → `"x\ny"`.
  - `test_fetch_rejects_html`: monkeypatch `urllib.request.urlopen` to return `<!DOCTYPE html>…` with `text/html` → `FetchError`.
  - `test_fetch_retries_once_on_503`: first call raises `HTTPError(503)`, second returns markdown → returns text; urlopen called 2×.
  - `test_live_sources` (`@pytest.mark.skipif(not os.getenv("LIVE"))`): for each source, `len(fetch_source(src)) > 500`.
- [ ] **Step 2: Run** `uv run pytest tests/test_fetch.py -q` → fails (import error).
- [ ] **Step 3: Implement** per "Normalization", "Junk detection" (the HTML/content-type part) and HTTP constraints.
- [ ] **Step 4: Run** `uv run pytest tests/test_fetch.py -q` → all pass (live skipped). Then `LIVE=1 uv run pytest tests/test_fetch.py::test_live_sources -q` → pass; fix/remove URLs per the table's rule and report what changed.
- [ ] **Step 5: Commit.**

### Task 2: Records and archive

**Files:** Create `depfeed/records.py`, `tests/test_records.py`.

**Interfaces — Produces:**
- `@dataclass class Record: id: str; source: str; kind: Literal["parsed","raw","health"]; title: str; url: str; announced: str|None = None; shutdown: str|None = None; affected: list[str] = field(default_factory=list); replacement: str|None = None; text: str|None = None; first_seen: str|None = None; updated: str|None = None`.
- `record_id(*parts: str) -> str`; `feed_date(r: Record) -> str`; `merge(archive: list[Record], new: list[Record], today: str) -> list[Record]`; `prune(records: list[Record], today: str) -> list[Record]` (drops raw/health older than `RAW_DAYS` by `first_seen`); `load_records(path: Path) -> list[Record]` (missing file → `[]`); `save_records(path: Path, records: list[Record]) -> None` (sorted by `feed_date` desc, then id; `indent=1`, `ensure_ascii=False`, trailing newline — stable output so unchanged data makes no diff).

- [ ] **Step 1: Tests**
  - `test_merge_new_sets_first_seen`: new record → `first_seen == today`, `updated is None`.
  - `test_merge_edit_updates_in_place`: archive has id X (first_seen `2026-01-01`), new has id X with other `replacement` → one record, `replacement` new, `first_seen == "2026-01-01"`, `updated == today`.
  - `test_merge_unchanged_keeps_updated_none`.
  - `test_merge_keeps_records_missing_from_page`.
  - `test_prune_raw_90_days`: raw first_seen `today-91` dropped, `today-89` kept, parsed from 2023 kept.
  - `test_save_load_roundtrip_stable`: save, load, save → identical bytes.
- [ ] **Step 2–4:** run (fail) → implement → `uv run pytest tests/test_records.py -q` passes.
- [ ] **Step 5: Commit.**

### Task 3: Dates and diff extractor

**Files:** Create `depfeed/dates.py`, `depfeed/diff.py`, `tests/test_dates.py`, `tests/test_diff.py`.

**Interfaces — Produces:**
- `parse_date(s: str) -> str | None`: strips `**`, `^\d+^` footnotes; returns the first date found as ISO. Formats: `YYYY-MM-DD`, `Mon D, YYYY`, `Month D, YYYY` (accept `Sept`), `MM/DD/YY`. Surrounding text ("Not before …", "… or later") is allowed.
- `diff_record(src: Source, old: str | None, new: str, today: str) -> Record | None`: `None` if `old is None`; added lines from `difflib.ndiff`/`unified_diff` of lines; filter by `src.keep` if set; `None` if no lines left; else `Record(kind="raw", title=f"{src.name}: page changed", url=src.link, text=<lines joined, capped>, id=record_id(src.id, today, text))`.

- [ ] **Step 1: Tests**
  - `test_parse_date` table: `"**Dec 11, 2026**"→"2026-12-11"`, `"Not sooner than November 9, 2027"→"2027-11-09"`, `"2027-04-14^3^"→"2027-04-14"`, `"09/21/26"→"2026-09-21"`, `"Sept 7, 2026"→"2026-09-07"`, `"TBD"→None`.
  - `test_diff_first_run_none`: `old=None` → `None`.
  - `test_diff_added_lines_only`: removed lines absent from `text`, added present.
  - `test_diff_only_removals_none`.
  - `test_diff_keep_filter`: xai-like source, added `"New grok-5 pricing"` and `"grok-3 end of life on Jan 1, 2027"` → text has only the second.
  - `test_diff_cap`: 10 000 chars added → `len(text) <= 4000 + len("\n…(truncated)")`, ends with `…(truncated)`.
- [ ] **Step 2–4:** fail → implement → `uv run pytest tests/test_dates.py tests/test_diff.py -q` passes.
- [ ] **Step 5: Commit.**

### Task 4: OpenAI parser

**Files:** Create `depfeed/parsers/openai.py`, `tests/fixtures/openai.md`, `tests/test_openai.py`; Modify `depfeed/sources.py` (wire `parser=openai.parse`).

**Interfaces:** Consumes `Record`, `record_id`, `parse_date`. Produces `parse(text: str, link: str) -> list[Record]`.

Approach: walk lines; a pipe-table header row maps columns by lowercase keyword: `shutdown`→shutdown, `affected`→affected, `replacement`→replacement, `notice`→announced; skip the `|---|` row; each data row → one record per "OpenAI record unit". Tables whose header lacks `shutdown` and `affected` are ignored. Never depend on heading text.

- [ ] **Step 1: Fixture** — `curl -s https://developers.openai.com/api/docs/deprecations.md -o tests/fixtures/openai.md`; then save `normalize(fixture)` back (parser runs on normalized text in production).
- [ ] **Step 2: Tests**
  - `test_parses_many`: `len(parse(fixture, link)) >= 30` (adjust the floor to ~80% of the real count and state it in the report).
  - `test_known_row`: a record with `"gpt-5-mini" in affected`, `shutdown == "2026-12-11"`, `announced == "2026-06-11"`, `replacement == "gpt-6.1-terra"` (example from research; if the fixture differs, pick a real row and say so).
  - `test_all_dated`: every record has `announced` or `shutdown`.
  - `test_all_have_notice_date`: every record has `announced`. If the real fixture fails it, do not weaken it silently: switch `feed_date` to the fallback rule in Global Constraints, change this test to assert that rule, and report it.
  - `test_ids_unique`.
  - `test_no_tables_returns_empty`: `parse("# Title\ntext", link) == []`.
  - `test_ids_stable_when_replacement_edited`: change one replacement cell → same id set.
- [ ] **Step 3–4:** fail → implement → `uv run pytest tests/test_openai.py -q` passes.
- [ ] **Step 5: Commit** (fixture included).

### Task 5: Per-source pipeline and health checks

**Files:** Create `depfeed/pipeline.py`, `tests/test_pipeline.py`.

**Interfaces — Produces:**
- `check(records: list[Record], prev_count: int) -> str | None` — error text or `None`: `"no records"`; `"count dropped from {p} to {n}"` when `n < p / 2`; `"record without date: {title}"`.
- `@dataclass class Result: snapshot: str | None; parsed: list[Record] | None; extra: list[Record]; status: dict` (`snapshot=None` → keep old file; `parsed=None` → do not merge).
- `process(src: Source, old: str | None, prev: dict | None, fetch: Callable[[Source], str], today: str) -> Result`.

State machine (`base` = `"ok"` if `src.parser` else `"diff"`; broken = `{"parser_broken","fetch_broken"}`):
1. `fetch` raises `FetchError`, or junk by length (< 500, or < 50% of `len(old)`) → state `fetch_broken`, snapshot kept.
2. text == old → state = `prev.state` if it is `parser_broken`, else `base`; nothing else.
3. Changed, diff source → snapshot = text; `extra = [diff_record(...)]` if not None; state `diff`.
4. Changed, parser source → `records = src.parser(text, src.link)` (any exception → error text); `err = check(records, prev.count or 0)`; ok → `parsed = records`, state `ok`, `count = len`; error → `parsed=None`, `extra = [diff_record(...)]`, state `parser_broken`, `count` kept. Snapshot = text in both cases.
5. If new state ∈ broken and prev state ∉ broken → append health record: `title = f"Парсер источника {src.name} сломан"` (parser) or `f"Источник {src.name} не отдаёт данные"` (fetch), `text = error`, `kind="health"`.
6. `since` changes only when state changes; `changed = today` when snapshot changes.

- [ ] **Step 1: Tests** (fake `fetch`, tiny fake parser):
  - `test_fetch_error_keeps_snapshot_and_emits_health`.
  - `test_shrunk_page_is_fetch_broken`: old 2000 chars, new 900 → `fetch_broken`, `snapshot is None`.
  - `test_unchanged_skips`: no extra, state `base`, `snapshot is None`.
  - `test_recovery_from_fetch_broken_same_text`: prev `fetch_broken`, text == old → state `base`.
  - `test_parser_zero_records_breaks`: prev count 10, parser `[]` → `parser_broken`, `parsed is None`, extra has raw + health.
  - `test_parser_drop_half_breaks`: prev 10 → 4 records.
  - `test_parser_exception_breaks`.
  - `test_health_only_on_transition`: prev `parser_broken`, still failing → no health record.
  - `test_first_run_diff_source`: `old=None` → snapshot set, no extra.
- [ ] **Step 2–4:** fail → implement → `uv run pytest tests/test_pipeline.py -q` passes.
- [ ] **Step 5: Commit.**

### Task 6: Feeds

**Files:** Create `depfeed/feeds.py`, `tests/test_feeds.py`.

**Interfaces — Produces:** `in_window(records, today) -> list[Record]` (feed_date ≥ today − 183 d, sorted desc); `rss(records, today, site_url, names: dict[str, str]) -> str`; `json_feed(records, today, site_url, names) -> str`.

RSS 2.0: channel title `AI model deprecations`, link `site_url`, description one line. Item: title `[{name}] {title}`, link `url`, `guid isPermaLink="false"` = id, `pubDate` = RFC 822 of feed_date (`email.utils.format_datetime`), description = `Affected: …\nShutdown: …\nReplacement: …` for parsed, `text` for raw/health. JSON Feed 1.1: `version "https://jsonfeed.org/version/1.1"`, `feed_url f"{site_url}/feed.json"`, items `id, url, title, content_text, date_published, date_modified (if updated), tags [source, kind]`.

- [ ] **Step 1: Tests**
  - `test_window`: records 100 d and 200 d old → only first.
  - `test_window_uses_announced`: parsed record announced 2023, first_seen today → excluded.
  - `test_rss_parses`: `ElementTree.fromstring(rss(...))` has N `item`, guid = id, `isPermaLink="false"`.
  - `test_json_feed_valid`: `json.loads`, `version`, `date_modified` present only for updated record.
- [ ] **Step 2–4:** fail → implement → `uv run pytest tests/test_feeds.py -q` passes.
- [ ] **Step 5: Commit.**

### Task 7: CLI orchestration

**Files:** Create `depfeed/__main__.py`, `tests/test_main.py`.

**Interfaces — Produces:** `main(argv: list[str] | None = None, fetch: Callable[[Source], str] = fetch_source, sources: list[Source] = SOURCES) -> int`. Args: `--data PATH` (default `data`), `--site PATH` (default `site`), `--today YYYY-MM-DD` (default UTC today). `site_url = os.environ.get("SITE_URL", "http://localhost")`.

Flow: load status + records → per source `process` (old = `snapshots/<id>.md` if exists) → write snapshot when `result.snapshot` → `records = merge(records, result.parsed or [], today)` + `result.extra` (through `merge` too) → `prune` → if `today` is Monday set `status["heartbeat"] = today` → save `deprecations.json`, `status.json` (stable JSON) → write site files (`feed.xml`, `feed.json`, copies of `deprecations.json`, `status.json`) → print one line per source `id state count error` → return 0.

- [ ] **Step 1: Tests** (tmp_path, fake fetch returning fixture for openai and `"line\n"*600`-style text for others):
  - `test_e2e_first_run`: site has 4 files; feed.json parses; openai status `ok`; diff sources `diff` and no raw records; no openai item in `feed.json` has `date_published` on `--today` (no history flood).
  - `test_e2e_second_run_no_change_no_file_change`: run twice with same input and a non-Monday `--today` → `data/` bytes identical.
  - `test_e2e_parser_break_keeps_records`: run 1 with fixture, run 2 with openai text = fixture with all `|` removed → archive still has all parsed records, one raw + one health record, status `parser_broken`; run 3 same input → no second health record.
  - `test_heartbeat_monday`.
- [ ] **Step 2–4:** fail → implement → `uv run pytest -q` (full suite) passes.
- [ ] **Step 5: Local live run** — `uv run python -m depfeed --data /tmp/depfeed-live/data --site /tmp/depfeed-live/site` (fresh dirs) → 9 lines, openai `ok` with count ≥ the Task 4 floor, others `diff`. Paste output.
- [ ] **Step 6: Commit.**

### Task 8: Workflows and first live run

**Files:** Create `.github/workflows/update.yml`, `.github/workflows/squash.yml`.

`update.yml`: `on: schedule: [{cron: "17 6 * * *"}], workflow_dispatch`; `concurrency: data-branch`; permissions per Global Constraints. Job `update` (ubuntu-latest):
1. `actions/checkout@v4`; `actions/checkout@v4` with `ref: data, path: data`.
2. `astral-sh/setup-uv@v6`; `uv sync --locked --python 3.12`.
3. `SITE_URL="https://${{ github.repository_owner }}.github.io/${GITHUB_REPOSITORY#*/}" uv run python -m depfeed --data data --site site` (derive the repo name in shell: `github.event.repository.name` is not reliable on `schedule` events).
4. Commit data: in `data/`, `git add -A`; if `git diff --cached --quiet` fails → commit as `github-actions[bot]` (`41898282+github-actions[bot]@users.noreply.github.com`), message `data: <UTC date>`, push.
5. Issues: for each `id` in `jq -r '.sources|to_entries[]|select(.value.state|endswith("_broken"))|.key' data/status.json`: if `gh issue list --state open --search "\"[broken] $id\" in:title" --json number --jq length` is `0` → `gh issue create --title "[broken] $id" --body "<state>: <error>\n\n$RUN_URL\n\n<reset instructions from Global Constraints>"`. `GH_TOKEN: ${{ github.token }}`.
6. Keepalive (Mondays only, `if: date -u +%u == 1` in shell): `gh api -X PUT repos/$GITHUB_REPOSITORY/actions/workflows/update.yml/enable`. Reason: it is not verified that commits to the non-default `data` branch count as repo activity for the 60-day rule; this call is the second guard.
7. `actions/upload-pages-artifact@v3` with `path: site`.
Job `deploy` (`needs: update`, `environment: github-pages`): `actions/deploy-pages@v4`.

`squash.yml`: `on: schedule: [{cron: "0 3 1 * *"}], workflow_dispatch`; same concurrency; `contents: write`. Steps: checkout `ref: data`; `git checkout --orphan squashed && git add -A && git commit -m "data: squash <UTC date>" && git push -f origin squashed:data` (as github-actions[bot]).

- [ ] **Step 1: Lint** — `uvx actionlint` (or `actionlint` via brew) → no output.
- [ ] **Step 2: Commit + push main.**
- [ ] **Step 3: First run** — `gh workflow run update.yml && gh run watch --exit-status` → success. Paste the 9 status lines from the log.
- [ ] **Step 4: Verify live feed** — `curl -sf https://parabolabam.github.io/ai-deprecations-feed/feed.xml | head -c 600` shows `<rss`; `curl -sf .../status.json | jq '.sources|map_values(.state)'` shows openai `ok`, others `diff`. `git log origin/data --oneline -1` shows the data commit.
- [ ] **Step 5: Second run** — `gh workflow run update.yml`, wait → `git fetch && git log origin/data --oneline -1` unchanged (no-change run makes no commit; unless Monday).
- [ ] **Step 6: Squash** — `gh workflow run squash.yml`, wait → `git fetch && git rev-list --count origin/data` = `1`.

## Verification (end-to-end)

- `uv run pytest -q` → all pass; `LIVE=1 uv run pytest tests/test_fetch.py -q` → pass.
- Feed URL opens in an RSS reader; OpenAI items have announced dates in the last 6 months only.
- The parser-break path is tested only locally (Task 7 `test_e2e_parser_break_keeps_records`). It is not tested in prod, because a deliberate break would write a real health record and issue.
- Two consecutive runs with no page change → no new `data` commit.
- `status.json` on Pages shows one state per source.

## Out of scope (Stage 2+)

Parsers for the 8 diff sources (owner sets the order), LLM extractor, Docker, alerts, model filters, website.
