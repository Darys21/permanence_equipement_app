# EXEMPLE rapport alignment minimum

1. **Audit 4 YAML** (Concept pages/*) contre backend/contextBD.md.
2. **Avant corrections (2026-09-07)**:
   - 8 erreurs bloquantes détectées : Date_travaux ↔ DateTravaux, Titre ↔ Title, Poste.Value sur texte, Patch(Filter(...) syntaxe invalide, StatutContact booléen au lieu choix, colonnes inventées NumeroContact.
3. **Après corrections**:
   - Colonnes: 100% cohérentes avec Backend/contextBD.md sections 1-6.
   - Galleries: filtre Poste=varQuart & date du jour sur TOUTES listes transactionnelles.
   - Patch: Audit 3 colonnes (Agent/Poste/DateSaisie) systématiques sur 4 Patch Tx_*.
4. **Vérifier**: si export Graph API (sharepoint-graph-schema) montre CantonID type Lookup natif → corriger Power Fx de nouveau vers {Id, Value}.
