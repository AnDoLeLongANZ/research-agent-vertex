# AI/LLM Framework Evaluation Criteria Matrix

Research Date: February 25, 2026
Purpose: Define objective, repeatable scoring rubric for comparing AI/LLM frameworks for autonomous testing

## Overview

This document defines the weighted scoring methodology used to evaluate AI/LLM frameworks against four core requirements for building autonomous testing agents in TypeScript with Vertex AI integration.

## Scoring Weights

The evaluation uses a weighted scoring system with the following distribution:

| Criterion | Weight | Rationale |
|-----------|--------|-----------|
| Vertex AI Authentication Support | 30% | Critical requirement - must integrate with Google Cloud Vertex AI |
| TypeScript Support | 25% | Essential for type-safe, maintainable test automation codebase |
| Agentic Capabilities | 25% | Core functionality - frameworks must support autonomous agent behavior |
| Community Strength | 20% | Affects long-term viability, support availability, and ecosystem maturity |

Total Weight: 100%

## Scoring Scale

All criteria are scored on a 0-10 scale where:
- 10 = Exceptional - exceeds requirements significantly
- 7-9 = Strong - meets requirements with minor gaps
- 4-6 = Adequate - meets minimum requirements with notable limitations
- 1-3 = Weak - significant gaps or limitations
- 0 = Unsupported - does not meet requirement

Final Score = (Vertex AI Score * 0.30) + (TypeScript Score * 0.25) + (Agentic Score * 0.25) + (Community Score * 0.20)

Maximum possible score: 10.0

## 1. Vertex AI Authentication Support (30% weight)

Evaluation Dimension: How well does the framework integrate with Google Cloud Vertex AI authentication and model access?

### Scoring Rubric

| Score | Level | Criteria | Examples |
|-------|-------|----------|----------|
| 10 | Native - First Class | - Official package for Vertex AI integration<br>- Native ADC support<br>- Access to full model catalog<br>- Regular updates for new Vertex AI features<br>- Zero configuration complexity | @langchain/google-vertexai<br>@anthropic-ai/vertex-sdk |
| 7-9 | Native - Good | - Official Vertex AI support<br>- ADC authentication works<br>- Access to most models<br>- Some configuration required<br>- Occasional lag on new features | @google/genai |
| 4-6 | Adapter/Wrapper | - Community or third-party adapter<br>- Requires custom provider implementation<br>- ADC possible with effort<br>- Limited model access<br>- Moderate integration complexity | Vercel AI SDK (custom provider)<br>LlamaIndex (@llamaindex/google-vertexai) |
| 1-3 | Workaround/Hack | - No official support<br>- Requires significant custom code<br>- Fragile integration<br>- Limited to specific models<br>- High maintenance burden | Custom HTTP wrapper |
| 0 | Unsupported | - No Vertex AI integration possible<br>- Incompatible authentication<br>- Different cloud provider only | OpenAI SDK<br>Semantic Kernel (Azure only) |

### Key Evaluation Questions
- Does an official Vertex AI package exist?
- Does it support Application Default Credentials (ADC)?
- Can it access Claude models via Vertex AI?
- Can it access Gemini models via Vertex AI?
- How much custom code is required for integration?
- Is authentication handling production-ready?

## 2. TypeScript Support (25% weight)

Evaluation Dimension: Quality, maturity, and completeness of TypeScript SDK and type definitions.

### Scoring Rubric

| Score | Level | Criteria | Examples |
|-------|-------|----------|----------|
| 10 | Official + Complete Types | - Official TypeScript SDK from framework maintainer<br>- Comprehensive type definitions<br>- Full IDE autocomplete support<br>- Strict type safety (minimal `any` usage)<br>- Type inference works correctly<br>- Active TypeScript-first development | @anthropic-ai/sdk<br>Vercel AI SDK<br>@google/genai |
| 7-9 | Official SDK | - Official TypeScript SDK<br>- Good type coverage (>80%)<br>- IDE support functional<br>- Some `any` types present<br>- Generally type-safe<br>- Regular type improvements | langchain<br>llamaindex |
| 4-6 | Community/Partial | - Community-maintained TypeScript port<br>- Basic type definitions<br>- Limited IDE support<br>- Frequent `any` usage<br>- Type safety gaps<br>- Lagging behind primary SDK | semantic-kernel (TypeScript port) |
| 1-3 | Minimal/Typed Wrappers | - JavaScript SDK with minimal .d.ts files<br>- Poor type coverage<br>- Little IDE support<br>- Mostly `any` types<br>- Type safety not enforced | Legacy JavaScript libraries with basic types |
| 0 | None | - No TypeScript support<br>- JavaScript only<br>- No type definitions available | Pure JavaScript libraries |

### Key Evaluation Questions
- Is the SDK officially maintained by framework creators?
- What percentage of the API has type definitions?
- Does IDE autocomplete work reliably?
- Are generic types used correctly for type inference?
- How many escape hatches (`any`, `unknown`) exist?
- Is the codebase TypeScript-first or ported from another language?

## 3. Agentic Capabilities (25% weight)

Evaluation Dimension: Built-in support for autonomous agent behavior, tool calling, multi-step reasoning, and orchestration.

### Scoring Rubric

| Score | Level | Criteria | Examples |
|-------|-------|----------|----------|
| 10 | Purpose-Built Agent Framework | - Dedicated agent orchestration system<br>- Multiple agent patterns (ReAct, Plan-Execute, etc.)<br>- Tool/function calling built-in<br>- Multi-agent coordination<br>- State management and memory<br>- Workflow/graph-based orchestration<br>- Production-ready agent primitives | LangChain (with LangGraph)<br>LlamaIndex (with agents) |
| 7-9 | Extensible Agent Support | - Strong tool calling support<br>- Multi-step reasoning capable<br>- Conversation state management<br>- Function execution framework<br>- Agent patterns achievable with extension<br>- Good for single-agent scenarios | Claude SDK (tool use + extended thinking)<br>Vercel AI SDK (tools + streaming) |
| 4-6 | Basic Tool Calling | - Function/tool calling available<br>- Single-turn or limited multi-turn<br>- Basic state management<br>- Requires significant custom orchestration<br>- Limited agent patterns<br>- Manual workflow implementation | @google/genai (function calling)<br>OpenAI SDK (function calling) |
| 1-3 | Protocol/Primitive Only | - Low-level primitives only<br>- No orchestration support<br>- Requires full custom agent layer<br>- Minimal built-in patterns | Model Context Protocol SDK |
| 0 | None | - No agent support<br>- No tool calling<br>- Single-turn completions only | Basic completion APIs |

### Key Evaluation Questions
- Are agent patterns built into the framework?
- What tool/function calling mechanisms exist?
- Can the framework handle multi-step reasoning autonomously?
- Is there state management between agent steps?
- Can multiple agents coordinate?
- What orchestration patterns are supported (sequential, parallel, conditional)?
- How much custom code is required to build an autonomous agent?

## 4. Community Strength (20% weight)

Evaluation Dimension: Ecosystem maturity, community size, production usage, and long-term viability.

### Scoring Rubric

| Score | Level | Criteria | Examples |
|-------|-------|----------|----------|
| 10 | Very Strong | - npm downloads: 500k+ per week<br>- GitHub stars: 50k+ (or official backing)<br>- Active daily commits<br>- Stack Overflow: 1000+ questions<br>- Production usage: Widespread in enterprise<br>- Rich ecosystem of plugins/integrations<br>- Responsive maintainers | Vercel AI SDK (500k+ downloads)<br>OpenAI SDK (1M+ downloads) |
| 7-9 | Strong | - npm downloads: 100k-500k per week<br>- GitHub stars: 10k-50k<br>- Regular commits (weekly)<br>- Stack Overflow: 500-1000 questions<br>- Production usage: Common<br>- Growing ecosystem<br>- Active community support | LangChain (100k+ downloads)<br>@google/genai (official Google) |
| 4-6 | Healthy | - npm downloads: 20k-100k per week<br>- GitHub stars: 5k-10k<br>- Regular updates (monthly)<br>- Stack Overflow: 100-500 questions<br>- Production usage: Emerging<br>- Core ecosystem present<br>- Community exists but smaller | LlamaIndex (20k+ downloads)<br>MCP SDK (30k downloads, Anthropic-backed) |
| 1-3 | Emerging/Weak | - npm downloads: <20k per week<br>- GitHub stars: <5k<br>- Sporadic updates<br>- Stack Overflow: <100 questions<br>- Production usage: Early adopters only<br>- Limited ecosystem<br>- Small community | Reactive Agents<br>Community ports (semantic-kernel TS) |
| 0 | Inactive/Dead | - No recent updates (>6 months)<br>- No community activity<br>- Deprecated or abandoned<br>- No production usage | Abandoned projects |

### Key Evaluation Questions
- How many npm downloads per week?
- How many GitHub stars and active contributors?
- When was the last commit/release?
- How many Stack Overflow questions exist?
- Are there production case studies or testimonials?
- What is the ecosystem size (plugins, integrations, tools)?
- How responsive are maintainers to issues?
- Is there official backing (company/foundation)?

## Cost/Pricing Considerations (Qualitative - Not Scored)

While not included in the numerical score, cost implications are documented for each framework:

### Evaluation Dimensions
- Framework license cost (most are free/open-source)
- Underlying LLM model costs (Vertex AI pricing)
- Infrastructure costs (hosting, compute)
- Hidden costs (vendor lock-in, migration costs)
- Cost optimization features (caching, batching, streaming)

### Key Questions
- Is the framework open-source or commercial?
- Are there usage-based fees?
- What Vertex AI models does it support (cost variance)?
- Does it support cost optimization features?
- What are the infrastructure requirements?

### Framework Cost Notes

| Framework | License | Cost Considerations |
|-----------|---------|---------------------|
| LangChain | Open Source (MIT) | Free framework, pay for model usage only |
| Claude SDK | Open Source (Apache 2.0) | Free SDK, pay for Claude model usage via Vertex AI |
| Vercel AI SDK | Open Source (Apache 2.0) | Free SDK, pay for model usage |
| LlamaIndex | Open Source (MIT) | Free framework, pay for model usage |
| Google GenAI | Open Source (Apache 2.0) | Free SDK, pay for Gemini/Vertex AI usage |
| OpenAI SDK | Open Source (Apache 2.0) | Free SDK, incompatible with Vertex AI (uses OpenAI API pricing) |

## Evaluation Methodology

### Step-by-Step Evaluation Process

1. Framework Discovery
   - Identify candidate frameworks through npm search, GitHub exploration, technical knowledge
   - Initial screening for basic compatibility (TypeScript, LLM integration)

2. Criterion Assessment
   - For each framework, evaluate against all 4 criteria
   - Assign 0-10 score for each criterion based on rubric
   - Document evidence supporting each score

3. Weighted Score Calculation
   - Apply weights: Vertex AI (30%), TypeScript (25%), Agentic (25%), Community (20%)
   - Calculate final weighted score
   - Rank frameworks by total score

4. Qualitative Analysis
   - Document cost/pricing considerations
   - Identify unique strengths and weaknesses
   - Note special use cases or scenarios
   - Provide "When to Choose" guidance

5. Validation
   - Cross-check scores against documented evidence
   - Verify consistency across similar frameworks
   - Review for bias toward specific architectures

### Evidence Requirements

For each criterion, document:
- Specific package names and versions
- npm download metrics (npmjs.com or npm info)
- GitHub repository metrics (stars, commits, contributors)
- Code examples demonstrating capabilities
- Official documentation links
- Community activity indicators

### Scoring Consistency Rules

1. All frameworks scored against same rubric version
2. Scores based on current state (February 2026), not roadmap promises
3. Evidence required for scores >7 (no assumptions)
4. When uncertain between score levels, choose lower score (conservative)
5. Framework-specific strengths noted separately, not inflated in scores

## Example Evaluation Template

```
Framework Name: [Name]
Version: [x.y.z]
Evaluation Date: [Date]

1. Vertex AI Authentication Support: [Score]/10
   - Evidence: [Package name, authentication method, documentation]
   - Justification: [Why this score?]

2. TypeScript Support: [Score]/10
   - Evidence: [Official SDK, type coverage, examples]
   - Justification: [Why this score?]

3. Agentic Capabilities: [Score]/10
   - Evidence: [Agent patterns, tool calling, orchestration]
   - Justification: [Why this score?]

4. Community Strength: [Score]/10
   - Evidence: [npm downloads, GitHub metrics, community activity]
   - Justification: [Why this score?]

Weighted Score: [Calculated]
= ([Vertex AI Score] * 0.30) + ([TypeScript Score] * 0.25) + ([Agentic Score] * 0.25) + ([Community Score] * 0.20)

Cost Considerations: [Qualitative notes]

Strengths: [List]
Weaknesses: [List]
When to Choose: [Guidance]
```

## Rubric Version History

- v1.0 (February 25, 2026): Initial rubric creation for US-002
  - Defined 4 weighted criteria
  - Created 0-10 scoring scales
  - Documented evaluation methodology
  - Added cost considerations (qualitative)

## Next Steps

This evaluation criteria matrix will be applied in:
- US-003: LangChain detailed evaluation
- US-004: Google ADK detailed evaluation
- US-005: Claude SDK detailed evaluation
- US-006: Alternative Framework #1 (Vercel AI SDK) evaluation
- US-007: Alternative Framework #2 (LlamaIndex) evaluation

Scores will be compiled into comparative analysis in US-017.
