from app.security import detect_risk_indicators


def test_urgency_indicator():
    reasons = detect_risk_indicators("Act now to verify your account immediately.")
    assert "Urgency detected" in reasons


def test_credential_indicator():
    reasons = detect_risk_indicators("Please verify your password and login.")
    assert "Credential request" in reasons


def test_suspicious_link_indicator():
    reasons = detect_risk_indicators("Click here to verify here.")
    assert "Suspicious link language" in reasons
