# Alignement BASE Excel vs backend Graph export
Excel: `PERMANENCE EQUIPEMENT 2026 v4.xlsx` - Sheets: RECAP POSTE , RECAP POSTE 2, Feuil1, Feuil2, RECAP JOURNEES TRAVAUX, FEEDBACK, POINT DE RUPTURES FEVRIER 2026 , GLOBALE LTV 2026, LISTES, TEMPS MOYEN EN CANTON, ENG.-DEG. TARDIFS

## Valeurs Graph Choix backend
- `Ref_cantons.Division` : Division 1 / Division 2 / Division 3
- `Tx_Feedbacks.MoyenCom` : Whatsapp / Telephone / Thuraya / Thuraya + Telephone
- `Tx_Feedbacks.Poste` : P1 / P2 / P3
- `Tx_incidents_Ruptures.Localisation_Type` : Pleinne barre/FD / Pleinne barre/FG / Voie directe en garre
- `Tx_incidents_Ruptures.Etat` : Consolidée / Traitée / En cours
- `Tx_incidents_Ruptures.Poste` : P1 / P2 / P3
- `Tx_LTV.Statut_LTV` : Imposée / Supprimée
- `Tx_LTV.Poste` : P1 / P2 / P3
- `Tx_Travaux.R_x00e9_gimetravaux` : TSDL / VI / DIG / CAT A / CAT B / TAC / TAV
- `Tx_Travaux.Poste` : P1 / P2 / P3

## Extraction brute Sheets Excel

### Sheet: RECAP POSTE 
```
 | RECAPITULATIF PERMANENCE EQUIPEMENT |  |  |  |  |  | 2025-12-25 00:00:00 |  | RECAPITULATIF PERMANENCE EQUIPEMENT |  |  |  | 
 | P1 (06:00/14:00) |  |  | ATOUMBOU Félix |  |  | 1900-01-05 00:00:00 |  | P2 (14:00/22:00) |  |  | ATOUMBOU Félix | 
 | Division | INCIDENT |  |  |  |  |  |  | Division | INCIDENT |  |  | 
 |  | Rupture de rail |  |  |  |  |  |  |  | Rupture de rail |  |  | 
 |  | PK | Localisation | Canton | Debut | Fin | Temps d'intervention |  |  | PK | Localisation | Canton | Debut
 |  |  |  |  |  |  | 00:00:00 |  |  |  |  |  | 
 |  |  |  |  |  |  | 00:00:00 |  |  |  |  |  | 
 |  |  |  |  |  |  | 00:00:00 |  |  |  |  |  | 
 |  |  |  |  |  |  | 00:00:00 |  |  |  |  |  | 
 |  |  |  |  |  |  | 00:00:00 |  |  |  |  |  | 
 | BALANCEMENT ANORMAL |  |  |  |  |  |  |  | BALANCEMENT ANORMAL |  |  |  | 
 | Division | PK | Canton | Remarques: |  |  |  |  | Division | PK | Canton | Remarques: | 
 |  |  |  | AUCUN BALANCEMENT SIGNALE |  |  |  |  |  |  |  | AUCUN BALANCEMENT SIGNALE | 
 | AUTRES |  |  |  |  |  |  |  | AUTRES |  |  |  | 
 | Division | Motif du ralentissement | PK | Canton | Remarques: |  |  |  | Division | Motif du ralentissement | PK | Canton | Remarques:
 |  |  |  |  | AUCUN AUTRE EVENEMENT SIGNALE |  |  |  |  |  |  |  | AUCUN AUTRE EVENEMENT SIGNALE
 | RALENTISSEMENTS |  |  |  |  |  |  |  | RALENTISSEMENTS |  |  |  | 
 | Ralentissements Imposés |  |  |  |  |  |  |  | Ralentissements Imposés |  |  |  | 
 | Division | Motif du ralentissement | PK début | PK fin | Canton | Taux | Qui imposé? |  | Division | Motif du ralentissement | PK début | PK fin | Canton
 |  |  |  |  |  |  |  |  | Division 1 | Défaut Géométrique de la Voie | 142700 | 142800 | Oyan -Abanga
```

### Sheet: RECAP POSTE 2
```
 | RERECAPITULATIF PERMANECE DMI |  |  |  |  |  | 2026-06-16 00:00:00 |  | RERECAPITULATIF PERMANECE DMI |  |  |  | 
 | P1 (06:00-14:00) |  |  | OYANE NZAMBA Rosy |  |  | Mardi |  | P2 (14:00-22:00) |  |  | OBOUNE NGUEMA Jean Cedric | 
 | Division | INCIDENT |  |  |  |  |  |  | Division | INCIDENT |  |  | 
 |  | Rupture de rail |  |  |  |  |  |  |  | Rupture de rail |  |  | 
 |  | PK | Localisation | Canton | Début | Fin | Temps d'intervention |  |  | PK | Localisation | Canton | Début
 |  |  |  |  |  |  |  |  | 3 | 602+469 | Pleine barre/FD | M'boungou-Moanda | 
 |  |  |  |  |  |  |  |  | 2 | 218+210 | Pleine barre/FG | Alembé-Otoumbi | 15:17:00
 |  |  |  |  |  |  |  |  | 3 | 605+970 | Pleine barre/FD | M'boungou-Moanda | 17:25:00
 | BALANCEMENT ANORMAL |  |  |  |  |  |  |  | BALANCEMENT ANORMAL |  |  |  | 
 | Division | PK | Canton | Remarques |  |  |  |  | Division | PK | Canton | Remarques | 
 |  |  |  |  |  |  |  |  |  |  |  | RAS | 
 | AUTRES SITUATIONS |  |  |  |  |  |  |  | AUTRES SITUATIONS |  |  |  | 
 | Division | Motif | PK | Canton | Remarques |  |  |  | Division | Motif | PK | Canton | Observation
 |  |  |  |  |  |  |  |  |  |  |  |  | 
 |  |  |  |  |  |  |  |  |  |  |  |  | RAS
 | RALENTISSEMENTS |  |  |  |  |  |  |  | RALENTISSEMENTS |  |  |  | 
 | Ralentissements Imposés |  |  |  |  |  |  |  | Ralentissements Imposés |  |  |  | 
 | Division | Motif du ralentissement | PK début | PK Fin | Canton | Taux | Acteurs |  | Division | Motif du ralentissement | PK début | PK Fin | Canton
 |  |  |  |  |  |  |  |  | 2 | Rupture de Rail | 218+200 | 218+300 | Alembé-Otoumbi
 |  |  |  |  |  |  |  |  | 3 | Rupture de Rail | 605+900 | 606+000 | M'boungou-Moanda
```

### Sheet: Feuil1
```
DATES | 2026-05-12 00:00:00 |  |  |  |  |  |  |  |  |  |  |  | 
SEMAINES | (Tous) |  |  |  |  |  |  |  |  |  |  |  | 
MOIS | (Tous) |  |  |  |  |  |  |  |  |  |  |  | 
ANNEE | (Tous) |  |  |  |  |  |  |  |  |  |  |  | 
Étiquettes de lignes | Somme de HEURE AUTORISEE 01 | Nombre de HEURE FIN PREVUE 01 | Somme de HEURE ENGAGEMENT 01 | Somme de VOIE RETABLIE 01 | ENGAGEMENT TARDIF | DEGAGEMENT TARDIF |  |  |  | CANTON | H AUTORISEE | H FIN PREVUE | H ENGAGEMENT
Abanga - Ndjolé | 08:39:00 | 1900-01-01 00:00:00 | 08:50:00 | 21:10:00 | 00:11:00 | 02:47:00 |  |  |  | Triage |  |  | 
Alembé | 14:02:00 | 1900-01-01 00:00:00 | 14:25:00 | 17:30:00 | 00:23:00 | 00:00:00 |  |  |  | Voie DMAT |  |  | 
Andem - Mbel | 10:43:00 | 1900-01-01 00:00:00 | 11:00:00 | 19:58:00 | 00:17:00 | 01:25:00 |  |  |  | Owendo / Virié |  |  | 
Bissouma | 12:14:00 | 1900-01-01 00:00:00 | 12:20:00 | 15:03:00 | 03:02:00 | 01:45:00 |  |  |  | Owendo - Essassa | 09:20:00 | 1900-01-01 00:00:00 | 10:05:00
Bissouma - Ayem | 09:20:00 | 1900-01-01 00:00:00 | 11:14:00 | 17:17:00 | 01:54:00 | 00:06:00 |  |  |  | Essassa | 10:28:00 | 1900-01-01 00:00:00 | 11:30:00
Booué | 13:41:00 | 1900-01-01 00:00:00 | 13:57:00 | 15:56:00 | 00:16:00 | 00:00:00 |  |  |  | Essassa - Ntoum | 08:36:00 | 1900-01-01 00:00:00 | 08:57:00
Doumé - Lifouta | 08:09:00 | 1900-01-01 00:00:00 | 08:25:00 | 20:50:00 | 00:16:00 | 00:50:00 |  |  |  | Ntoum |  |  | 
Essassa | 10:28:00 | 1900-01-01 00:00:00 | 11:30:00 | 13:40:00 | 01:02:00 | 00:00:00 |  |  |  | Ntoum - Andem | 11:02:00 | 1900-01-01 00:00:00 | 11:32:00
Essassa - Ntoum | 08:36:00 | 1900-01-01 00:00:00 | 08:57:00 | 17:24:00 | 00:21:00 | 01:00:00 |  |  |  | Andem |  |  | 
Ivindo - Mouyabi | 12:00:00 | 1900-01-01 00:00:00 | 12:16:00 | 21:00:00 | 00:16:00 | 03:00:00 |  |  |  | Andem - Mbel | 10:43:00 | 1900-01-01 00:00:00 | 11:00:00
Lastourville | 08:52:00 | 1900-01-01 00:00:00 | 09:05:00 | 09:47:00 | 00:43:00 | 00:00:00 |  |  |  | Mbel | 1900-01-01 05:13:00 | 1900-01-02 00:00:00 | 1900-01-01 05:59:00
Lifouta - Mboungou B. | 08:47:00 | 1900-01-01 00:00:00 | 08:56:00 | 21:13:00 | 00:09:00 | 00:26:00 |  |  |  | Mbel - Oyan | 14:46:00 | 1900-01-01 00:00:00 | 15:22:00
Mbel | 1900-01-01 05:13:00 | 1900-01-02 00:00:00 | 1900-01-01 05:59:00 | 1900-01-01 13:49:00 | 01:32:00 | 18:00:00 |  |  |  | Oyan | 08:27:00 | 1900-01-01 00:00:00 | 09:00:00
Mbel - Oyan | 14:46:00 | 1900-01-01 00:00:00 | 15:22:00 | 17:56:00 | 00:36:00 | 00:00:00 |  |  |  | Oyan - Abanga | 13:09:00 | 1900-01-01 00:00:00 | 13:12:00
Mboungou B. - Moanda | 10:20:00 | 1900-01-01 00:00:00 | 10:45:00 | 15:46:00 | 00:25:00 | 00:00:00 |  |  |  | Abanga |  |  | 
```

### Sheet: Feuil2
```
 | CANTONS/GARES | HEURE FIN PREVUE 01 | VOIE RETABLIE 01 | ENGAGEMENT TARDIF | DEGAGEMENT TARDIF |  | CANTONS/GARES | TEMPS ENGAGEMENT TARDIF | TEMPS DEGAGEMENT TARDIF
 | Owendo - Essassa | 17:20:00 | 17:25:00 |  | 00:05:00 |  | Owendo - Essassa |  | 00:05:00
 | Essassa - Ntoum | 16:24:00 | 17:24:00 | 00:21:00 | 01:00:00 |  | Essassa - Ntoum | 00:21:00 | 01:00:00
 | Andem - Mbel | 18:33:00 | 19:58:00 | 00:17:00 | 01:25:00 |  | Andem - Mbel | 00:17:00 | 01:25:00
 | Mbel | 19:00:00 | 19:49:00 |  | 00:49:00 |  | Mbel |  | 00:49:00
 | Oyan | 13:00:00 | 14:14:00 | 00:33:00 | 01:14:00 |  | Oyan | 00:33:00 | 01:14:00
 | Abanga - Ndjolé | 18:23:00 | 21:10:00 | 00:11:00 | 02:47:00 |  | Abanga - Ndjolé | 00:11:00 | 02:47:00
 | Ndjolé - Alembé | 17:13:00 | 19:01:00 | 01:13:00 | 01:48:00 |  | Ndjolé - Alembé | 01:13:00 | 01:48:00
 | Bissouma | 16:00:00 | 15:03:00 | 03:02:00 | 01:45:00 |  | Bissouma | 03:02:00 | 01:45:00
 | Bissouma - Ayem | 17:11:00 | 17:17:00 | 01:54:00 | 00:06:00 |  | Bissouma - Ayem | 01:54:00 | 00:06:00
 | Milolé - Lastourville | 18:10:00 | 19:16:00 | 00:28:00 | 01:06:00 |  | Milolé - Lastourville | 00:28:00 | 01:06:00
 | Doumé - Lifouta | 20:00:00 | 20:50:00 | 00:16:00 | 00:50:00 |  | Doumé - Lifouta | 00:16:00 | 00:50:00
 | Lifouta - Mboungou B. | 20:47:00 | 21:13:00 | 00:09:00 | 00:26:00 |  | Lifouta - Mboungou B. | 00:09:00 | 00:26:00
```

### Sheet: RECAP JOURNEES TRAVAUX
```
DATES | JOURS | ANNEE | MOIS | SEMAINES | DIVISIONS | CANTONS/GARES | REGIME TRAVAUX | HEURE DEMANDE 01 | HEURE FIN 01 | ACCORD CGC 01 | HEURE AUTORISEE 01 | HEURE FIN PREVUE 01 | MOTIFS D'ENGAGEMENT
2025-11-25 00:00:00 | jjjj | 2025 | 11 | 48 | Division 01 | Ntoum | DIG | 06:58:00 | 20:00:00 | 07:49:00 | 07:49:00 | 19:00:00 | 
2025-11-25 00:00:00 | jjjj | 2025 | 11 | 48 | Division 01 | Ntoum - Andem | VI | 06:55:00 | 20:00:00 | 07:35:00 | 07:58:00 | 19:35:00 | 
2025-11-25 00:00:00 | jjjj | 2025 | 11 | 48 | Division 01 | Andem - Mbel | VI | 06:55:00 | 20:00:00 | 07:34:00 | 07:42:00 | 19:34:00 | 
2025-11-25 00:00:00 | jjjj | 2025 | 11 | 48 | Division 01 | Mbel | DIG | 09:42:00 | 20:00:00 | 11:06:00 | 11:06:00 | 17:00:00 | 
2025-11-25 00:00:00 | jjjj | 2025 | 11 | 48 | Division 01 | Mbel - Oyan | VI | 07:04:00 | 20:00:00 | 07:40:00 | 08:20:00 | 21:00:00 | 
2025-11-25 00:00:00 | jjjj | 2025 | 11 | 48 | Division 01 | Oyan - Abanga | VI | 07:07:00 | 20:00:00 | 07:42:00 | 08:58:00 | 19:42:00 | 
2025-11-25 00:00:00 | jjjj | 2025 | 11 | 48 | Division 01 | Abanga | DIG | 15:07:00 | 20:30:00 | 15:16:00 | 15:16:00 | 18:00:00 | 
2025-11-25 00:00:00 | jjjj | 2025 | 11 | 48 | Division 01 | Abanga - Ndjolé | VI | 12:41:00 | 20:00:00 | 12:55:00 | 12:59:00 | 19:00:00 | 
2025-11-25 00:00:00 | jjjj | 2025 | 11 | 48 | Division 02 | Otoumbi | DIG | 10:53:00 | 18:30:00 | 11:00:00 | 11:00:00 | 18:30:00 | 
2025-11-25 00:00:00 | jjjj | 2025 | 11 | 48 | Division 02 | Otoumbi - Bissouma | VI | 10:52:00 | 20:00:00 | 10:57:00 | 11:17:00 | 20:00:00 | 
2025-11-25 00:00:00 | jjjj | 2025 | 11 | 48 | Division 02 | Bissouma | DIG | 14:59:00 | 18:00:00 | 15:07:00 | 15:07:00 | 18:00:00 | 
2025-11-25 00:00:00 | jjjj | 2025 | 11 | 48 | Division 02 | Bissouma - Ayem | VI | 09:32:00 | 20:00:00 | 09:38:00 | 09:42:00 | 20:00:00 | 
2025-11-25 00:00:00 | jjjj | 2025 | 11 | 48 | Division 02 | Booué - Ivindo | VI | 10:19:00 | 20:00:00 | 10:24:00 | 10:32:00 | 17:00:00 | 
2025-11-25 00:00:00 | jjjj | 2025 | 11 | 48 | Division 02 | Ivindo | DIG | 11:44:00 | 20:00:00 | 11:48:00 | 11:50:00 | 18:00:00 | 
2025-11-25 00:00:00 | jjjj | 2025 | 11 | 48 | Division 02 | Ivindo - Mouyabi | VI | 16:19:00 | 20:00:00 | 16:30:00 | 16:43:00 | 19:00:00 | 
2025-11-25 00:00:00 | jjjj | 2025 | 11 | 48 | Division 03 | Lastourville | DIG | 09:52:00 | 19:00:00 | 10:15:00 | 10:20:00 | 19:00:00 | 
2025-11-25 00:00:00 | jjjj | 2025 | 11 | 48 | Division 03 | Lastourville - Doumé | VI | 09:03:00 | 23:00:00 | 09:12:00 | 09:26:00 | 23:00:00 | 
2025-11-25 00:00:00 | jjjj | 2025 | 11 | 48 | Division 03 | Doumé - Lifouta | VI | 09:22:00 | 23:00:00 | 09:43:00 | 09:51:00 | 22:00:00 | 
2025-11-25 00:00:00 | jjjj | 2025 | 11 | 48 | Division 03 | Lifouta - Mboungou B. | VI | 13:07:00 | 20:00:00 | 13:14:00 | 13:30:00 | 20:00:00 | 
```

### Sheet: FEEDBACK
```
Dates | Jour | Année | MOIS | Semaine | Régions | Gares ou Cantons | Cantons | Chantiers | Types de Chantier | Acteurs | Monyens Com | Heures Eng | 1er Contact
(3h après Eng)
2026-02-27 00:00:00 | jjjj | 2026 | 2 | 9 | R1 | 2 | Ntoum - Andem | chantier 1 | TX PRN RR |  | WhatsApp |  | 
2026-02-27 00:00:00 | jjjj | 2026 | 2 | 9 | R1 | 2 | Abanga - Ndjolé | chantier 1 | TX Maint R1 | CDT NAWSON NZEMBA | Phone |  | OUI
2026-02-27 00:00:00 | jjjj | 2026 | 2 | 9 | R3 | 2 | Doumé - Lifouta | chantier 1 | TX PRN PTH | CBR MIKOUMA | WhatsApp |  | 
2026-02-28 00:00:00 | jjjj | 2026 | 2 | 9 | R3 | 2 | Moanda - Franceville | chantier 1 | TX Maint R3 | CBR LOSSA | Phone |  | 
2026-03-03 00:00:00 | jjjj | 2026 | 3 | 10 | R1 | 1 | Owendo | chantier 1 | TX Maint Rég1 | CBR EDOU MBA | Phone |  | OUI
2026-03-03 00:00:00 | jjjj | 2026 | 3 | 10 | R1 | 2 | Owendo | chantier 1 | TX Maint Rég1 | CBR EDOU MBA | Phone |  | OUI
2026-03-03 00:00:00 | jjjj | 2026 | 3 | 10 | R1 | 2 | Ntoum - Andem | chantier 1 | TX Maint Rég1 | Technicien RR/L NZAMBA IBINGA | WhatsApp | 13:09:00 | OUI
2026-03-03 00:00:00 | jjjj | 2026 | 3 | 10 | R3 | 2 | Milolé - Lastourville | chantier 1 | TX Maint Rég3 | CDT OBORI | Phone | 13:03:00 | OUI
2026-03-03 00:00:00 | jjjj | 2026 | 3 | 10 | R3 | 2 |  | chantier 2 |  | CBR MOUKETOU |  |  | 
2026-03-03 00:00:00 | jjjj | 2026 | 3 | 10 | R3 | 2 | Doumé - Lifouta | chantier 2 | TX PRN PTH | CBR MIKOUMA | Thuraya | 16:48:00 | OUI
2026-03-03 00:00:00 | jjjj | 2026 | 3 | 10 | R3 | 2 | Lifouta - Mboungou | chantier 2 | TX PRN SMD80 | CBR BIA | Thuraya | 16:05:00 | NON
2026-03-06 00:00:00 | jjjj | 2026 | 3 | 10 | R1 | 1 | Ntoum | chantier 1 | TX PRN RR | CDIV HOSNI | Phone | 10:37:00 | OUI
2026-03-06 00:00:00 | jjjj | 2026 | 3 | 10 | R3 | 2 | Doumé - Lifouta | chantier 3 | TX PRN PTH | NGOYE | Thuraya | 11:27:00 | NON
2026-03-06 00:00:00 | jjjj | 2026 | 3 | 10 | R3 | 2 | Lifouta - Mboungou | chantier 3 | TX PRN SMD80 | OLIVIER | Thuraya | 12:03:00 | OUI
2026-03-10 00:00:00 | jjjj | 2026 | 3 | 11 | R3 | 2 | Doumé - Lifouta | chantier 1 |  | NGOYE | Thuraya | 08:56:00 | OUI
2026-03-10 00:00:00 | jjjj | 2026 | 3 | 11 | R3 | 2 | Lifouta - Mboungou | chantier 1 |  | OLIVIER | Thuraya | 08:12:00 | OUI
2026-03-17 00:00:00 | jjjj | 2026 | 3 | 12 |  |  | Mbel - Oyan | chantier 1 | TX Maint Rég1 | CBR OBAME OLLAME | Phone | 08:53:00 | OUI
2026-03-17 00:00:00 |  |  |  |  |  |  | Mbel - Oyan | chantier 2 |  | CBR PAILLAT |  |  | OUI
2026-03-17 00:00:00 |  |  |  |  |  |  | Abanga - Ndjolé | chantier 1 |  |  | Phone |  | OUI
```

### Sheet: POINT DE RUPTURES FEVRIER 2026 
```
 | SUIVI HEBDOMADAIRE DES RUPTURES DE L'ANNEE 2026 |  |  |  |  |  |  |  |  |  |  |  | 
 | PERMANENCE-DMIV SETRAG |  |  |  |  |  |  |  |  |  |  |  | 
 | Dates | PK | Localisation | Canton | Consoliation |  |  | Etat | Commentaires |  |  |  | 
 |  |  |  |  | Début | Fin | Temps Mis |  | Etat |  |  |  | 
 | DIVISION 01 : OWENDO - ALEMBE |  |  |  |  |  |  |  |  |  |  |  | 
 | 2026-02-01 00:00:00 | 56350 | PB / FG /Plancher Bois  / UIC50 | Andem | 22:32:00 | 22:41:00 | 00:09:00 | Consolidée |  |  |  |  | 
 | 2026-02-03 00:00:00 | 63551 | PB / FG /Plancher Bois  / 
UIC50 | Andem-Mbel | 10:23:00 | 10:31:00 | 00:08:00 | Consolidée | Découverte dans les travaux |  |  |  | 
 | 2026-02-04 00:00:00 | 56166 | PB / FD /Plancher Bois / 
UIC50 | Andem-Mbel | 09:00:00 | 09:11:00 | 00:11:00 | Consolidée | Voie directe en gare d'Andem |  |  |  | 
 | 2026-02-09 00:00:00 | 590776 | PB / FD /Plancher Bois / 
UIC50 | Mboungou-Moanda | 15:11:00 | 15:45:00 | 00:34:00 | Consolidée | Déclarée par le CRL du train 5611 |  |  |  | 
 | 2026-02-16 00:00:00 | 56577 | PB / FD /Plancher Bois / 
UIC50 | Andem | 09:54:00 | 10:20:00 | 00:26:00 | Consolidée |  |  |  |  | 
 |  | 18341 | PB / FD /Plancher Bois / 
UIC50 | Essassa | 14:05:00 | 14:43:00 | 00:38:00 | Consolidée | Découverte par le CS. |  |  |  | 
 |  | 18435 | PB / FD /Plancher Bois / 
UIC50 | Essassa | 14:45:00 | 15:00:00 | 00:15:00 | Consolidée | Découverte par le CBR Edou Mba |  |  |  | 
 | 2026-02-24 00:00:00 | 86+110 | PB / FG /Plancher Bois  / 
UIC50 | Mbel | 07:29:00 | 07:51:00 | 00:22:00 | Consolidée | Découverte par le CS en poste à 06h35. |  |  |  | 
 | 2026-03-11 00:00:00 | 170167 | PB / FD /Plancher Bois / 
UIC50 | Abanga-Ndjolé | 17:20:00 | 19:17:00 | 01:57:00 | Consolidée | Pose d'un coupon de 5ml |  |  |  | 
 | 2026-03-13 00:00:00 | 35817 | PB / FG /Plancher Bois  / 
UIC50 | Ntoum | 22:25:00 | 1900-01-01 00:00:00 | 01:35:00 | Consolidée |  |  |  |  | 
 | 2026-03-17 00:00:00 | 54990 | PB / FG /Plancher Bois  / 
UIC50 | Ntoum-Andem | 12:43:00 | 13:00:00 | 00:17:00 | Consolidée |  |  |  |  | 
 | 2026-03-17 00:00:00 | 85085 | PB / FG /Plancher Bois  / 
UIC50 | Mbel | 12:20:00 | 12:30:00 | 00:10:00 | Consolidée |  |  |  |  | 
 | 2026-03-18 00:00:00 | 101614 | Soudure rompue FG/Plancher Béton / U50 | Mbel-Oyan | 13:53:00 | 14:06:00 | 00:13:00 | Consolidée |  |  |  |  | 
 | 2026-03-24 00:00:00 | 85998 | PB / FD /Plancher Bois / 
UIC50 | Gare de Mbel | 02:06:00 | 02:23:00 | 00:17:00 | Consolidée |  |  |  |  | 
 | 2026-04-14 00:00:00 | 181884 | PB / FG /Plancher Bois  / 
UIC50 | Ndjolé | 08:06:00 | 08:45:00 | 00:39:00 | Consolidée |  |  |  |  | 
```

### Sheet: GLOBALE LTV 2026
```
 | S12 | DIRECTION MAINTENANCE INFRASTRUCTURES
DEPARTEMENT BUREAU METHODE VOIE
SERVICE : PERMANENCE DMI
                                                    

                                               LA GLOBALE DES LTV GRANDS TRAVAUX  DU 20/03/2026 |  |  |  |  |  |  |  |  |  |  | 
 | N° | LIMITATIONS TEMPORAIRES DE VITESSE IMPOSEES |  |  |  |  |  |  |  |  |  |  | 
 |  | Divisions | Motif du ralentissement | PK début | PK fin | Canton | Taux | Acteurs DMI |  |  |  |  | 
 | 1 |  |  |  |  |  |  |  |  |  |  |  | 
 | 2 |  |  |  |  |  |  |  |  |  |  |  | 
 | 3 |  |  |  |  |  |  |  |  |  |  |  | 
 | 4 |  |  |  |  |  |  |  |  |  |  |  | 
 | 5 |  |  |  |  |  |  |  |  |  |  |  | 
 | 6 |  |  |  |  |  |  |  |  |  |  |  | 
 | 7 |  |  |  |  |  |  |  |  |  |  |  | 
 | 8 |  |  |  |  |  |  |  |  |  |  |  | 
 | N° |  |  |  |  |  |  | TOTAL : 05 |  |  |  |  | 
 |  | LIMITATIONS TEMPORAIRES DE VITESSE SUPPRIMEES |  |  |  |  |  |  |  |  |  |  | 
 |  | Divisions | Motif du ralentissement | PK début | PK fin | Canton | Taux | Acteurs DMI |  |  |  |  | 
 | 1 |  |  |  |  |  |  |  |  |  |  |  | 
 | 2 |  |  |  |  |  |  |  |  |  |  |  | 
 | 3 |  |  |  |  |  |  |  |  |  |  |  | 
 | 4 |  |  |  |  |  |  |  |  |  |  |  | 
 | 5 |  |  |  |  |  |  |  |  |  |  |  | 
 | 6 |  |  |  |  |  |  |  |  |  |  |  | 
```

### Sheet: LISTES
```
 |  |  |  |  |  |  |  |  |  |  |  |  | 
BR DFIP | District 1 | Nature de l'événement |  | Limites des Cantons repris sur le comptage des unités produites |  |  | CANTON | Position rupture de rail | Période | ATOUMBOU Félix | Affaissement de la voie | REGIME TRAVAUX | NOMS ET PRENOMS
BR 110 | District 1 | Défaut de nivellement |  | Km début | Km fin | Unité | Port - Faisceaux Grumiers | Talonnage d'aiguille n°°01 |  | ATOUMBOU Félix + LABINDAGOMO Gildas | Attente Ballastage + Joints Multiples | TSDL | CDIV NYONDA MINDA
BR TH1 | District 2 | Affaissement de la Voie | DIV 1 | 0 | 1557 | Owendo | Triage | PB / FD /Plancher Bois / 
UIC50 | P1 (06:00/14:00) | ATOUMBOU Félix + MBADINGA  Gluors | Attente Complément Ballast | VI | CDIV SASSI
BR 210 | District 3 | Aiguille |  | 1557 | 18327 | Owendo | Voie DMAT | PB / FG /Plancher Bois  / 
UIC50 | P2 (14:00/22:00) | ATOUMBOU Félix + OBOUNE NGUEMA Jean Cédric | Attente de soudures | DIG | CDIV MAMBOUNDOU
BR 211 | District 3 | Avarie Voie |  | 16726 | 18273 | Owendo | Owendo / Virié | Décrochement de métal / FD/Plancher Bois / UIC50 | P3 (22:00/06:00) | ATOUMBOU Félix +M'FOUO Eddy Olsen | Attente Stabilisation | CAT A | CDT CHAUBI
BR 213 | District 4 | Balancement anormal |  | 18273 | 33560 | Owendo | Owendo - Essassa | Décrochement de métal / FG /Plancher Bois / UIC50 | P2 (15:00/06:00) | ATOUMBOU Félix +OYANE NZAMBA Rosy | Attente travaux RVB | CAT B | CDT NAWSON NZEMBA
BR 214 | District 4 | Balayage de canton |  | 33560 | 35746 | Owendo | Essassa | Soudure rompue FD/Plancher Bois / UIC50 | P2 (18:00/06:00) | EMANE BITHEGUE Loïc + ATOUMBOU Félix | Cœur de l'ADV 14 Défectueux | TAC | CDT OBORI
BR 310 | District 5 | Cés cassés |  | 35746 | 54999 | Owendo | Essassa - Ntoum | Soudure rompue FG/Plancher Mixte / U50 |  | EMANE BITHEGUE Loïc + MANGALA Dorland | Cœur de l'aiguille avarié | TAV | CDT NDONG LITCHANGOU
 | BR TH2 | District 5 | Collision d'un arbustre |  | 54999 | 57184 | Owendo | Soudure rompue FD/Plancher Béton / U50 |  | EMANE BITHEGUE Loïc + MBADINGA  Gluors | Défaut de Nivellement |  | CDT NGUEMA
BR 311 | District 5 | Comportement |  | 57184 | 84107 | Mbel | Ntoum - Andem | PB / FD /Plancher Bois / UIC60 |  | EMANE BITHEGUE Loïc + LABINDAGOMO Gildas | Défaut d'écartement |  | CDT SALA
BR 312 | District 5 | Décrochement de métal |  | 84107 | 86290 | Mbel | Andem | PB / FG /Plancher Bois  / UIC60 |  | M'FOUO Eddy Olsen +EMANE BITHEGUE Loïc | Défaut Géométrique de la Voie |  | CDT KOBANGOYE
BR 313 | District 6 | Défaut de géométrie |  | 86290 | 118623 | Mbel | Andem - Mbel | Décrochement de métal / FD/Plancher Béton / UIC60 |  | LABINDAGOMO Gildas | Défaut géométrique de la voie + joints de raccords |  | CBR MOUSSOUNDA
BR 410 | District 6 | Déformation de la voie |  | 118623 | 119742 | Mbel | Mbel | Décrochement de métal / FG /Plancher Béton / UIC60 |  | LABINDAGOMO Gildas  + M'FOUO Eddy Olsen | Défaut Géométrique de la Voie + Rupture de Rail |  | CBR BIBANA
BR 411 | District 7 | Dégagement tardif |  | 119742 | 148061 | Mbel | Mbel / Makora | Soudure rompue FD/Plancher Béton / UIC60 |  | LABINDAGOMO Gildas  + OBOUNE NGUEMA Jean Cédric | Défaut Géométrique de la voie +Insuffisance de ballast |  | CBR ASSIGNET
BR 511 | District 8 | Déraillement |  | 148061 | 149994 | Ndjolé | Mbel - Oyan | Soudure rompue FG/Plancher Béton / UIC60 | 10 | LABINDAGOMO Gildas + OYANE NZAMBA Rosy | Empreintes de Patinage |  | CBR EDOU MBA
BR 609 | District 9 | Désserage Eclisse |  | 149994 | 183553 | Ndjolé | Oyan | Attente mise en hauteur de la voie | 20 | LABINDAGOMO Gildas +MBADINGA  Gluors | Gauche Hors Tolérence |  | CBR ALLOGHO
BR 611 | District 10 | Détresse |  | 181393 | 183553 | Ndjolé | Oyan - Abanga | Attente soudures | 30 | MANGALA Dorland | Insuffisanse de Ballast |  | CBR EMANE
BR 711 | District 10 | Eboulement |  | 183553 | 201457 | Ndjolé | Abanga |  | 40 | MANGALA Dorland +  OYANE NZAMBA Rosy | Joints de raccord |  | CBR NKOGHO
BR 712 | District 11 | Eclisses desserées |  | 201457 | 202798 | Ndjolé | Abanga - Ndjolé |  | 60 | MANGALA Dorland + ATOUMBOU Félix | Lame de l'ADV défectueuse |  | CBR KASSA
```

### Sheet: TEMPS MOYEN EN CANTON
```
ANNEE | 2026
MOIS | (Tous)
SEMAINES | (Tous)
DATES | (Tous)
Étiquettes de lignes | Temps moyen en canton
Owendo - Essassa | 2:39:15
Ntoum - Andem | 6:22:55.714000
Andem - Mbel | 6:24:18.571000
Mbel - Oyan | 6:02:05.333000
Oyan - Abanga | 4:09:07.500000
Abanga - Ndjolé | 6:47:26.512000
Ndjolé - Alembé | 4:49:51.892000
Alembé - Otoumbi | 4:07:35
Otoumbi - Bissouma | 2:50:41.250000
Bissouma - Ayem | 3:30:22.105000
Essassa - Ntoum | 3:54:09.091000
Ayem - Lopé | 4:28:24.828000
Lopé - Offoué | 3:30:42.500000
Offoué - Booué | 5:08:20.625000
Booué - Ivindo | 4:33:04
```

### Sheet: ENG.-DEG. TARDIFS
```
ANNEE | 2026 | 
MOIS | 6 | 
DATES | 2026-06-19 00:00:00 | 
Étiquettes de lignes | ENGAGEMENTS TARDIFS | DEGAGEMENTS TARDIFS
Essassa - Ntoum | 0:21:00 | 0:13:00
Abanga | 0:06:00 | 0:05:00
Abanga - Ndjolé | 0:33:00 | 0:34:00
Ndjolé | 0:28:00 | 0:35:00
Lifouta - Mboungou B. | 0:07:00 | 0:29:00
Mboungou B. | 0:33:00 | 0:10:00
Mboungou B. - Moanda | 0:05:00 | 0:52:00
Total général | 2:13:00 | 2:58:00
```
