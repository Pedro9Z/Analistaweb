from services.scoring_service import compute_score


def test_compute_score():
    results = {
        'blacklists': {'google_safe_browsing': 'listed'},
        'redirect': {'history': [301]},
        'tls': {'error': 'expired'},
    }
    assert compute_score(results) == 85


def test_compute_score_clean():
    results = {
        'blacklists': {'google_safe_browsing': 'clean'},
        'redirect': {'history': []},
        'tls': {},
        'dns': {'SPF': 'v=spf1 ...'},
    }
    assert compute_score(results) == 0
