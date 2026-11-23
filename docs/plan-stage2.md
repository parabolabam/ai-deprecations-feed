# AI Deprecations Feed — Stage 2 Implementation Plan (parsers)

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development. Steps use `- [ ]`.
> **Owner rules (from ~/.claude/CLAUDE.md):** implementing agents run with `model: "sonnet"`, type `general-purpose`, invoke `ponytail` before writing code, and paste each verify command with its real output. The main session re-runs every verify command and reviews `git diff --staged` before each commit.

**Goal:** Move Anthropic, Groq, Azure, Vertex, Gemini, Bedrock and Cohere from raw diffs to structured records, one source at a time, without flooding subscribers.

**Architecture:** One generic table parser (`depfeed/parsers/tables.py`) driven by a per-source list of `TableSpec`s covers every pipe-table page (OpenAI, Anthropic, Groq, Azure, Vertex) and Gemini after a Markdoc→pipe pre-pass. Bedrock (bullet records) and Cohere (dated prose sections) get small own parsers. A *baseline* flag keeps the first parse of a source out of the feed.

**Spec:** `docs/design.md` (stage 2: «Парсеры по одному»). Stage 1 plan: `docs/plan.md`.

## Global Constraints

- Order (owner-approved): baseline → generic parser (OpenAI migrated) → Anthropic → Groq → Azure → Vertex → Gemini → Bedrock → Cohere. xAI stays on diff.
- One source per task; each task is pushed and run live before the next starts, so one broken parser never hides another.
- OpenAI record ids must not change (Slack subscribers would get reposts). Guard: Task 2 freezes today's id set as a fixture.
- Parser input is the normalized snapshot text (`normalize()` output). Fixtures are normalized live fetches taken in the task, committed under `tests/fixtures/<id>.md`.
- Stdlib only. No HTML parsing.
- A parser raises `ValueError` on rows it cannot read when the spec says the row must be dated; `process()` already turns any exception into `parser_broken`.
- Whenever a source's URL list changes, delete its `snapshots/<id>.md` on branch `data` in the same push (worktree: `git worktree add /tmp/df-data origin/data`, `git rm`, commit, `git push origin HEAD:data`; do not run `ls` there — the shell alias hangs). `old = None` skips the shrink check and makes the next parse a baseline.

## Decisions

**Baseline.** The first successful parse of a source (previous `count == 0`, i.e. first run or the switch from diff) marks its new records `baseline=True`. Feeds drop baseline records that have no `announced` date; baseline records with `announced` inside the 6-month window still appear. `merge` keeps `baseline` from the archived record and does not compare it (no spurious `updated`). Later new rows of the same source are not baseline and post normally.

**Record additions.** `baseline: bool = False`. Parsed descriptions show `Details: {text}` (before `Docs:`) when `text` is set.

**`check()` change.** The "record without date" rule moves into the parsers (per spec `require_date`). `check()` keeps "no records" and the >50% drop rule.

**`TableSpec`** (frozen dataclass in `depfeed/parsers/tables.py`):

| field | meaning |
|---|---|
| `match: tuple[str, ...]` | lowercase keywords that must all occur in the header cells to take a table |
| `columns: dict[str, str]` | header keyword → field: `affected`, `shutdown`, `announced`, `replacement`, `status`, `version`, `text` |
| `affected: str = "ids"` | how `affected` is built from its cell: `"ids"` = backticked IDs, else comma-split (Stage 1 model tables); `"cell"` = `[_plain(cell)]` (Stage 1 feature table); `"model_version"` = `[f"{model} {version}"]` (Azure) |
| `prefix: str` | title prefix, e.g. `Model retirement` |
| `heading_date: str \| None` | `"announced"` or `"shutdown"`: take the date from the nearest `###` heading |
| `body_announced: str \| None` | regex with one group; first match in the section body gives `announced` (Groq) |
| `skip_undated: bool = False` | rows with no `shutdown` date are skipped (not a deprecation yet) |
| `require_date: bool = True` | a kept row without `announced` and `shutdown` raises `ValueError` |
| `id_fields: tuple[str, ...]` | record fields (plus `section`) that form the id after `source` |

`parse_tables(text, link, source, specs) -> list[Record]`: tracks the current `##`/`###` heading (strip `[text](#anchor)` wrappers and `{% … %}` tags), reads pipe tables with `_plain` header cells (bold headers), maps columns, builds titles `"{prefix} {shutdown or raw}: {section + ': ' if section-in-title}{affected}"`, keeps `links` and the existing duplicate-id suffix. `markdoc_tables(text) -> str` converts `{% table %}` blocks (`* cell` lines, `---` row breaks) to pipe tables.

**Per-source specs** (headers verified on 2026-11-22 snapshots):

| Source | Table match → mapping | Dates | id fields | Notes |
|---|---|---|---|---|
| openai | as Stage 1 (three tables, prefixes Model / Feature/endpoint / Shutdown) | notice column → announced | as Stage 1 | ids frozen |
| anthropic | `Retirement date \| Deprecated model \| Recommended replacement` under `### YYYY-MM-DD: …` | heading → announced | announced, affected[0] | skip `## Model status`; `## API parameter deprecations` (`Parameter \| Status \| Behavior \| Recommended replacement`) with `require_date=False`, prefix `API parameter deprecation`, behavior → text |
| groq | `Deprecated Model \| Shutdown Date \| Recommended Replacement Model ID` | body regex `On (.+?), we announced` → announced; `MM/DD/YY` shutdown | announced, affected[0] | headings are `### [Month D, YYYY: …](#…)` |
| azure | `Model \| Version \| Lifecycle \| Retirement date \| Replacement`; fine-tuned `Training retirement date \| Deployment retirement date` (deployment → shutdown) | none (baseline matters) | section, affected, status | `affected="model_version"`; lifecycle in id: GA→Deprecated makes a new item; vendor `###` in title; `skip_undated` |
| vertex | `Model ID \| Release date \| Retirement date \| Replacement model ID / Recommended upgrade`; `Feature \| Deprecated date \| Shutdown date \| Details` | feature: deprecated date → announced | affected | `skip_undated` ("No retirement date announced"); details → text. Split source: `vertex` = model-versions + deprecations (parser), new `vertex-partners` = partner-models URL (diff) |
| gemini | after `markdoc_tables`: `Model \| Release date \| Shutdown date \| Recommended replacement` | none | affected | `skip_undated` ("No shutdown date announced") |
| bedrock | own parser: bullet groups `- **Provider**`, `- **Model name:**`, `- **Model ID:**`, `- **Regions:** … / **Legacy date:** … / **EOL date:** …` (one or more region lines) | earliest EOL → shutdown; announced = None (owner decision 2026-11-23, option B: no switch-day posts); Legacy/EOL/extended-access dates per region → text | model id (duplicate entry: + status) | status `Legacy` under "Models with a scheduled EOL date", `EOL reached` under "Models that have reached EOL"; per-region lines → text |
| cohere | own parser: each `### YYYY-MM-DD: title` under `## Deprecation History` is one record | heading → shutdown | shutdown, title | affected = backticked IDs in the section; section body (≤1500 chars) → text |

## Review Focus

1. **Switch-day flood**: a source moving from diff to parser posts only records with `announced` in the window (Task 1 test + live check per task).
2. **OpenAI id drift** after the refactor → frozen id-set test (Task 2).
3. **Azure lifecycle transition** GA→Deprecated produces exactly one new item; a retirement-date change produces an update, not an item (Task 5).
4. **Undated "not yet" rows** (Vertex, Gemini, Azure) are skipped, and a later date addition produces one new item (Tasks 5–7).
5. **Multi-region Bedrock rows** collapse into one record per model id with the earliest EOL date (Task 8).

---

### Task 1: Baseline

**Files:** Modify `depfeed/records.py`, `depfeed/pipeline.py`, `depfeed/__main__.py`, `depfeed/feeds.py`; tests in `tests/test_records.py`, `tests/test_pipeline.py`, `tests/test_feeds.py`, `tests/test_main.py`.

**Interfaces:** `Record.baseline: bool = False`; `Result.baseline: bool` (True when the source has a parser, the parse succeeded and prev `count` was 0); `__main__` sets `baseline=True` on `res.parsed` records before `merge` when `res.baseline`; `merge` excludes `baseline` from the comparison and keeps the archived value; `in_window` drops `r.baseline and not r.announced`.

- [ ] Tests: `test_merge_keeps_baseline_no_update`; `test_pipeline_first_parse_is_baseline` (prev None and prev `diff` → `baseline` True; prev `ok` count 156 → False); `test_window_drops_undated_baseline` (baseline without announced dropped, baseline with announced in window kept); `test_e2e_switch_from_diff_no_flood` (run 1 with a source without parser, run 2 with a parser returning 3 undated rows and 1 row announced today−10 → feed has exactly that 1 row from the source).
- [ ] Implement; `uv run pytest -q` passes.
- [ ] Commit, push, run `update.yml`; `status.json` unchanged (openai ok 156).

### Task 2: Generic table parser, OpenAI migrated

**Files:** Create `depfeed/parsers/tables.py`, `tests/test_tables.py`, `tests/fixtures/openai_ids.json`; rewrite `depfeed/parsers/openai.py` as `SPECS` + `parse = partial(parse_tables, source="openai", specs=SPECS)` (keep the name `parse`); modify `depfeed/pipeline.py` (`check` loses the date rule) and `depfeed/feeds.py` (`Details:` line).

- [ ] **Before any code change:** write `tests/fixtures/openai_ids.json` = sorted ids from the current `parse(fixture, "https://developers.openai.com/api/docs/deprecations")`.
- [ ] Tests: `test_openai_ids_frozen` (new parse gives exactly that id set and the same titles); all existing `tests/test_openai.py` tests pass unchanged; the only existing test that changes is `tests/test_pipeline.py::test_check_rules` (drop its "record without date" case); `test_tables.py`: bold headers, heading `[text](#a)` unwrapping, `{% id %}` stripping, `heading_date`, `body_announced`, `skip_undated`, `require_date` raising `ValueError`, `markdoc_tables` on a 2-row sample.
- [ ] Implement; `uv run pytest -q` passes.
- [ ] Commit, push, run; live `feed.json` item ids identical to before the run (compare `jq '[.items[].id]'` before/after).

### Tasks 3–7: Anthropic, Groq, Azure, Vertex, Gemini (one task each, same shape)

**Files per task:** Create `depfeed/parsers/<id>.py` (`SPECS` + `parse`), `tests/fixtures/<id>.md`, `tests/test_<id>.py`; modify `depfeed/sources.py` (`parser=`). Task 6 also adds the `vertex-partners` source, removes that URL from `vertex`, and deletes `snapshots/vertex.md` on `data` in the same push (Global Constraints). Task 7 applies `markdoc_tables` before `parse_tables`.

- [ ] Fixture: `uv run python -c "from depfeed.fetch import fetch_source; from depfeed.sources import SOURCES; s={x.id:x for x in SOURCES}['<id>']; open('tests/fixtures/<id>.md','w').write(fetch_source(s)+'\n')"`.
- [ ] Tests (values read from the fixture and stated in the report): `test_count` (≥ 80% floor), `test_known_row` with the rows below, `test_ids_unique`, `test_all_dated_or_skipped`, `test_source_wired`.
  - anthropic: `claude-sonnet-4-5-20250929` → announced `2026-09-30`, shutdown `2026-11-30`, replacement `claude-sonnet-5-5`; one record with prefix `API parameter deprecation` and affected containing `temperature`.
  - groq: `groq/compound` → announced `2026-08-24`, shutdown `2026-09-21`, replacement None.
  - azure: `codex-mini` `2025-05-16` → status `Deprecated`, shutdown `2026-11-17`; `test_lifecycle_change_new_id` (same row with `GA` → different id); fine-tuned `gpt-4.1` → shutdown `2027-10-14`.
  - vertex: `veo-3.0-generate-001` → shutdown `2026-06-30`, replacement `veo-3.1-generate-001`; `gemini-4-hydrogen` skipped; feature row "Generative AI module in the Vertex AI SDK" → announced `2025-06-24`, shutdown `2026-06-24`, text set.
  - gemini: `gemini-4-neon` skipped (no shutdown date); a deprecated-model row with a real shutdown date read from the fixture.
- [ ] Implement; `uv run pytest -q` passes; `LIVE=1 uv run pytest -q -k live` passes.
- [ ] Commit, push, run `update.yml`. Verify: `status.json` shows `<id> ok <count>`; feed items from `<id>` are exactly the records with `announced` in the window (paste their titles — this is what Slack will post).

### Task 8: Bedrock parser

**Files:** Create `depfeed/parsers/bedrock.py`, `tests/fixtures/bedrock.md`, `tests/test_bedrock.py`; modify `depfeed/sources.py`.

- [ ] Tests: `anthropic.claude-3-haiku-20240307-v1:0` → one record, shutdown = earliest EOL across its region lines (`2026-11-13`), announced is None, text contains the Legacy date `2026-10-10`, status `Legacy`, text lists regions; `ai21.jamba-1-5-large-v1:0` → shutdown `2026-11-26`; records under "Models that have reached EOL" have status `EOL reached`; count floor; ids unique.
- [ ] Implement, verify, commit, push, run, check live as in Tasks 3–7.

### Task 9: Cohere parser

**Files:** Create `depfeed/parsers/cohere.py`, `tests/fixtures/cohere.md`, `tests/test_cohere.py`; modify `depfeed/sources.py`.

- [ ] Tests: section `2026-04-04: Embed v2.0, Aya Expanse 8B` → shutdown `2026-04-04`, affected ⊇ {`embed-english-v2.0`, `c4ai-aya-expanse-8b`}, text starts with "Effective April 4th, 2026"; 5 records (one per `###` under Deprecation History); sections after `# Best Practices` ignored.
- [ ] Implement, verify, commit, push, run, check live.

### Task 10: Docs

- [ ] README: sources table (parser / diff), "Known limits" updated: xAI and vertex-partners stay on diff; Azure GA rows are scheduled retirements, and after a GA→Deprecated change the old GA record stays in the archive (merge never retires records); Bedrock entries on the new `model-lifecycle.md` page sit under no status heading, so their `status` is None.
- [ ] Commit, push.

## Verification (end-to-end)

- After each source task: `status.json` `ok` with the expected count; no `parser_broken`; feed delta = only records announced within 6 months (Slack posts exactly those).
- After Task 10: `uv run pytest -q` and `LIVE=1 uv run pytest -q -k live` pass; two consecutive runs make no `data` commit.
