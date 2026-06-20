from analytics.logger import StreamLogger


class FakeMessage:
    def __init__(self, username, message, timestamp):
        self.username = username
        self.message = message
        self.timestamp = timestamp


class FakeObsSnapshot:
    connected = True
    streaming = True
    recording = False
    current_scene = "Main"
    fps = 60.0
    cpu_usage = 8.5
    memory_usage_mb = 900.0
    render_lag_percent = 0.0
    encoding_lag_percent = 0.0
    error = ""


def test_stream_logger_summary_filters_bots(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    logger = StreamLogger()
    logger.add_chat(
        [
            FakeMessage("stream_pops", "bot message", logger.started_at + 1),
            FakeMessage("real_viewer", "hello there", logger.started_at + 2),
        ]
    )

    summary = logger.summary()

    assert summary["total_chat_messages"] == 1
    assert summary["unique_chatters"] == 1
    assert summary["bot_chat_messages"] == 1
    assert summary["top_viewers"][0]["username"] == "real_viewer"


def test_stream_logger_detects_viewer_spike_and_drop(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    logger = StreamLogger()

    base = {
        "timestamp_epoch": logger.started_at + 1,
        "stream_time": "00:00:01",
        "connected": True,
        "live": True,
        "viewer_count": 1,
        "game_name": "Squad",
    }

    logger.add_twitch_snapshot(dict(base))

    # Force event cooldown to allow immediate detection in test.
    logger._last_viewer_event = 0
    logger.add_twitch_snapshot(dict(base, viewer_count=4))

    assert any(event.event_type == "viewer_spike" for event in logger.events)

    logger._last_viewer_event = 0
    logger.add_twitch_snapshot(dict(base, viewer_count=1))

    assert any(event.event_type == "viewer_drop" for event in logger.events)


def test_stream_logger_adds_obs_sample(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    logger = StreamLogger()
    logger.add_obs(FakeObsSnapshot())

    assert len(logger.obs_samples) == 1
    assert logger.obs_samples[0]["connected"] is True
    assert logger.obs_samples[0]["scene"] == "Main"
