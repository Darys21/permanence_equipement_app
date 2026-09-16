# Écran 3 : Suivi des Feedbacks Terrain & Points de Contact

## 📋 Présentation Générale
Cet écran permet au permanent de documenter les points de contact et feedbacks terrain tout au long du quart de travail. Il s'agit de tracer :
- Les appels reçus/émis auprès des équipes ou autres acteurs
- Les échanges via différents moyens de communication (WhatsApp, téléphone, Thuraya)
- Le statut de réponse/confirmation (OUI/NON)
- Les commentaires bruts du terrain
- L'horodatage exact de chaque interaction

Cet historique est **rattaché à un chantier spécifique** et alimente à la fois la transparence opérationnelle et la traçabilité pour les rapports de fin de poste.

---

## 🎨 Maquette (Référence)
![Maquette Écran Feedback](feedback.png)

---

## 🖼️ Wireframe / Description des Éléments

### Barre supérieure
- Logo **SETRAG ERAMET**
- Titre **PERMANENCE ÉQUIPEMENT**
- Profil utilisateur (email) avec menu déroulant
- Fil d'Ariane : "Écran 2 > Suivi Feedbacks" (contexte de navigation)

### Section 1 : Chantier en Cours
- **Titre du chantier** : Affichage du chantier actif (ex: "Remplacement éclisse - Owendo")
- **Infos rapides** :
  - 📍 **Canton** : Owendo - Essassa
  - 🕐 **Heure d'engagement** : HH:MM
  - 🏗️ **Régime travaux** : TSDL / VI / etc.
- Indication visuelle : barre colorée (orange) à gauche pour rappeler le contexte

### Section 2 : Historique des Points de Contact (Tableau de Feedbacks)
Liste chronologique des feedbacks saisis, en ordre décroissant (plus récents en haut).

Chaque ligne du tableau comporte :
| Colonne | Description |
|---------|-------------|
| **Heure** | HH:MM (ex: 14:30) |
| **Moyen de Comm** | Icône + texte : 📱 WhatsApp / ☎️ Phone / 📡 Thuraya |
| **Statut Contact** | Badge coloré : 🟢 OUI (succès) / 🔴 NON (échec/pas de réponse) |
| **Commentaire** | Extrait du texte (max 60 caractères) avec "Voir plus" si dépassement |
| **Action** | 🗑️ Supprimer / ✏️ Éditer (icônes) |

### Section 3 : Ajout d'un Nouveau Feedback
Formulaire de saisie avec les champs suivants :

1. **Heure de Contact** (obligatoire)
   - Champ date/heure : pré-rempli avec l'heure actuelle
   - Format : HH:MM
   - Bouton "Maintenant" pour auto-remplir l'heure actuelle

2. **Moyen de Communication** (obligatoire)
   - Dropdown : WhatsApp / Phone / Thuraya
   - Icône respective à côté

3. **Statut du Contact** (obligatoire)
   - Groupe de boutons radio ou toggle :
     - ◯ OUI (confirmé, objectif atteint)
     - ◯ NON (pas de réponse, échec, contact perdu)

4. **Commentaire** (optionnel)
   - Champ texte multiligne (300 caractères max)
   - Placeholder : "Saisissez vos observations terrain..."
   - Compteur de caractères visible

5. **Boutons d'action**
   - 🟠 **AJOUTER LE FEEDBACK** (primaire, orange)
   - ⚫ **ANNULER** (secondaire, gris)

---

## 🗄️ Liaison Frontend (Power Apps) ↔ Backend (SharePoint)

| Élément de l'Écran | Liste SharePoint | Colonne(s) SharePoint | Type de Lien |
|---------------------|------------------|-----------------------|--------------|
| Chantier en cours | Tx_Travaux | Title, CantonID, RegimeTravaux, Heure_Engagement | Filtre : chantier actif (sélectionné depuis Écran 2) |
| Infos rapides (Canton) | Ref_Cantons | Title, Division | Lookup via CantonID depuis Tx_Travaux |
| Historique des feedbacks | Tx_Feedbacks | HeureContact, MoyenCom, StatutContact, Commentaire | Filtre : TravailID = ID du chantier en cours |
| Heure de contact | Tx_Feedbacks | HeureContact | Date/Heure (NOW() pour défaut) |
| Moyen de communication | Tx_Feedbacks | MoyenCom | Choix (WhatsApp, Phone, Thuraya) |
| Statut du contact | Tx_Feedbacks | StatutContact | Choix (OUI, NON) |
| Commentaire | Tx_Feedbacks | Commentaire | Texte multiple |
| TravailID (lien parent) | Tx_Feedbacks | TravailID | Lookup vers Tx_Travaux |

---

## 📝 User Stories Associées

| ID | User Story | Critères d'acceptation |
|----|------------|-------------------------|
| US3.1 | En tant que permanent, je veux ajouter des feedbacks horodatés pour tracer tous mes points de contact terrain et justifier mes actions. | - Je peux ajouter un nouveau feedback via un formulaire simple<br>- L'heure est auto-remplie ou je peux la modifier<br>- Je peux choisir le moyen de communication (WhatsApp, Phone, Thuraya)<br>- Je peux indiquer le statut du contact (OUI/NON)<br>- Je peux ajouter un commentaire libre<br>- Les feedbacks s'affichent dans un tableau chronologique<br>- Je peux modifier ou supprimer un feedback<br>- Chaque feedback est rattaché au chantier actif |
| US3.2 (bonus) | En tant que manager DMI, je veux consulter l'historique complet des feedbacks d'un chantier pour évaluer la qualité du suivi opérationnel. | - L'historique est consultable depuis le rapport de fin de poste<br>- Les feedbacks sont triés par heure décroissante<br>- Les statuts sont visuellement distincts (OUI vs NON) |

---

## 🔄 Flux Utilisateur

1. **Navigation vers l'Écran 3** : Depuis l'Écran 2 (Journal de Bord), le permanent clique sur "Ajouter un feedback" ou accède à la section "Suivi des Feedbacks".

2. **Affichage du contexte** : Le chantier en cours (avec ses infos : canton, heure d'engagement, régime) est affiché en haut pour rappeler le contexte.

3. **Consultation de l'historique** : Le tableau des feedbacks précédents pour ce chantier est visible (si des feedbacks existent).

4. **Ajout d'un nouveau feedback** :
   - Le permanent remplit le formulaire avec l'heure, le moyen de communication, le statut et un commentaire optionnel.
   - Il clique sur "AJOUTER LE FEEDBACK".

5. **Validation et sauvegarde** :
   - Les données sont validées (champs obligatoires remplis).
   - Une nouvelle ligne est créée dans Tx_Feedbacks avec le lien vers le chantier actif (TravailID).
   - Un message de confirmation apparaît ("Feedback ajouté avec succès").

6. **Retour et continuité** :
   - Le nouveau feedback apparaît en haut du tableau (plus récent).
   - Le formulaire est réinitialisé pour un nouvel ajout.
   - Le permanent peut continuer à ajouter d'autres feedbacks ou retourner à l'Écran 2.

7. **Édition/Suppression (optionnel)** :
   - Le permanent peut modifier un feedback en cliquant sur ✏️.
   - Le permanent peut supprimer un feedback en cliquant sur 🗑️ (avec confirmation).

---

## 🎯 Objectifs & Bénéfices

✅ **Traçabilité complète** : Chaque interaction est horodatée et documentée.  
✅ **Transparence opérationnelle** : L'historique des contacts justifie les actions du permanent.  
✅ **Intégrité des données** : Les statuts standardisés (OUI/NON) et les moyens de comm. contrôlés évitent les saisies libres redondantes.  
✅ **Aide à la décision** : Les managers peuvent analyser la cadence des contacts et identifier les goulots.  
✅ **Amélioration continue** : Les commentaires terrain alimentent les bases de connaissance et les analyses de performance.

---

## 📋 Notes Techniques

- **Relation avec Tx_Travaux** : Chaque feedback doit obligatoirement être rattaché à un chantier (TravailID non null).
- **Tri** : Les feedbacks sont triés par HeureContact décroissant (plus récents en haut).
- **Validation** : HeureContact et MoyenCom et StatutContact sont obligatoires ; Commentaire est optionnel.
- **Historique immuable** : Une fois créé, un feedback ne doit pas pouvoir être modifié (sauf si business rule différente) ; la suppression peut être restreinte aux admins.
- **Performance** : Si un chantier a beaucoup de feedbacks (> 100), envisager une pagination ou filtre par plage horaire.
