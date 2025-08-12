from level_loader import level_loader
from editor.components.overlay.message_overlay import MessageOverlay


def verify_level_issues():
    """Verifies if there are issues on the level, returning a boolean value and showing a message overlay if there are."""

    issues = level_loader.level.issues
    if len(issues) > 0:
        MessageOverlay(f"There are some issues with the level:", paragraphs=issues)
        return True
    return False
