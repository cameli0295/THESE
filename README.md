# Projet complet — Détection d'intrusions réseau (CICIDS2017)

Ce dépôt contient une implémentation **de bout en bout** pour ton projet de thèse:
- ingestion du dataset CICIDS2017,
- préparation et nettoyage des données,
- entraînement de plusieurs modèles supervisés,
- évaluation des performances,
- export du modèle choisi,
- API + application web Flask pour la prédiction,
- schéma SQL et journalisation des prédictions.

## 1) Prérequis
- Python 3.10+
- `pip`
- (Optionnel) PostgreSQL si tu veux stocker les logs dans une vraie base SQL

## 2) Installation
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 3) Télécharger le dataset
Source fournie:
`http://205.174.165.80/CICDataset/CIC-IDS-2017/Dataset/CIC-IDS-2017/CSVs/MachineLearningCSV.zip`

```bash
python scripts/download_dataset.py
```

Les fichiers sont extraits dans `data/raw/MachineLearningCVE/`.

## 4) Préparer les données
```bash
python scripts/prepare_data.py
```
Sorties:
- `data/processed/train.csv`
- `data/processed/test.csv`
- `models/preprocessor.joblib`

## 5) Entraîner les modèles
```bash
python scripts/train_model.py
```
Sorties:
- `models/model.joblib` (meilleur modèle)
- `models/label_encoder.joblib`
- `models/metrics.json`

## 6) Évaluer et afficher un rapport
```bash
python scripts/evaluate_model.py
```

## 7) Base SQL (optionnel)
Créer les tables:
```bash
psql "$DATABASE_URL" -f sql/schema.sql
```

Exemple `DATABASE_URL`:
```bash
export DATABASE_URL="postgresql+psycopg2://user:password@localhost:5432/ids_ai"
```

## 8) Lancer l'application web (front + back)
```bash
export FLASK_ENV=development
python app/app.py
```

- Interface web: http://127.0.0.1:5000/
- Healthcheck API: http://127.0.0.1:5000/health
- Endpoint prédiction: `POST /predict`

## 9) Structure du projet
```text
app/
  app.py
  templates/index.html
scripts/
  download_dataset.py
  prepare_data.py
  train_model.py
  evaluate_model.py
src/cicids_project/
  config.py
  io_utils.py
  data_pipeline.py
  modeling.py
  predict.py
sql/
  schema.sql
data/
  raw/
  processed/
models/
```

## 10) Identifiants de test
Aucun compte requis pour la version locale.

## 11) Notes importantes
- Le dataset CICIDS2017 peut être volumineux : prévoir de la RAM/disque.
- Les performances finales dépendent de ton environnement et du nettoyage.
- Tu peux facilement adapter le pipeline en binaire (`BENIGN` vs `ATTACK`) ou multiclasse.
