# ai-deprecations-feed

Daily RSS and JSON feed of model and API deprecation announcements from OpenAI, Anthropic, Google AI (Gemini), Google Vertex AI, AWS Bedrock, Cohere, Groq, xAI and Azure AI Foundry. GitHub Actions fetches each provider's page once a day; OpenAI is parsed into structured records, the other sources publish the added lines of each page change. Broken sources open an issue and never delete stored records.

Feeds (GitHub Pages):

- `https://<user>.github.io/ai-deprecations-feed/feed.xml` — RSS, last 6 months
- `https://<user>.github.io/ai-deprecations-feed/feed.json` — JSON Feed 1.1, last 6 months
- `https://<user>.github.io/ai-deprecations-feed/deprecations.json` — full archive
- `https://<user>.github.io/ai-deprecations-feed/status.json` — state of each source

Code lives on `main`, state (snapshots, archive, status) on branch `data`.

## Reset a broken source

If a source changed legitimately (for example, a page was split) and stays `fetch_broken` or `parser_broken`, delete `snapshots/<id>.md` and the `sources.<id>` entry in `status.json` on branch `data`. The next run treats the source as new.

See `docs/design.md` and `docs/plan.md`.
