from __future__ import annotations

import pandas as pd
import joblib

from src.cicids_project.config import DATA_PROCESSED, PREPROCESSOR_PATH, TEST_PATH, TRAIN_PATH
from src.cicids_project.data_pipeline import (
    build_preprocessor,
    clean_dataframe,
    load_all_csvs,
    split_data,
)
from src.cicids_project.io_utils import ensure_dir


def main() -> None:
    ensure_dir(DATA_PROCESSED)
    ensure_dir(PREPROCESSOR_PATH.parent)

    df = load_all_csvs()
    df = clean_dataframe(df)

    X_train, X_test, y_train, y_test = split_data(df)
    train = X_train.copy()
    train["target"] = y_train.values
    test = X_test.copy()
    test["target"] = y_test.values

    train.to_csv(TRAIN_PATH, index=False)
    test.to_csv(TEST_PATH, index=False)

    preprocessor, _ = build_preprocessor(df)
    preprocessor.fit(X_train)
    joblib.dump(preprocessor, PREPROCESSOR_PATH)

    print(f"Train sauvé: {TRAIN_PATH} ({len(train)} lignes)")
    print(f"Test sauvé: {TEST_PATH} ({len(test)} lignes)")
    print(f"Preprocessor sauvé: {PREPROCESSOR_PATH}")


if __name__ == "__main__":
    main()
