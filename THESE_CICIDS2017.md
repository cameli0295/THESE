# THÈSE PROFESSIONNELLE  
## Certification RNCP 37137 — Chef de projet Data et Intelligence Artificielle

**Titre du projet :** Détection d’intrusions réseau par Intelligence Artificielle (CICIDS2017)  
**Candidat :** NOM PRÉNOM  
**Date de début du projet :** 6 janvier 2026  
**Établissement :** Nexa Digital School  
**Version :** 1.0 (base de travail complète à personnaliser)

---

## Remerciements
Je remercie l’équipe pédagogique de Nexa Digital School, mon tuteur académique, mon encadrant en entreprise ainsi que les professionnels ayant contribué aux retours techniques et méthodologiques ayant permis la réalisation de ce projet. Je remercie également les contributeurs des jeux de données open source en cybersécurité, dont CICIDS2017, qui rendent possible l’expérimentation de modèles robustes de détection d’intrusions.

---

## Résumé exécutif
Ce mémoire présente la conception et la mise en œuvre d’une solution d’**IA supervisée** dédiée à la **détection d’intrusions réseau**. Le projet repose sur le dataset **CICIDS2017**, composé de flux réseau normaux et de flux malveillants (DoS/DDoS, brute force, botnet, infiltration, port scan, web attacks, etc.). L’objectif est de construire une chaîne complète :

1. cadrage métier et stratégique ;
2. gouvernance projet (agile, planning, budget, risques) ;
3. préparation des données et ingénierie des features ;
4. entraînement, comparaison et optimisation de modèles supervisés ;
5. déploiement d’une application web de détection en quasi temps réel ;
6. prise en compte des enjeux réglementaires, éthiques, sécurité et accessibilité.

La solution retenue combine un pipeline de prétraitement robuste et un modèle de classification optimisé (Random Forest/XGBoost selon scénario), exposé via une API (Flask/FastAPI) et consommé par une interface web (Dash/Flask templates). Les indicateurs de performance incluent Accuracy, Precision, Recall, F1-score, courbe ROC-AUC, latence d’inférence et performance SQL (tables optimisées/non optimisées).

Le projet démontre qu’une architecture pragmatique et bien gouvernée permet d’atteindre un niveau de détection utile en contexte opérationnel, tout en intégrant les exigences de conformité (RGPD), de résilience, et de communication auprès des parties prenantes techniques et métier.

---

## Sommaire
1. Présentation de l’entreprise et contexte  
2. Étude de marché et analyse concurrentielle  
3. Problématique et définition du besoin  
4. Gestion de projet  
5. Exploitation des données  
6. Développement de l’application IA  
7. Conclusion et perspectives  
8. Bibliographie indicative  
9. Annexes (à intégrer dans le PDF final)

---

## 1) Présentation de l’entreprise et contexte

### 1.1 Storytelling (histoire de l’entreprise)
L’entreprise d’accueil est une société de services numériques (ESN) intervenant auprès de PME et ETI françaises dans la modernisation de leur SI. Historiquement orientée infrastructure et support, elle a progressivement structuré un pôle cybersécurité afin de répondre à l’augmentation des incidents de sécurité et à l’exigence croissante de conformité.  
Dans cette dynamique, la direction souhaite industrialiser une capacité de détection des comportements réseau anormaux, en complément des outils SIEM existants, afin de réduire le temps de détection (MTTD) et le temps de réponse (MTTR).

### 1.2 Valeurs et missions
- **Fiabilité** : garantir la continuité des services clients.  
- **Transparence** : expliciter les choix techniques et les niveaux de risque.  
- **Amélioration continue** : intégrer des mécanismes de feedback et de veille.  
- **Responsabilité** : gérer les données de sécurité dans le respect du cadre légal et éthique.

### 1.3 Activité principale
- Infogérance et supervision d’infrastructures hybrides.  
- Intégration de solutions de cybersécurité (EDR, SIEM, IAM).  
- Conseil en gouvernance sécurité et conformité.

### 1.4 Environnement économique et sociétal
Le coût des incidents cyber est en hausse, et la surface d’attaque augmente avec le cloud, le télétravail et l’IoT. Les entreprises recherchent des solutions capables de prioriser les alertes et de limiter la fatigue analyste. Le projet se situe à l’interface entre performance opérationnelle, maîtrise des risques et confiance numérique.

### 1.5 Environnement technologique
- SI hétérogène (on-premise + cloud).  
- Journalisation centralisée via stack de collecte.  
- Besoin d’un composant IA interopérable (API) avec les outils existants.

### 1.6 Environnement de données
- Logs et métadonnées réseau (NetFlow-like).  
- Volumétrie élevée, variabilité temporelle importante.  
- Contraintes : qualité des labels, déséquilibre des classes, bruit, dérive des comportements.

---

## 2) Étude de marché et analyse concurrentielle

### 2.1 Analyse de marché
La cybersécurité est portée par :
- la hausse des attaques opportunistes et ciblées ;
- l’obligation croissante de conformité ;
- la pénurie de profils SOC expérimentés ;
- la nécessité d’automatisation par IA/ML pour le tri des alertes.

Pour une version finale académique, il est recommandé d’intégrer :
- chiffres macro (croissance du marché cyber France/Europe) ;
- coûts moyens d’un incident ;
- taux d’adoption des solutions XDR/SIEM augmentées par IA ;
- contraintes réglementaires sectorielles (NIS2 selon périmètre).

> **Important (version finale PDF)** : intégrer des sources ≤ 5 ans et les citer en notes de bas de page (ANSSI, ENISA, Eurostat, rapports gouvernementaux, observatoires sectoriels, cabinets reconnus).

### 2.2 Analyse concurrentielle (3 acteurs minimum)

#### Concurrent direct 1 — Darktrace
- **Positionnement** : détection comportementale réseau assistée par IA.  
- **Points forts** : couverture large, capacités d’analyse autonome, réponse automatisée.  
- **Points faibles** : coût, opacité perçue sur certains mécanismes, dépendance éditeur.  
- **Comparaison** : solution robuste mais parfois surdimensionnée pour des PME ; notre approche est plus modulaire et personnalisable.

#### Concurrent direct 2 — Vectra AI
- **Positionnement** : NDR orienté détection des attaques dans les environnements hybrides.  
- **Points forts** : expertise cybersécurité, détection latérale, priorisation des menaces.  
- **Points faibles** : intégration complexe selon SI, coût total de possession.  
- **Comparaison** : notre projet privilégie la maîtrise du pipeline et l’adaptation métier.

#### Concurrent indirect — Splunk + modèles personnalisés
- **Positionnement** : SIEM/observabilité avec capacité ML via apps et pipelines.  
- **Points forts** : écosystème riche, extensibilité, adoption large.  
- **Points faibles** : besoin de compétences avancées, coût licence/ingestion.  
- **Comparaison** : notre approche propose un socle IA plus ciblé intrusion réseau, potentiellement moins coûteux en phase pilote.

### 2.3 Synthèse concurrentielle
Le marché est mature sur des offres enterprise complètes mais coûteuses. Une opportunité existe pour une solution centrée sur :
1. performance de détection mesurable ;
2. interopérabilité API-first ;
3. gouvernance des risques et conformité dès la conception.

---

## 3) Problématique et définition du besoin

### 3.1 Problématique
**Comment détecter efficacement des intrusions réseau variées dans un environnement d’entreprise, en réduisant les faux positifs et en garantissant un déploiement exploitable en conditions réelles ?**

### 3.2 Genèse de la solution
Constat initial :
- forte volumétrie d’événements ;
- surcharge d’alertes ;
- difficultés de priorisation manuelle ;
- hétérogénéité des comportements légitimes.

Hypothèse : un modèle supervisé entraîné sur CICIDS2017, complété par des contrôles de qualité, peut améliorer le taux de détection sans exploser le taux de fausses alertes.

### 3.3 Besoins fonctionnels
- Ingestion de flux réseau normalisés ;
- Prédiction binaire (benin/malveillant) + score de confiance ;
- Journalisation des prédictions ;
- Visualisation des alertes prioritaires ;
- Export pour investigation SOC.

### 3.4 Besoins non fonctionnels
- Latence faible (quasi temps réel) ;
- Disponibilité élevée de l’API ;
- Traçabilité (logs, versioning modèle) ;
- Sécurité (auth, chiffrement, contrôle d’accès) ;
- Maintenabilité et explicabilité minimale des décisions.

### 3.5 Pourquoi cette solution est optimale
- Dataset riche en classes d’attaque ;
- Pipeline reproductible ;
- Modèle supervisé performant sur données tabulaires ;
- Déploiement web rapide et industrialisable ;
- Mesure explicite des performances techniques et opérationnelles.

---

## 4) Gestion de projet

### 4.1 Pilotage et méthodologie
Méthode choisie : **Scrum-Kanban hybride**.
- Sprints de 2 semaines pour la production incrémentale ;
- Board Kanban pour visualiser les blocages ;
- Rituels : sprint planning, daily court, review, rétrospective.

### 4.2 Rétroplanning (janvier → août 2026)
| Période | Jalons principaux | Livrables |
|---|---|---|
| Janvier 2026 | Cadrage entreprise + marché + problématique | Chapitres 1 à 3 validés |
| Février 2026 | Architecture data + collecte + dictionnaire | Schéma technique, data map |
| Mars 2026 | EDA, nettoyage, feature engineering | Notebook d’analyse, rapport qualité |
| Avril 2026 | Entraînement + benchmark modèles | Rapport métriques comparatives |
| Mai 2026 | Développement application web IA | MVP applicatif local |
| Juin 2026 | Durcissement sécurité, tests, accessibilité | Version release candidate |
| Juillet 2026 | Finalisation dossier + support oral | PDF mémoire + slides |
| Avant 17 août 2026 | Dépôt livrables sur Teams | ZIP final + annexes |

### 4.3 Outils d’accompagnement projet
- **Gestion** : Jira/Trello, GitHub Projects.  
- **Planification** : Gantt (MS Project/Notion/GanttProject).  
- **Documentation** : Notion/Confluence + README technique.  
- **Suivi code** : GitHub (branches, PR, revues).

### 4.4 Tableaux de bord et indicateurs
- Avancement sprint (% stories done) ;
- Vélocité ;
- Taux de bugs ouverts/fermés ;
- Couverture tests ;
- Accuracy/F1/Recall du modèle ;
- Latence moyenne API (ms) ;
- Disponibilité service (% uptime).

### 4.5 Budget prévisionnel (exemple)
| Poste | Coût estimé |
|---|---:|
| Ressources humaines (4 mois) | 18 000 € |
| Infrastructure (VM, stockage) | 1 500 € |
| Outils logiciels / monitoring | 800 € |
| Sécurité / audit | 1 200 € |
| Divers / imprévus (10%) | 2 150 € |
| **Total prévisionnel** | **23 650 €** |

### 4.6 Veille technologique, sectorielle et réglementaire
| Source | Type de veille | Date dernière MAJ | Outil | Fréquence |
|---|---|---|---|---|
| ANSSI | Réglementaire / menaces | Hebdomadaire | RSS + alertes | Hebdo |
| CERT-FR | Vulnérabilités / incidents | Quotidienne | Mail + Flux | Quotidien |
| ENISA | Tendances UE cyber | Mensuelle | Veille manuelle | Mensuel |
| CVE/NVD | Vulnérabilités techniques | Quotidienne | API scripts | Quotidien |
| Papers arXiv/IEEE | Veille IA/ML sécurité | Bi-mensuelle | Zotero + alertes | 2x/mois |

### 4.7 Cartographie des risques
| Risque | Probabilité | Impact | Criticité | Mesures de mitigation |
|---|---|---|---|---|
| Déséquilibre de classes | Élevée | Élevé | Critique | Re-sampling, class weights, métriques adaptées |
| Faux positifs excessifs | Moyenne | Élevé | Élevée | Seuil adaptatif, calibration, feedback SOC |
| Dérive des données | Moyenne | Élevé | Élevée | Monitoring drift + réentraînement planifié |
| Fuite de données sensibles | Faible | Très élevé | Critique | Chiffrement, anonymisation, RBAC |
| Non-conformité RGPD | Faible | Très élevé | Critique | DPIA simplifiée, minimisation, traçabilité |

### 4.8 Charte éthique (synthèse)
1. Finalité explicite et proportionnée de la détection.  
2. Minimisation des données collectées.  
3. Transparence sur le rôle de l’IA (outil d’aide, pas décision autonome finale).  
4. Auditabilité et droit à l’explication interne.  
5. Revue périodique des biais et impacts sociétaux.

---

## 5) Exploitation des données

### 5.1 Identification des sources de données
- **Source principale** : CICIDS2017 (fichiers CSV).  
- **Sources complémentaires** (optionnel) : enrichissement IP/ASN, blacklist publiques, règles SOC internes.

### 5.2 Volumétrie et typologie
- Volumétrie : plusieurs millions de lignes selon agrégation ;
- Types : numériques continues, catégorielles, dérivées temporelles ;
- Cible : `Label` (Benign vs Attack, et multi-classe en option).

### 5.3 Dictionnaire de données (exemple)
| Variable | Type | Description |
|---|---|---|
| Flow Duration | Numérique | Durée du flux |
| Total Fwd Packets | Numérique | Nombre de paquets sortants |
| Total Backward Packets | Numérique | Nombre de paquets entrants |
| Fwd Packet Length Mean | Numérique | Longueur moyenne paquet forward |
| Bwd Packet Length Mean | Numérique | Longueur moyenne paquet backward |
| Flow Bytes/s | Numérique | Débit moyen en octets/s |
| Flow Packets/s | Numérique | Débit moyen en paquets/s |
| Label | Catégorie | Type de trafic |

### 5.4 Conformité collecte/usage
- Données de test anonymisées ;
- Absence de données directement identifiantes dans les features retenues ;
- Contrôles d’accès par rôle ;
- Journalisation des actions sur les datasets ;
- Procédure de purge et durée de conservation définies.

### 5.5 Installation base de données et tables
Exemple d’architecture :
- PostgreSQL (schéma `ids_ai`) ;
- table brute `raw_flows` ;
- table nettoyée `flows_clean` ;
- table features `flows_features` ;
- table prédictions `predictions_log`.

### 5.6 Analyse qualité des données
#### Valeurs manquantes
- Détection par colonne (% missing) ;
- Imputation médiane pour variables robustes ;
- Suppression contrôlée des colonnes trop incomplètes.

#### Incohérences
- Valeurs infinies remplacées ;
- Outliers traités (winsorisation/log transform selon variable) ;
- Uniformisation des libellés de classes.

### 5.7 Sécurisation des données
- Chiffrement en transit (TLS) ;
- Chiffrement au repos (volume/DB) ;
- Gestion des secrets via variables d’environnement ;
- RBAC + rotation des credentials ;
- Sauvegardes chiffrées + tests de restauration.

### 5.8 Modélisation supervisée
#### Split des données
- Train: 70% ; Validation: 15% ; Test: 15% ;
- Stratification pour préserver la distribution des classes.

#### Algorithmes testés
- Logistic Regression ;
- Decision Tree ;
- Random Forest ;
- KNN (benchmark) ;
- (option) XGBoost/LightGBM si autorisé.

#### Exemple de résultats (à adapter à vos scores réels)
| Modèle | Accuracy | Precision | Recall | F1-score | Latence inférence |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.932 | 0.915 | 0.901 | 0.908 | 5 ms |
| Decision Tree | 0.948 | 0.936 | 0.927 | 0.931 | 3 ms |
| Random Forest | **0.978** | **0.971** | **0.965** | **0.968** | 8 ms |
| KNN | 0.955 | 0.942 | 0.934 | 0.938 | 22 ms |

**Modèle retenu : Random Forest**, compromis robuste entre performance et interprétabilité partielle (importance des variables).

### 5.9 Évaluation performances SQL (optimisation)
Comparaison requêtes sur tables non optimisées vs optimisées (index B-tree sur timestamps/label/hash flux, partition journalière).

| Requête | Non optimisée | Optimisée | Gain |
|---|---:|---:|---:|
| Top attaques par heure | 3.2 s | 0.7 s | -78% |
| Recherche flux suspects (fenêtre 24h) | 5.1 s | 1.1 s | -78% |
| Agrégation par type d’attaque | 2.8 s | 0.6 s | -79% |

### 5.10 Documentation technique du modèle
- Pipeline `preprocess -> train -> evaluate -> serialize`;  
- Standardisation/normalisation selon modèle ;  
- Encodage labels ;  
- Sauvegarde modèle `joblib`;  
- Versioning via tags Git + métadonnées d’entraînement.

### 5.11 Prise en compte de l’éthique
- Vérification des faux positifs par segment ;
- Alerte assistée, décision humaine finale ;
- Documentation des limites et zones d’incertitude ;
- Processus d’escalade en cas de doute.

### 5.12 Tableau de suivi des problématiques techniques
| Index | Date problème | Problème | Date résolution | Solution |
|---:|---|---|---|---|
| 1 | 2026-03-04 | Colonnes à variance nulle | 2026-03-05 | Filtre automatique prefit |
| 2 | 2026-03-11 | Déséquilibre classes attaques rares | 2026-03-13 | Class weights + seuils |
| 3 | 2026-04-02 | Temps d’inférence élevé | 2026-04-06 | Optimisation features + batch |
| 4 | 2026-04-18 | Fuite de data entre train/test | 2026-04-19 | Rebuild pipeline split strict |

---

## 6) Développement d’une application incorporant un algorithme supervisé

### 6.1 Architecture applicative
- **Front** : Flask templates ou Dash (tableaux + alertes + formulaires upload).  
- **Back** : API Flask/FastAPI `/predict` et `/health`.  
- **Modèle** : Random Forest sérialisé (`.joblib`).  
- **DB** : PostgreSQL pour logs et traçabilité.

### 6.2 Fonctionnalités principales
1. Import de flux (CSV/API).  
2. Prétraitement automatique identique à l’entraînement.  
3. Prédiction et score de confiance.  
4. Affichage d’alertes critiques en priorité.  
5. Historique consultable et exportable.

### 6.3 Déploiement local
- Environnement Python (venv/conda) ;
- Variables `.env` ;
- Lancement DB + API + Front ;
- Vérification endpoints ;
- Tests fonctionnels et de charge légère.

### 6.4 Mesures réglementaires et protection données
- Politique de minimisation ;
- Journal de consentement/usage lorsque nécessaire ;
- Masquage des champs sensibles ;
- Contrôles d’accès ;
- Plan de réponse à incident.

### 6.5 Accessibilité (situation de handicap)
- Contraste couleurs conforme ;
- Navigation clavier ;
- Textes alternatifs et labels explicites ;
- Taille de police adaptable ;
- Messages d’erreur compréhensibles.

### 6.6 URL application
- **URL locale (exemple)** : `http://localhost:8050`  
- **URL publique (à renseigner pour rendu final)** : `https://<votre-url>`

---

## 7) Conclusion
Ce projet démontre la faisabilité d’une solution de détection d’intrusions pilotée par IA supervisée, de la donnée brute au service applicatif. Le modèle retenu présente de bonnes performances, sous réserve d’un pilotage continu de la dérive et d’une validation métier régulière.

### 7.1 Contraintes rencontrées
- Qualité hétérogène des données ;
- Déséquilibre des classes ;
- Arbitrage performance/interprétabilité ;
- Exigences de sécurité et conformité.

### 7.2 Enjeux et impacts
- Réduction du temps de détection ;
- Aide à la priorisation SOC ;
- Amélioration de la résilience opérationnelle ;
- Renforcement de la gouvernance cyber.

### 7.3 Évolutions possibles
1. Passage multi-classe avancé (familles d’attaques).  
2. Détection hybride supervisée + anomalie (semi-supervisé).  
3. MLOps complet (CI/CD modèle, monitoring drift, auto-retraining contrôlé).  
4. Intégration SIEM/SOAR avec playbooks de remédiation.

---

## 8) Bibliographie indicative (à compléter dans le rendu final)
- Documentation CICIDS2017 (University of New Brunswick / Canadian Institute for Cybersecurity).  
- Guides ANSSI sur l’hygiène informatique et détection.  
- ENISA Threat Landscape (édition récente).  
- OWASP (bonnes pratiques applicatives).  
- Scikit-learn documentation (modèles de classification).  
- Articles académiques récents sur IDS basé ML/DL.

---

## 9) Annexes à inclure dans le PDF final
1. Captures d’écran sécurité DB et application.  
2. Extraits de notebooks (EDA, entraînement, tests).  
3. Extraits de code commentés (prétraitement, entraînement, API).  
4. Gantt détaillé et backlog sprint.  
5. Charte éthique complète signée.  
6. Procédure d’installation (README/PDR).  
7. Jeu d’identifiants de test et environnement de recette.

---

# Plan de soutenance orale (90 minutes)

## A. Présentation (30 min)
- 0–5 min : Contexte, enjeux cyber, problématique.
- 5–10 min : Données (CICIDS2017), méthodologie, qualité.
- 10–18 min : Modélisation, résultats comparatifs, modèle choisi.
- 18–24 min : Démo application (front + API + logs).
- 24–28 min : Gouvernance projet, risques, conformité.
- 28–30 min : Conclusion et roadmap.

## B. Q/R (15 min)
Préparer des réponses sur:
- biais et faux positifs ;
- généralisation hors dataset ;
- coût et ROI ;
- gouvernance et sécurité.

## C. Entretien pro (15 min)
Argumenter votre posture chef de projet : arbitrage, communication, décisions sous contrainte.

## D. Jeu de rôle client (30 min)
- Traiter un changement d’environnement (ex: migration cloud).  
- Reprioriser backlog, budget, risques.  
- Démontrer écoute active, reformulation, plan d’action.

---

# Check-list livrables avant dépôt (17 août 2026, 23:59)
- [ ] `NOM_PRENOM_THESE.pdf` (~50 pages hors annexes).  
- [ ] `NOM_PRENOM_PREZ.pdf` (support oral).  
- [ ] ZIP technique contenant :
  - [ ] URL publique application ;
  - [ ] URL dépôt Git (facultatif) ;
  - [ ] code source complet ;
  - [ ] dump SQL ;
  - [ ] fichiers de configuration ;
  - [ ] README/PDR (prérequis, install, comptes de test, accès admin, infos multi-navigateurs).

---

## Conseils de personnalisation immédiate
1. Remplacer les hypothèses (entreprise, budget, métriques) par vos données réelles.  
2. Ajouter vos captures et extraits notebook/code en annexes.  
3. Compléter la bibliographie avec sources datées et fiables.  
4. Harmoniser la charte graphique (logo, pagination, styles).  
5. Répéter la soutenance avec chrono strict et démonstration applicative.
