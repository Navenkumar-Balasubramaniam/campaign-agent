# AI Campaign Agent

AI Campaign Agent is a Streamlit prototype that turns a campaign trigger into a full
campaign pack for a marketing team. It is built around a single brand — **Estrella Damm** —
and **grounds every new campaign on that brand's past campaigns and their performance
data**, so the output reflects what has actually worked before rather than generic copy.

The agent produces a trigger classification, a data-backed decision (which creative
angle to lead with and why), campaign strategy, ad copy, visual concept prompts,
real AI campaign images (or mock creative previews as a fallback), a budget split, an
A/B test matrix, KPI guidance, and a responsible-use reflection.

## What makes it an agent (not just a prompt)

The pipeline combines **classification, retrieval, AI reasoning, and decision support**:

1. **Classify** — the free-text trigger is turned into structured tags
   (`season`, `themes`, `urgency`, `suggested_angle`, `risk_flags`).
2. **Retrieve** — the most relevant past campaigns are pulled from the brand
   knowledge base (`data/estrella/`) by matching theme, season, channel, and goal.
3. **Decide** — historical results (`results.csv`) are aggregated into benchmarks,
   and the agent recommends the creative angle that has historically won for this
   goal (CTR for awareness, ROAS for sales), with expected-performance ranges.
4. **Generate** — strategy and copy are produced **grounded on** the brand
   guidelines and the retrieved winning campaigns.
5. **Report** — everything is assembled into a campaign pack with data-derived
   reasoning, KPI guidance, limitations, and ethical considerations.

## Generation modes

| Mode | What it does | Needs |
|---|---|---|
| **OpenRouter** | Runs the **entire grounded pipeline** — classifier, strategy, copy, and decision narrative — on free, openly available models | OpenRouter key |
| **Gemini** | Same pipeline on Google's Gemini; gives the strongest reference-matched images | Gemini API key, or Vertex AI |
| **Offline demo** | Same pipeline, deterministic rules instead of a live model. No network, never fails | Nothing |

The knowledge layer (past campaigns + benchmarks + decision) runs the **same in every
mode** — only the text generation switches between a live model and deterministic rules.
Both live modes can also generate real campaign images and accept uploaded **reference
images** (a product photo and/or campaign references) to ground the visuals.

## Marketing problem

Marketing teams need to react quickly to external moments (weather, events, seasonality).
This agent converts a trigger sentence and brief into a first campaign pack **informed by
the brand's own history**, supporting faster planning and clearer, evidence-based decisions.

## Target user

A junior marketer, social media manager, or small marketing team preparing a paid
social campaign for an established brand.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate         # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Select **Offline demo** to run with no key, or **OpenRouter** / **Gemini** after adding a
key. Copy the env template first:

```bash
cp .env.template .env
```

## Setup

**OpenRouter (runs the full pipeline on free models):** add a key from
<https://openrouter.ai/keys> to `.env`:

```bash
OPENROUTER_API_KEY=your_key_here
```

Quick check: `python scripts/check_openrouter.py`

**Gemini:** add a key from <https://aistudio.google.com>, or use Vertex AI:

```bash
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-2.5-flash-lite
# or, instead of a key, use Vertex AI (auth via `gcloud auth application-default login`):
# GOOGLE_GENAI_USE_VERTEXAI=true
# GOOGLE_CLOUD_PROJECT=your_project_id
```

Quick check: `python scripts/check_gemini.py`. Each campaign run makes ~4 model calls; the
clients retry on rate limits, and offline mode is the safe fallback for live presentations.

### Optional: AI image generation

Tick **"Generate AI campaign images"** (OpenRouter or Gemini mode) to turn the visual
prompts into real poster images. It is opt-in and **off by default**, capped by
`MAX_IMAGES_PER_CAMPAIGN`. Upload a **product photo** or **reference images** in the form
to ground the visuals on the real product (Gemini matches references best). An image
failure (e.g. a safety refusal on alcohol creative) never breaks the rest of the pack.

## Run tests

```bash
pytest
```

Tests use offline/deterministic clients and never call a paid API.

## Project structure

```text
app.py                          Streamlit user interface
config/settings.py              Environment settings (Gemini, OpenRouter)
data/estrella/                  Brand knowledge base
  brand_guidelines.md           Brand voice/positioning the agent reasons against
  campaigns.json                Real past campaigns (briefs + creative)
  results.csv                   Per-variant historical performance metrics
  PROVENANCE.md                 What is real vs. modelled, and how to source real data
src/orchestrator.py             Coordinates the classify -> retrieve -> decide -> generate flow
src/knowledge/campaign_store.py Loads + retrieves relevant past campaigns
src/knowledge/benchmarks.py     Aggregates historical results into benchmarks
src/agents/classifier_agent.py  Trigger -> structured tags (AI + rules)
src/agents/decision_agent.py    Data-backed angle/budget recommendation
src/agents/strategy_agent.py    Campaign strategy, grounded on past campaigns
src/agents/copy_agent.py        Ad copy, grounded on past winning copy
src/agents/visual_agent.py      Visual concept prompts
src/agents/mockup_agent.py      Offline mock creative previews
src/agents/asset_agent.py       Mock/reference image sources
src/agents/budget_agent.py      Budget split
src/agents/ab_test_agent.py     A/B test matrix
src/agents/report_agent.py      Assembles the final campaign pack
src/clients/gemini_client.py    Gemini client (API key or Vertex AI)
src/clients/demo_client.py      Offline deterministic client
src/clients/openrouter_client.py OpenRouter client (free models)
tests/                          Unit tests (offline)
docs/                           Submission guide + development notes
```

## Limitations

- Historical results in `data/estrella/results.csv` are **realistic but synthetic**;
  replace them with a real Ads Manager export before relying on the numbers.
- Past campaign copy is paraphrased for academic use, not the brand's verbatim copy.
- The prototype does not connect to a live ad account, CRM, or competitor data.
- Generated copy needs human review for brand accuracy and platform policy compliance.
- Offline mock creatives are draft layouts, not final AI-generated photography.
- For alcohol, target only legal-drinking-age audiences and review responsible-drinking rules.

See `data/estrella/PROVENANCE.md` for data sourcing and how to make it fully real.
