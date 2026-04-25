from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier


@dataclass
class ModelResult:
    name: str
    accuracy: float
    f1: float
    report: dict
    pipeline: Pipeline


def candidate_models() -> dict:
    return {
        "logistic_regression": LogisticRegression(max_iter=400, n_jobs=None),
        "decision_tree": DecisionTreeClassifier(random_state=42, max_depth=18),
        "random_forest": RandomForestClassifier(
            n_estimators=250,
            random_state=42,
            n_jobs=-1,
            class_weight="balanced_subsample",
        ),
        "knn": KNeighborsClassifier(n_neighbors=7),
    }


def train_and_select_best(preprocessor, X_train, y_train, X_test, y_test) -> ModelResult:
    best: ModelResult | None = None

    for name, estimator in candidate_models().items():
        pipeline = Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("model", estimator),
            ]
        )

        pipeline.fit(X_train, y_train)
        pred = pipeline.predict(X_test)

        acc = float(accuracy_score(y_test, pred))
        f1 = float(f1_score(y_test, pred, average="weighted"))
        report = classification_report(y_test, pred, output_dict=True)

        result = ModelResult(name=name, accuracy=acc, f1=f1, report=report, pipeline=pipeline)

        if best is None or result.f1 > best.f1:
            best = result

    if best is None:
        raise RuntimeError("Aucun modèle n'a pu être entraîné.")

    return best


def summarize_metrics(result: ModelResult) -> dict:
    weighted = result.report.get("weighted avg", {})
    return {
        "best_model": result.name,
        "accuracy": result.accuracy,
        "f1_weighted": result.f1,
        "precision_weighted": float(weighted.get("precision", np.nan)),
        "recall_weighted": float(weighted.get("recall", np.nan)),
    }
