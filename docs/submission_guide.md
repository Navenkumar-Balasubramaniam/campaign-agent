# AI Campaign Agent Submission Guide

## 1. Agent Concept Brief

**Agent name:** AI Campaign Agent

**Marketing problem it solves:** Marketing teams need to react quickly to external triggers such as weather, events, seasonality, or cultural moments. Without a structured process, teams may spend time manually turning the trigger into copy, visual directions, mock assets, tests, and budget recommendations.

**Target user:** A junior marketer, social media manager, or small marketing team preparing a paid social campaign. For the demo, the group can frame itself as the marketing team for Estrella.

**Input received by the agent:**

- Product
- Brand or company
- Campaign trigger
- Target audience
- Campaign goal
- Budget
- Channel
- Tone
- Duration
- Call to action
- Reference images (optional): a product photo and/or campaign reference images that ground the generated visuals

**Process followed by the agent:**

1. **Classifies** the free-text trigger into structured tags (season, themes, urgency, suggested angle, risk flags).
2. **Retrieves** the most relevant past Estrella campaigns from the brand knowledge base by matching theme, season, channel, and goal.
3. **Decides**, from historical results, which creative angle has historically won for this goal (CTR for awareness, ROAS for sales), with an expected-performance range and a budget tilt.
4. Builds a campaign strategy (positioning, message pillars, content plan, launch checklist) **grounded on** the brand guidelines and the retrieved winning campaigns.
5. Generates ad copy variants grounded on past winning copy.
6. Creates visual concept prompts and, when enabled, generates real AI campaign images from them — grounded on any uploaded product/reference images so the visual matches the real product and brand.
7. Splits the budget into campaign buckets and builds an A/B test matrix.
8. Produces an executive recommendation, KPI plan, data-derived reasoning, assumptions, limitations, and ethical considerations.

**Final output generated:** A campaign pack containing a trigger classification, a data-backed decision, the past campaigns it learned from, a historical-performance benchmark table, strategy, copy, visual concepts, generated AI campaign images (or offline mock creative previews as a fallback), budget recommendation, test plan, reasoning notes, KPI guidance, and reflection.

**Expected business value:** The agent helps marketers move faster from idea to first campaign draft, and grounds the recommendation in the brand's own past performance instead of generic copy. It supports decision-making by making the evidence and recommended angle explicit.

## 2. Technical Design

The prototype uses a modular agent design with a knowledge layer:

```text
User brief
  -> CampaignOrchestrator
  -> ClassifierAgent        (trigger -> structured tags; AI or rules)
  -> CampaignStore.retrieve (top-k relevant past campaigns from data/estrella/)
  -> Benchmarks             (aggregate results.csv by angle/audience)
  -> DecisionAgent          (data-backed angle + budget recommendation)
  -> StrategyAgent          (grounded on brand guidelines + past campaigns)
  -> CopyAgent              (grounded on past winning copy)
  -> VisualAgent / MockupAgent / AssetAgent
  -> BudgetAgent / ABTestAgent
  -> ReportAgent
  -> Campaign pack
```

**Generation modes (a dropdown):** *OpenRouter* runs the **entire grounded pipeline**
— classification, strategy, copy, and the decision narrative — on free, openly available
language models, so the full AI prototype works with no paid key. *Gemini* uses Google's
Gemini models (via an API key or Vertex AI) and produces the strongest reference-matched
images. *Offline demo* runs the same pipeline with deterministic rules and needs no key at
all. The knowledge/retrieval/decision layer is identical in every mode, so the *reasoning*
and *decision* are consistent regardless of which model writes the narrative. Both live
modes can also generate real campaign images and accept uploaded reference images.

**ClassifierAgent:** Turns the free-text trigger into structured tags (season, themes,
urgency, suggested angle, compliance risk flags) so the pipeline routes on structure, not
keyword guesses.

**CampaignStore + Benchmarks (knowledge layer):** `CampaignStore` loads the brand's past
campaigns (`data/estrella/campaigns.json`) and brand guidelines, and retrieves the most
relevant past campaigns for the new brief. `Benchmarks` aggregates per-variant historical
results (`data/estrella/results.csv`) into averages by creative angle and audience type.

**DecisionAgent:** The core decision-support step. It computes — from the benchmarks —
which angle has historically performed best for the campaign goal (CTR for awareness,
ROAS for sales), an expected-performance range, and a budget tilt. Numbers are computed
deterministically so they are never hallucinated; in live mode the model only writes the
reasoning over those numbers.

**StrategyAgent:** Creates the whole-campaign plan (name, objective, positioning, message
pillars, content plan, launch checklist), grounded on the brand guidelines and the
retrieved past campaigns.

**CopyAgent:** Generates three ad copy variants, grounded on the brand voice and the
copy of past campaigns that performed well. Live mode uses the model; offline uses
deterministic copy.

**VisualAgent:** Creates three image prompts that act as visual strategy notes and as the input to image generation.

**Image generation:** When the user opts in, the live clients turn the visual prompts into real campaign images. If the user uploaded a product photo or reference images, those are passed to the image model as visual ground truth so the result keeps the product's real appearance, packaging, and logo. The Gemini image model gives the strongest reference matching.

**MockupAgent:** Creates offline PNG mock creative previews used as a fallback when no real AI images are generated (e.g. offline mode). These are draft layout assets, not final photography.

**AssetAgent:** Suggests free mock/reference image sources (a Commons Estrella bottle reference and free lifestyle sources) for academic campaign concepts when no images are generated.

**BudgetAgent:** Applies simple decision rules. For Instagram, Facebook, and Meta campaigns, it splits budget into prospecting, retargeting, and creative testing.

**ABTestAgent:** Combines the first two headlines and first two visual prompts into four A/B test variants.

**ReportAgent:** Combines all agent outputs into one campaign pack and adds reasoning, KPI guidance, limitations, and ethical considerations.

## 3. Working Prototype Demonstration

**Sample input:**

```text
Product: Crafted beer
Brand: Estrella
Trigger: The sun is out so we want people to go to beer gardens or the park and enjoy a nice cold beer.
Audience: young adults aged 18-24
Goal: Sales
Budget: 1000
Channel: Instagram
Tone: Fun, party, good vibes
Duration: 14 days
CTA: Shop Now
Generation mode: Offline demo (or OpenRouter for the free live-AI run)
```

**Processing steps:**

1. The classifier reads the trigger → season: summer, themes: summer/outdoor/social, urgency: high, risk flag: alcohol.
2. The store retrieves the most relevant past campaigns (e.g. *Terrace Retargeting Push*, *Cold & Crisp Summer Offer*, *Summer '78*).
3. The benchmarks show product-led/retargeting historically won on ROAS (~4.x) and CPA, while purpose angles converted worst.
4. The decision agent recommends the **product-led** angle for this Sales goal, with an expected ROAS range (~3.1–4.2) and a budget tilt toward retargeting.
5. The strategy and copy agents generate an on-brand plan and three copy variants grounded on those past winners.
6. The visual, mockup, asset, budget, and A/B agents produce the supporting creative and media plan.
7. The report agent assembles the pack and surfaces the data-derived reasoning.

**Final output:** The app displays the trigger classification, the data-backed decision
(recommended angle, evidence, expected performance), the past campaigns it learned from, a
historical-performance-by-angle table, an executive recommendation, campaign strategy,
copy variants, generated AI campaign images (or mock creative previews as a fallback),
visual strategy notes, any uploaded reference images, budget split, A/B test plan, KPI
plan, assumptions, limitations, and responsible-use notes.

**Usefulness for a marketing team:** The output is a first draft that is *justified by the
brand's own history*. A marketer sees not just suggested copy but which angle the data
backs, the expected performance range, and where to weight budget — then validates and
runs a small test.

**Sample output (offline run, Sales brief):** recommended angle `product-led`; primary
metric `ROAS`; expected ROAS `3.11–4.21`, CTR `0.95–1.29%`, CPA `6.15–8.33`; grounded on
the 2022/2023 product/retargeting summer campaigns.

## 4. Reflection

**What the agent does well:**

- Goes beyond prompting: it **classifies, retrieves, reasons, and decides**.
- Grounds new campaigns on the brand's **own past campaigns and performance data**.
- Makes a **data-backed decision** (recommended angle + expected performance + budget tilt) rather than just generating text.
- Computes all metrics deterministically so figures are never hallucinated, while still using AI for reasoning and generation.
- Uses brand guidelines as an input, keeping output on-brand.
- Runs the **whole AI pipeline on free models** (OpenRouter mode) and keeps a deterministic offline fallback, so the full prototype works with no paid key and never fails in a live demo.
- Generates real campaign images and can **ground them on an uploaded product photo**, so visuals match the actual product rather than a generic stand-in.
- Produces multiple creative variants and a full, structured campaign pack.

**Limitations:**

- The historical results are **realistic but synthetic** (see `PROVENANCE.md`); they should be replaced with a real Ads Manager export before the numbers are trusted.
- Past campaign copy is paraphrased for academic use, not the brand's verbatim copy.
- It does not connect to a live ad account, CRM, or competitor data.
- Retrieval is tag/keyword based (not semantic embeddings).
- Free models have per-minute rate limits; the clients retry with backoff to absorb short bursts, and offline mode remains the ultimate fallback.
- Offline mock creatives are draft layouts, not final professional imagery.

**How it could be improved:**

- Replace synthetic results with a real Meta Ads Manager export and real Ad Library copy.
- Add embeddings-based semantic retrieval (`text-embedding-004`).
- Add a PDF export of the campaign pack and a brand-guidelines upload step.
- Add a human approval/sign-off step before any real launch.
- Expand the knowledge base to multiple brands.

**Risks and ethical considerations:**

- The agent could generate misleading or exaggerated marketing claims.
- Sensitive products, such as alcohol or health products, need extra review.
- Audience targeting should avoid discriminatory or exploitative practices.
- Human approval should remain required before any real campaign launch.

**Real marketing context:** A real team could use this as an early planning assistant. The agent would create a first draft, while marketers would validate claims, check policies, refine the creative, and use real performance data to optimize the campaign after launch.
