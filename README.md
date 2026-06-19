# 🦖 Dad_R3x Command Center Pro

An AI-powered streaming command center built for creators who want deeper analytics, better production tools, and actionable insights without adding more load to their streaming PC.

Instead of simply showing numbers, Dad_R3x Command Center Pro acts like a virtual producer by monitoring OBS, Twitch, viewer engagement, chat activity, and stream health while generating intelligent recommendations in real time.

---

# Features

## 🎥 OBS Integration

* Live OBS monitoring over WebSocket
* Current scene detection
* FPS monitoring
* CPU usage
* Memory usage
* Render lag detection
* Encoding lag detection
* Stream status
* Recording status

---

## 📺 Twitch Integration

* Secure OAuth login
* Automatic access token refresh
* Live viewer count
* Stream title
* Game/category
* Followers
* Subscribers
* EventSub support
* Chat monitoring

---

## 🤖 AI Producer

During your stream the AI Producer continuously analyzes:

* Viewer trends
* Chat activity
* OBS health
* Stream events
* Highlight opportunities

Instead of generic advice, it provides real-time production suggestions such as:

* Conversation prompts
* Viewer engagement ideas
* Clip reminders
* Technical warnings
* Commentary suggestions

The AI Producer updates automatically throughout the stream.

---

## 📈 Stream Analytics

After every stream the application generates detailed analytics including:

* Average viewers
* Peak viewers
* Viewer growth
* Viewer drops
* Human chat activity
* Bot filtered engagement
* Stream score
* Context-aware highlight detection
* Clip confidence scoring

---

## 🎬 Highlight Detection

The application automatically detects moments worth reviewing.

Examples include:

* Viewer spikes
* Viewer drops
* Follow events
* Subscription events
* Bits
* Manual clip markers
* Chat spikes

Each highlight includes surrounding context to explain **why** the moment was important.

---

## 🧠 AI Stream Reports

Generate two reports after every stream.

### Highlight Report

Quick overview of:

* Best clip opportunities
* Viewer spikes
* Community events
* Recommended timestamps

### Deep Analytics Report

Comprehensive breakdown including:

* Stream score
* Viewer performance
* Engagement analysis
* AI observations
* Improvement suggestions
* Clip ideas

---

## 🛡 Bot Filtering

Common chat bots are automatically excluded from engagement analytics.

Supported by default:

* StreamElements
* Nightbot
* Wizebot
* Streamlabs
* Tangia
* SoundAlerts
* CommanderRoot
* And more

Raw logs are preserved while reports focus on genuine viewer interaction.

---

# Project Goals

This project aims to become an AI-powered streaming assistant capable of acting as a real producer during live broadcasts.

Long-term goals include:

* Live embedded stream preview
* AI Coach
* Historical stream comparisons
* Viewer retention analysis
* Stream "DNA" learning
* Automatic clip generation
* Streamer.bot integration
* Speaker.bot integration
* Discord integration
* Windows companion application
* Local AI support
* Multi-platform streaming support

---

# Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/dadr3x-command-center.git
cd dadr3x-command-center
```

Create a virtual environment:

```bash
python3.13 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Copy the example configuration:

```bash
cp .env.example .env
```

Run the application:

```bash
python app.py
```

---

# Twitch Setup

Create an application in the Twitch Developer Console.

Required Redirect URL:

```text
http://localhost:17563/callback
```

Add the following values to `.env`:

```text
TWITCH_CLIENT_ID=
TWITCH_CLIENT_SECRET=
TWITCH_REDIRECT_URI=http://localhost:17563/callback
TWITCH_CHANNEL=
```

The application automatically handles:

* OAuth login
* Access token storage
* Token refresh
* EventSub authentication

---

# OBS Setup

Enable the OBS WebSocket server.

```
OBS
→ Tools
→ WebSocket Server Settings
```

Configure:

* Enable WebSocket Server
* Port: 4455
* Authentication (recommended)

Update your `.env`:

```text
OBS_HOST=
OBS_PORT=4455
OBS_PASSWORD=
```

---

# Roadmap

## Version 0.2

* Modular architecture
* Twitch OAuth
* OBS monitoring
* AI Producer
* Analytics
* Reports

## Version 0.3

* Embedded stream preview
* Live graphs
* Timeline view
* Enhanced analytics
* AI Timeline

## Version 0.4

* Windows companion agent
* GPU monitoring
* Event Viewer integration
* Crash detection

## Version 0.5

* Streamer.bot integration
* Speaker.bot integration
* Discord integration

## Version 1.0

* AI Coach
* Historical stream learning
* Stream DNA
* Automatic clip generation
* Full production suite

---

# Contributing

Issues, suggestions, and pull requests are welcome.

If you discover a bug or have an idea for a feature, please open an issue so it can be discussed and tracked.

---

# License

This project is licensed under the MIT License.

---

# About

Created by **Dad_R3x**.

Built to help streamers spend less time managing software and more time creating great content.
