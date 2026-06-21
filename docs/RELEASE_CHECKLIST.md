# Release Checklist

Use this checklist before creating a version tag.

## 1. Code readiness

- [ ] All intended changes are committed
- [ ] Working tree is clean
- [ ] Feature branch merged into `develop`
- [ ] `develop` merged into `main` through pull request
- [ ] CI is green
- [ ] `pytest` passes locally
- [ ] `ruff check .` passes locally
- [ ] `black --check .` passes locally

## 2. Version readiness

- [ ] `core/version.py` updated
- [ ] `CHANGELOG.md` updated
- [ ] `ROADMAP.md` updated if milestone status changed
- [ ] README still accurate
- [ ] Release notes drafted

## 3. Build readiness

- [ ] Source ZIP builds locally

```bash
python build/scripts/build_source_zip.py --version local
```

- [ ] macOS build works locally

```bash
bash build/scripts/build_mac.sh local
```

- [ ] macOS app launches

```bash
open "dist/DadR3x Command Center.app"
```

- [ ] Release ZIP appears in `release/`
- [ ] SHA256 file appears in `release/`

## 4. Tag release

From `main`:

```bash
git checkout main
git pull origin main
git tag -a v0.2.1 -m "Release engineering pipeline"
git push origin v0.2.1
```

## 5. GitHub verification

- [ ] GitHub Actions release workflow starts
- [ ] Source ZIP artifact created
- [ ] Windows ZIP artifact created
- [ ] macOS Apple Silicon ZIP artifact created
- [ ] macOS Intel ZIP artifact created
- [ ] Release is created
- [ ] Assets are attached to release
- [ ] Checksums are attached to release

## 6. Post-release

- [ ] Download release artifact
- [ ] Verify ZIP opens
- [ ] Verify app launches
- [ ] Create next milestone branch
