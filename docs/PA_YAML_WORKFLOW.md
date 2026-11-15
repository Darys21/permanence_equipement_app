# Workflow de développement Power Apps Canvas — Permanence Équipement

**Version :** 1.0  
**Date d'adoption :** 16/11/2026  
**Périmètre :** tous les fichiers `.pa.yaml` de l'application Permanence Équipement.

Ce document définit le contrat de travail pour toute création ou correction YAML. Il complète le backlog ; il ne remplace ni la recette Power Apps Studio ni la validation métier.

## 1. Principes non négociables

1. Travailler uniquement sur les écrans et fichiers nécessaires à la demande.
2. Lire la spécification fonctionnelle, le backlog, le YAML actuel et les conventions déjà utilisées avant de modifier.
3. Ne jamais inventer une propriété de contrôle, un nom de contrôle, une source de données, une colonne SharePoint ou une valeur Choice.
4. Préserver les noms de contrôles, variables, collections, sources et identifiants existants sauf demande explicite et justification.
5. Préférer un diff minimal à une réécriture complète d'écran.
6. Séparer clairement : validité YAML, import/compilation, comportement Power Fx, rendu UX et validation métier.
7. Ne jamais annoncer « terminé » sur la seule base d'un YAML plausible ou d'un import réussi.

## 2. Phase A — Découverte obligatoire

Avant toute écriture :

- Identifier l'écran, le fichier source et les dépendances.
- Lire le YAML complet de l'écran et les composants connexes réellement utilisés.
- Lire le backlog et les décisions métier pertinentes.
- Identifier les contrôles existants et leurs propriétés à partir du YAML source, de la documentation officielle ou des métadonnées de contrôle disponibles.
- Vérifier les types SharePoint : texte, nombre, date/heure, booléen, Choice, Lookup, colonnes obligatoires et noms internes.
- Lister les variables, collections, formules et chemins de navigation affectés.
- Établir les critères d'acceptation et les scénarios de non-régression.

### Outils de découverte des contrôles

Si les outils `list_controls` et `describe_control` sont disponibles dans l'environnement d'exécution, ils doivent être appelés avant de choisir ou modifier un contrôle. Pour chaque contrôle utilisé, ne retenir que les propriétés effectivement documentées par leur sortie.

Si ces outils ne sont pas disponibles, ne pas prétendre les avoir utilisés : s'appuyer sur les contrôles déjà présents dans le projet et sur une documentation fiable, signaler explicitement cette limite et éviter toute propriété incertaine. Une propriété inconnue doit être vérifiée dans Power Apps Studio avant d'être introduite.

## 3. Phase B — Plan par écran

Pour chaque écran touché, consigner avant modification :

- Objectif métier.
- Sources de données et colonnes utilisées.
- Contrôles concernés.
- Formules concernées : `OnVisible`, `OnSelect`, `Items`, `Default`, `Visible`, etc.
- États : chargement, vide, succès, erreur, accès interdit si applicable.
- Navigation entrante et sortante.
- Critères d'acceptation et tests de non-régression.

Ne pas modifier les écrans hors périmètre.

## 4. Phase C — Règles de génération YAML / Power Fx

- Toute formule Power Fx doit commencer par `=`.
- Pour une formule multiligne, utiliser un bloc YAML `|-` et placer `=` sur la première ligne de contenu.
- Protéger les chaînes contenant `: ` avec des guillemets adaptés.
- Protéger les records Power Fx et les chaînes contenant des accolades afin qu'ils restent des scalaires YAML, pas des mappings YAML.
- Respecter l'indentation et la structure de contrôle déjà utilisées dans le projet.
- Ne pas convertir arbitrairement les contrôles classiques en contrôles Modern : vérifier leur disponibilité, leurs propriétés et leur compatibilité dans l'application cible.
- Ne pas remplacer un assemblage existant par Avatar, Badge, Progress ou autre primitive sans vérifier qu'elle existe dans le schéma de l'environnement.
- Dans les conteneurs AutoLayout, vérifier les interactions entre `FillPortions`, `Height`, `Width`, alignement et dimensionnement des enfants. Ne pas appliquer aveuglément une règle de hauteur fixe : choisir une formule cohérente avec le parent et le responsive.
- Pour les libellés, badges et éléments de navigation, vérifier `Wrap` et le comportement sur les largeurs réellement utilisées avant de forcer `false`.

### Règle SharePoint / Patch

- Création : `Patch(Source, Defaults(Source), ...)`.
- Modification : cibler le record existant ou le retrouver par sa clé stable ; ne jamais utiliser `Defaults()` dans le chemin de modification.
- Suppression : cibler explicitement le record existant.
- Choice et Lookup : respecter la forme attendue par le type de colonne et le schéma réellement connecté.
- Après sauvegarde : vérifier les erreurs, le résultat, l'identifiant conservé, le refresh et l'état du formulaire.
- En cas d'échec : conserver les données saisies et afficher un message d'erreur exploitable.
- Ne vider le formulaire et afficher le succès qu'après confirmation effective de l'opération.

## 5. Phase D — Audit statique avant livraison

Vérifier au minimum :

- Structure YAML et indentation.
- Formules préfixées par `=`.
- Blocs multilignes correctement formés.
- Chaînes et records correctement protégés.
- Propriétés présentes et de type cohérent pour le contrôle.
- Références de contrôles, variables, collections, sources et colonnes existantes.
- Parent/enfant, AutoLayout, tailles, FillPortions, Wrap et débordements.
- Navigation et conditions d'accès.
- États chargement/vide/erreur/succès.
- Formules de sauvegarde, gestion des erreurs et conservation des IDs.
- Aucun changement hors périmètre.

## 6. Phase E — Validation et QA

Effectuer les validations dans cet ordre :

1. **Validation YAML** : parseur/linter si disponible.
2. **Compilation Canvas** : exécuter `compile_canvas` si cet outil est réellement disponible.
3. **Import Power Apps Studio** : vérifier que le fichier est accepté par l'environnement cible.
4. **QA visuelle** : dimensions, alignement, responsive, wrap, débordements, états vides et lisibilité.
5. **QA fonctionnelle** : jouer les scénarios d'acceptation et les cas d'erreur.
6. **QA données** : contrôler les lignes, IDs, Choice, Lookup et dates directement dans SharePoint.
7. **Non-régression** : rejouer les parcours voisins affectés.

Si `compile_canvas` ou un outil QACheck n'est pas disponible, le signaler et ne pas simuler une réussite. L'import dans Studio et les tests manuels restent nécessaires.

## 7. Règle d'itération

- Corriger une cause à la fois.
- Après chaque correction, relancer les validations pertinentes.
- Ne pas masquer une erreur en supprimant un contrôle ou une formule sans comprendre son rôle.
- Conserver les preuves : message d'erreur, scénario, résultat attendu, résultat observé.
- Si une information métier ou un schéma manque, poser une seule question ciblée plutôt que d'inventer.

## 8. Format obligatoire du compte rendu

Chaque intervention doit fournir :

1. **Périmètre** : écran(s) et fichier(s) concernés.
2. **Découverte** : sources, contrôles et dépendances examinés.
3. **Outils** : outils réellement appelés ; préciser ceux indisponibles.
4. **Modifications** : résumé et diff minimal.
5. **Validation** : YAML, compilation/import, QA visuelle, QA fonctionnelle et données — chaque niveau avec statut distinct.
6. **Risques / limites** : points non vérifiés ou dépendances.
7. **Tests manuels** : étapes reproductibles, résultat attendu et résultat à renseigner.
8. **Backlog** : IDs mis à jour sans doublon et statut fondé sur les preuves.

## 9. États de validation à utiliser

| État | Signification |
|---|---|
| À analyser | Découverte ou spécification incomplète |
| Modifié — non validé | Code édité, validations non exécutées |
| YAML valide | Syntaxe YAML vérifiée |
| Importé | Import Power Apps Studio accepté |
| Compilé | Compilation Canvas confirmée par l'outil |
| QA technique validée | Contrôles statiques et visuels exécutés |
| Fonctionnel à valider | Tests métier non terminés |
| Validé métier | Scénarios acceptés par les utilisateurs métier |

Ne pas fusionner ces états. Un niveau supérieur ne peut être déclaré que si les preuves correspondantes existent.

## 10. Première application au projet

Le prochain chantier prioritaire reste le Journal de bord :

1. Récupérer la version exacte et complète de `JournalDeBord_3.pa.yaml` depuis la source de vérité.
2. Cartographier les formulaires et opérations CRUD Travaux, LTV et Incidents.
3. Corriger d'abord la création/reprise LTV et la modification Travaux sans changement d'ID.
4. Auditer ensuite le CRUD Incidents/Ruptures.
5. Exécuter les tests Power Apps + SharePoint et mettre à jour les IDs `JOUR-xx` correspondants.

**Limite d'outillage constatée lors de l'adoption (16/11/2026) :** les actions `list_controls`, `describe_control`, `compile_canvas` et les QAChecks Canvas ne sont pas exposées dans les outils connectés de cette session. Elles ne doivent donc pas être revendiquées. La découverte doit être faite à partir des sources et de Power Apps Studio tant qu'un environnement outillé ne les fournit pas.
