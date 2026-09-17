from app import app

def test_health_route_exists():
    assert "/health" in [rule.rule for rule in app.url_map.iter_rules()]

def test_index_route_exists():
    assert "/" in [rule.rule for rule in app.url_map.iter_rules()]
