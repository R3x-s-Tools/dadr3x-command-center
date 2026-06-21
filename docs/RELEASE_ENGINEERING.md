# v0.2.1 Release Engineering

This release uses the real repo layout:

```text
DadR3xCommandCenter.spec
build/scripts/build_mac.sh
build/scripts/build_windows.ps1
build/scripts/build_source_zip.py
.github/workflows/release.yml
```

## Local test

### Source ZIP

```bash
python build/scripts/build_source_zip.py --version local
```

### macOS app

```bash
bash build/scripts/build_mac.sh local
```

This builds for your current Mac architecture.

If you are on Apple Silicon, it builds Apple Silicon.
If you are on Intel, it builds Intel.

## GitHub release builds

The patch includes the workflow as:

```text
COPY_THIS_TO_.github_workflows/release.yml
```

Copy it to:

```text
.github/workflows/release.yml
```

## Release tags

After merging to main:

```bash
git checkout main
git pull origin main
git tag -a v0.2.1 -m "Release engineering pipeline"
git push origin v0.2.1
```

GitHub should build:

```text
Source ZIP
Windows ZIP
macOS Apple Silicon ZIP
macOS Intel ZIP
```

## macOS unsupported app warning

If macOS says the app is unsupported, you probably downloaded the wrong architecture.

Use:

- Apple Silicon build for M1/M2/M3/M4
- Intel build for older Intel Macs

Until the app is signed/notarized, macOS may also require:

```text
Right-click app → Open
```
