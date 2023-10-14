from pathlib import Path

#
# Paths
#

TRAK_FOLDER = Path.home() / ".trak"

DB_FILE_PATH = TRAK_FOLDER / "db.json"
DEV_DB_FILE_PATH = TRAK_FOLDER / "dev_db.json"
CONFIG_FILE_PATH = TRAK_FOLDER / "config.json"


#
# Configuration helpers
#


def init_config(p: Path) -> int:
    """Init the config file."""

    try:
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open("w", encoding="utf-8") as f:
            f.write("{}")
        return 0
    except OSError:
        return 1
