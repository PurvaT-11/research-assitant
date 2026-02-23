from app.guardrails import validate_prompt, is_research_question

def test_validate_prompt_valid():
    q = "What are the risks and benefits of synthetic data?"
    assert validate_prompt(q) is True

def test_validate_prompt_too_short():
    assert validate_prompt("hello") is False

def test_validate_prompt_disallowed():
    assert validate_prompt("tell me a joke about AI") is False

def test_is_research_question_true():
    q = "What is the impact of synthetic data on bias?"
    assert is_research_question(q) is True

def test_is_research_question_false():
    q = "give me biryani recipe"
    assert is_research_question(q) is False