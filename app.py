import streamlit as st

from config.settings import settings
from src.clients.demo_client import DemoClient
from src.clients.openrouter_client import OpenRouterClient
from src.models.schemas import CampaignBrief
from src.orchestrator import CampaignOrchestrator


CAMPAIGN_PRESETS = {
    "Estrella beer mock campaign": {
        "brand": "Estrella",
        "product": "Mediterranean-style beer",
        "audience": "young adults aged 18-24 who enjoy social nights out",
        "goal_index": 0,
        "budget": 1000,
        "channel_index": 0,
        "tone": "Fun, party, good vibes",
        "duration_days": 14,
        "cta": "Shop Now",
    },
    "Custom campaign": {
        "brand": "Custom Brand",
        "product": "Organic Herbal Tea",
        "audience": "Women aged 25-45 interested in wellness and natural products",
        "goal_index": 0,
        "budget": 1000,
        "channel_index": 0,
        "tone": "Premium, calming, wellness-focused",
        "duration_days": 14,
        "cta": "Shop Now",
    },
}


st.set_page_config(page_title=settings.APP_NAME, layout="wide")

st.title("AI Campaign Agent Demo")
st.caption("Creative brief in. Campaign pack out.")

preset_name = st.selectbox(
    "Campaign Preset",
    list(CAMPAIGN_PRESETS.keys()),
)
preset = CAMPAIGN_PRESETS[preset_name]


with st.form("campaign_brief"):
    st.subheader("Creative Brief")

    brand = st.text_input("Company / Brand", preset["brand"])

    product = st.text_input("Product", preset["product"])

    audience = st.text_area(
        "Target Audience",
        preset["audience"],
    )

    goal = st.selectbox(
        "Campaign Goal",
        ["Sales", "Awareness", "Lead Generation"],
        index=preset["goal_index"],
    )

    budget = st.number_input(
        "Budget",
        min_value=1,
        value=preset["budget"],
    )

    channel = st.selectbox(
        "Channel",
        ["Instagram", "Facebook", "Meta", "LinkedIn"],
        index=preset["channel_index"],
    )

    tone = st.text_input(
        "Tone",
        preset["tone"],
    )

    duration_days = st.number_input(
        "Duration in Days",
        min_value=1,
        value=preset["duration_days"],
    )

    cta = st.text_input("CTA", preset["cta"])

    generation_mode = st.selectbox(
        "Generation Mode",
        ["Free demo mode", "OpenRouter API"],
    )

    generate_image = st.checkbox(
        "Generate 3 paid images using OpenRouter",
        value=False,
        disabled=generation_mode == "Free demo mode",
    )

    submitted = st.form_submit_button("Generate Campaign Pack")


if submitted:
    try:
        brief = CampaignBrief(
            brand=brand,
            product=product,
            audience=audience,
            goal=goal,
            budget=budget,
            channel=channel,
            tone=tone,
            duration_days=duration_days,
            cta=cta,
        )

        client = DemoClient() if generation_mode == "Free demo mode" else OpenRouterClient()
        orchestrator = CampaignOrchestrator(client)

        with st.spinner("Generating campaign pack..."):
            result = orchestrator.run(
                brief,
                generate_image=generate_image,
            )

        pack = result["campaign_pack"]

        st.success("Campaign pack generated successfully.")

        st.divider()

        st.header("Campaign Pack")

        st.subheader("Executive Recommendation")
        st.write(pack["recommendation_note"])

        st.subheader("Campaign Strategy")
        strategy = pack["campaign_strategy"]
        st.markdown(f"**Campaign Name:** {strategy['campaign_name']}")
        st.markdown(f"**Objective:** {strategy['objective']}")
        st.markdown(f"**Target Insight:** {strategy['target_insight']}")
        st.markdown(f"**Positioning:** {strategy['positioning']}")

        st.markdown("**Message Pillars**")
        for pillar in strategy["message_pillars"]:
            st.markdown(f"- **{pillar['pillar']}:** {pillar['message']}")

        st.markdown("**Content Plan**")
        for item in strategy["content_plan"]:
            with st.container(border=True):
                st.markdown(f"**{item['phase']} - {item['format']}**")
                st.write(item["concept"])
                st.caption(item["purpose"])

        st.subheader("Agent Reasoning")
        for item in pack["decision_rationale"]:
            with st.container(border=True):
                st.markdown(f"**{item['step']}**")
                st.markdown(f"**Input Signal:** {item['input_signal']}")
                st.markdown(f"**Decision:** {item['decision']}")

        st.subheader("Campaign Brief")
        brief_summary = pack["brief_summary"]

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"**Brand:** {brief_summary['brand']}")
            st.markdown(f"**Product:** {brief_summary['product']}")
            st.markdown(f"**Audience:** {brief_summary['audience']}")
            st.markdown(f"**Goal:** {brief_summary['goal']}")
            st.markdown(f"**Channel:** {brief_summary['channel']}")

        with col2:
            st.markdown(f"**Tone:** {brief_summary['tone']}")
            st.markdown(f"**Budget:** {brief_summary['budget']}")
            st.markdown(f"**Duration:** {brief_summary['duration_days']} days")
            st.markdown(f"**CTA:** {brief_summary['cta']}")

        st.divider()

        st.subheader("Recommended Ad Copy")

        headlines = pack["copy_variants"]["headlines"]
        primary_texts = pack["copy_variants"]["primary_texts"]
        ctas = pack["copy_variants"]["ctas"]

        for i, headline in enumerate(headlines, start=1):
            primary_text = primary_texts[i - 1] if i - 1 < len(primary_texts) else ""
            selected_cta = ctas[0] if ctas else brief_summary["cta"]

            with st.container(border=True):
                st.markdown(f"### Variant {i}")
                st.markdown(f"**Headline:** {headline}")
                st.markdown("**Primary Text:**")
                st.write(primary_text)
                st.markdown(f"**CTA:** {selected_cta}")

        st.divider()

        st.subheader("Generated Campaign Posters")

        image_urls = pack.get("generated_image_urls", [])

        if image_urls:
            cols = st.columns(3)

            for i, image_url in enumerate(image_urls):
                with cols[i % 3]:
                    st.image(
                        image_url,
                        caption=f"Poster Concept {i + 1}",
                        use_container_width=True,
                    )
        elif generation_mode == "Free demo mode":
            st.info("Free demo mode uses visual prompts instead of paid image generation.")
        else:
            st.info("Image generation was not selected.")

        st.divider()

        st.subheader("Visual Strategy Notes")

        image_prompts = pack["visual_concepts"]["image_prompts"]

        for i, prompt in enumerate(image_prompts, start=1):
            with st.expander(f"Visual Concept {i} Prompt"):
                st.write(prompt)

        st.subheader("Mock Asset Sources")
        mock_assets = pack["mock_assets"]
        st.write(mock_assets["asset_strategy"])
        st.caption(mock_assets["usage_note"])

        asset_cols = st.columns(3)
        for i, asset in enumerate(mock_assets["assets"]):
            with asset_cols[i % 3]:
                with st.container(border=True):
                    if asset["image_url"]:
                        st.image(asset["image_url"], use_container_width=True)
                    st.markdown(f"**{asset['title']}**")
                    st.caption(asset["asset_type"])
                    st.markdown(f"Source: [{asset['source']}]({asset['source_url']})")
                    st.markdown(f"License: {asset['license']}")
                    st.write(asset["use_case"])
                    st.caption(asset["note"])

        st.divider()

        st.subheader("Budget Recommendation")
        st.write(pack["budget_note"])

        budget_plan = pack["budget_plan"]

        st.markdown(f"**Total Budget:** {budget_plan['total_budget']}")
        st.markdown(f"**Recommended Daily Budget:** {budget_plan['daily_budget']}")

        for item in budget_plan["budget_split"]:
            st.markdown(
                f"- **{item['bucket']}**: {item['percentage']}% "
                f"({item['amount']})"
            )

        st.divider()

        st.subheader("A/B Testing Recommendation")
        st.write(pack["ab_test_note"])

        kpi_plan = pack["kpi_plan"]
        st.markdown(f"**Primary Metric:** {kpi_plan['primary_metric']}")
        st.markdown(f"**Secondary Metrics:** {', '.join(kpi_plan['secondary_metrics'])}")
        st.markdown(f"**Optimization Rule:** {kpi_plan['optimization_rule']}")

        for test in pack["ab_test_plan"]["tests"]:
            with st.container(border=True):
                st.markdown(f"### Variant {test['variant']}")
                st.markdown(f"**Headline:** {test['headline']}")
                st.markdown(f"**Primary Text:** {test['primary_text']}")
                st.markdown(f"**Success Metric:** {test['success_metric']}")

        st.divider()

        st.subheader("Reflection and Responsible Use")

        reflection_col1, reflection_col2 = st.columns(2)

        with reflection_col1:
            st.markdown("**Assumptions**")
            for item in pack["assumptions"]:
                st.markdown(f"- {item}")

            st.markdown("**Limitations**")
            for item in pack["limitations"]:
                st.markdown(f"- {item}")

        with reflection_col2:
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
