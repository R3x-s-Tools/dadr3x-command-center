from ui.main_window import MainWindow


def test_should_post_ai_timeline_rules_without_qtbot(monkeypatch):
    # Bypass QMainWindow init. We only need the pure helper method.
    window = object.__new__(MainWindow)
    window.last_ai_notes_text = "same"
    window.last_ai_timeline_post = 1000
    window.ai_force_repeat_seconds = 600

    monkeypatch.setattr("ui.main_window.time.time", lambda: 1100)

    assert window._should_post_ai_timeline("", auto=True) is False
    assert window._should_post_ai_timeline("different", auto=True) is True
    assert window._should_post_ai_timeline("same", auto=True) is False
    assert window._should_post_ai_timeline("same", auto=False) is True

    monkeypatch.setattr("ui.main_window.time.time", lambda: 1701)

    assert window._should_post_ai_timeline("same", auto=True) is True
