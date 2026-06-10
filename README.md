# AI Campaign Agent

AI Campaign Agent is a Streamlit prototype that turns a campaign brief and trigger into a full campaign pack for a marketing team. It produces campaign strategy, ad copy variants, visual concept prompts, draft creative mockups, reference asset sources, budget guidance, A/B testing recommendations, KPI guidance, and a responsible-use reflection section.

The app requires an OpenRouter API key. Offline PIL mockups are generated locally without any API cost.

## Marketing Problem

Marketing teams often need to react quickly to external moments: weather, events, trends, seasonality, or cultural moments. This agent converts a real-world trigger and a structured brief into a first campaign pack, supporting faster planning and clearer decision-making.

## Target User

Junior marketers, social media managers, or small marketing teams preparing a paid social campaign.

## Agent Workflow

1. The user selects a preset (Estrella — Summer outdoor moment) or creates a custom campaign.
2. The user edits the brief: brand, product, audience, goal, budget, channel, tone, duration, and CTA.
3. The user enters a campaign trigger — the real-world moment the campaign should react to.
4. The user optionally enables AI image generation (uses image API credits).
5. The **strategy agent** creates a trigger-based campaign plan with positioning, message pillars, content plan, and launch checklist.
6. The **copy agent** generates three ad copy variants (headline, body, CTA).
7. The **visual agent** creates three visual concept prompts for campaign posters.
8. The **mockup agent** renders three draft creative previews (Feed Ad, Story Ad, Product Ad) using real background photography and brand-matched colour palettes — no API cost.
9. The **asset agent** suggests free reference image sources appropriate to the brand and product.
10. The **budget agent** splits the budget across prospecting, retargeting, and creative testing.
11. The A/B testing agent combines copy, visual prompts, and mock assets into a test matrix.
12. The **report agent** assembles the final campaign pack with decision rationale, KPI guidance, limitations, and ethical considerations.

## Run Locally

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Copy the env template and add your key:

```bash
cp .env.template .env
```

Edit `.env`:

```
OPENROUTER_API_KEY=your_key_here
```

Start the app:

```bash
streamlit run app.py
```

## Configuration

All configuration lives in `.env`. The following variables are supported:

| Variable | Default | Description |
|---|---|---|
| `OPENROUTER_API_KEY` | *(required)* | Your OpenRouter API key |
| `OPENROUTER_TEXT_MODEL` | `google/gemma-4-31b-it:free` | Model used for all text generation |
| `OPENROUTER_IMAGE_MODEL` | `black-forest-labs/flux.2-klein-4b` | Model used when AI image generation is enabled |
| `MAX_IMAGES_PER_CAMPAIGN` | `3` | Maximum number of AI images to generate per campaign |
| `APP_NAME` | `AI Campaign Agent Demo` | App title shown in the browser tab and sent to OpenRouter |

The `.env` file overrides the defaults in `config/settings.py`. Variables not present in `.env` fall back to the defaults shown above.

## API Key

The app requires an OpenRouter API key. Without one the app shows an error on startup and stops.

- Sign up at [openrouter.ai](https://openrouter.ai)
- The default text model (`google/gemma-4-31b-it:free`) is free tier — no credits required for text generation
- AI image generation is optional and requires a model with image support (incurs API cost)

## Presets

The app ships with two presets selectable from the dropdown:

**Estrella — Summer outdoor moment** — pre-filled brief for a Mediterranean lager brand reacting to warm-weather outdoor occasions. All fields are editable; this is a starting point, not a locked config.

**Custom campaign** — blank slate for any brand, product, and trigger.

Any brief field (including the brand name) can be changed freely. All output — strategy, copy, mockups, assets — is generated from what the user enters, not from hardcoded brand logic.

## Draft Creative Mockups

The mockup agent generates three visually distinct layouts using PIL (no API call required):

| Variant | Format | Layout |
|---|---|---|
| A | Feed Ad (1080 × 1080) | Full-bleed background photo, dark gradient overlay, brand badge top-left, headline and CTA pinned to the bottom third |
| B | Story Ad (1080 × 1920) | Photo fills top 52%, dark panel fills bottom 48%, headline bridges both zones |
| C | Product Ad (1080 × 1080) | Accent colour sidebar left, photo in top-right zone, text panel below |

Background photos are sourced from [picsum.photos](https://picsum.photos) using a seed derived from the brand name, so the same brand always produces the same photos. If the network is unavailable the layouts fall back to the brand colour palette.

Colour palettes (navy/blue, charcoal/coral, forest/cream, midnight/sky, warm-black/amber) are assigned deterministically by brand name. Alcohol products automatically append a responsible-drinking legal line.

## Project Structure

```text
app.py                           Streamlit user interface
config/settings.py               Env-backed configuration
src/orchestrator.py              Coordinates all agents
src/models/schemas.py            CampaignBrief Pydantic model
src/brand_profiles.py            Brand context builder
src/clients/openrouter_client.py OpenRouter API client (text + image)
src/agents/strategy_agent.py     Trigger-based campaign strategy
src/agents/copy_agent.py         Ad copy variants (headline/body/CTA)
src/agents/visual_agent.py       Visual concept prompts
src/agents/mockup_agent.py       Offline PIL draft creative previews
src/agents/asset_agent.py        Reference asset source suggestions
src/agents/budget_agent.py       Budget split across buckets
src/agents/ab_test_agent.py      A/B test matrix
src/agents/report_agent.py       Final campaign pack assembly
tests/                           Unit tests
docs/submission_guide.md         Assignment-ready write-up
```

## OpenRouter Client

The client (`src/clients/openrouter_client.py`) handles:

- `"stream": False` added to every payload — prevents chunked response errors on certain provider models
- Automatic retry (up to 3 attempts) on HTTP 429 with the `retry_after_seconds` backoff from the error response
- `ChunkedEncodingError` retry with a 3-second wait between attempts
- `"choices"` key guard — surfaces the model error message cleanly instead of raising a `KeyError`

## Run Tests

```bash
pytest
```

The test suite does not require a paid API key.

## Manual API Check

```bash
python scripts/manual_openrouter_check.py
```

## Limitations

- Offline draft creative mockups are layout previews, not AI-generated photography.
- The prototype does not connect to live campaign, CRM, or competitor data.
- Generated recommendations should be reviewed by a human marketer before real use.
- Free-tier models may be rate-limited under heavy concurrent use.
- AI image generation is optional and incurs additional API cost.
- Mock images and copy are for academic demonstration only and must not be used in real commercial campaigns without appropriate review and rights clearance.
