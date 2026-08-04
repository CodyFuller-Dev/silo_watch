import pytest

import weather_service


def test_take_humidity_returns_humidity(monkeypatch):
    monkeypatch.setenv("OPENWEATHER_API_KEY", "test-key")

    class DummyResponse:
        def json(self):
            return {"main": {"humidity": 63}}

    def fake_get(url):
        assert "Charleston,IL,US" in url
        assert "appid=test-key" in url
        return DummyResponse()

    monkeypatch.setattr(weather_service.requests, "get", fake_get)

    assert weather_service.take_humidity("Charleston,IL,US") == 63


def test_take_humidity_requires_api_key(monkeypatch):
    monkeypatch.delenv("OPENWEATHER_API_KEY", raising=False)

    with pytest.raises(ValueError, match="OPENWEATHER_API_KEY environment variable not set."):
        weather_service.take_humidity("Charleston,IL,US")
