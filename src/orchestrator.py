from src.agents.copy_agent import CopyAgent
from src.agents.visual_agent import VisualAgent
from src.agents.budget_agent import BudgetAgent
from src.agents.ab_test_agent import ABTestAgent
from src.agents.report_agent import ReportAgent
from src.agents.strategy_agent import StrategyAgent
from src.agents.asset_agent import AssetAgent
from src.agents.mockup_agent import MockupAgent
from src.agents.classifier_agent import ClassifierAgent
from src.agents.decision_agent import DecisionAgent
from src.knowledge.campaign_store import CampaignStore
from src.knowledge.benchmarks import Benchmarks
from config.settings import settings


class CampaignOrchestrator:
    def __init__(self, client):
        self.client = client
        self.classifier_agent = ClassifierAgent(client)
        self.decision_agent = DecisionAgent(client)
        self.strategy_agent = StrategyAgent(client)
        self.copy_agent = CopyAgent(client)
        self.visual_agent = VisualAgent()
        self.budget_agent = BudgetAgent()
        self.ab_test_agent = ABTestAgent()
        self.report_agent = ReportAgent()
        self.asset_agent = AssetAgent()
        self.mockup_agent = MockupAgent()

    def run(self, brief, generate_image=False, reference_images=None):
        # 1. Load the brand knowledge base (past campaigns + results).
        store = CampaignStore(brand=brief.brand)
        benchmarks = Benchmarks(brand=brief.brand)

        # 2. Classify the free-text trigger into structured tags.
        classification = self.classifier_agent.classify(brief)

        # 3. Retrieve the most relevant past campaigns to ground the new one.
        retrieved = []
        if store.is_available():
            retrieved = store.retrieve(
                themes=classification.get("themes"),
                season=classification.get("season"),
                channel=brief.channel,
                goal=brief.goal,
                query=brief.campaign_trigger,
                k=3,
            )

        # 4. Use historical results to make the core decision.
        decision = self.decision_agent.generate(
            brief, classification, benchmarks, retrieved
        )

        context = {
            "classification": classification,
            "retrieved": retrieved,
            "brand_guidelines": store.brand_guidelines,
            "recommended_angle": decision.get("recommended_angle"),
        }

        # 5. Generate the grounded campaign assets.
        strategy = self.strategy_agent.generate(brief, context)
        copy = self.copy_agent.generate(brief, context)
        visuals = self.visual_agent.generate_prompts(brief)
        budget = self.budget_agent.generate(brief)
        mock_assets = self.asset_agent.generate(brief)
        mockups = self.mockup_agent.generate(brief, copy, strategy)
        ab_tests = self.ab_test_agent.generate(
            copy,
            visuals["image_prompts"],
            mockups["assets"],
        )

        # Image generation is opt-in and paid. A failure on one image (e.g. a
        # safety refusal or quota blip) must not break the rest of the pack.
        image_urls = []
        image_errors = []
        if generate_image:
            prompts = visuals["image_prompts"][: settings.MAX_IMAGES_PER_CAMPAIGN]
            for prompt in prompts:
                try:
                    image_urls.append(
                        self.client.generate_image(
                            prompt, reference_images=reference_images
                        )
                    )
                except Exception as e:
                    image_errors.append(str(e))

        # 6. Assemble the campaign pack.
        return self.report_agent.generate(
            brief_summary=brief.brief_summary(),
            copy=copy,
            visuals=visuals,
            budget=budget,
            ab_tests=ab_tests,
            image_urls=image_urls,
            image_errors=image_errors,
            strategy=strategy,
            mock_assets=mock_assets,
            mockups=mockups,
            classification=classification,
            retrieved=retrieved,
            decision=decision,
            benchmarks=benchmarks,
        )
