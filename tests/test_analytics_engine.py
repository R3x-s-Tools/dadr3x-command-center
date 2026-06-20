from analytics.engine import AnalyticsEngine


def test_contextual_moment_detects_raid_context():
    engine = AnalyticsEngine(chat_window_seconds=180)

    events = [
        {
            "timestamp_epoch": 1000,
            "stream_time": "00:10:00",
            "event_type": "viewer_spike",
            "score": 8,
            "reason": "Viewer count increased by 5, now 7.",
            "details": {"delta": 5, "viewer_count": 7},
        }
    ]

    chat = [
        {
            "timestamp_epoch": 1010,
            "stream_time": "00:10:10",
            "username": "cowboy_chuck",
            "message": "Squad family inbound for you sir",
        }
    ]

    moments = engine.build_contextual_moments(events, chat, [])

    assert len(moments) == 1
    assert "community support" in moments[0]["likely_cause"].lower()
    assert moments[0]["score"] == 10


def test_viewer_drop_score_is_capped():
    engine = AnalyticsEngine()

    events = [
        {
            "timestamp_epoch": 1000,
            "stream_time": "00:10:00",
            "event_type": "viewer_drop",
            "score": 8,
            "reason": "Viewer count dropped.",
            "details": {},
        }
    ]

    moments = engine.build_contextual_moments(events, [], [])

    assert moments[0]["score"] <= 6
