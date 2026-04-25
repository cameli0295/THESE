from __future__ import annotations

import joblib
import pandas as pd

from src.cicids_project.config import (
    LABEL_ENCODER_PATH,
    METRICS_PATH,
    MODEL_PATH,
    PREPROCESSOR_PATH,
    TEST_PATH,
    TRAIN_PATH,
)
from src.cicids_project.data_pipeline import fit_label_encoder
from src.cicids_project.io_utils import save_json
from src.cicids_project.modeling import summarize_metrics, train_and_select_best


def main() -> None:
    train_df = pd.read_csv(TRAIN_PATH)
    test_df = pd.read_csv(TEST_PATH)

    X_train = train_df.drop(columns=["target"])
    y_train = train_df["target"]

    X_test = test_df.drop(columns=["target"])
    y_test = test_df["target"]

    preprocessor = joblib.load(PREPROCESSOR_PATH)

    label_encoder = fit_label_encoder(y_train)
    y_train_encoded = label_encoder.transform(y_train)
    y_test_encoded = label_encoder.transform(y_test)

    result = train_and_select_best(
        preprocessor=preprocessor,
        X_train=X_train,
        y_train=y_train_encoded,
        X_test=X_test,
        y_test=y_test_encoded,
    )

    metrics = summarize_metrics(result)
    metrics["classes"] = [str(c) for c in label_encoder.classes_]

    joblib.dump(result.pipeline, MODEL_PATH)
    joblib.dump(label_encoder, LABEL_ENCODER_PATH)
    save_json(METRICS_PATH, metrics)

    print("Modèle entraîné avec succès")
    print(f"Meilleur modèle: {metrics['best_model']}")
    print(f"Accuracy: {metrics['accuracy']:.4f}")
    print(f"F1 weighted: {metrics['f1_weighted']:.4f}")


if __name__ == "__main__":
    main()
