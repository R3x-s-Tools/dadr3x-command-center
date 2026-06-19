from __future__ import annotations

import time, webbrowser
from datetime import datetime
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QMessageBox, QSplitter, QGroupBox
)
from PySide6.QtCore import Qt

from core.config import Settings
from services.twitch_auth import TwitchAuthService
from services.twitch_chat import TwitchChatService
from services.twitch_api import TwitchApiService
from services.eventsub_service import EventSubService
from services.obs_service import ObsService, ObsSnapshot
from analytics.logger import StreamLogger
from ai.producer import AiProducer
from reports.generator import ReportGenerator

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = Settings()
        self.setWindowTitle("Dad_R3x Command Center Pro")
        self.resize(1300, 900)

        self.auth = TwitchAuthService(self.settings.twitch_client_id, self.settings.twitch_client_secret, self.settings.twitch_redirect_uri)
        self.obs = ObsService(self.settings.obs_host, self.settings.obs_port, self.settings.obs_password)
        self.logger = StreamLogger()
        self.ai = AiProducer(self.settings.ai_provider, self.settings.openai_api_key, self.settings.openai_model)
        self.reporter = ReportGenerator(self.settings.ai_provider, self.settings.openai_api_key, self.settings.openai_model)

        self.chat = None
        self.twitch_api = None
        self.eventsub = None
        self.latest_obs = ObsSnapshot()
        self.latest_twitch = None
        self.recent_chat = []
        self.last_twitch_poll = 0
        self.last_ai_refresh = 0

        self._build_ui()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(self.settings.obs_poll_seconds * 1000)

    def _build_ui(self):
        root = QWidget()
        layout = QVBoxLayout(root)
        self.setCentralWidget(root)

        title = QLabel("🦖 Dad_R3x Command Center Pro")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        layout.addWidget(self._auth_group())
        layout.addWidget(self._obs_group())
        layout.addWidget(self._twitch_group())

        splitter = QSplitter(Qt.Vertical)
        self.chat_box = self._text_panel(splitter, "Recent Twitch Chat")
        self.ai_box = self._text_panel(splitter, "AI Producer Notes")
        self.event_box = self._text_panel(splitter, "Recent Twitch Events / Highlights")
        layout.addWidget(splitter, stretch=1)

        buttons = QHBoxLayout()
        for label, handler in [
            ("Mark Clip Moment", self._manual_clip),
            ("Generate Reports", self._reports),
            ("Refresh AI Notes", self._ai_notes),
        ]:
            b = QPushButton(label)
            b.clicked.connect(handler)
            buttons.addWidget(b)
        layout.addLayout(buttons)

        self.footer = QLabel(f"Session log: {self.logger.session_file}")
        layout.addWidget(self.footer)

    def _group(self, title):
        box = QGroupBox(title)
        layout = QVBoxLayout(box)
        return box, layout

    def _auth_group(self):
        box, layout = self._group("Twitch Auth")
        row = QHBoxLayout()
        self.auth_status = QLabel("Auth: checking...")
        row.addWidget(self.auth_status, stretch=1)
        for label, handler in [
            ("Login with Twitch", self._login),
            ("Refresh Token", self._refresh_token),
            ("Start Twitch", self._start_twitch_services),
            ("Open Preview", self._open_preview),
        ]:
            b = QPushButton(label)
            b.clicked.connect(handler)
            row.addWidget(b)
        layout.addLayout(row)
        return box

    def _obs_group(self):
        box, layout = self._group("OBS Health")
        self.obs_status = QLabel("OBS: waiting...")
        self.obs_stats = QLabel("Stats: waiting...")
        layout.addWidget(self.obs_status)
        layout.addWidget(self.obs_stats)
        return box

    def _twitch_group(self):
        box, layout = self._group("Twitch Analytics")
        self.twitch_status = QLabel("Twitch: not started")
        layout.addWidget(self.twitch_status)
        return box

    def _text_panel(self, splitter, title):
        box = QGroupBox(title)
        layout = QVBoxLayout(box)
        edit = QTextEdit()
        edit.setReadOnly(True)
        layout.addWidget(edit)
        splitter.addWidget(box)
        return edit

    def _login(self):
        ok = self.auth.login_interactive()
        QMessageBox.information(self, "Twitch Login", "Login complete." if ok else f"Login failed: {self.auth.last_error}")
        self._update_auth_status()

    def _refresh_token(self):
        token = self.auth.refresh()
        QMessageBox.information(self, "Twitch Token", "Token refreshed." if token else f"Refresh failed: {self.auth.last_error}")
        self._update_auth_status()

    def _start_twitch_services(self):
        token = self.auth.ensure_access_token()
        if not token:
            QMessageBox.warning(self, "Twitch", "Login with Twitch first.")
            return
        self.chat = TwitchChatService(self.settings.twitch_channel, self.settings.twitch_channel, self.auth.oauth_token)
        self.twitch_api = TwitchApiService(self.settings.twitch_client_id, self.settings.twitch_channel, self.auth.access_token)
        self.eventsub = EventSubService(self.settings.twitch_client_id, self.settings.twitch_channel, self.auth.access_token)
        self.chat.start()
        self.eventsub.start()
        QMessageBox.information(self, "Twitch", "Twitch services started.")

    def _open_preview(self):
        webbrowser.open(f"https://www.twitch.tv/{self.settings.twitch_channel}")

    def _tick(self):
        self._update_auth_status()
        self._update_obs()
        self._update_chat()
        self._update_twitch_api()
        self._update_eventsub()
        self._auto_ai_notes()

    def _update_auth_status(self):
        self.auth.ensure_access_token()
        val = self.auth.validate()
        extra = f" | scopes: {' '.join(val.get('scopes', []))}" if val else ""
        self.auth_status.setText(f"Auth: {self.auth.status}{extra}")

    def _update_obs(self):
        self.latest_obs = self.obs.snapshot()
        live = "LIVE" if self.latest_obs.streaming else "Not streaming"
        self.obs_status.setText(f"OBS: {'Connected' if self.latest_obs.connected else 'Disconnected'} | {live} | Scene: {self.latest_obs.current_scene}")
        self.obs_stats.setText(
            f"FPS: {self.latest_obs.fps} | CPU: {self._fmt(self.latest_obs.cpu_usage)}% | "
            f"Render Lag: {self._fmt(self.latest_obs.render_lag_percent)}% | "
            f"Encoding Lag: {self._fmt(self.latest_obs.encoding_lag_percent)}%"
        )
        self.logger.add_obs(self.latest_obs)

    def _update_chat(self):
        if not self.chat:
            return
        messages = self.chat.drain()
        if messages:
            self.recent_chat.extend(messages)
            self.recent_chat = self.recent_chat[-50:]
            self.logger.add_chat(messages)
            for m in messages:
                stamp = datetime.fromtimestamp(m.timestamp).strftime("%H:%M:%S")
                self.chat_box.append(f"[{stamp}] {m.username}: {m.message}")

    def _update_twitch_api(self):
        if not self.twitch_api:
            return
        if time.time() - self.last_twitch_poll < self.settings.twitch_analytics_seconds:
            return
        self.last_twitch_poll = time.time()
        self.latest_twitch = self.twitch_api.snapshot(self.logger.stream_time())
        self.logger.add_twitch_snapshot(self.twitch_api.to_dict(self.latest_twitch))
        if self.latest_twitch.connected:
            self.twitch_status.setText(
                f"Twitch: {'LIVE' if self.latest_twitch.live else 'Offline'} | "
                f"Viewers: {self.latest_twitch.viewer_count} | Game: {self.latest_twitch.game_name} | "
                f"Followers: {self.latest_twitch.follower_total if self.latest_twitch.follower_total is not None else '?'} | "
                f"Subs: {self.latest_twitch.subscriber_total if self.latest_twitch.subscriber_total is not None else '?'}"
            )
        else:
            self.twitch_status.setText(f"Twitch API error: {self.latest_twitch.error}")

    def _update_eventsub(self):
        if not self.eventsub:
            return
        events = self.eventsub.drain()
        if events:
            dicts = [self.eventsub.to_dict(e) for e in events]
            self.logger.add_twitch_events(dicts)
            for e in events:
                stamp = datetime.fromtimestamp(e.timestamp_epoch).strftime("%H:%M:%S")
                self.event_box.append(f"[{stamp}] {e.message}")

    def _auto_ai_notes(self):
        if time.time() - self.last_ai_refresh < self.settings.ai_refresh_seconds:
            return
        self.last_ai_refresh = time.time()
        self._ai_notes()

    def _ai_notes(self):
        recent_events = self.logger.twitch_events[-10:]
        recent_highlights = [
            {"stream_time": e.stream_time, "event_type": e.event_type, "score": e.score, "reason": e.reason}
            for e in self.logger.events[-10:]
        ]
        notes = self.ai.suggest(self.latest_obs, self.recent_chat, self.latest_twitch, recent_events, recent_highlights)
        self.ai_box.setPlainText(notes)

    def _manual_clip(self):
        e = self.logger.manual_clip(self.latest_obs.current_scene)
        self.event_box.append(f"[{e.stream_time}] Manual clip marker: {self.latest_obs.current_scene}")

    def _reports(self):
        h, a = self.reporter.generate(self.logger.summary())
        QMessageBox.information(self, "Reports generated", f"Highlight report:\\n{h}\\n\\nDeep analytics report:\\n{a}")

    @staticmethod
    def _fmt(value):
        if value is None:
            return "?"
        return f"{value:.2f}" if isinstance(value, float) else str(value)
