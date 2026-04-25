from __future__ import annotations

import json

from src.cicids_project.config import METRICS_PATH


def main() -> None:
    with open(METRICS_PATH, "r", encoding="utf-8") as f:
        metrics = json.load(f)

    print("=== Rapport de performance ===")
    for key, value in metrics.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
