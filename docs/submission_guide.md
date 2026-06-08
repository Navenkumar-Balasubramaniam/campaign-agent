# AI Campaign Agent Submission Guide

## 1. Agent Concept Brief

**Agent name:** AI Campaign Agent

**Marketing problem it solves:** Marketing teams need to turn a short creative brief into a practical campaign plan. Without a structured process, teams may spend time manually writing copy, thinking of visual directions, planning tests, and deciding how to allocate budget.

**Target user:** A junior marketer, social media manager, or small marketing team preparing a paid social campaign.

**Input received by the agent:**

- Product
- Target audience
- Campaign goal
- Budget
- Channel
- Tone
- Duration
- Call to action

**Process followed by the agent:**

1. Interprets the campaign brief.
2. Generates ad copy variants.
3. Creates visual concept prompts.
4. Splits the budget into campaign buckets.
5. Builds an A/B test matrix.
6. Produces an executive recommendation, KPI plan, assumptions, limitations, and ethical considerations.

**Final output generated:** A campaign pack containing copy, visual concepts, budget recommendation, test plan, reasoning notes, KPI guidance, and reflection.

**Expected business value:** The agent helps marketers move faster from idea to first campaign draft. It supports decision-making by making recommendations explicit and by giving the team a structured plan to test and improve.

## 2. Technical Design

The prototype uses a modular agent design:

```text
User brief
  -> CampaignOrchestrator
  -> CopyAgent
  -> VisualAgent
  -> BudgetAgent
  -> ABTestAgent
  -> ReportAgent
  -> Campaign pack
```

**CopyAgent:** Generates three ad copy variants. In free demo mode, this is handled locally by `DemoClient`. In optional OpenRouter mode, it can call an external AI model.

**VisualAgent:** Creates three image prompts that can be used as visual strategy notes or sent to an image model.

**BudgetAgent:** Applies simple decision rules. For Instagram, Facebook, and Meta campaigns, it splits budget into prospecting, retargeting, and creative testing.

**ABTestAgent:** Combines the first two headlines and first two visual prompts into four A/B test variants.

**ReportAgent:** Combines all agent outputs into one campaign pack and adds reasoning, KPI guidance, limitations, and ethical considerations.

## 3. Working Prototype Demonstration

**Sample input:**

```text
Product: Crafted beer
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
2. The copy agent creates three possible ad messages.
3. The visual agent creates three poster concept prompts.
4. The budget agent recommends a daily budget and media split.
5. The A/B testing agent creates variants A-D.
6. The report agent creates the final campaign pack and explains the reasoning.

**Final output:** The app displays an executive recommendation, campaign brief, copy variants, visual strategy notes, budget split, A/B test plan, KPI plan, assumptions, limitations, and responsible-use notes.

**Usefulness for a marketing team:** The output is useful as a first draft for planning. A marketer could review the copy, choose the strongest visual direction, prepare a small test, and adjust the budget based on early campaign results.

## 4. Reflection

**What the agent does well:**

- Turns a brief into a structured campaign pack.
- Shows a clear input, processing, and output workflow.
- Produces multiple creative variants instead of one answer.
- Gives budget and A/B testing recommendations that support decision-making.
- Runs in free demo mode without paid API usage.

**Limitations:**

- Free demo mode is deterministic and does not use a live AI model.
- It does not use real campaign performance data.
- It does not check competitor activity, platform policy, or brand guidelines.
- Budget rules are simplified for academic demonstration.

**How it could be improved:**

- Connect to real ad performance data.
- Add brand guidelines as an input.
- Score copy variants against campaign goals.
- Export the campaign pack as a PDF.
- Add approval steps for human review.

**Risks and ethical considerations:**

- The agent could generate misleading or exaggerated marketing claims.
- Sensitive products, such as alcohol or health products, need extra review.
- Audience targeting should avoid discriminatory or exploitative practices.
- Human approval should remain required before any real campaign launch.

**Real marketing context:** A real team could use this as an early planning assistant. The agent would create a first draft, while marketers would validate claims, check policies, refine the creative, and use real performance data to optimize the campaign after launch.
