from __future__ import annotations

import urllib.request
import zipfile

from pathlib import Path

from src.cicids_project.config import DATA_RAW, DATASET_EXTRACTED_DIR, DATASET_URL, DATASET_ZIP
from src.cicids_project.io_utils import ensure_dir


def main() -> None:
    ensure_dir(DATA_RAW)

    if not DATASET_ZIP.exists():
        print(f"Téléchargement du dataset depuis: {DATASET_URL}")
        urllib.request.urlretrieve(DATASET_URL, DATASET_ZIP)
    else:
        print(f"Archive déjà présente: {DATASET_ZIP}")

    ensure_dir(DATASET_EXTRACTED_DIR)
    with zipfile.ZipFile(DATASET_ZIP, "r") as zf:
        zf.extractall(DATASET_EXTRACTED_DIR)

    csv_count = len(list(Path(DATASET_EXTRACTED_DIR).glob("*.csv")))
    print(f"Extraction terminée dans {DATASET_EXTRACTED_DIR} ({csv_count} CSV détectés)")


if __name__ == "__main__":
    main()
