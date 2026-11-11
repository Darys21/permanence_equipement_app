
# Analyse du Projet PERMANANCE EQUIPEMENT & Adaptation du Processus de Développement pour Power Apps

---

## 📋 Partie 1 : Compréhension du Projet (PERMANANCE EQUIPEMENT.pdf)

### Objectif Général
Développer une **application Power Apps unifiée** pour la gestion de la permanence DMI (Direction de la Maintenance de l'Infrastructure) SETRAG, afin de :
- Moderniser et automatiser le suivi des chantiers, des LTV (Limitations Temporaires de Vitesse) et des incidents de la voie
- Fiabiliser la donnée opérationnelle
- Accélérer la prise de décision

### Objectifs Spécifiques
1. **Centralisation et Standardisation de la Saisie**
   - Remplacer le fichier Excel par une interface unique et sécurisée
   - Supprimer les saisies libres redondantes via des données de référence strictes (Cantons, Gares, PK, Équipes)
   - Éliminer les erreurs de frappe, doublons et incohérences de format
2. **Intégrité Relationnelle des Données**
   - Passer de la logique "tableur" à une base de données relationnelle
   - Séparer Master Data, données transactionnelles et historique d'avancement
3. **Automatisation et Clarté Opérationnelle**
   - Automatiser le calcul des indicateurs de temps (durées d'engagement, retards de dégagement)
   - Générer automatiquement les rapports de fin de poste
4. **Exploitation Analytique et Aide à la Décision**
   - Alimenter des dashboards Power BI / GMAO avec des données brutes immédiatement disponibles
   - Analyser le temps moyen en canton, identifier les goulots d'étranglement, suivre les LTV, calculer la récurrence des points de rupture

### Architecture Technique Cible
- **Frontend :** Power Apps (interface utilisateur)
- **Backend :** Listes SharePoint (base de données relationnelle)
- **Automatisation :** Power Automate (flux de travail, alertes mail, rapports)
- **Analytics :** Power BI (tableaux de bord de performance)

---

## 🗄️ Partie 2 : Structure des Listes SharePoint (6 Listes)

### 1. Master Data (Référentiels)
- **Ref_Cantons** : Gares, Divisions, PK (Point Kilométrique)
  - Title : Nom du Canton/Gare (ex: Owendo-Essassa, Andem)
  - Division : Division 1, 2 ou 3
  - PK_Debut : Numérique
  - PK_Fin : Numérique

- **Ref_Acteurs** : Noms et fonctions des agents
  - Title : Nom et Prénom (ex: ATOUMBOU Félix)
  - Fonction : CDIV, CBR, Technicien RR/L, etc.

### 2. Listes Transactionnelles (Opérationnel)
- **Tx_Travaux** : Fenêtres de travaux (1 ligne = 1 fenêtre)
  - Title : Code/description rapide du chantier
  - DateTravaux : Date du jour
  - CantonID : Lien vers Ref_Cantons
  - RegimeTravaux : Choix (TSDL, VI, etc.)
  - ActeurID : Lien vers Ref_Acteurs
  - Timestamps : Heure_Demande, Heure_Fin_Prevue, Heure_Autorisee, Heure_Engagement, Heure_Degagement, Heure_Voie_Retablie
  - Motifs : Motif_Engagement, Motif_Engagement_Tardif, Motif_Degagement_Tardif

- **Tx_Feedbacks** : Historique des points de contact (relation 1-à-plusieurs avec Tx_Travaux)
  - TravailID : ID de la ligne correspondante dans Tx_Travaux
  - HeureContact : Date/Heure exacte du pointage
  - MoyenCom : Choix (WhatsApp, Phone, Thuraya)
  - StatutContact : Choix (OUI / NON)
  - Commentaire : Texte multiple (feedback brut)

- **Tx_Incidents_Ruptures** : Suivi des rails cassés
  - Title : Numéro d'incident/description
  - DateIncident : Date
  - CantonID : Lien vers Ref_Cantons
  - PK : Emplacement précis
  - Localisation_Type : Choix (Pleine barre/FD, Pleine barre/FG, Voie directe en gare, etc.)
  - Heure_Debut / Heure_Fin : Date/Heure
  - Etat : Choix (Consolidée, Traitée, En cours)
  - Commentaires : Texte

- **Tx_LTV** : Limitations de vitesse
  - Title : ID/motif
  - Motif_Ralentissement : Texte
  - CantonID : Lien vers Ref_Cantons
  - PK_Debut / PK_Fin : Numérique
  - Taux : Numérique (ex: 30 pour 30 km/h)
  - ActeurID : Lien vers Ref_Acteurs
  - Statut_LTV : Choix (Imposée (Active) / Supprimée (Levée))
  - Date_Imposition / Date_Suppression : Date/Heure

---

## 📱 Partie 3 : Écrans de l'Application Power Apps

### Écran 1 : Prise de Poste & Relève
- Auto-identification via compte Microsoft 365
- Sélection du quart : P1 (06h-14h), P2 (14h-22h), P3 (22h-06h)
- Récupération automatique des chantiers et LTV non clôturés du poste précédent

### Écran 2 : Journal de Bord Opérationnel
- Saisie guidée des chantiers (menus déroulants en cascade : Division → Canton)
- Automatisation des horodatages et calcul des durées/retards
- Verrous de cohérence temporelle
- Gestion des LTV (ajout/levée)
- Déclaration des ruptures de rail

### Écran 3 : Suivi des Feedbacks Terrain
- Ajout de points de contact horodatés rattachés à un chantier
- Enregistrement du moyen de communication et du statut de réponse

### Écran 4 : Clôture & Relève
- Validation du poste
- Déclenchement automatique d'un flux Power Automate pour générer et envoyer le rapport par mail

---

## 🔄 Partie 4 : Adaptation du Processus de Développement à la Stack Power Platform

Le processus générique (process_developpement_app.pdf) est adapté comme suit pour Power Apps, SharePoint et Power Automate :

### Étape 1 : Idée, problème et objectifs ✅ (Complété)
- Problème principal : Fichier Excel peu fiable, double saisie, erreurs de frappe
- Objectifs métiers définis (centralisation, intégrité, automatisation, analytics)

### Étape 2 : Analyse et spécifications ✅ (Complété via User Stories)
User Stories extraites du PDF :
- [Écran 1] US1.1 : Auto-identification via compte M365
- [Écran 1] US1.2 : Sélection du quart
- [Écran 1] US1.3 : Aspiration des "En Cours"
- [Écran 2] US2.1 : Saisie guidée des chantiers (menus déroulants en cascade)
- [Écran 2] US2.2 : Automatisation des horodatages et calculs
- [Écran 2] US2.3 : Verrous de cohérence temporelle
- [Écran 2] US2.4 : Gestion des LTV
- [Écran 2] US2.5 : Déclaration des ruptures de rail
- [Écran 3] US3.1 : Ajout de feedbacks terrain
- [Écran 4] US4.1 : Validation du poste
- [Écran 4] US4.2 : Automatisation du rapport par mail

### Étape 3 : Design UX / UI et architecture
- Wireframes des 4 écrans
- Validation des parcours utilisateurs
- Finalisation de la structure des 6 listes SharePoint

### Étape 4 : Développement (implémentation)
1. Création des 6 listes SharePoint avec les colonnes et types appropriés
2. Mise en place des relations entre les listes
3. Création de l'application Power Apps :
   - Écran 1 : Prise de Poste
   - Écran 2 : Journal de Bord
   - Écran 3 : Feedbacks Terrain
   - Écran 4 : Clôture et Relève
4. Développement des flux Power Automate :
   - Flux d'envoi du rapport de fin de poste par mail
   - Flux d'alerte en cas de rupture de rail (optionnel)

### Étape 5 : Tests et assurance qualité
- Tests fonctionnels par écran
- Tests d'intégration (Power Apps ↔ SharePoint ↔ Power Automate)
- Tests utilisateurs beta avec des permanents DMI

### Étape 6 : Déploiement et mise en production
- Partage de l'application Power Apps avec les utilisateurs concernés
- Configuration des permissions sur les listes SharePoint
- Formation des utilisateurs

### Étape 7 : Maintenance, monitoring et évolutions
- Suivi de l'usage et des retours utilisateurs
- Mises à jour régulières de l'application et des listes
- Évolution du dashboard Power BI

 

---

## Addendum — état réel des écrans au 11/11/2026

Cet addendum actualise les hypothèses historiques ci-dessus. En cas de contradiction, le présent addendum, le backlog et les exports YAML synchronisés font foi.

### Parcours actuel

1. **Identification agent — `scrIdentificationAgent`** : sélection du permanent dans `Ref_Permanents`, saisie d'un PIN, contrôle et mise à jour du statut actif.
2. **Prise de poste — `PrisePoste_2`** : suggestion horaire et choix manuel P1/P2/P3 ; consultation des travaux, LTV et incidents à reprendre.
3. **Journal — `JournalDeBord_3`** : onglets Travaux, Incidents/Ruptures et LTV/RAL.
4. **Feedback — `scrFeedback`** : pointage terrain rattaché à un événement Travaux.
5. **Clôture — `scrCloture_2`** : synthèse, commentaire, transmission et confirmation.

### Corrections de conception par rapport à l'analyse initiale

- L'auto-identification M365 décrite dans la première version n'est plus le parcours retenu : le parcours courant utilise sélection du permanent + PIN.
- P1, P2 et P3 sont conservés. Les notes historiques demandant la suppression de P3 sont obsolètes au regard de la version actuelle.
- Le deuxième permanent est facultatif.
- L'écran de feedback est un écran distinct.
- Les écrans et leurs exports YAML sont documentés dans `Frontend/`.

### État fonctionnel prudent

La création Travaux a été confirmée fonctionnelle lors des tests précédents. La modification Travaux doit préserver l'ID SharePoint et reste à corriger/ret tester selon les anomalies signalées ensuite. La création et la reprise LTV restent à fiabiliser. Les incidents doivent être audités. La clôture et la transmission automatique ne sont pas considérées comme terminées tant que le transfert SharePoint et le rapport automatisé n'ont pas été testés.

Voir `BACKLOG.md` et `Documentation/ETAT_AVANCEMENT_2026-11-11.md` pour le suivi opérationnel.
