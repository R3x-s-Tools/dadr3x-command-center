# Dad_R3x Command Center Pro v0.2.1

## Release Engineering Pipeline

This release focuses on packaging, builds, and release automation.

## Added

- Local macOS build script
- Local Windows build script
- Clean source ZIP script
- GitHub release workflow
- PyInstaller release spec updates
- SHA256 checksum generation
- Release checklist
- Roadmap
- GitHub issue templates
- Pull request template
- Release engineering documentation
- Version metadata file

## Changed

- Release process now uses version tags
- Release artifacts are generated from clean build scripts
- Build outputs are separated from source files
- Source ZIP excludes secrets, logs, virtual environments, reports, and cache files

## Fixed

- Build script no longer deletes `build/scripts`
- PyInstaller spec path now matches the real repo layout
- Local macOS app build verified
- Source ZIP build verified

## Notes

macOS builds are not signed or notarized yet. Users may need to right-click the app and select **Open**.

Apple Silicon and Intel Mac builds are separate.
