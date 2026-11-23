# ai-deprecations-feed

Daily RSS and JSON feed of model and API deprecation announcements from OpenAI, Anthropic, Google AI (Gemini), Google Vertex AI, AWS Bedrock, Cohere, Groq, xAI and Azure AI Foundry. GitHub Actions fetches each provider's page once a day. Eight sources are parsed into structured records; xAI and Google Vertex AI partner models publish the added lines of each page change. Broken sources open an issue and never delete stored records.

Feeds (GitHub Pages):

- `https://parabolabam.github.io/ai-deprecations-feed/feed.xml` — RSS, last 6 months
- `https://parabolabam.github.io/ai-deprecations-feed/feed.json` — JSON Feed 1.1, last 6 months
- `https://parabolabam.github.io/ai-deprecations-feed/deprecations.json` — full archive
- `https://parabolabam.github.io/ai-deprecations-feed/status.json` — state of each source

Code lives on `main`, state (snapshots, archive, status) on branch `data`.

## Sources

| id | Provider | Mode |
|---|---|---|
| openai | OpenAI | parser (tables) |
| anthropic | Anthropic | parser (tables) |
| groq | Groq | parser (tables) |
| azure | Azure AI Foundry | parser (tables) |
| vertex | Google Vertex AI (model versions, feature deprecations) | parser (tables) |
| vertex-partners | Google Vertex AI (partner models) | diff |
| gemini | Google AI (Gemini) | parser (Markdoc tables) |
| bedrock | AWS Bedrock | parser (bullet groups) |
| cohere | Cohere | parser (dated sections) |
| xai | xAI | diff (only lines about end of life, deprecation or retirement) |

The first successful parse of a source is a baseline: its records go to the archive, but only those with an announcement date in the last 6 months go to the feed.

## Reset a broken source

If a source changed legitimately (for example, a page was split) and stays `fetch_broken` or `parser_broken`, delete `snapshots/<id>.md` and the `sources.<id>` entry in `status.json` on branch `data`. The next run treats the source as new.

See `docs/design.md`, `docs/plan.md` and `docs/plan-stage2.md`.

## Known limits

- xAI and Vertex AI partner models stay on diff: their pages have no stable table or list format.
- Azure GA rows are scheduled retirements. The lifecycle is part of the record id, so a GA→Deprecated change makes a new item, and the old GA record stays in the archive (merge never retires records).
- Bedrock records have no announcement date (`announced` is empty); the Legacy date per region is in the record text. A model that enters Legacy posts on the day the feed first sees it. Entries on the newer `model-lifecycle.md` page sit under no status heading, so their `status` is empty.
- Cohere `affected` holds every backticked token of a section, so it also lists replacement models and endpoint names. Cohere takes the shutdown date from the section heading; for "2024-12-02: Rerank v2.0" that is the announcement date (the real shutdown, 2025-04-30, is in the section text).
- Groq takes the announcement date from "On <date>, we announced" or "On <date>, we emailed" in the section text.
- OpenAI feature and endpoint rows take `affected` from backticked text, so it can hold values like `service_tier: fast` instead of model IDs.
- A page that shrinks by more than half stays `fetch_broken` until it is reset (see above). This is on purpose: a silent loss of content must be visible.
- RSS items keep their `pubDate` when a record is edited; the JSON feed shows the edit as `date_modified`.
