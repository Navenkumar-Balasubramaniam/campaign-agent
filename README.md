# AI Campaign Agent

AI Campaign Agent is a Streamlit prototype that turns a short creative brief into a campaign pack for a marketing team. It produces ad copy variants, visual concept prompts, budget guidance, A/B testing recommendations, KPI guidance, and a reflection section for responsible use.

The project can run in **Free demo mode** without an OpenRouter API key. OpenRouter image generation is optional and should only be used if the team chooses to pay for API usage.

## Marketing Problem

Marketing teams often start with a rough campaign idea but still need to turn it into a practical launch plan. This agent helps by converting one structured brief into a first campaign pack that supports faster planning and clearer decision-making.

## Target User

The target user is a junior marketer, social media manager, or small marketing team preparing a paid social campaign.

## Agent Workflow

1. The user enters a creative brief with product, audience, goal, budget, channel, tone, duration, and CTA.
2. The copy agent generates three ad copy variants.
3. The visual agent creates three visual concept prompts for campaign posters.
4. The budget agent splits the budget across prospecting, retargeting, and creative testing.
5. The A/B testing agent combines copy and visual options into a test matrix.
6. The report agent assembles the final campaign pack, adds decision rationale, KPI guidance, limitations, and ethical considerations.

## No-Cost Demo Mode

The default mode is **Free demo mode**. It does not call OpenRouter and does not require a paid API key.

Free demo mode includes:

- Campaign copy variants
- Visual strategy prompts
- Budget recommendation
- A/B testing plan
- Agent reasoning
- KPI plan
- Reflection and responsible-use notes

Paid OpenRouter mode is optional and only needed for live model/image generation.

## Run Locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Then select **Free demo mode** in the app.

## Optional OpenRouter Setup

Only use this if the team chooses to use paid API calls.

```bash
cp .env.template .env
```

Add an OpenRouter API key to `.env`:

```bash
OPENROUTER_API_KEY=your_key_here
```

The manual API check is kept outside the normal test suite:

```bash
python scripts/manual_openrouter_check.py
```

## Run Tests

```bash
pytest
```

The test suite uses fake/demo clients and should not require paid API calls.

## Project Structure

```text
app.py                         Streamlit user interface
config/settings.py             Environment settings
src/orchestrator.py            Coordinates all agents
src/agents/copy_agent.py       Generates ad copy
src/agents/visual_agent.py     Generates visual concept prompts
src/agents/budget_agent.py     Creates budget split
src/agents/ab_test_agent.py    Creates A/B test matrix
src/agents/report_agent.py     Builds final campaign pack
src/clients/demo_client.py     Free local demo generator
src/clients/openrouter_client.py Optional OpenRouter client
tests/                         Unit tests
docs/submission_guide.md       Assignment-ready write-up
```

## Limitations

- Free demo mode is deterministic and does not use a live AI model.
- The prototype does not connect to live campaign, CRM, or competitor data.
- Generated recommendations should be reviewed by a human marketer before real use.
- Paid image generation is optional and not required for the academic demo.
