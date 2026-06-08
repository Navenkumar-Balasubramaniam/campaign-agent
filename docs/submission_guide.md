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

**Process followed by the agent:**

1. Interprets the campaign trigger and brief.
2. Applies the Estrella brand profile to keep the output Mediterranean, social, summery, and responsible.
3. Builds a campaign strategy with positioning, message pillars, content plan, and launch checklist.
4. Generates ad copy variants.
5. Creates visual concept prompts.
6. Generates offline mock creative previews.
7. Suggests mock/reference image sources.
8. Splits the budget into campaign buckets.
9. Builds an A/B test matrix.
10. Produces an executive recommendation, KPI plan, assumptions, limitations, and ethical considerations.

**Final output generated:** A campaign pack containing strategy, copy, visual concepts, offline mock creative previews, mock asset sources, budget recommendation, test plan, reasoning notes, KPI guidance, and reflection.

**Expected business value:** The agent helps marketers move faster from idea to first campaign draft. It supports decision-making by making recommendations explicit and by giving the team a structured plan to test and improve.

## 2. Technical Design

The prototype uses a modular agent design:

```text
User brief
  -> CampaignOrchestrator
  -> StrategyAgent
  -> CopyAgent
  -> VisualAgent
  -> MockupAgent
  -> AssetAgent
  -> BudgetAgent
  -> ABTestAgent
  -> ReportAgent
  -> Campaign pack
```

**StrategyAgent:** Interprets the trigger and creates a whole-campaign plan, including campaign name, objective, positioning, message pillars, content plan, and launch checklist.

**CopyAgent:** Generates three ad copy variants. In free demo mode, this is handled locally by `DemoClient`. In optional OpenRouter mode, it can call an external AI model.

**VisualAgent:** Creates three image prompts that can be used as visual strategy notes or sent to an image model.

**MockupAgent:** Creates three offline PNG mock creative previews in free demo mode. These are draft layout assets, not final AI-generated photography.

**AssetAgent:** Suggests free mock/reference image sources that can be used for academic campaign concepts. These include a Commons Estrella bottle reference and free lifestyle sources from Unsplash/Pexels.

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
Generation mode: Free demo mode
```

**Processing steps:**

1. The orchestrator receives the structured brief.
2. The strategy agent interprets the sunny-weather trigger and creates the whole-campaign plan.
3. The copy agent creates three possible ad messages.
4. The visual agent creates three poster concept prompts.
5. The mockup agent creates three offline visual ad previews.
6. The asset agent recommends mock/reference image sources.
7. The budget agent recommends a daily budget and media split.
8. The A/B testing agent creates variants A-D.
9. The report agent creates the final campaign pack and explains the reasoning.

**Final output:** The app displays an executive recommendation, campaign strategy, campaign brief, copy variants, generated mock creative previews, visual strategy notes, mock asset sources, budget split, A/B test plan, KPI plan, assumptions, limitations, and responsible-use notes.

**Usefulness for a marketing team:** The output is useful as a first draft for planning. A marketer could review the copy, choose the strongest visual direction, prepare a small test, and adjust the budget based on early campaign results.

## 4. Reflection

**What the agent does well:**

- Turns a brief into a structured campaign pack.
- Reacts to an external trigger instead of only filling a generic brief.
- Keeps the project focused around one company for a clearer demonstration.
- Shows a clear input, processing, and output workflow.
- Produces multiple creative variants instead of one answer.
- Gives budget and A/B testing recommendations that support decision-making.
- Runs in free demo mode without paid API usage.

**Limitations:**

- Free demo mode is deterministic and does not use a live AI model.
- Offline mock creative previews are draft layouts and not final professional image generation.
- It does not use real campaign performance data.
- It does not check competitor activity, platform policy, or brand guidelines.
- It uses mock/reference image sources, not official approved brand assets.
- Budget rules are simplified for academic demonstration.

**How it could be improved:**

- Connect to real ad performance data.
- Add brand guidelines as an input.
- Score copy variants against campaign goals.
- Export the campaign pack as a PDF.
- Add an official brand asset upload step.
- Add approval steps for human review.

**Risks and ethical considerations:**

- The agent could generate misleading or exaggerated marketing claims.
- Sensitive products, such as alcohol or health products, need extra review.
- Audience targeting should avoid discriminatory or exploitative practices.
- Human approval should remain required before any real campaign launch.

**Real marketing context:** A real team could use this as an early planning assistant. The agent would create a first draft, while marketers would validate claims, check policies, refine the creative, and use real performance data to optimize the campaign after launch.
