import streamlit as st

from config.settings import settings
from src.clients.openrouter_client import OpenRouterClient
from src.models.schemas import CampaignBrief
from src.orchestrator import CampaignOrchestrator


st.set_page_config(page_title=settings.APP_NAME, layout="wide")

st.title("AI Campaign Agent Demo")
st.caption("Creative brief in. Campaign pack out.")

with st.form("campaign_brief"):
    product = st.text_input("Product", "Organic Herbal Tea")
    audience = st.text_area("Target Audience", "Women aged 25-45 interested in wellness and natural products")
    goal = st.selectbox("Campaign Goal", ["Sales", "Awareness", "Lead Generation"])
    budget = st.number_input("Budget", min_value=1, value=1000)
    channel = st.selectbox("Channel", ["Instagram", "Facebook", "Meta", "LinkedIn"])
    tone = st.text_input("Tone", "Premium, calming, wellness-focused")
    duration_days = st.number_input("Duration in Days", min_value=1, value=14)
    cta = st.text_input("CTA", "Shop Now")

    generate_image = st.checkbox("Generate 1 paid image using OpenRouter", value=False)

    submitted = st.form_submit_button("Generate Campaign Pack")

if submitted:
    try:
        brief = CampaignBrief(
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

        with st.spinner("Generating campaign pack..."):
            result = orchestrator.run(brief, generate_image=generate_image)

        pack = result["campaign_pack"]

        st.subheader("Campaign Summary")
        st.json(pack["brief_summary"])

        st.subheader("Copy Variants")
        st.json(pack["copy_variants"])

        st.subheader("Visual Concepts")
        st.json(pack["visual_concepts"])

        if pack["generated_image_url"]:
            st.subheader("Generated Poster")
            st.image(pack["generated_image_url"])

        st.subheader("Budget Plan")
        st.json(pack["budget_plan"])

        st.subheader("A/B Test Plan")
        st.json(pack["ab_test_plan"])

    except Exception as e:
        st.error(str(e))