from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING

from depfeed.parsers import anthropic, azure, bedrock, cohere, gemini, groq, openai, vertex

if TYPE_CHECKING:
    from depfeed.records import Record


@dataclass(frozen=True)
class Source:
    id: str
    name: str
    urls: tuple[str, ...]
    link: str
    parser: Callable[[str, str], list[Record]] | None = None
    keep: str | None = None
    ignore: tuple[str, ...] = ()


SOURCES: list[Source] = [
    Source("openai", "OpenAI",
           ("https://developers.openai.com/api/docs/deprecations.md",),
           "https://developers.openai.com/api/docs/deprecations", parser=openai.parse),
    Source("anthropic", "Anthropic",
           ("https://platform.claude.com/docs/en/about-claude/model-deprecations.md",),
           "https://platform.claude.com/docs/en/about-claude/model-deprecations", parser=anthropic.parse),
    Source("gemini", "Google AI (Gemini)",
           ("https://aistudio.google.com/docs/deprecations.md",),
           "https://aistudio.google.com/docs/deprecations", parser=gemini.parse),
    Source("vertex", "Google Vertex AI",
           ("https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/model-versions.md.txt",
            "https://docs.cloud.google.com/vertex-ai/generative-ai/docs/deprecations.md.txt"),
           "https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/model-versions",
           parser=vertex.parse),
    Source("vertex-partners", "Google Vertex AI (partner models)",
           ("https://docs.cloud.google.com/vertex-ai/generative-ai/docs/deprecations/partner-models.md.txt",),
           "https://docs.cloud.google.com/vertex-ai/generative-ai/docs/deprecations/partner-models"),
    Source("bedrock", "AWS Bedrock",
           ("https://docs.aws.amazon.com/bedrock/latest/userguide/model-lifecycle-legacy.md",
            "https://docs.aws.amazon.com/bedrock/latest/userguide/model-lifecycle.md"),
           "https://docs.aws.amazon.com/bedrock/latest/userguide/model-lifecycle-legacy.html",
           parser=bedrock.parse),
    Source("cohere", "Cohere",
           ("https://docs.cohere.com/docs/deprecations.md",),
           "https://docs.cohere.com/docs/deprecations",
           parser=cohere.parse),
    Source("groq", "Groq",
           ("https://console.groq.com/docs/deprecations.md",),
           "https://console.groq.com/docs/deprecations", parser=groq.parse),
    Source("xai", "xAI",
           ("https://docs.x.ai/developers/release-notes",),
           "https://docs.x.ai/developers/release-notes",
           keep=r"(?i)end of life|deprecat|retire|sunset|shut ?down"),
    Source("azure", "Azure AI Foundry",
           ("https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/model-retirement-schedule?accept=text/markdown",),
           "https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/model-retirement-schedule", parser=azure.parse),
]
