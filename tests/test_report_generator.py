from reports.generator import ReportGenerator


def test_report_generator_writes_files(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    generator = ReportGenerator(ai_provider="off")

    payload = {
        "stream_length": "01:00:00",
        "viewer_summary": {
            "average_viewers": 2.5,
            "peak_viewers": 5,
            "low_viewers": 1,
            "samples": 10,
        },
        "stream_score": {
            "overall": 75,
            "viewer_retention": 55,
            "chat_engagement": 80,
            "clip_potential": 90,
            "technical": 100,
        },
        "latest_twitch": {"live": True, "title": "Test", "game_name": "Squad"},
        "total_chat_messages": 5,
        "unique_chatters": 2,
        "bot_chat_messages": 3,
        "recent_twitch_events": [],
        "contextual_moments": [
            {
                "stream_time": "00:10:00",
                "event_type": "viewer_spike",
                "score": 10,
                "reason": "Viewer count increased.",
                "likely_cause": "Likely community support.",
                "human_chat_nearby": [],
            }
        ],
    }

    highlight, analytics = generator.generate(payload)

    assert highlight.exists()
    assert analytics.exists()
    assert "Dad_R3x Highlight Report" in highlight.read_text(encoding="utf-8")
    assert "Dad_R3x Deep Stream Analytics Report" in analytics.read_text(encoding="utf-8")
