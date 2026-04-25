CREATE SCHEMA IF NOT EXISTS ids_ai;

CREATE TABLE IF NOT EXISTS ids_ai.predictions_log (
  id BIGSERIAL PRIMARY KEY,
  ts_utc TIMESTAMPTZ NOT NULL,
  payload_json JSONB NOT NULL,
  prediction TEXT NOT NULL,
  probabilities_json JSONB NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_predictions_log_ts ON ids_ai.predictions_log (ts_utc DESC);

CREATE OR REPLACE VIEW ids_ai.v_attacks_per_hour AS
SELECT
  date_trunc('hour', ts_utc) AS hour_utc,
  prediction,
  COUNT(*) AS total
FROM ids_ai.predictions_log
GROUP BY 1, 2
ORDER BY 1 DESC;
