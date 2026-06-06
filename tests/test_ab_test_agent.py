from src.agents.ab_test_agent import ABTestAgent


def test_ab_test_matrix_has_expected_variants():
    copy_variants = {
        "headlines": ["Headline A", "Headline B"],
        "primary_texts": ["Text A", "Text B"],
        "ctas": ["Shop Now", "Learn More"],
    }

    visual_prompts = ["Prompt A", "Prompt B"]

    result = ABTestAgent().generate(copy_variants, visual_prompts)

    assert "tests" in result
    assert len(result["tests"]) == 4
    assert result["tests"][0]["variant"] == "A"