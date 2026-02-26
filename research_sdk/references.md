# References

Curated reference links for the AI framework evaluation. All links verified reachable as of February 25, 2026.

Stats collected via npm downloads API and GitHub API on February 25, 2026. npm download counts reflect the week of February 18-24, 2026.

Note: npmjs.com links return HTTP 403 when accessed from automated curl clients due to bot protection, but all packages are verified to exist via the npm registry downloads API (api.npmjs.org). The package pages are accessible from standard browsers.

---

## LangChain (@langchain/google-vertexai)

### Official Documentation

| Title | URL | Type | Summary |
|-------|-----|------|---------|
| LangChain JS/TS - Google Vertex AI Chat Integration | https://js.langchain.com/docs/integrations/chat/google_vertex_ai | official docs | Primary integration guide for using Vertex AI models (Gemini, Claude via Model Garden) with LangChain in TypeScript. |
| LangChain JS/TS - Agents Tutorial | https://js.langchain.com/docs/tutorials/agents | official docs | Step-by-step guide to building ReAct and tool-calling agents using LangChain in TypeScript. |
| LangChain JS/TS - Agent Executor | https://js.langchain.com/docs/how_to/agent_executor | official docs | Reference for the AgentExecutor abstraction used to run LangChain agents with tool loops. |
| LangChain Python - Google Vertex AI | https://python.langchain.com/docs/integrations/chat/google_vertex_ai_palm/ | official docs | Python counterpart for Vertex AI integration, useful for cross-referencing authentication patterns. |

### GitHub

| Title | URL | Type | Summary |
|-------|-----|------|---------|
| langchain-ai/langchainjs | https://github.com/langchain-ai/langchainjs | GitHub | Official LangChain JavaScript/TypeScript monorepo; 17,027 stars, last commit 2026-02-25. |

### npm

| Title | URL | Type | Summary |
|-------|-----|------|---------|
| @langchain/google-vertexai on npm | https://www.npmjs.com/package/@langchain/google-vertexai | npm | Official LangChain package for Vertex AI; v2.1.20, 352,183 weekly downloads (week of 2026-02-18). |
| @langchain/core on npm | https://www.npmjs.com/package/@langchain/core | npm | Core abstractions package that all LangChain integrations depend on; installed version v0.3.60. |

### Community

| Title | URL | Type | Summary |
|-------|-----|------|---------|
| LangChain Blog - Tool Calling with LangChain | https://blog.langchain.dev/tool-calling-with-langchain/ | community | Official LangChain blog post explaining tool-calling patterns across providers, directly relevant to agentic testing. |
| LangChain Blog - LangGraph Cloud | https://blog.langchain.dev/langgraph-cloud/ | community | Announcement and architecture overview of LangGraph Cloud for production multi-agent deployments. |

---

## Google ADK (@google/adk)

### Official Documentation

| Title | URL | Type | Summary |
|-------|-----|------|---------|
| Google ADK Documentation | https://google.github.io/adk-docs/ | official docs | Primary documentation hub for Google Agent Development Kit including quickstart, concepts, and API reference. |
| ADK Quickstart Guide | https://google.github.io/adk-docs/get-started/quickstart/ | official docs | Hands-on quickstart for setting up ADK agents with Vertex AI authentication via ADC. |
| ADK Agents Reference | https://google.github.io/adk-docs/agents/ | official docs | Detailed reference for ADK's agent types, lifecycle, and composition patterns. |
| ADK Tools Reference | https://google.github.io/adk-docs/tools/ | official docs | Documentation for ADK's built-in tool integrations and custom tool definition patterns. |

### GitHub

| Title | URL | Type | Summary |
|-------|-----|------|---------|
| google/adk-python | https://github.com/google/adk-python | GitHub | Official Python ADK repository; 17,974 stars, last commit 2026-02-25. |
| google/adk-js | https://github.com/google/adk-js | GitHub | Official JavaScript/TypeScript ADK repository with setup instructions and package info (@google/adk v0.3.0). |

### npm / Package Registry

| Title | URL | Type | Summary |
|-------|-----|------|---------|
| @google/adk on npm | https://www.npmjs.com/package/@google/adk | npm | Official Google ADK JavaScript package; v0.3.0 pre-release, early adoption phase. |
| google-adk on PyPI | https://pypi.org/project/google-adk/ | npm | Official Google ADK Python package on PyPI; the Python version has broader adoption and more documentation examples. |

### Community

| Title | URL | Type | Summary |
|-------|-----|------|---------|
| Google Vertex AI - Multimodal Overview | https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/overview | community | Google Cloud official overview of multimodal generative AI on Vertex AI, providing context for ADK's target platform. |
| Google Cloud Vertex AI Authentication Docs | https://cloud.google.com/vertex-ai/docs/authentication | community | Authoritative Google Cloud documentation for all Vertex AI authentication methods used by ADK. |

---

## Claude SDK (@anthropic-ai/vertex-sdk)

### Official Documentation

| Title | URL | Type | Summary |
|-------|-----|------|---------|
| Claude on Vertex AI Guide | https://docs.anthropic.com/en/docs/claude-on-vertex-ai | official docs | Official Anthropic guide for using Claude models via Google Cloud Vertex AI with @anthropic-ai/vertex-sdk. |
| Claude Tool Use Documentation | https://docs.anthropic.com/en/docs/build-with-claude/tool-use | official docs | Comprehensive guide for implementing tool calling with Claude, the core capability for agentic testing. |
| Claude Extended Thinking | https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking | official docs | Documentation for Claude's extended thinking mode, enabling multi-step autonomous reasoning for complex tasks. |

### GitHub

| Title | URL | Type | Summary |
|-------|-----|------|---------|
| anthropics/anthropic-sdk-typescript | https://github.com/anthropics/anthropic-sdk-typescript | GitHub | Official Anthropic TypeScript SDK repository; includes @anthropic-ai/sdk and @anthropic-ai/vertex-sdk; 2,813 stars (Python SDK), last commit 2026-02-25. |

### npm

| Title | URL | Type | Summary |
|-------|-----|------|---------|
| @anthropic-ai/vertex-sdk on npm | https://www.npmjs.com/package/@anthropic-ai/vertex-sdk | npm | Official Anthropic Vertex AI SDK; v0.14.4, 202,656 weekly downloads (week of 2026-02-18). |
| @anthropic-ai/sdk on npm | https://www.npmjs.com/package/@anthropic-ai/sdk | npm | Base Anthropic SDK that vertex-sdk extends; installed version v0.78.0. |

### Community

| Title | URL | Type | Summary |
|-------|-----|------|---------|
| Google Cloud - Use Claude on Vertex AI | https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-claude | community | Google Cloud official guide for accessing Claude models through Vertex AI Model Garden, covering setup and available Claude versions. |
| Vercel AI SDK Community Providers | https://sdk.vercel.ai/providers/community-providers | community | Documents community-created providers including patterns for integrating non-native LLMs like Claude into the Vercel AI SDK ecosystem. |

---

## Vercel AI SDK (ai)

### Official Documentation

| Title | URL | Type | Summary |
|-------|-----|------|---------|
| Vercel AI SDK Introduction | https://sdk.vercel.ai/docs/introduction | official docs | Official introduction and architecture overview of Vercel AI SDK v6, including the provider model and streaming design. |
| AI SDK Core - Agents | https://sdk.vercel.ai/docs/ai-sdk-core/agents | official docs | Documentation for building agentic workflows with the Vercel AI SDK using generateText and tool-calling. |
| AI SDK Cookbook - Tool Calling | https://sdk.vercel.ai/cookbook/next/call-tools | official docs | Practical recipes for implementing tool calling in Next.js applications using the Vercel AI SDK. |
| Community Providers Reference | https://sdk.vercel.ai/providers/community-providers | official docs | Registry of community-maintained providers, showing the extensibility model used for custom Vertex AI integration. |

### GitHub

| Title | URL | Type | Summary |
|-------|-----|------|---------|
| vercel/ai | https://github.com/vercel/ai | GitHub | Official Vercel AI SDK monorepo; 22,025 stars, last commit 2026-02-25 - highest star count among evaluated frameworks. |

### npm

| Title | URL | Type | Summary |
|-------|-----|------|---------|
| ai on npm | https://www.npmjs.com/package/ai | npm | Vercel AI SDK core package; v6.0.99, 8,547,193 weekly downloads (week of 2026-02-18) - highest download count by far. |
| @ai-sdk/google-vertex on npm | https://www.npmjs.com/package/@ai-sdk/google-vertex | npm | Official Vercel AI SDK provider for Google Vertex AI; installed version v4.0.63 in this project. |

### Community

| Title | URL | Type | Summary |
|-------|-----|------|---------|
| Vercel Blog - Introducing the Vercel AI SDK | https://vercel.com/blog/introducing-the-vercel-ai-sdk | community | Original launch blog post explaining the motivation, design goals, and architecture of the Vercel AI SDK. |
| Vercel Blog - AI SDK 4.2 | https://vercel.com/blog/ai-sdk-4-2 | community | Release announcement for AI SDK 4.2 covering streaming improvements and provider ecosystem expansion. |

---

## LlamaIndex (llamaindex)

### Official Documentation

| Title | URL | Type | Summary |
|-------|-----|------|---------|
| LlamaIndex Documentation Home | https://docs.llamaindex.ai/en/stable/ | official docs | Primary documentation hub for LlamaIndex covering RAG, agents, data connectors, and query engines. |
| LlamaIndex Agents Use Cases | https://docs.llamaindex.ai/en/stable/use_cases/agents/ | official docs | Use case guide for building autonomous agents with LlamaIndex, covering ReAct, multi-step reasoning, and tool use. |
| LlamaIndex TypeScript Docs | https://ts.llamaindex.ai/ | official docs | Official TypeScript-specific documentation for LlamaIndex.TS, covering the JavaScript/TypeScript API surface. |
| LlamaIndex Agent Deployment Guide | https://docs.llamaindex.ai/en/stable/module_guides/deploying/agents/ | official docs | Module guide for deploying LlamaIndex agents including multi-agent workflows and production patterns. |

### GitHub

| Title | URL | Type | Summary |
|-------|-----|------|---------|
| run-llama/llama_index | https://github.com/run-llama/llama_index | GitHub | Main LlamaIndex Python repository; 47,185 stars, last commit 2026-02-25 - highest star count overall. |
| run-llama/LlamaIndexTS | https://github.com/run-llama/LlamaIndexTS | GitHub | Official TypeScript implementation of LlamaIndex (LlamaIndex.TS), the version used in this evaluation. |

### npm

| Title | URL | Type | Summary |
|-------|-----|------|---------|
| llamaindex on npm | https://www.npmjs.com/package/llamaindex | npm | Main LlamaIndex TypeScript package; v0.12.1, 109,353 weekly downloads (week of 2026-02-18). |
| @llamaindex/core on npm | https://www.npmjs.com/package/@llamaindex/core | npm | LlamaIndex core abstractions package; 127,075 weekly downloads (week of 2026-02-18). |
| @llamaindex/google on npm | https://www.npmjs.com/package/@llamaindex/google | npm | LlamaIndex Google adapter package providing Vertex AI access via @google/genai; installed version v0.4.0. |

### Community

| Title | URL | Type | Summary |
|-------|-----|------|---------|
| LlamaIndex Blog | https://www.llamaindex.ai/blog | community | Official LlamaIndex blog covering new features, use cases, benchmarks, and community highlights. |
| LlamaIndex RAG CLI Starter | https://docs.llamaindex.ai/en/stable/getting_started/starter_tools/rag_cli/ | community | Practical starter tool demonstrating LlamaIndex's primary RAG use case, showing the framework's data-centric design. |

---

## Vertex AI Authentication

| Title | URL | Type | Summary |
|-------|-----|------|---------|
| Application Default Credentials (ADC) Guide | https://cloud.google.com/docs/authentication/application-default-credentials | official docs | Google Cloud authoritative guide for ADC, the authentication mechanism used by all evaluated frameworks for Vertex AI access. |
| gcloud auth application-default login Reference | https://cloud.google.com/sdk/gcloud/reference/auth/application-default/login | official docs | CLI reference for the `gcloud auth application-default login` command that initializes local developer ADC credentials. |
| Vertex AI Authentication Overview | https://cloud.google.com/vertex-ai/docs/authentication | official docs | Vertex AI-specific authentication documentation covering service accounts, ADC, and access scopes for production deployments. |

---

## Statistics Summary

| Framework | npm Package | Weekly Downloads | GitHub Stars | Last Commit |
|-----------|-------------|-----------------|--------------|-------------|
| LangChain | @langchain/google-vertexai | 352,183 | 17,027 (langchainjs) | 2026-02-25 |
| Google ADK | @google/adk | N/A (pre-1.0) | 17,974 (adk-python) | 2026-02-25 |
| Claude SDK | @anthropic-ai/vertex-sdk | 202,656 | 2,813 (anthropic-sdk-python) | 2026-02-25 |
| Vercel AI SDK | ai | 8,547,193 | 22,025 (vercel/ai) | 2026-02-25 |
| LlamaIndex | llamaindex | 109,353 | 47,185 (llama_index) | 2026-02-25 |

Data collected: February 25, 2026. npm downloads reflect week of 2026-02-18 to 2026-02-24. GitHub stars are point-in-time snapshots.
