# Changelog

All notable changes to Dad_R3x Command Center Pro will be documented in this file.

## v0.2.1 - Release Engineering Pipeline

### Added

- Local macOS application build script
- Local Windows application build script
- Source ZIP build script
- PyInstaller release spec
- GitHub release workflow support
- SHA256 checksum generation
- Release engineering documentation
- Application version source file

### Changed

- Release builds now use the root `DadR3xCommandCenter.spec`
- macOS builds now produce zipped `.app` artifacts
- Source ZIP excludes local secrets, virtual environments, logs, reports, and cache folders

### Fixed

- Release build path mismatch for the PyInstaller spec
- macOS app packaging workflow
- Source packaging accidentally including local development files

## v0.2.0 - Producer Console

### Added

- Producer Console UI
- Live Status panel
- High-signal moments panel
- AI Producer timeline
- Analytics tab
- Viewer memory
- Regular viewer detection
- AI suggestion throttling
- OBS reconnect cooldown
- Structured logging
- Expanded unit tests

### Changed

- Dashboard layout reorganized around live production use
- AI notes are separated from raw logs and chat
- Twitch and OBS status visibility improved

### Fixed

- Repeated AI timeline spam
- OBS connection attempts freezing the app
- Newline display issues in the UI
- Several CI formatting and test issues

## v0.1.0 - Initial Pro Build

### Added

- PySide6 desktop app
- OBS monitoring
- Twitch authentication
- Twitch chat support
- Twitch API analytics
- EventSub support
- AI Producer
- Report generation
- GitHub CI starter
