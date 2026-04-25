from __future__ import annotations

import pandas as pd


def predict_from_payload(model_pipeline, payload: dict) -> dict:
    frame = pd.DataFrame([payload])
    pred = model_pipeline.predict(frame)[0]

    probabilities = {}
    if hasattr(model_pipeline, "predict_proba"):
        proba = model_pipeline.predict_proba(frame)[0]
        classes = model_pipeline.classes_
        probabilities = {str(cls): float(p) for cls, p in zip(classes, proba)}

    return {
        "prediction": str(pred),
        "probabilities": probabilities,
    }
