# Product Backlog - Mini-Projet Systèmes Distribués (Federated Learning)

**Équipe** : Basma LAHMIMSI - Mariam AIROUQUI - Nouhaila LANCAR - Yahya MIHNANE - Taib MOUTASAOUI  
**Année** : 2024 – 2025

---

## 🎯 Objectif Général
Implémenter un système d’Apprentissage Fédéré (FedAvg) distribué, robuste et tolérant aux pannes, tout en respectant les contraintes de confidentialité des données.

---

## 📋 User Stories / Tâches

### Phase 1 : Architecture de Base (Terminée)
- [x] Conception de l’architecture Client-Serveur
- [x] Implémentation de la communication via Sockets TCP
- [x] Définition et entraînement du modèle (SimpleCNN avec PyTorch)
- [x] Implémentation de l’algorithme **FedAvg**

### Phase 2 : Fonctionnalités Distribuées (Terminée)
- [x] Gestion dynamique des clients (enregistrement)
- [x] Distribution du modèle global
- [x] Entraînement local sur données hétérogènes
- [x] Agrégation pondérée des poids
- [x] Monitoring en temps réel (Loguru + métriques)

### Phase 3 : Tolérance aux Pannes & Résilience (Terminée)
- [x] Mise en place du **Quorum** (ex: minimum 3 clients sur 5)
- [x] **Heartbeat** pour détecter les clients déconnectés
- [x] **Retry avec backoff exponentiel** en cas de perte de paquets
- [x] **Checkpointing** du modèle global
- [x] Détection des clients **Byzantins** (via norme L2)
- [x] Simulation de pannes (déconnexion client, perte paquets, crash serveur)

### Phase 4 : Synchronisation & Théorie
- [x] Utilisation des **horloges logiques de Lamport** dans les messages
- [x] Étude du **Théorème CAP** (choix AP)
- [x] Gestion de la cohérence éventuelle

### Phase 5 : Déploiement & Documentation (En cours / À finaliser)
- [x] Dockerisation (Dockerfile + docker-compose)
- [x] Scripts de simulation de pannes
- [ ] Tests unitaires et d’intégration
- [x] Visualisation des résultats (Accuracy / Loss)
- [x] README.md détaillé
- [ ] Rapport final (déjà bien avancé)

---

## 📊 Critères de Validation (selon le cahier des charges du prof)

| Critère | Statut | Commentaire |
|--------|-------|-----------|
| Système distribué réel (non centralisé) | ✅ | Client-Serveur + Sockets |
| Simulation des pannes + solutions | ✅ | Déconnexion, perte paquets, crash, byzantin |
| Étude approfondie (CAP, Lamport, etc.) | ✅ | Présent dans le rapport |
| GitHub Project + Backlog clair | ✅ | Ce fichier |
| Code propre + Docker | ✅ | Structure modulaire |
| Rapport complet (théorie + pratique) | ✅ | Rapport fourni |

---

## 🚀 Perspectives d’Amélioration (Bonus)

- Passage de Sockets vers **gRPC**
- Ajout de **Differential Privacy**
- **Secure Aggregation**
- Utilisation de **Raft** pour le consensus
- Déploiement sur Kubernetes / Cloud

---

**Dernière mise à jour** : 10 Mai 2026
