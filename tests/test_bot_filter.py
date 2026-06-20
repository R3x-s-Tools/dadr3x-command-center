from analytics.bot_filter import filter_human_chat, is_bot


def test_known_bots_are_detected():
    assert is_bot("streamelements")
    assert is_bot("WizeBot")
    assert is_bot("stream_pops")
    assert is_bot("dad_r3x")


def test_human_user_is_not_bot():
    assert not is_bot("real_viewer_123")


def test_filter_human_chat_removes_bots():
    chat = [
        {"username": "streamelements", "message": "automated message"},
        {"username": "real_viewer", "message": "hello"},
        {"username": "wizebot", "message": "live online"},
    ]

    filtered = filter_human_chat(chat)

    assert len(filtered) == 1
    assert filtered[0]["username"] == "real_viewer"
