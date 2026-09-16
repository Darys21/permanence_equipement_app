# Rapport de revue Power Apps

## A. Erreurs bloquantes d'import corrigees

- Les formules YAML contenant `: ` etaient ecrites comme scalaires simples. Elles ont ete converties en blocs `|-`, ce qui supprime la cause PA1001 `YamlInvalidSyntax`.
- L'ecran `PrisePoste_2` a ete renomme `PrisePoste_1` pour correspondre a toutes les navigations.
- Les noms de colonnes internes ont ete alignees sur les listes SharePoint fournies : `Date_travaux`, `Heures_Autorisee`, `Heures_Degagement`, `Heures_Voie_Retablie` et `Date_imposition`.

## B. Erreurs Power Fx corrigees

- Les valeurs de type texte attendues par `Tx_LTV.CantonID`, `Tx_LTV.ActeurID` et `Tx_incidents_Ruptures.CantonID` sont ecrites avec `Text(...Selected.ID)`.
- Les references aux colonnes absentes `Poste`, `Agent`, `DateSaisie` et `StatutContact` ont ete retirees des Patch et filtres.
- Le statut de contact est conserve dans `Commentaire`, car `Tx_Feedbacks` ne comporte pas de colonne `StatutContact`.
- Les references aux controles et ecrans ont ete verifiees : aucune reference manquante.

## C. References SharePoint a verifier

- Les formules utilisent les noms affiches/fournis. Verifier dans Power Apps que les noms internes exposes par le connecteur sont identiques, en particulier les accents et underscores.
- Le filtrage par quart n'est pas persiste : les colonnes `Poste`, `Agent` et `DateSaisie` n'existent pas dans le schema SharePoint fourni. L'application ne peut donc pas isoler durablement les donnees par poste sans ajout de colonnes.
- Les champs `PK_Debut` et `PK_Fin` sont utilises uniquement dans `Tx_LTV`, ou ils existent. Ils ne sont plus ecrits dans `Tx_Travaux`.

## D. Risques de delegation

- Les compteurs utilisent encore `CountRows(Filter(...))`, qui peut etre limite par le seuil de delegation SharePoint sur de grands volumes.
- Les conversions `DateValue(Text(...))` ont ete supprimees. Les filtres dates utilisent maintenant des bornes date/heure (`>= Today()` et `< DateAdd(...)`).

## E. Validation finale

- Les quatre fichiers YAML sont parses avec PyYAML sans erreur.
- Les blocs `Properties` et `Children` ont ete controles.
- 1 580 formules Power Fx ont ete controlees pour l'equilibrage des parentheses, crochets et accolades.
- Aucun caractere HTML encode (`&amp;`, `&lt;`, `&gt;`, `&quot;`, `&#39;`) ne subsiste.
