# Development Notes — Iteration History

This documents how the agent was designed, tested, and improved (Option 2:
spec-driven development). It shows the reasoning behind the architecture, not just
the final result.

## Iteration 1 — Template prototype

**What we built:** a modular multi-agent Streamlit app (orchestrator + strategy,
copy, visual, mockup, asset, budget, A/B, report agents) that turned a brief into a
campaign pack. It ran offline with deterministic templates and had an optional
OpenRouter mode.

**What worked:** clean separation of concerns, a clear input → process → output flow,
multiple creative variants, budget/A-B/KPI guidance, and responsible-use notes.

**Problem we identified:** in the default mode there was **no real AI**. The "agents"
were f-string templates and `if "sun" in trigger` keyword checks. The "agent reasoning"
section was hardcoded text. Against the brief's criterion *"goes beyond simple prompting
and uses AI for reasoning, automation, classification, generation, or decision support"*,
a reviewer running the demo would see zero AI and no real decision-making. The output
was also generic — it did not reflect the brand or any evidence.

## Iteration 2 — Grounded, data-driven agent

We reframed the project around **one brand (Estrella Damm)** and gave the agent a
**knowledge base of that brand's past campaigns and their performance**, so new
campaigns are based on evidence. Four changes:

1. **Real AI via Gemini (free tier).** Added `GeminiClient` (Google `google-genai`
   SDK, JSON mode). The classifier, strategy, copy, and decision narrative now use a
   live model. The offline deterministic path was kept as a labelled fallback so a
   live demo never fails on quota/network. Provider is a dropdown.

2. **Classification, not keyword `if`s.** `ClassifierAgent` turns the free-text
   trigger into structured tags (`season`, `themes`, `urgency`, `suggested_angle`,
   `risk_flags`). Live mode uses the model; offline uses rules. Downstream agents now
   branch on the structured classification.

3. **Retrieval grounding (RAG-lite).** `CampaignStore` loads `data/estrella/` and
   retrieves the top-k most relevant past campaigns by theme/season/channel/goal
   overlap. Strategy and copy are generated *grounded on* those winning examples and
   the brand guidelines, so output is on-brand and evidence-based.

4. **Decision support from real results.** `Benchmarks` aggregates
   `results.csv` into averages by creative angle and audience type. `DecisionAgent`
   computes — deterministically — which angle has historically won for the campaign's
   goal (CTR for awareness, ROAS for sales), the expected-performance range, and how
   to tilt the budget. In live mode the model writes the *reasoning* but only over the
   computed numbers, so figures are never hallucinated. This replaced the previously
   hardcoded "agent reasoning".

## Key design decision: numbers are computed, reasoning is generated

To get the benefits of an LLM without the risk of invented metrics, the decision agent
**computes all numbers in Python** from the benchmark data, then (optionally) asks the
model to explain the recommendation using only those numbers. This keeps the decision
defensible and reproducible while still demonstrating AI reasoning.

## Testing

- 24 unit tests run fully offline (no API key, no network):
  - `test_campaign_store.py` — corpus loads; retrieval prioritises relevant campaigns; unknown brand is safe.
  - `test_benchmarks.py` — aggregation; Sales favours product-led on ROAS; Awareness uses CTR; missing file is safe.
  - `test_classifier_agent.py` — summer + alcohol-risk detection; goal-driven angle suggestion.
  - `test_decision_agent.py` — recommends product-led for Sales with evidence; safe with no data.
  - plus the original agent/orchestrator/schema tests.
- We verified the end-to-end offline run: a sunny **Sales** brief is classified as a
  high-urgency summer moment, retrieves the product-led/retargeting summer campaigns,
  and recommends the **product-led** angle (best historical ROAS ~4.x) with an expected
  CTR/CPA/ROAS range — a genuine, data-backed decision.

## How to extend further

- Replace synthetic `results.csv` with a real Meta Ads Manager export.
- Replace paraphrased copy with real ads from the Meta Ad Library.
- Add embeddings-based retrieval (`text-embedding-004`) instead of tag overlap.
- Add a PDF export of the campaign pack and a brand-guidelines upload step.
