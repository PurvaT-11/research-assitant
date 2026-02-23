from app.credibility import score_credibility

def test_arxiv_high_score():
    score = score_credibility("https://arxiv.org/abs/1234")
    assert score >= 0.8

def test_medium_lower_score():
    score = score_credibility("https://medium.com/article")
    assert score <= 0.5