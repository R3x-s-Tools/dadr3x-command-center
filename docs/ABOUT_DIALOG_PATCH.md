# About Dialog Patch

This patch adds version metadata.

## Add import to `ui/main_window.py`

```python
from core.version import __app_name__, __release_name__, __version__
```

## Add button to controls

In the controls button list, add:

```python
("About", self._about),
```

## Add method to `MainWindow`

```python
def _about(self):
    QMessageBox.information(
        self,
        "About DadR3x Command Center",
        (
            f"{__app_name__}\n\n"
            f"Version: v{__version__}\n"
            f"Release: {__release_name__}\n\n"
            "An AI-powered stream producer dashboard for OBS, Twitch, "
            "viewer analytics, and creator coaching."
        ),
    )
```

## Optional

Later we can add Git commit hash and build timestamp automatically from GitHub Actions.
