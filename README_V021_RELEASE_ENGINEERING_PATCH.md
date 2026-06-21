# v0.2.1 Release Engineering Patch

Copy these files into your repo:

```text
build/pyinstaller/DadR3xCommandCenter.spec
build/scripts/build_mac.sh
build/scripts/build_windows.ps1
build/scripts/build_source_zip.py
COPY_THIS_TO_.github_workflows/release.yml
docs/RELEASE_ENGINEERING.md
```

Then put the workflow in the correct GitHub path:

```bash
mkdir -p .github/workflows
cp COPY_THIS_TO_.github_workflows/release.yml .github/workflows/release.yml
chmod +x build/scripts/build_mac.sh
```

## Test source ZIP locally

```bash
python build/scripts/build_source_zip.py --version local
```

## Test Mac build locally

```bash
bash build/scripts/build_mac.sh local
```

## Commit

```bash
git checkout develop
git pull origin develop
git add .github/workflows/release.yml build/pyinstaller/DadR3xCommandCenter.spec build/scripts/build_mac.sh build/scripts/build_windows.ps1 build/scripts/build_source_zip.py docs/RELEASE_ENGINEERING.md
git commit -m "Add v0.2.1 release engineering pipeline"
git push origin develop
```

Open PR:

```text
develop -> main
```

After merge:

```bash
git checkout main
git pull origin main
git tag -a v0.2.1 -m "Release engineering pipeline"
git push origin v0.2.1
```
