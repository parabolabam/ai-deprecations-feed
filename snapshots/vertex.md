This document defines key terms related to the lifecycle stages and important dates for generally available Gemini and embedding models that are available on Google Cloud Gemini Enterprise Agent Platform. It also gives you the recommended upgrades for the models and points you to available migration paths.
<br />
## Latest available models
The following tables list the generally available (GA) models and their
retirement dates. While retirement timelines may be extended, they won't be
moved to an earlier date than what is listed.
> [!NOTE]
> **Note:** Preview models aren't included in these tables. Each Preview model's documentation page lists its version IDs and release dates. For more information about available Preview models, see the Preview sections of the [Google models](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/google-models.md.txt) page.
### Models available for at least 12 months after release
The following table lists the models that will be available for at least 12
months after initial release:
### Gemini models
| Model ID | Release date | Retirement date | Replacement model ID |
|---|---|---|---|
| [`gemini-4-argon`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/4-argon.md.txt) | October 13, 2026 | October 13, 2027 or later | |
| [`gemini-3.8-live`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-8-live.md.txt) | September 24, 2026 | September 25, 2027 or later | |
| [`gemini-3.8-flash`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-8-flash.md.txt) | September 2, 2026 | September 2, 2027 or later | |
| [`gemini-3.5-flash-lite`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-5-flash-lite.md.txt) | July 21, 2026 | July 21, 2027 or later | |
| [`gemini-3.5-flash`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-5-flash.md.txt) | May 19, 2026 | May 19, 2027 or later | |
| [`gemini-3.1-flash-lite`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-1-flash-lite.md.txt) | May 7, 2026 | May 7, 2027 or later | |
| [`gemini-2.5-pro`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/2-5-pro.md.txt) | June 17, 2025 | October 20, 2026 | [`gemini-3.8-flash`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-8-flash.md.txt) or [`gemini-3.5-flash`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-5-flash.md.txt) |
| [`gemini-2.5-flash`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/2-5-flash.md.txt) | June 17, 2025 | October 20, 2026 | [`gemini-3.8-flash`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-8-flash.md.txt) or [`gemini-3.5-flash-lite`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-5-flash-lite.md.txt) |
| [`gemini-2.5-flash-lite`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/2-5-flash-lite.md.txt) | July 22, 2025 | October 20, 2026 | [`gemini-3.8-flash`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-8-flash.md.txt) or [`gemini-3.5-flash-lite`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-5-flash-lite.md.txt) or [Gemma 4](https://console.cloud.google.com/agent-platform/publishers/google/model-garden/gemma4) |
| [`gemini-live-2.5-flash-native-audio`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/2-5-flash-live-api.md.txt) | December 12, 2025 | December 13, 2026 | [`gemini-3.8-live`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-8-live.md.txt) |
<br />
### Gemini image models
| Model ID | Release date | Retirement date | Replacement model ID |
|---|---|---|---|
| [`gemini-3.1-flash-lite-image`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-1-flash-lite-image.md.txt) | June 23, 2026 | June 28, 2027 or later | |
| [`gemini-3-pro-image`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-pro-image.md.txt) | May 28, 2026 | May 28, 2027 or later | |
| [`gemini-3.1-flash-image`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-1-flash-image.md.txt) | May 28, 2026 | May 28, 2027 or later | |
| [`gemini-2.5-flash-image`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/2-5-flash-image.md.txt) | October 2, 2025 | March 15, 2027 | [`gemini-3.1-flash-lite-image`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-1-flash-lite-image.md.txt) |
<br />
### Gemini Omni models
| Model ID | Release date | Retirement date | Replacement model ID |
|---|---|---|---|
| [`gemini-omni-1.2-flash`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/omni-1-2-flash.md.txt) | November 5, 2026 | November 5, 2027 or later | |
<br />
### Veo models
| Model ID | Release date | Retirement date | Replacement model ID |
|---|---|---|---|
| [`veo-3.1-generate-001`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/veo/3-1-generate.md.txt#3.1-generate-001) | November 17, 2025 | May 4, 2027 or later | [`gemini-omni-1.2-flash`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/omni-1-2-flash.md.txt) |
| [`veo-3.1-fast-generate-001`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/veo/3-1-generate.md.txt#3.1-fast-generate-001) | November 17, 2025 | May 4, 2027 or later | [`gemini-omni-1.2-flash`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/omni-1-2-flash.md.txt) |
<br />
### Embeddings models
| Model ID | Release date | Retirement date | Replacement model ID |
|---|---|---|---|
| [`gemini-embedding-2`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/embedding-2.md.txt) | April 22, 2026 | | |
| [`gemini-embedding-001`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/embeddings/get-text-embeddings.md.txt) | May 20, 2025 | No sooner than May 20, 2028 | |
| [`text-embedding-005`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/embeddings/get-text-embeddings.md.txt) | November 18, 2024 | April 1, 2027 | |
| [`text-embedding-004`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/embeddings/get-text-embeddings.md.txt) | May 14, 2024 | April 1, 2027 | |
| [`text-multilingual-embedding-002`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/embeddings/get-text-embeddings.md.txt) | May 14, 2024 | April 1, 2027 | |
| [`multimodalembedding@001`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/embeddings/get-multimodal-embeddings.md.txt) | February 12, 2024 | April 1, 2027 | |
<br />
### Models available for shorter availability periods
Short-term availability models remain active until a replacement model is
released and a retirement date is announced. When we schedule a model for
retirement, we post a fixed date in the following table that gives you at least
45 days to migrate. Even after a replacement launches, a model remains active
until we announce its retirement date.
The following table lists models available for shorter terms:
| Model ID | Release date | Retirement date | Replacement model ID |
|---|---|---|---|
| [`gemini-4-hydrogen`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/4-hydrogen.md.txt) | November 12, 2026 | No retirement date announced | |
| [`gemini-4-carbon`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/4-carbon.md.txt) | November 10, 2026 | No retirement date announced | |
| [`gemini-4-carbon-cyber-permissive`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/4-carbon.md.txt#cyber) | November 10, 2026 | No retirement date announced | |
| [`gemini-4-argon-cyber-permissive`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/4-argon.md.txt#cyber) | October 13, 2026 | No retirement date announced | |
| [`gemini-3.8-flash-cyber`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-8-flash-cyber.md.txt) | September 16, 2026 | No retirement date announced | |
| [`gemini-3.7-flash`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-7-flash.md.txt) | August 13, 2026 | January 28, 2027 | [`gemini-3.8-flash`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-8-flash.md.txt) |
| [`gemini-3.6-flash`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-6-flash.md.txt) | July 21, 2026 | November 19, 2026 | [`gemini-3.8-flash`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-8-flash.md.txt) |
| [`gemini-nano-banana-2.1`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/nano-banana-2-1.md.txt) | October 6, 2026 | No retirement date announced | |
<br />
### Retired models
#### The following table lists the retired models (click to expand)
| Model ID | Release date | Retirement date | Recommended upgrade |
|---|---|---|---|
| `veo-3.0-generate-001` | July 29, 2025 | June 30, 2026 | [`veo-3.1-generate-001`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/veo/3-1-generate.md.txt#3.1-generate-001) |
| `veo-3.0-fast-generate-001` | July 29, 2025 | June 30, 2026 | [`veo-3.1-fast-generate-001`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/veo/3-1-generate.md.txt#3.1-fast-generate-001) |
| `veo-2.0-generate-001` | May 27, 2025 | June 30, 2026 | [`veo-3.1-generate-001`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/veo/3-1-generate.md.txt#3.1-generate-001) |
| `imagen-4.0-generate-001` | August 14, 2025 | June 30, 2026 | [`gemini-2.5-flash-image`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/2-5-flash-image.md.txt) |
| `imagen-4.0-ultra-generate-001` | August 14, 2025 | June 30, 2026 | [`gemini-2.5-flash-image`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/2-5-flash-image.md.txt) |
| `imagen-3.0-generate-002` | January 29, 2025 | June 30, 2026 | [`gemini-2.5-flash-image`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/2-5-flash-image.md.txt) |
| `imagen-3.0-generate-001` | December 10, 2024 | June 30, 2026 | [`gemini-2.5-flash-image`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/2-5-flash-image.md.txt) |
| `imagegeneration@006` | March 27, 2024 | June 30, 2026 | [`gemini-2.5-flash-image`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/2-5-flash-image.md.txt) |
| `imagegeneration@005` | November 22, 2023 | June 30, 2026 | [`gemini-2.5-flash-image`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/2-5-flash-image.md.txt) |
| `imagegeneration@004` | | June 30, 2026 | [`gemini-2.5-flash-image`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/2-5-flash-image.md.txt) |
| `imagegeneration@003` | | June 30, 2026 | [`gemini-2.5-flash-image`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/2-5-flash-image.md.txt) |
| `imagegeneration@002` | August 17, 2023 | June 30, 2026 | [`gemini-2.5-flash-image`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/2-5-flash-image.md.txt) |
| `gemini-2.0-flash` | February 5, 2025 | June 1, 2026 | [`gemini-3.5-flash-lite`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-5-flash-lite.md.txt) |
| `gemini-2.0-flash-lite` | February 25, 2025 | June 1, 2026 | [`gemini-3.5-flash-lite`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-5-flash-lite.md.txt) |
| `gemini-1.5-pro-001` | May 24, 2024 | May 24, 2025 | [`gemini-2.5-flash`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/2-5-flash.md.txt) |
| `gemini-1.5-pro-002` | September 24, 2024 | September 24, 2025 | [`gemini-2.5-flash`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/2-5-flash.md.txt) |
| `gemini-1.5-flash-001` | May 24, 2024 | May 24, 2025 | [`gemini-2.5-flash-lite`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/2-5-flash-lite.md.txt) |
| `gemini-1.5-flash-002` | September 24, 2024 | September 24, 2025 | [`gemini-2.5-flash-lite`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/2-5-flash-lite.md.txt) |
| `textembedding-gecko@003\*` | December 12, 2023 | May 24, 2025 | [`gemini-embedding-001`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/embeddings/get-text-embeddings.md.txt) |
| `textembedding-gecko-multilingual@001` | November 2, 2023 | May 24, 2025 | [`gemini-embedding-001`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/embeddings/get-text-embeddings.md.txt) |
| `gemini-1.0-pro-001` | February 15, 2024 | April 21, 2025 | [`gemini-2.5-flash`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/2-5-flash.md.txt) |
| `gemini-1.0-pro-002` | April 9, 2024 | April 21, 2025 | [`gemini-2.5-flash`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/2-5-flash.md.txt) |
| `gemini-1.0-pro-vision-001` | February 15, 2024 | April 21, 2025 | [`gemini-2.5-flash`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/2-5-flash.md.txt) |
| `text-bison` | May 2023 | April 21, 2025 | [`gemini-2.5-flash-lite`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/2-5-flash-lite.md.txt) |
| `chat-bison` | May 2023 | April 21, 2025 | [`gemini-2.5-flash-lite`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/2-5-flash-lite.md.txt) |
| `code-gecko` | May 2023 | April 21, 2025 | [`gemini-2.5-flash-lite`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/2-5-flash-lite.md.txt) |
| `textembedding-gecko@002` | November 2, 2023 | April 21, 2025 | [`gemini-embedding-001`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/embeddings/get-text-embeddings.md.txt) |
| `textembedding-gecko@001` | June 7, 2023 | April 21, 2025 | [`gemini-embedding-001`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/embeddings/get-text-embeddings.md.txt) |
| `imagetext` | June 7, 2023 | September 24, 2025 | [`gemini-2.5-flash-image`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/2-5-flash-image.md.txt) |
## Migrate to a latest available model
To learn how to migrate to a latest stable model, see
[Migrate to the latest Gemini models](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/migrate.md.txt).
This guide gives you a set of migration steps that aims to minimize some
potential risks involved in model migration and helps you use new models in an
optimal way.
However, if you don't have time to follow the guide and just need to quickly
resolve the errors caused by models reaching their retirement dates, do the following:
1. Update your application to point to the recommended upgrades.
2. Test all mission critical features to make sure everything works as expected.
3. Deploy the updates like you normally would.
## What's next
Resource
### [Deployment and endpoint locations](https://docs.cloud.google.com/gemini-enterprise-agent-platform/resources/locations.md.txt)
Learn about deployment and endpoint locations for models in Agent Platform.
The
[Google Cloud Platform Terms of Service (section "Discontinuation of Services")](https://docs.cloud.google.com/terms)
defines the deprecation policy that applies to Generative AI on Vertex AI.
The [deprecation policy](https://docs.cloud.google.com/terms/deprecation) only applies to the services,
features, or products listed therein.
After a service, feature, or product is officially
deprecated, it continues to be available for at least the period of time defined in the
Terms of Service. After this period of time, the service is scheduled for shutdown.
| **Feature** | **Deprecated date** | **Shutdown date** | **Details** |
|---|---|---|---|
| Generative AI module in the Vertex AI SDK | June 24, 2025 | June 24, 2026 | Starting on June 24, 2025, the Generative AI module in the Vertex AI SDK is deprecated. The Generative AI module will be removed on June 24, 2026. For information about migrating to the Google Gen AI SDK, see [Vertex AI SDK migration guide](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/genai-vertexai-sdk.md). |
After a period of time, [MaaS
models](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-partner-models) are
deprecated and typically replaced with newer model versions. To provide you with
time to test and migrate to newer models, this page lists all models that are
deprecated along with their shutdown date.
## Anthropic's Claude 3 Haiku
Anthropic's Claude 3 Haiku is **deprecated as of February 23, 2026** and will be
**shut down on August 23, 2026**. Anthropic's Claude 3 Haiku is available to
existing customers only.
Anthropic's Claude 3 Haiku is Anthropic's fastest vision and text model for
near-instant responses to basic queries, meant for seamless AI experiences
mimicking human interactions.
| Model ID | `claude-3-haiku` ||
| Launch stage | deprecated ||
| Supported inputs \& outputs | - Inputs: Text, Code, Images - Outputs: Text ||
| Token limits | - Maximum input tokens: 200,000 - Maximum output tokens: 8,000 ||
| Capabilities | - Supported - [Prompt caching](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/claude/prompt-caching) - [Function calling](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/claude/use-claude#tool_use_function_calling) - [Count tokens](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/claude/count-tokens) - Not supported - [Batch predictions](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/claude/batch) - [Extended thinking](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/claude/use-claude#use_a_curl_command) ||
| Usage types | - Supported - [Fixed quota](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/quotas) - [Provisioned Throughput](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/provisioned-throughput) - Not supported ||
| Technical specifications |
| Technical specifications |
| Technical specifications |
|---|---|---|
| Images | - **Limitation and specifications:** See [Vision](https://docs.anthropic.com/en/docs/build-with-claude/vision) in Anthropic's documentation |
| Documents | - **Limitation and specifications:** See [PDF support](https://docs.anthropic.com/en/docs/build-with-claude/pdf-support) in Anthropic's documentation |
| Model availability (Includes fixed quota \& Provisioned Throughput) | - United States - `us-east5` - Europe - `europe-west1` - Asia Pacific - `asia-southeast1` |
| ML processing | - United States - `Multi-region` - Europe - `Multi-region` - Asia Pacific - `asia-southeast1` |
## Claude 3.5 Haiku
Claude 3.5 Haiku is **deprecated as of January 5, 2026** and
will be **shut down on July 5, 2026**. Claude 3.5 Haiku is
available to existing customers only.
Claude 3.5 Haiku, the next
generation of Anthropic's fastest and most cost-effective model, is
optimal for use cases where speed and affordability matter.
[View model card in Model Garden](https://console.cloud.google.com/vertex-ai/publishers/anthropic/model-garden/claude-3-5-haiku)
| Model ID | `claude-3-5-haiku` ||
| Launch stage | deprecated ||
| Supported inputs \& outputs | - Inputs: Text, Code, Images - Outputs: Text ||
| Token limits | - Maximum input tokens: 200,000 - Maximum output tokens: 8,000 ||
| Capabilities | - Supported - [Batch predictions](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/claude/batch) - [Prompt caching](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/claude/prompt-caching) - [Function calling](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/claude/use-claude#tool_use_function_calling) - [Count tokens](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/claude/count-tokens) - Not supported - [Extended thinking](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/claude/use-claude#use_a_curl_command) ||
| Usage types | - Supported - [Fixed quota](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/quotas) - [Provisioned Throughput](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/provisioned-throughput) - Not supported ||
| Technical specifications |
| Technical specifications |
| Technical specifications |
|---|---|---|
| Images | - **Limitation and specifications:** See [Vision](https://docs.anthropic.com/en/docs/build-with-claude/vision) in Anthropic's documentation |
| Documents | - **Limitation and specifications:** See [PDF support](https://docs.anthropic.com/en/docs/build-with-claude/pdf-support) in Anthropic's documentation |
| Model availability (Includes fixed quota \& Provisioned Throughput) | - United States - `us-east5` - Europe - `europe-west1` |
| ML processing | - United States - `Multi-region` - Europe - `Multi-region` |
## Claude 3.7 Sonnet
Claude 3.7 Sonnet is **deprecated as of November 11, 2025** and
will be **shut down on May 11, 2026**. Claude 3.7 Sonnet is
available to existing customers only.
Claude 3.7 Sonnet is a state-of-the-art model for real-world
software engineering tasks and agentic capabilities.
| Model ID | `claude-3-7-sonnet` ||
| Launch stage | deprecated ||
| Supported inputs \& outputs | - Inputs: Text, Code, Images - Outputs: Text ||
| Token limits | - Maximum input tokens: 200,000 - Maximum output tokens: 128,000 ||
| Capabilities | - Supported - [Batch predictions](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/claude/batch) - [Prompt caching](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/claude/prompt-caching) - [Function calling](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/claude/use-claude#tool_use_function_calling) - [Count tokens](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/claude/count-tokens) - Not supported - [Extended thinking](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/claude/use-claude#use_a_curl_command) ||
| Usage types | - Supported - [Fixed quota](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/quotas) - [Provisioned Throughput](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/provisioned-throughput) - Not supported ||
| Technical specifications |
| Technical specifications |
| Technical specifications |
|---|---|---|
| Images | - **Limitation and specifications:** See [Vision](https://docs.anthropic.com/en/docs/build-with-claude/vision) in Anthropic's documentation |
| Documents | - **Limitation and specifications:** See [PDF support](https://docs.anthropic.com/en/docs/build-with-claude/pdf-support) in Anthropic's documentation |
| Model availability (Includes fixed quota \& Provisioned Throughput) | - United States - `us-east5` - Europe - `europe-west1` - Global - `global endpoint` |
| ML processing | - United States - `Multi-region` - Europe - `Multi-region` |
## Claude 3.5 Sonnet v2
Claude 3.5 Sonnet v2 is **deprecated as of August 20, 2025** and
will be
**shut down on February 19, 2026**. Claude 3.5 Sonnet v2 is
available to existing customers only.
Claude 3.5 Sonnet v2 is a state-of-the-art model for real-world
software engineering tasks and agentic capabilities.
[Try in Vertex AI](https://console.cloud.google.com/vertex-ai/generative/multimodal/create/text?model=claude-3-5-sonnet-v2)
| Model ID | `claude-3-5-sonnet-v2` ||
| Launch stage | GA ||
| Supported inputs \& outputs | - Inputs: Text, Code, Images - Outputs: Text ||
| Token limits | - Maximum input tokens: 200,000 - Maximum output tokens: 8,000 ||
| Capabilities | - Supported - [Batch predictions](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/claude/batch) - [Prompt caching](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/claude/prompt-caching) - [Function calling](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/claude/use-claude#tool_use_function_calling) - [Count tokens](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/claude/count-tokens) - Not supported - [Extended thinking](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/claude/use-claude#use_a_curl_command) ||
| Usage types | - Supported - [Fixed quota](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/quotas) - [Provisioned Throughput](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/provisioned-throughput) - Not supported ||
| Technical specifications |
| Technical specifications |
| Technical specifications |
|---|---|---|
| Images | - **Limitation and specifications:** See [Vision](https://docs.anthropic.com/en/docs/build-with-claude/vision) in Anthropic's documentation |
| Documents | - **Limitation and specifications:** See [PDF support](https://docs.anthropic.com/en/docs/build-with-claude/pdf-support) in Anthropic's documentation |
| Model availability (Includes fixed quota \& Provisioned Throughput) | - United States - `us-east5` - Europe - `europe-west1` - Global - `global endpoint` |
| ML processing | - United States - `Multi-region` - Europe - `Multi-region` |
## Claude 3.5 Sonnet
Claude 3.5 Sonnet is **deprecated as of August 20, 2025** and
will be
**shut down on February 19, 2026**. Claude 3.5 Sonnet is
available to existing customers only.
Claude 3.5 Sonnet outperforms Anthropic's
Claude 3 Opus on a wide range of Anthropic's evaluations with the
speed and cost of Anthropic's mid-tier model, Claude 3 Sonnet.
| Model ID | `claude-3-5-sonnet` ||
| Launch stage | GA ||
| Supported inputs \& outputs | - Inputs: Text, Code, Images - Outputs: Text ||
| Token limits | - Maximum input tokens: 200,000 - Maximum output tokens: 8,000 ||
| Capabilities | - Supported - [Prompt caching](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/claude/prompt-caching) - [Function calling](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/claude/use-claude#tool_use_function_calling) - [Count tokens](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/claude/count-tokens) - Not supported - [Batch predictions](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/claude/batch) - [Extended thinking](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/claude/use-claude#use_a_curl_command) ||
| Usage types | - Supported - [Fixed quota](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/quotas) - [Provisioned Throughput](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/provisioned-throughput) - Not supported ||
| Technical specifications |
| Technical specifications |
| Technical specifications |
|---|---|---|
| Images | - **Limitation and specifications:** See [Vision](https://docs.anthropic.com/en/docs/build-with-claude/vision) in Anthropic's documentation |
| Documents | - **Limitation and specifications:** See [PDF support](https://docs.anthropic.com/en/docs/build-with-claude/pdf-support) in Anthropic's documentation |
| Model availability (Includes fixed quota \& Provisioned Throughput) | - United States - `us-east5` - Europe - `europe-west1` - Asia Pacific - `asia-southeast1` |
| ML processing | - United States - `Multi-region` - Europe - `Multi-region` - Asia Pacific - `asia-southeast1` |
## Jamba 1.5 Large
Jamba 1.5 Large is **deprecated as of August 27, 2025** and will be
**shut down on February 27, 2026**. Jamba 1.5 Large is available to
existing customers only.
AI21 Labs's Jamba 1.5 Large is well balanced across quality,
throughput, and low cost.
[View model card in Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)
| Model ID | `jamba-1.5-large` ||
| Launch stage | Preview ||
| Supported inputs \& outputs | - Inputs: Text, Documents - Outputs: Text ||
| Usage types | - Supported - [Fixed quota](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/quotas) - Not supported - [Provisioned Throughput](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/provisioned-throughput) ||
| Knowledge cutoff date | March 2024 ||
| Versions | - `jamba-1.5-large` - **Launch stage:** Preview - **Release date:** August 22, 2024 ||
| Supported regions |
| Supported regions |
| Supported regions |
|---|---|---|
| Model availability | - United States - `us-central1` - Europe - `europe-west4` |
| ML processing | - United States - `Multi-region` |
## Jamba 1.5 Mini
Jamba 1.5 Mini is **deprecated as of August 27, 2025** and will be
**shut down on February 27, 2026**. Jamba 1.5 Mini is available to existing
customers only.
AI21 Labs's Jamba 1.5 Mini is well balanced across quality, throughput,
and low cost.
[View model card in Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)
| Model ID | `jamba-1.5-mini` ||
| Launch stage | Preview ||
| Supported inputs \& outputs | - Inputs: Text, Documents - Outputs: Text ||
| Usage types | - Supported - [Fixed quota](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/quotas) - Not supported - [Provisioned Throughput](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/provisioned-throughput) ||
| Knowledge cutoff date | March 2024 ||
| Versions | - `jamba-1.5-mini` - **Launch stage:** Preview - **Release date:** August 22, 2024 ||
| Supported regions |
| Supported regions |
| Supported regions |
|---|---|---|
| Model availability | - United States - `us-central1` - Europe - `europe-west4` |
| ML processing | - United States - `Multi-region` |
## Claude 3 Opus
Anthropic's Claude 3 Opus is **deprecated as of June 30, 2025** and will be
**shut down on August 1, 2025**. Claude 3 Opus is available to
existing customers only.
Anthropic's Claude 3 Opus is a powerful AI model with top-level performance on highly
complex tasks. It can navigate open-ended prompts and sight-unseen scenarios
with remarkable fluency and human-like understanding. Claude 3 Opus
is optimized for the following use cases:
- Task automation, such as interactive coding and planning, or running complex
actions across APIs and databases.
- Research and development tasks, such as research review, brainstorming and
hypothesis generation, and product testing.
- Strategy tasks, such as advanced analysis of charts and graphs, financials
and market trends, and forecasting.
- Vision tasks, such as processing images to return text output. Also,
analysis of charts, graphs, technical diagrams, reports, and other visual
content.
| Model ID | `claude-3-opus` ||
| Launch stage | deprecated ||
| Supported inputs \& outputs | - Inputs: Text, Code, Images - Outputs: Text ||
| Token limits | - Maximum input tokens: 200,000 - Maximum output tokens: 8,000 ||
| Capabilities | - Supported - [Prompt caching](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/claude/prompt-caching) - [Function calling](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/claude/use-claude#tool_use_function_calling) - [Count tokens](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/claude/count-tokens) - Not supported - [Batch predictions](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/claude/batch) - [Extended thinking](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/claude/use-claude#use_a_curl_command) ||
| Usage types | - Supported - [Fixed quota](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/quotas) - [Provisioned Throughput](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/provisioned-throughput) - Not supported ||
| Technical specifications |
| Technical specifications |
| Technical specifications |
|---|---|---|
| Images | - **Limitation and specifications:** See [Vision](https://docs.anthropic.com/en/docs/build-with-claude/vision) in Anthropic's documentation |
| Documents | - **Limitation and specifications:** See [PDF support](https://docs.anthropic.com/en/docs/build-with-claude/pdf-support) in Anthropic's documentation |
| Model availability (Includes fixed quota \& Provisioned Throughput) | - United States - `us-east5` |
| ML processing | - United States - `Multi-region` |