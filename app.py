import streamlit as st

from config.settings import settings
from src.clients.openrouter_client import OpenRouterClient
from src.models.schemas import CampaignBrief
from src.orchestrator import CampaignOrchestrator


CAMPAIGN_PRESETS = {
    "Estrella — Summer outdoor moment": {
        "brand": "Estrella",
        "campaign_trigger": (
            "The sun is out and people are heading to beer gardens, "
            "parks, and terraces to enjoy the warm weather."
        ),
        "product": "Mediterranean-style lager",
        "audience": "Adults aged 18–34 who enjoy social outdoor occasions",
        "goal_index": 0,
        "budget": 1000,
        "channel_index": 0,
        "tone": "Warm, social, Mediterranean, effortlessly cool",
        "duration_days": 14,
        "cta": "Shop Now",
    },
    "Custom campaign": {
        "brand": "Your Brand",
        "campaign_trigger": (
            "Describe the moment or event that should trigger this campaign."
        ),
        "product": "Your Product",
        "audience": "Your target audience",
        "goal_index": 0,
        "budget": 1000,
        "channel_index": 0,
        "tone": "Describe the tone",
        "duration_days": 14,
        "cta": "Learn More",
    },
}

GOALS = ["Sales", "Awareness", "Lead Generation"]
CHANNELS = ["Instagram", "Facebook", "Meta", "LinkedIn"]

st.set_page_config(page_title=settings.APP_NAME, layout="wide")

st.title("AI Campaign Agent")
st.caption("Fill in the brief. Get a full campaign pack.")

# ── API key guard ─────────────────────────────────────────────────────
if not settings.OPENROUTER_API_KEY:
    st.error(
        "No OpenRouter API key found. Add `OPENROUTER_API_KEY` to your "
        "`.env` file and restart the app."
    )
    st.stop()

# ── Preset selector ───────────────────────────────────────────────────
preset_name = st.selectbox(
    "Start from a preset", list(CAMPAIGN_PRESETS.keys())
)
preset = CAMPAIGN_PRESETS[preset_name]

# ── Brief form ────────────────────────────────────────────────────────
with st.form("campaign_brief"):
    st.subheader("Creative Brief")

    col_a, col_b = st.columns(2)

    with col_a:
        brand = st.text_input("Brand name", preset["brand"])
        product = st.text_input("Product", preset["product"])
        audience = st.text_area("Target audience", preset["audience"])
        goal = st.selectbox(
            "Campaign goal", GOALS, index=preset["goal_index"]
        )
        budget = st.number_input(
            "Budget (€)", min_value=1, value=preset["budget"]
        )

    with col_b:
        channel = st.selectbox(
            "Channel", CHANNELS, index=preset["channel_index"]
        )
        tone = st.text_input("Tone", preset["tone"])
        duration_days = st.number_input(
            "Duration (days)", min_value=1, value=preset["duration_days"]
        )
        cta = st.text_input("CTA", preset["cta"])

    campaign_trigger = st.text_area(
        "Campaign trigger",
        preset["campaign_trigger"],
        help=(
            "Describe the real-world moment or event the campaign "
            "should react to."
        ),
    )

    st.divider()

    generate_images = st.checkbox(
        "Generate AI images via OpenRouter (uses image API credits)",
        value=False,
        help=(
            "When enabled, the agent calls the OpenRouter image API to "
            "generate campaign visuals. This incurs additional API cost."
        ),
    )

    submitted = st.form_submit_button("Generate Campaign Pack")


# ── Run ───────────────────────────────────────────────────────────────
if submitted:
    try:
        brief = CampaignBrief(
            brand=brand,
            campaign_trigger=campaign_trigger,
            product=product,
            audience=audience,
            goal=goal,
            budget=budget,
            channel=channel,
            tone=tone,
            duration_days=duration_days,
            cta=cta,
        )

        client = OpenRouterClient()
        orchestrator = CampaignOrchestrator(client)

        with st.spinner("Generating campaign pack…"):
            result = orchestrator.run(brief, generate_image=generate_images)

        pack = result["campaign_pack"]

        st.success("Campaign pack generated.")
        st.divider()

        # ── Executive recommendation ──────────────────────────────────
        st.header("Campaign Pack")
        st.subheader("Executive Recommendation")
        st.write(pack["recommendation_note"])

        # ── Strategy ─────────────────────────────────────────────────
        st.subheader("Campaign Strategy")
        strategy = pack["campaign_strategy"]
        brand_profile = strategy["brand_profile"]
        st.markdown(f"**Campaign Name:** {strategy['campaign_name']}")
        st.markdown(f"**Trigger:** {strategy['trigger']}")
        st.markdown(f"**Objective:** {strategy['objective']}")
        st.markdown(f"**Target Insight:** {strategy['target_insight']}")
        st.markdown(f"**Positioning:** {strategy['positioning']}")

        st.markdown("**Brand Profile**")
        st.markdown(f"- **Context:** {brand_profile['brand_context']}")
        st.markdown(f"- **Tone:** {brand_profile['tone']}")
        st.markdown(f"- **Mission:** {brand_profile['mission']}")

        st.markdown("**Message Pillars**")
        for pillar in strategy["message_pillars"]:
            st.markdown(f"- **{pillar['pillar']}:** {pillar['message']}")

        st.markdown("**Content Plan**")
        for item in strategy["content_plan"]:
            with st.container(border=True):
                st.markdown(f"**{item['phase']} — {item['format']}**")
                st.write(item["concept"])
                st.caption(item["purpose"])

        # ── Agent reasoning ───────────────────────────────────────────
        st.subheader("Agent Reasoning")
        for item in pack["decision_rationale"]:
            with st.container(border=True):
                st.markdown(f"**{item['step']}**")
                st.markdown(f"**Input:** {item['input_signal']}")
                st.markdown(f"**Decision:** {item['decision']}")

        # ── Brief summary ─────────────────────────────────────────────
        st.subheader("Campaign Brief")
        bs = pack["brief_summary"]
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**Brand:** {bs['brand']}")
            st.markdown(f"**Trigger:** {bs['campaign_trigger']}")
            st.markdown(f"**Product:** {bs['product']}")
            st.markdown(f"**Audience:** {bs['audience']}")
            st.markdown(f"**Goal:** {bs['goal']}")
            st.markdown(f"**Channel:** {bs['channel']}")
        with c2:
            st.markdown(f"**Tone:** {bs['tone']}")
            st.markdown(f"**Budget:** €{bs['budget']}")
            st.markdown(f"**Duration:** {bs['duration_days']} days")
            st.markdown(f"**CTA:** {bs['cta']}")

        st.divider()

        # ── Ad copy ───────────────────────────────────────────────────
        st.subheader("Recommended Ad Copy")
        headlines = pack["copy_variants"]["headlines"]
        primary_texts = pack["copy_variants"]["primary_texts"]
        ctas = pack["copy_variants"].get("ctas", [cta])

        for i, headline in enumerate(headlines, start=1):
            n = i - 1
            primary_text = primary_texts[n] if n < len(primary_texts) else ""
            selected_cta = ctas[0] if ctas else bs["cta"]
            with st.container(border=True):
                st.markdown(f"### Variant {i}")
                st.markdown(f"**Headline:** {headline}")
                st.markdown("**Primary Text:**")
                st.write(primary_text)
                st.markdown(f"**CTA:** {selected_cta}")

        st.divider()

        # ── AI-generated images ───────────────────────────────────────
        image_urls = pack.get("generated_image_urls", [])
        if image_urls:
            st.subheader("AI-Generated Campaign Visuals")
            cols = st.columns(3)
            for i, image_url in enumerate(image_urls):
                with cols[i % 3]:
                    st.image(
                        image_url,
                        caption=f"Visual Concept {i + 1}",
                        use_container_width=True,
                    )
            st.divider()

        # ── Mock creative mockups ─────────────────────────────────────
        st.subheader("Draft Creative Mockups")
        mockup_assets = pack["mockup_assets"]
        st.caption(mockup_assets["generation_note"])
        mockup_cols = st.columns(3)
        for i, asset in enumerate(mockup_assets["assets"]):
            with mockup_cols[i % 3]:
                with st.container(border=True):
                    st.image(
                        asset["image_data_url"],
                        caption=asset["format"],
                        use_container_width=True,
                    )
                    st.markdown(
                        f"**Variant {asset['variant']}: {asset['headline']}**"
                    )
                    st.write(asset["body"])
                    st.caption(asset["design_notes"])

        st.divider()

        # ── Visual prompts ────────────────────────────────────────────
        st.subheader("Visual Strategy Notes")
        for i, prompt in enumerate(
            pack["visual_concepts"]["image_prompts"], start=1
        ):
            with st.expander(f"Visual Concept {i} Prompt"):
                st.write(prompt)

        # ── Mock asset sources ────────────────────────────────────────
        st.subheader("Reference Asset Sources")
        mock_assets = pack["mock_assets"]
        st.write(mock_assets["asset_strategy"])
        st.caption(mock_assets["usage_note"])
        asset_cols = st.columns(len(mock_assets["assets"]))
        for i, asset in enumerate(mock_assets["assets"]):
            with asset_cols[i]:
                with st.container(border=True):
                    st.markdown(f"**{asset['title']}**")
                    st.caption(asset["asset_type"])
                    if asset["source_url"]:
                        src = asset["source"]
                        url = asset["source_url"]
                        st.markdown(f"Source: [{src}]({url})")
                    else:
                        st.markdown(f"Source: {asset['source']}")
                    st.markdown(f"License: {asset['license']}")
                    st.write(asset["use_case"])
                    st.caption(asset["note"])

        st.divider()

        # ── Budget ────────────────────────────────────────────────────
        st.subheader("Budget Recommendation")
        st.write(pack["budget_note"])
        budget_plan = pack["budget_plan"]
        st.markdown(f"**Total Budget:** €{budget_plan['total_budget']}")
        st.markdown(
            f"**Recommended Daily Budget:** €{budget_plan['daily_budget']}"
        )
        for item in budget_plan["budget_split"]:
            st.markdown(
                f"- **{item['bucket']}**: {item['percentage']}% "
                f"(€{item['amount']})"
            )

        st.divider()

        # ── A/B testing ───────────────────────────────────────────────
        st.subheader("A/B Testing Recommendation")
        st.write(pack["ab_test_note"])
        kpi_plan = pack["kpi_plan"]
        st.markdown(f"**Primary Metric:** {kpi_plan['primary_metric']}")
        st.markdown(
            f"**Secondary Metrics:** "
            f"{', '.join(kpi_plan['secondary_metrics'])}"
        )
        st.markdown(f"**Optimisation Rule:** {kpi_plan['optimization_rule']}")

        for test in pack["ab_test_plan"]["tests"]:
            with st.container(border=True):
                st.markdown(f"### Variant {test['variant']}")
                st.markdown(f"**Headline:** {test['headline']}")
                st.markdown(f"**Primary Text:** {test['primary_text']}")
                if test.get("mockup_asset"):
                    st.markdown(f"**Mockup Asset:** {test['mockup_asset']}")
                st.markdown(f"**Success Metric:** {test['success_metric']}")

        st.divider()

        # ── Reflection ────────────────────────────────────────────────
        st.subheader("Reflection and Responsible Use")
        r1, r2 = st.columns(2)
        with r1:
            st.markdown("**Assumptions**")
            for item in pack["assumptions"]:
                st.markdown(f"- {item}")
            st.markdown("**Limitations**")
            for item in pack["limitations"]:
                st.markdown(f"- {item}")
        with r2:
            st.markdown("**Ethical Considerations**")
            for item in pack["ethical_considerations"]:
                st.markdown(f"- {item}")
            st.markdown("**Real-World Use**")
            st.write(pack["real_world_use"])

        st.divider()
        st.subheader("Launch Status")
        st.success(pack["launch_status"])

    except Exception as e:
        st.error(str(e))
