from src.knowledge.benchmarks import Benchmarks


def test_benchmarks_load_and_aggregate():
    bench = Benchmarks(brand="Estrella")
    assert bench.is_available()
    by_angle = bench.by_angle()
    assert "product-led" in by_angle
    assert "emotional-narrative" in by_angle
    assert by_angle["product-led"]["variants"] >= 1


def test_sales_goal_favours_product_led_by_roas():
    bench = Benchmarks(brand="Estrella")
    angle, metrics, metric = bench.best_angle_for_goal("Sales")
    assert metric == "roas"
    assert angle == "product-led"
    # Product-led should out-convert the purpose angle on ROAS.
    by_angle = bench.by_angle()
    assert by_angle["product-led"]["roas"] > by_angle["purpose-sustainability"]["roas"]


def test_awareness_goal_uses_ctr():
    bench = Benchmarks(brand="Estrella")
    _, _, metric = bench.best_angle_for_goal("Awareness")
    assert metric == "ctr"


def test_missing_results_file_is_safe():
    bench = Benchmarks(brand="NoSuchBrand")
    assert not bench.is_available()
    assert bench.by_angle() == {}
