from __future__ import annotations

import re
from pathlib import Path
from typing import Tuple

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, StandardScaler

from .config import DATASET_EXTRACTED_DIR


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    normalized = [re.sub(r"\s+", " ", c.strip()) for c in df.columns]
    df.columns = normalized
    return df


def load_all_csvs(dataset_dir: Path = DATASET_EXTRACTED_DIR) -> pd.DataFrame:
    csv_paths = sorted(dataset_dir.glob("*.csv"))
    if not csv_paths:
        raise FileNotFoundError(
            f"Aucun CSV trouvé dans {dataset_dir}. Lance d'abord scripts/download_dataset.py"
        )

    frames = []
    for path in csv_paths:
        df = pd.read_csv(path, low_memory=False)
        df = _normalize_columns(df)
        frames.append(df)

    combined = pd.concat(frames, ignore_index=True)
    return combined


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    if "Label" not in df.columns:
        # fallback if weird spacing/encoding
        label_col = [c for c in df.columns if c.lower().strip() == "label"]
        if not label_col:
            raise ValueError("Colonne Label introuvable dans le dataset.")
        df = df.rename(columns={label_col[0]: "Label"})

    df = df.replace([np.inf, -np.inf], np.nan)

    # Suppression des colonnes object inutiles sauf label
    obj_cols = [c for c in df.select_dtypes(include=["object"]).columns if c != "Label"]
    if obj_cols:
        df = df.drop(columns=obj_cols)

    # Drop colonnes avec > 40% de valeurs manquantes
    missing_ratio = df.isna().mean()
    to_drop = missing_ratio[missing_ratio > 0.40].index.tolist()
    if to_drop:
        df = df.drop(columns=to_drop)

    # Standardisation binaire: BENIGN vs ATTACK
    df["Label"] = df["Label"].astype(str)
    df["LabelBinary"] = np.where(df["Label"].str.upper() == "BENIGN", "BENIGN", "ATTACK")

    return df


def build_preprocessor(df: pd.DataFrame) -> Tuple[ColumnTransformer, list[str]]:
    feature_cols = [c for c in df.columns if c not in {"Label", "LabelBinary"}]
    numeric_cols = [c for c in feature_cols if pd.api.types.is_numeric_dtype(df[c])]

    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, numeric_cols),
        ],
        remainder="drop",
    )

    return preprocessor, numeric_cols


def split_data(df: pd.DataFrame):
    X = df.drop(columns=["Label", "LabelBinary"])
    y = df["LabelBinary"]

    return train_test_split(
        X,
        y,
        test_size=0.30,
        random_state=42,
        stratify=y,
    )


def fit_label_encoder(y_train: pd.Series) -> LabelEncoder:
    le = LabelEncoder()
    le.fit(y_train)
    return le
