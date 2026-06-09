# Data Provenance & Methodology

This folder is the **company knowledge base** the agent grounds new campaigns on.
It models Estrella Damm for an academic project. It is **not** official brand data.

## What is real vs. modelled

| Item | Source / status |
|---|---|
| Campaign names, years, themes, angles | **Real.** Estrella Damm's *Mediterraneamente* summer films (2009-2025) and sustainability campaigns are publicly documented. |
| Brand positioning, tone, themes (`brand_guidelines.md`) | **Real, paraphrased** from public Estrella Damm / Damm Corporate communications. |
| Ad copy in `campaigns.json` (`creative` blocks) | **Modelled.** Short paraphrased copy written to reflect each real campaign's documented message and angle. Not the verbatim brand copy. |
| Performance metrics (`results.csv`, `results_summary`) | **Synthetic but realistic.** Numbers are sampled to sit inside published benchmark ranges for beverage / alcohol paid social (see below). They are illustrative, not actual Estrella Damm results. |

## How to make it fully real (optional upgrade)
1. **Creative:** pull the brand's actual past ads from the **Meta Ad Library**
   (`facebook.com/ads/library`) and replace the `creative` blocks with real copy.
2. **Metrics:** replace `results.csv` with rows from a public ads dataset
   (e.g. a Kaggle "Facebook Ad Campaign" / "Social Media Ads" dataset) or with a
   client's real Meta Ads Manager export.

## Benchmark ranges used for the synthetic metrics
Modelled to be plausible for beverage / alcohol paid social on Meta:
- CTR: ~0.8%-2.2%
- CPC: ~£0.25-£0.40
- Conversion rate: ~1%-5.5%
- CPA: derived as `cpc / conversion_rate` so the table is internally consistent
- ROAS: ~1.4-4.6 (reported modelled value)

## Patterns deliberately encoded (so decision support has something to find)
- **Emotional-narrative & lifestyle** angles win on **CTR / awareness** (summer films).
- **Product-led** angles, especially on **retargeting** audiences, win on **CPA / conversion / ROAS**.
- **Purpose-sustainability** angles drive engagement but the **weakest direct conversion**.
- **Summer** seasonality lifts CTR across the board.

These patterns are what the `DecisionAgent` reads back out of `benchmarks.py`.

## Sources
- Damm Corporate — Ten summers Mediterraneamente; Summer '78; "Lo mismo de siempre"; end of plastic pack rings (dammcorporate.com)
- estrelladamm.com — brand positioning
- General Meta advertising benchmark ranges for the beverage category (illustrative)
