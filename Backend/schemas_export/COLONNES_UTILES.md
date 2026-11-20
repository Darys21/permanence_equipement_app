# RÉSUMÉ COLONNES UTILES BACKEND PAR LISTE - Pour contexte LLM - Source Graph API réel 2026-09-08

# POSTE = CHOIX dans TOUTES listes transactionnelles! → lecture ThisItem.Poste.Value / écriture Poste: {Value: varQuart}
# AGENTSAISIE = PERSONNE type Claims record (pas texte!)
# COLONNES internes (name) sont à utiliser TELLES QUELLES dans YAML / Power Fx (jamais displayName)

---

## Ref_Cantons
- Title: Texte - nom canton
- Division: CHOIX {Division 1, Division 2, Division 3}
- PK_d_x00e9_but: Nombre - PK début
- PK_fin: Nombre - PK fin

## Ref_Acteurs
- Title: Texte - nom / prénom acteur
- Fonction: Texte REQUIRED

## Tx_Travaux (26 cols utiles)
- Title: Texte REQUIRED - identifiant chantier
- Datetravaux: DateTime REQUIRED default Today - DATE TRAVAUX intern Datetravaux (sans underscore, t minuscule!)
- CantonID: Number REQUIRED - FK simple (pas lookup) vers Ref_Cantons.ID
- R_x00e9_gimetravaux: CHOIX {TSDL, VI, DIG, CAT A, CAT B, CAT C, CAT D, ATTACHEMENT}
- ActeurID: Number - FK simple vers Ref_Acteurs.ID
- Heure_demande: DateTime
- Heure_Fin_Prevue: DateTime
- Heures_Autorisee: DateTime (PLURIEL interne Heures_)
- Heure_engagement: DateTime (SINGULIER)
- Heures_Degagement: DateTime (PLURIEL Heures_)
- Heures_Voie_Retablie: DateTime (PLURIEL Heures_)
- Motif_Engagement: Texte 255
- Motifs_Engagement_Tardif: Texte 255 (PLURIEL Motifs_)
- Motif_Degagement_Tardif: Texte 255 (SINGULIER Motif_)
- PK_Debut: Number
- PK_Fin: Number
- Poste: CHOIX REQUIRED {P1, P2, P3}
- AgentSaisie: PERSONNE REQUIRED (Claims / DisplayName / Email)
- DateSaisie: DateTime REQUIRED

## Tx_Feedbacks
- Title: Texte
- TravailID: Number REQUIRED FK → Tx_Travaux.ID
- HeureContact: DateTime REQUIRED
- MoyenCom: CHOIX REQUIRED {Whatsapp, Telephone, Thuraya, Thuraya + Telephone}
- StatutContact: BOOLEAN (pas Choix! → true/false) default true
- Commentaire: Texte multiligne
- Poste: CHOIX REQUIRED {P1, P2, P3}
- AgentSaisie: PERSONNE REQUIRED
- DateSaisie: DateTime
- NumeroContact: Number (additionnel optionnel)
- PK: Texte (additionnel repérage)

## Tx_incidents_Ruptures
- Title: Texte
- DateIncident: DateTime dateOnly
- PK: Texte
- Localisation_Type: CHOIX {Pleinne barre/FD, Pleinne barre/FG, Voie directe en garre}
- Heure_D_x00e9_but: DateTime (é encodé D_x00e9_but)
- Heure_Fin: DateTime
- Etat: CHOIX {Consolidée, Traitée, En cours}
- Commentaires: Texte 255
- CantonID0: LOOKUP NATIF → Ref_Cantons Title {Id, Value} (Nom interne CantonID0!)
- Poste: CHOIX {P1, P2, P3}
- AgentSaisie: PERSONNE
- DateSaisie: DateTime

## Tx_LTV
- Title: Texte
- Motif_Ralentissement: Texte 255
- PK_Debut: Number
- PK_Fin: Number
- Taux: Number (km/h)
- Statut_LTV: CHOIX {Imposée, Supprimée} SANS parenthèses
- Date_imposition: DateTime (i minuscule!)
- Date_Suppression: DateTime (S MAJ!)
- CantonID_: LOOKUP NATIF → Ref_Cantons Title {Id, Value} (Nom interne CantonID_ underscore suffix!)
- ActeurID0: LOOKUP NATIF → Ref_Acteurs ID {Id, Value} (Nom interne ActeurID0 zero suffix!)
- Poste: CHOIX {P1, P2, P3}
- AgentSaisie: PERSONNE
- DateSaisie: DateTime

## Tx_SessionsPermamence
 - DateDebut
 - DateFin
 - Poste
 - PermanentPrincipalID
 - PermanentPrincipalNom
 - PermanentSecondaireID
 - PermanentSecondaireNom 
 - StatutSession
  

---

## RÈGLES 8 POUR FRONT-END POWER APPS YAML
1. Poste = CHOIX partout: TOUJOURS .Value en lecture, {Value: varQuart} en écriture
2. AgentSaisie = PERSONNE: écrire record Claims; lire .DisplayName .Email
3. CantonID0 (Incidents), CantonID_ (LTV), ActeurID0 (LTV) = LOOKUP: {Id, Value} en écriture, .Value en lecture
4. StatutContact = BOOLEAN: comparer "OUI" → bool; pas de {Value:}
5. Noms internes encodés unicode é: PK_d_x00e9_but, Heure_D_x00e9_but, R_x00e9_gimetravaux - utiliser TELS QUELS
6. Pluriel critiques: Heures_Autorisee, Heures_Degagement, Heures_Voie_Retablie, Motifs_Engagement_Tardif
7. Statut_LTV valeurs exactes: Filtrer galleries actives .Value = "Imposée"
8. Filtre galleries TOUJOURS Poste.Value = varQuart (avec .Value car CHOIX!) + date condition Datetravaux Today (Tx_Travaux) / DateIncident Today (Incidents)
