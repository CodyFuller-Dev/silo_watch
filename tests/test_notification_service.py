import notification_service


def test_send_notification_returns_without_credentials(monkeypatch):
    monkeypatch.delenv("MY_GMAIL", raising=False)
    monkeypatch.delenv("GMAIL_PASS", raising=False)

    assert notification_service.send_notification(72) is None


def test_send_notification_sends_email(monkeypatch):
    monkeypatch.setenv("MY_GMAIL", "sender@example.com")
    monkeypatch.setenv("GMAIL_PASS", "secret")

    calls = {}

    class FakeSMTP:
        def __init__(self, host, port):
            calls["host"] = host
            calls["port"] = port

        def starttls(self, context=None):
            calls["starttls"] = context

        def login(self, sender_email, password):
            calls["login"] = (sender_email, password)

        def sendmail(self, sender_email, receiver_email, message):
            calls["sendmail"] = (sender_email, receiver_email, message)

        def quit(self):
            calls["quit"] = True

    monkeypatch.setattr(notification_service.smtplib, "SMTP", FakeSMTP)
    monkeypatch.setattr(notification_service.ssl, "create_default_context", lambda: "ssl-context")

    notification_service.send_notification(88)

    assert calls["host"] == "smtp.gmail.com"
    assert calls["port"] == 587
    assert calls["starttls"] == "ssl-context"
    assert calls["login"] == ("sender@example.com", "secret")
    assert calls["sendmail"][0] == "sender@example.com"
    assert calls["sendmail"][1] == "sender@example.com"
    assert "88%" in calls["sendmail"][2]
    assert calls["quit"] is True
