# Sources Power Apps — référence

Ce dossier contient la documentation fonctionnelle et les exports YAML de référence des écrans Power Apps.

## Sources YAML synchronisées

Les fichiers ci-dessous ont été copiés depuis le dépôt `Darys21/PERMANENCE-EQUIPEMENT`, dossier `pa_yaml_script`, branche `main`, le 11/11/2026. Ils sont des snapshots de la source fournie, pas une preuve d'import réussi ou de validation runtime.

| Écran | Fichier canonique dans ce dépôt | Source |
|---|---|---|
| Identification agent | `Ecran 1 Prise de poste/scrIdentificationAgent.yaml` | `pa_yaml_script/scrIdentificationAgent.yaml` |
| Prise de poste | `Ecran 1 Prise de poste/PrisePoste_2.yaml` | `pa_yaml_script/PrisePoste_2.yaml` |
| Journal de bord | `Ecran 2 Journal de bord/JournalDeBord_3.yaml` | `pa_yaml_script/JournalDeBord_3.yaml` |
| Feedback terrain | `Ecran Feedback/scrFeedback.yaml` | `pa_yaml_script/scrFeedback.yaml` |
| Clôture et relève | `Ecran 4 Cloture et releve/scrCloture_2.yaml` | `pa_yaml_script/scrCloture_2.yaml` |

## Règles de maintenance

1. Les YAML listés ci-dessus sont les snapshots de référence synchronisés le 11/11/2026.
2. Lorsqu'un écran est modifié dans Power Apps, exporter son YAML et mettre à jour le fichier correspondant dans ce dépôt dans le même changement.
3. Ne pas modifier les YAML uniquement pour harmoniser la documentation : toute correction doit être testée dans Power Apps.
4. Les anciens fichiers `poste.yaml`, `dashboard.yaml` et `cloture.yaml` sont conservés pour l'historique tant que leur statut n'a pas été vérifié. Ne pas les considérer comme la version courante sans comparaison.
5. Vérifier les différences avec le dépôt source avant chaque synchronisation.
6. Ne jamais versionner de PIN réel, mot de passe, jeton, export de données personnelles ou données opérationnelles.

## Documentation associée

- `Ecran1.md` : parcours de prise de poste.
- `IdentificationAgent.md` : authentification du permanent.
- `../Ecran 2 Journal de bord/Ecran2.md` : journal Travaux/LTV/Incidents.
- `../Ecran Feedback/EcranFeedback.md` : pointages terrain.
- `../Ecran 4 Cloture et releve/EcranCloture.md` : clôture et relève.
- `../../Documentation/RETOURS_METIER_ET_DECISIONS.md` : demandes des permanents et arbitrages.
