from __future__ import annotations

import time
from typing import Any

class AiProducer:
    def __init__(self, provider: str = "off", api_key: str = "", model: str = "gpt-4.1-mini"):
        self.provider = (provider or "off").lower()
        self.api_key = api_key or ""
        self.model = model or "gpt-4.1-mini"
        self.last_error = ""
        self.last_notes_time = 0

    def suggest(self, obs: Any, recent_chat: list[Any], twitch_snapshot: Any = None, recent_events: list[Any] | None = None, recent_highlights: list[Any] | None = None) -> str:
        recent_events = recent_events or []
        recent_highlights = recent_highlights or []
        if self.provider == "openai" and self.api_key:
            return self._openai_suggest(obs, recent_chat, twitch_snapshot, recent_events, recent_highlights)
        return self._rules_only(obs, recent_chat, twitch_snapshot, recent_events, recent_highlights)

    def _rules_only(self, obs: Any, recent_chat: list[Any], twitch_snapshot: Any = None, recent_events: list[Any] | None = None, recent_highlights: list[Any] | None = None) -> str:
        notes = []
        if not getattr(obs, "connected", False):
            notes.append(f"OBS is disconnected. Check WebSocket/IP/password. Error: {getattr(obs, 'error', '')}")
        else:
            render_lag = getattr(obs, "render_lag_percent", None) or 0
            encoding_lag = getattr(obs, "encoding_lag_percent", None) or 0
            if render_lag >= 3:
                notes.append(f"Render lag is high at {render_lag:.2f}%. Reduce GPU load, overlays, or in-game settings.")
            if encoding_lag >= 3:
                notes.append(f"Encoding lag is high at {encoding_lag:.2f}%. Check encoder settings, bitrate, and GPU pressure.")
            if render_lag < 3 and encoding_lag < 3:
                notes.append("OBS looks healthy. Focus on content and clip moments.")

        if twitch_snapshot and getattr(twitch_snapshot, "live", False):
            notes.append(f"Live in {getattr(twitch_snapshot, 'game_name', '')} with {getattr(twitch_snapshot, 'viewer_count', '?')} viewer(s).")

        if recent_chat:
            last = recent_chat[-1]
            notes.append(f"Latest chat from {getattr(last, 'username', 'chat')}: {getattr(last, 'message', '')}")
        else:
            notes.append("Chat is quiet. Ask: “What Squad role should I run next?”")

        if recent_events:
            ev = recent_events[-1]
            msg = ev.get("message") if isinstance(ev, dict) else getattr(ev, "message", "")
            if msg:
                notes.append(f"Recent Twitch event: {msg}. Acknowledge it naturally.")

        if recent_highlights:
            notes.append("Recent highlight marker/event detected. Review it after the match or round.")

        return "\n".join(f"🦖 {n}" for n in notes[:5])

    def _openai_suggest(self, obs, recent_chat, twitch_snapshot, recent_events, recent_highlights) -> str:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)

            chat_lines = [f"{getattr(m, 'username', 'unknown')}: {getattr(m, 'message', '')}" for m in recent_chat[-12:]]
            event_lines = []
            for e in recent_events[-10:]:
                event_lines.append(e.get("message", str(e)) if isinstance(e, dict) else getattr(e, "message", str(e)))

            obs_context = {
                "connected": getattr(obs, "connected", False),
                "streaming": getattr(obs, "streaming", False),
                "scene": getattr(obs, "current_scene", "Unknown"),
                "fps": getattr(obs, "fps", None),
                "cpu_usage": getattr(obs, "cpu_usage", None),
                "render_lag_percent": getattr(obs, "render_lag_percent", None),
                "encoding_lag_percent": getattr(obs, "encoding_lag_percent", None),
                "error": getattr(obs, "error", ""),
            }

            twitch_context = None
            if twitch_snapshot:
                twitch_context = {
                    "live": getattr(twitch_snapshot, "live", False),
                    "viewer_count": getattr(twitch_snapshot, "viewer_count", None),
                    "title": getattr(twitch_snapshot, "title", ""),
                    "game_name": getattr(twitch_snapshot, "game_name", ""),
                    "follower_total": getattr(twitch_snapshot, "follower_total", None),
                    "subscriber_total": getattr(twitch_snapshot, "subscriber_total", None),
                }

            prompt = f"""
You are the live producer for Dad_R3x, a gaming streamer. Give short, immediately useful producer notes for the next 1-5 minutes.

Rules:
- Max 4 bullets.
- Each bullet must start with 🦖.
- Be practical and specific.
- Avoid generic hype.
- If chat is quiet, suggest one exact question.
- For Squad, suggest narration, objective explanation, clip markers, or chat prompts.
- If OBS has technical trouble, prioritize that.

OBS:
{obs_context}

Twitch:
{twitch_context}

Recent chat:
{chr(10).join(chat_lines) if chat_lines else "No recent chat."}

Recent Twitch events:
{chr(10).join(event_lines) if event_lines else "No recent Twitch events."}

Recent highlight markers/events:
{recent_highlights[-10:] if recent_highlights else "No recent highlight markers."}
"""
            text = client.responses.create(model=self.model, input=prompt).output_text.strip()
            self.last_error = ""
            self.last_notes_time = time.time()
            return text or self._rules_only(obs, recent_chat, twitch_snapshot, recent_events, recent_highlights)
        except Exception as exc:
            self.last_error = str(exc)
            return self._rules_only(obs, recent_chat, twitch_snapshot, recent_events, recent_highlights) + f"\n🦖 AI note engine error: {exc}"
