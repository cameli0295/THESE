from __future__ import annotations

from datetime import datetime, timezone
import json

import joblib
from flask import Flask, jsonify, render_template, request
from sqlalchemy import create_engine, text

from src.cicids_project.config import DATABASE_URL, LABEL_ENCODER_PATH, MODEL_PATH
from src.cicids_project.predict import predict_from_payload

app = Flask(__name__, template_folder="templates", static_folder="static")

model_pipeline = joblib.load(MODEL_PATH) if MODEL_PATH.exists() else None
label_encoder = joblib.load(LABEL_ENCODER_PATH) if LABEL_ENCODER_PATH.exists() else None

engine = create_engine(DATABASE_URL) if DATABASE_URL else None


def decode_result(result: dict) -> dict:
    if label_encoder is None:
        return result

    try:
        pred_int = int(result["prediction"])
        decoded = label_encoder.inverse_transform([pred_int])[0]
        result["prediction"] = str(decoded)

        if result.get("probabilities"):
            remapped = {}
            for k, v in result["probabilities"].items():
                decoded_k = label_encoder.inverse_transform([int(k)])[0]
                remapped[str(decoded_k)] = v
            result["probabilities"] = remapped
    except Exception:
        # If already decoded/string labels, keep as-is
        pass

    return result


def log_prediction(payload: dict, result: dict) -> None:
    if engine is None:
        return

    query = text(
        """
        INSERT INTO ids_ai.predictions_log (ts_utc, payload_json, prediction, probabilities_json)
        VALUES (:ts_utc, :payload_json, :prediction, :probabilities_json)
        """
    )

    with engine.begin() as conn:
        conn.execute(
            query,
            {
                "ts_utc": datetime.now(timezone.utc),
                "payload_json": json.dumps(payload, ensure_ascii=False),
                "prediction": result["prediction"],
                "probabilities_json": json.dumps(result.get("probabilities", {}), ensure_ascii=False),
            },
        )


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/health")
def health():
    return jsonify(
        {
            "status": "ok",
            "model_loaded": model_pipeline is not None,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        }
    )


@app.post("/predict")
def predict():
    if model_pipeline is None:
        return jsonify({"error": "Model not found. Run training first."}), 500

    payload = request.get_json(silent=True) or {}
    if not payload:
        return jsonify({"error": "Missing JSON payload."}), 400

    try:
        result = predict_from_payload(model_pipeline, payload)
        result = decode_result(result)
        log_prediction(payload, result)
        return jsonify(result)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
