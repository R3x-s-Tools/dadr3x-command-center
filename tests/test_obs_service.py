from services.obs_service import ObsService


def test_obs_snapshot_cooldown_after_failure(monkeypatch):
    service = ObsService("bad-host", 4455, "password")
    service.retry_cooldown_seconds = 30

    def fail_connect():
        raise TimeoutError("timed out")

    monkeypatch.setattr(service, "connect", fail_connect)

    first = service.snapshot()

    assert first.connected is False
    assert "timed out" in first.error
    assert service.client is None
    assert service.next_retry_epoch > 0

    def should_not_be_called():
        raise AssertionError("connect should not be called during cooldown")

    monkeypatch.setattr(service, "connect", should_not_be_called)

    second = service.snapshot()

    assert second.connected is False
    assert "Retrying in" in second.error


def test_obs_attr_helper_reads_multiple_names():
    class Obj:
        camelCaseName = "value"

    assert ObsService._attr(Obj(), "snake_case_name", "camelCaseName") == "value"
    assert ObsService._attr(Obj(), "missing", default="fallback") == "fallback"
