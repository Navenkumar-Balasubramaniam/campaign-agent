class BudgetAgent:
    def generate(self, brief):
        budget = brief.budget

        if brief.channel.lower() in ["instagram", "facebook", "meta"]:
            split = [
                {"bucket": "Prospecting", "percentage": 60, "amount": round(budget * 0.60)},
                {"bucket": "Retargeting", "percentage": 25, "amount": round(budget * 0.25)},
                {"bucket": "Creative Testing", "percentage": 15, "amount": budget - round(budget * 0.60) - round(budget * 0.25)},
            ]
        else:
            split = [
                {"bucket": "Primary Channel", "percentage": 70, "amount": round(budget * 0.70)},
                {"bucket": "Retargeting", "percentage": 20, "amount": round(budget * 0.20)},
                {"bucket": "Testing", "percentage": 10, "amount": budget - round(budget * 0.70) - round(budget * 0.20)},
            ]

        return {
            "total_budget": budget,
            "daily_budget": round(budget / brief.duration_days, 2),
            "budget_split": split,
        }