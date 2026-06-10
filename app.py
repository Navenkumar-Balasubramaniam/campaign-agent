import streamlit as st

from config.settings import settings
from src.clients.demo_client import DemoClient
from src.clients.gemini_client import GeminiClient
from src.clients.openrouter_client import OpenRouterClient
from src.models.schemas import CampaignBrief
from src.orchestrator import CampaignOrchestrator


CAMPAIGN_PRESETS = {
    "Estrella beer mock campaign": {
        "brand": "Estrella",
        "campaign_trigger": (
            "The sun is out so we want people to go to beer gardens or the park "
            "and enjoy a nice cold beer."
        ),
        "product": "Mediterranean-style beer",
        "audience": "adults aged 18-24 who enjoy social nights out",
        "goal_index": 0,
        "budget": 1000,
        "channel_index": 0,
        "tone": "Fun, party, good vibes",
        "duration_days": 14,
        "cta": "Shop Now",
    },
    "Custom campaign": {
        "brand": "Custom Brand",
        "campaign_trigger": "A social moment that should trigger a campaign.",
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

    campaign_trigger = st.text_area(
        "Campaign Trigger",
        preset["campaign_trigger"],
        help="Describe the external moment or event the campaign should react to.",
    )

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
        ["OpenRouter", "Gemini", "Offline demo"],
        help=(
            "Choose which AI backend generates the campaign. "
            "Offline demo runs without an API key."
        ),
    )

    generate_image = st.checkbox(
        "Generate AI campaign images",
        value=False,
        disabled=generation_mode == "Offline demo",
        help=(
            "Also generate real images from the visual prompts. "
            "Not available in offline mode."
        ),
    )

    st.markdown("**Reference Images (optional)**")
    st.caption(
        "Upload reference images when the campaign is not Estrella, or to match a "
        "specific product. The AI uses them to ground the generated visuals. "
        "Leave empty to generate freely."
    )

    product_image = st.file_uploader(
        "Product picture",
        type=["png", "jpg", "jpeg", "webp"],
        accept_multiple_files=False,
        help="A photo of the actual product. The AI will match its look when generating images.",
    )

    reference_files = st.file_uploader(
        "Campaign reference images",
        type=["png", "jpg", "jpeg", "webp"],
        accept_multiple_files=True,
        help="Brand, style, or mood references to guide the generated visuals.",
    )

    submitted = st.form_submit_button("Generate Campaign Pack")


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

        if generation_mode == "Gemini":
            client = GeminiClient()
        elif generation_mode == "OpenRouter":
            client = OpenRouterClient()
        else:
            client = DemoClient()

        orchestrator = CampaignOrchestrator(client)

        # Collect any uploaded references (product photo first, then the rest)
        # so image generation can match the real product/brand.
        uploaded_refs = []
        if product_image is not None:
            uploaded_refs.append((product_image, "Product reference"))
        for f in reference_files or []:
            uploaded_refs.append((f, "Campaign reference"))

        reference_images = [
            {"data": f.getvalue(), "mime_type": f.type or "image/png"}
            for f, _ in uploaded_refs
        ]

        with st.spinner("Generating campaign pack..."):
            result = orchestrator.run(
                brief,
                generate_image=generate_image,
                reference_images=reference_images or None,
            )

        pack = result["campaign_pack"]

        st.success("Campaign pack generated successfully.")

        st.divider()

        st.header("Campaign Pack")

        st.subheader("Executive Recommendation")
        st.write(pack["recommendation_note"])

        classification = pack.get("trigger_classification", {})
        decision = pack.get("decision", {})

        st.subheader("Trigger Classification")
        st.caption(
            f"Method: {classification.get('method', 'n/a')} · "
            f"Decision method: {decision.get('method', 'n/a')}"
        )
        cls1, cls2 = st.columns(2)
        with cls1:
            st.markdown(f"**Season:** {classification.get('season', '-')}")
            st.markdown(f"**Urgency:** {classification.get('urgency', '-')}")
            st.markdown(f"**Suggested Angle:** {classification.get('suggested_angle', '-')}")
        with cls2:
            st.markdown(f"**Themes:** {', '.join(classification.get('themes', [])) or '-'}")
            st.markdown(f"**Risk Flags:** {', '.join(classification.get('risk_flags', [])) or 'none'}")
        if classification.get("rationale"):
            st.caption(classification["rationale"])

        st.subheader("Data-Backed Decision")
        if decision.get("recommended_angle"):
            st.markdown(f"**Recommended Angle:** {decision['recommended_angle']}")
        st.markdown(f"**Primary Metric:** {decision.get('primary_metric', '-')}")
        st.markdown(f"**Confidence:** {decision.get('confidence', '-')}")
        if decision.get("historical_evidence"):
            st.markdown(f"**Historical Evidence:** {decision['historical_evidence']}")
        if decision.get("budget_tilt"):
            st.markdown(f"**Budget Tilt:** {decision['budget_tilt']}")
        expected = decision.get("expected_performance", {})
        if expected:
            st.markdown("**Expected Performance (from comparable past campaigns):**")
            st.markdown(
                f"- CTR: {expected.get('ctr_pct', '-')}%  ·  "
                f"CPA: {expected.get('cpa', '-')}  ·  "
                f"Conv. rate: {expected.get('conversion_rate_pct', '-')}%  ·  "
                f"ROAS: {expected.get('roas', '-')}"
            )

        grounded = pack.get("grounded_campaigns", [])
        if grounded:
            st.subheader("Learning From Past Campaigns")
            st.caption("Most relevant past campaigns the agent grounded this plan on.")
            for c in grounded:
                with st.container(border=True):
                    st.markdown(
                        f"**{c.get('name')} ({c.get('year')})** — angle: {c.get('angle')}"
                    )
                    r = c.get("results_summary", {})
                    st.caption(
                        f"CTR {r.get('ctr', '-')}% · CPA {r.get('cpa', '-')} · "
                        f"Conv. {r.get('conversion_rate', '-')}% · ROAS {r.get('roas', '-')} "
                        f"· match score {c.get('match_score', '-')}"
                    )
                    if r.get("note"):
                        st.write(r["note"])

        benchmarks_by_angle = pack.get("historical_benchmarks", {})
        if benchmarks_by_angle:
            st.subheader("Historical Performance by Creative Angle")
            table = [
                {
                    "Angle": angle,
                    "CTR %": m.get("ctr"),
                    "CPC": m.get("cpc"),
                    "CPA": m.get("cpa"),
                    "Conv. %": m.get("conversion_rate"),
                    "ROAS": m.get("roas"),
                    "Variants": m.get("variants"),
                }
                for angle, m in benchmarks_by_angle.items()
            ]
            st.dataframe(table, use_container_width=True, hide_index=True)

        st.subheader("Campaign Strategy")
        strategy = pack["campaign_strategy"]
        brand_profile = strategy["brand_profile"]
        st.markdown(f"**Campaign Name:** {strategy['campaign_name']}")
        st.markdown(f"**Trigger:** {strategy['trigger']}")
        st.markdown(f"**Objective:** {strategy['objective']}")
        st.markdown(f"**Target Insight:** {strategy['target_insight']}")
        st.markdown(f"**Positioning:** {strategy['positioning']}")
        if strategy.get("historical_insight"):
            st.markdown(f"**Historical Insight:** {strategy['historical_insight']}")
        if strategy.get("grounded_on"):
            st.caption("Grounded on: " + ", ".join(p for p in strategy["grounded_on"] if p))

        st.markdown("**Brand Alignment**")
        st.markdown(f"**Brand Context:** {brand_profile['brand_context']}")
        st.markdown(f"**Tone:** {brand_profile['tone']}")
        st.markdown(f"**Mission:** {brand_profile['mission']}")

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
                st.markdown(f"**{item.get('step', 'Step')}**")
                evidence = item.get("evidence") or item.get("input_signal", "")
                st.markdown(f"**Evidence:** {evidence}")
                st.markdown(f"**Decision:** {item.get('decision', '')}")

        st.subheader("Campaign Brief")
        brief_summary = pack["brief_summary"]

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"**Brand:** {brief_summary['brand']}")
            st.markdown(f"**Trigger:** {brief_summary['campaign_trigger']}")
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
        image_errors = pack.get("generated_image_errors", [])

        if image_urls:
            cols = st.columns(3)

            for i, image_url in enumerate(image_urls):
                with cols[i % 3]:
                    st.image(
                        image_url,
                        caption=f"Poster Concept {i + 1}",
                        use_container_width=True,
                    )
        elif not generate_image:
            if generation_mode == "Offline demo":
                st.info("Offline mode uses visual prompts and mock creatives instead of generated images.")
            else:
                st.info("AI image generation was not selected. Tick the checkbox to generate images.")

        if image_errors:
            st.warning(
                "Some images could not be generated (often a safety refusal for "
                "alcohol creative). Text and mock creatives are unaffected."
            )
            for err in image_errors:
                st.caption(err)

        # Mock creatives are a fallback visual. Only show them when no
        # real AI images were generated, so they don't clutter the AI output.
        if not image_urls:
            st.subheader("Mock Creative Assets (offline draft layouts)")
            mockup_assets = pack["mockup_assets"]
            st.caption(mockup_assets["generation_note"])

            mockup_cols = st.columns(3)
            for i, asset in enumerate(mockup_assets["assets"]):
                with mockup_cols[i % 3]:
                    with st.container(border=True):
                        st.image(asset["image_data_url"], caption=asset["format"], use_container_width=True)
                        st.markdown(f"**Variant {asset['variant']}: {asset['headline']}**")
                        st.write(asset["body"])
                        st.caption(asset["design_notes"])

        st.divider()

        st.subheader("Visual Strategy Notes")

        image_prompts = pack["visual_concepts"]["image_prompts"]

        for i, prompt in enumerate(image_prompts, start=1):
            with st.expander(f"Visual Concept {i} Prompt"):
                st.write(prompt)

        if uploaded_refs:
            st.subheader("Reference Images")
            st.caption(
                "Uploaded references used to ground the generated visuals."
            )
            ref_cols = st.columns(3)
            for i, (f, label) in enumerate(uploaded_refs):
                with ref_cols[i % 3]:
                    with st.container(border=True):
                        st.image(f.getvalue(), use_container_width=True)
                        st.markdown(f"**{label}**")
                        st.caption(f.name)

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
                if test.get("mockup_asset"):
                    st.markdown(f"**Mockup Asset:** {test['mockup_asset']}")
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
