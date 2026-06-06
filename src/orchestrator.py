from src.agents.copy_agent import CopyAgent
from src.agents.visual_agent import VisualAgent
from src.agents.budget_agent import BudgetAgent
from src.agents.ab_test_agent import ABTestAgent
from src.agents.report_agent import ReportAgent


class CampaignOrchestrator:
    def __init__(self, client):
        self.client = client
        self.copy_agent = CopyAgent(client)
        self.visual_agent = VisualAgent()
        self.budget_agent = BudgetAgent()
        self.ab_test_agent = ABTestAgent()
        self.report_agent = ReportAgent()

    def run(self, brief, generate_image=False):
        copy = self.copy_agent.generate(brief)
        visuals = self.visual_agent.generate_prompts(brief)
        budget = self.budget_agent.generate(brief)
        ab_tests = self.ab_test_agent.generate(copy, visuals["image_prompts"])

        image_urls = []

        if generate_image:
            for prompt in visuals["image_prompts"]:
                image_url = self.client.generate_image(prompt)
                image_urls.append(image_url)

        return self.report_agent.generate(
            brief_summary=brief.brief_summary(),
            copy=copy,
            visuals=visuals,
            budget=budget,
            ab_tests=ab_tests,
            image_urls=image_urls,
        )