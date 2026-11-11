# PERMANENCE ÉQUIPEMENT — SETRAG

## Présentation

Application Power Apps destinée à la gestion de la permanence DMI (Direction de la Maintenance de l'Infrastructure) de SETRAG.

Objectifs :
- Remplacer les saisies dispersées par un parcours opérationnel centralisé.
- Suivre les travaux, LTV/RAL, incidents/ruptures et feedbacks terrain.
- Fiabiliser les données SharePoint et la continuité entre les postes.
- Préparer les rapports de fin de poste et l'exploitation analytique.

## Stack

- **Frontend :** Microsoft Power Apps Canvas.
- **Données :** listes SharePoint.
- **Automatisation cible :** Power Automate.
- **Analyse cible :** Power BI.

## Structure

```text
.
├── Backend/                 # Schéma SharePoint, dictionnaire et alignement
├── Documentation/           # Spécifications, décisions et état du projet
├── Frontend/                # Documentation et YAML des écrans Power Apps
├── script/                  # Scripts d'analyse et d'extraction
├── skills/                  # Conventions et ressources de développement
├── BACKLOG.md               # Suivi consolidé des tâches
├── PROJET_ANALYSE.md        # Analyse et architecture fonctionnelle
└── README.md
```

## Écrans de l'application

1. **Identification agent** — sélection du permanent et validation par PIN.
2. **Prise de poste** — choix P1/P2/P3, suggestion horaire et consultation des événements à reprendre.
3. **Journal de bord** — gestion des Travaux, LTV/RAL et Incidents/Ruptures.
4. **Feedback terrain** — pointage terrain rattaché à un chantier.
5. **Clôture et relève** — synthèse, commentaire, confirmation et préparation de la transmission.

Les sources YAML synchronisées et leur provenance sont décrites dans [Frontend/README.md](Frontend/README.md). L'état fonctionnel des écrans est décrit dans [Documentation/ETAT_AVANCEMENT_2026-11-11.md](Documentation/ETAT_AVANCEMENT_2026-11-11.md).

## Documentation principale

- [Backlog](BACKLOG.md)
- [Analyse du projet](PROJET_ANALYSE.md)
- [Dictionnaire de données SharePoint](Backend/contextBD.md)
- [Retours métier et décisions](Documentation/RETOURS_METIER_ET_DECISIONS.md)
- [État d'avancement](Documentation/ETAT_AVANCEMENT_2026-11-11.md)
- [Sources Power Apps](Frontend/README.md)

## Sources SharePoint

Référentiels :
- `Ref_Permanents`
- `Ref_Cantons`
- `Ref_Acteurs`

Listes opérationnelles :
- `Tx_Travaux`
- `Tx_LTV`
- `Tx_incidents_Ruptures`
- `Tx_Feedbacks`

Le schéma exact des colonnes, types, noms internes et relations est décrit dans [Backend/contextBD.md](Backend/contextBD.md). Toujours vérifier ce schéma dans l'environnement Power Apps cible avant une modification.

## Source de vérité et synchronisation

- Dépôt de documentation et de suivi : `Darys21/permanence_equipement_app`.
- Dépôt source des exports YAML actuels au moment de la synchronisation : `Darys21/PERMANENCE-EQUIPEMENT`, dossier `pa_yaml_script`.
- Les fichiers synchronisés sont des snapshots datés. À chaque évolution d'écran, exporter le YAML et synchroniser le fichier correspondant.
- Les anciens YAML déjà présents dans les dossiers Frontend peuvent être historiques. Se référer à [Frontend/README.md](Frontend/README.md) pour identifier les fichiers canoniques.

## Sécurité et données

Ne jamais versionner de PIN réels, mots de passe, jetons, secrets, exports de données personnelles ou données opérationnelles réelles. Les identifiants techniques et URLs internes SharePoint ne doivent être partagés que si nécessaires et autorisés. Le dépôt doit rester privé tant qu'il contient des informations internes.
