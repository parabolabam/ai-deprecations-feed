# ai-deprecations-feed

Daily RSS and JSON feed of model and API deprecation announcements from OpenAI, Anthropic, Google AI (Gemini), Google Vertex AI, AWS Bedrock, Cohere, Groq, xAI and Azure AI Foundry. GitHub Actions fetches each provider's page once a day; OpenAI is parsed into structured records, the other sources publish the added lines of each page change. Broken sources open an issue and never delete stored records.

Feeds (GitHub Pages):

- `https://parabolabam.github.io/ai-deprecations-feed/feed.xml` — RSS, last 6 months
- `https://parabolabam.github.io/ai-deprecations-feed/feed.json` — JSON Feed 1.1, last 6 months
- `https://parabolabam.github.io/ai-deprecations-feed/deprecations.json` — full archive
- `https://parabolabam.github.io/ai-deprecations-feed/status.json` — state of each source

Code lives on `main`, state (snapshots, archive, status) on branch `data`.

## Reset a broken source

If a source changed legitimately (for example, a page was split) and stays `fetch_broken` or `parser_broken`, delete `snapshots/<id>.md` and the `sources.<id>` entry in `status.json` on branch `data`. The next run treats the source as new.

See `docs/design.md` and `docs/plan.md`.

## Known limits (Stage 1)

- Only OpenAI is parsed. The other 8 sources publish the added lines of each page change (xAI: only lines about end of life, deprecation or retirement).
- OpenAI feature and endpoint rows take `affected` from backticked text, so it can hold values like `service_tier: fast` instead of model IDs.
- A page that shrinks by more than half stays `fetch_broken` until it is reset (see above). This is on purpose: a silent loss of content must be visible.
- RSS items keep their `pubDate` when a record is edited; the JSON feed shows the edit as `date_modified`.
