from app.planner import generate_plan

def test_generate_plan_returns_queries():
    q = "synthetic data risks"
    plan = generate_plan(q)

    assert "queries" in plan
    assert len(plan["queries"]) >= 2
    assert "peer reviewed study" in plan["queries"][0]