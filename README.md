
# PERMANENCE EQUIPEMENT - SETRAG

## Description du projet
Application Power Apps pour la gestion de la permanence DMI (Direction de la Maintenance de l'Infrastructure) de SETRAG.

L'objectif est de :
- Remplacer le fichier Excel de permanence par une interface unique et sécurisée
- Automatiser le suivi des chantiers, LTV (Limitations Temporaires de Vitesse) et incidents de la voie
- Fiabiliser la donnée opérationnelle
- Accélérer la prise de décision

---

## Stack technique
- **Frontend** : Power Apps
- **Backend** : Listes SharePoint
- **Automatisation** : Power Automate
- **Analytics** : Power BI

---

## Structure du projet
```
PERMANANCE EQUIPEMENT/
├── Backend/                             # Contrats, alignements et schémas SharePoint
│   └── schemas_export/                  # Schémas de colonnes exportés
├── Frontend/                            # Sources YAML des écrans Power Apps
│   ├── Ecran 1 Prise de poste/
│   ├── Ecran 2 Journal de bord/
│   ├── Ecran 4 Cloture et releve/
│   └── Ecran Feedback/
├── Documentation/                       # Documentation fonctionnelle et processus
├── script/                              # Scripts d'analyse et d'extraction
├── skills/                              # Skills et conventions du projet
├── BACKLOG.md
├── PROJET_ANALYSE.md
├── RAPPORT_REVUE_POWER_APPS.md
└── README.md
```

---

## Documentation principale
- [Analyse complète du projet](PROJET_ANALYSE.md)
- [Backlog du projet](BACKLOG.md)
- [Revue Power Apps](RAPPORT_REVUE_POWER_APPS.md)
- [Spécification de l'écran 1](Frontend/Ecran%201%20Prise%20de%20poste/Ecran1.md)
- [Spécification de l'écran 2](Frontend/Ecran%202%20Journal%20de%20bord/Ecran2.md)
- [Spécification de l'écran Feedback](Frontend/Ecran%20Feedback/EcranFeedback.md)

---

## User stories principales
### Écran 1 - Prise de poste
- US1.1 : Auto-identification via compte M365
- US1.2 : Sélection du quart
- US1.3 : Aspiration des "En Cours"
(plus de détails dans [Ecran1.md](Frontend/Ecran%201%20Prise%20de%20poste/Ecran1.md))

---

## Listes SharePoint
- **Master Data**
  - Ref_Cantons
  - Ref_Acteurs
- **Transactionnelles**
  - Tx_Travaux
  - Tx_Feedbacks
  - Tx_Incidents_Ruptures
  - Tx_LTV

(plus de détails dans [PROJET_ANALYSE.md](PROJET_ANALYSE.md) et [Backend/contextBD.md](Backend/contextBD.md))

---

## Préparer le dépôt Git privé

Le dépôt contient les sources lisibles, la documentation, les scripts et les schémas nécessaires à la maintenance. Les données opérationnelles, les exports bruts, les environnements locaux, les outils installés et le fichier binaire `.msapp` ne sont pas destinés à Git.

Le fichier [.gitignore](.gitignore) formalise cette séparation. En particulier, il exclut :
- les environnements Python et caches locaux ;
- les secrets et fichiers `.env` ;
- `BASE/`, `Data brute/` et les exports transactionnels de `Backend/` ;
- `.agents/`, `copilot/` et les fichiers temporaires ou générés ;
- les fichiers `.msapp`, dont les sources de travail sont représentées ici par les YAML de `Frontend/`.

Avant le premier commit, vérifier les fichiers qui seront suivis :

```powershell
git init
git status --short --ignored
git add .
git status --short
```

Ne jamais ajouter de secret, de donnée personnelle ou d'export opérationnel. Les identifiants Microsoft Graph doivent rester dans des variables d'environnement locales, conformément aux exemples de `skills/sharepoint-graph-schema/references/`.

