from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[2]
DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"
MODELS_DIR = ROOT / "models"

DATASET_URL = (
    "http://205.174.165.80/CICDataset/CIC-IDS-2017/"
    "Dataset/CIC-IDS-2017/CSVs/MachineLearningCSV.zip"
)
DATASET_ZIP = DATA_RAW / "MachineLearningCSV.zip"
DATASET_EXTRACTED_DIR = DATA_RAW / "MachineLearningCVE"

TRAIN_PATH = DATA_PROCESSED / "train.csv"
TEST_PATH = DATA_PROCESSED / "test.csv"

PREPROCESSOR_PATH = MODELS_DIR / "preprocessor.joblib"
MODEL_PATH = MODELS_DIR / "model.joblib"
LABEL_ENCODER_PATH = MODELS_DIR / "label_encoder.joblib"
METRICS_PATH = MODELS_DIR / "metrics.json"

DATABASE_URL = os.getenv("DATABASE_URL", "")
