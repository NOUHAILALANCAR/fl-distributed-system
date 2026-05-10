# Federated Learning - Système Distribué

**Projet de Systèmes Distribués**  
**Équipe** : Basma LAHMIMSI • Mariam AIROUQUI • Nouhaila LANCAR • Yahya MIHNANE • Taib MOUTASAOUI  
**Année universitaire** : 2024 – 2025

##  Description

Implémentation complète d’un système d’**Apprentissage Fédéré (Federated Learning)** avec l’algorithme **FedAvg**, architecture client-serveur distribuée, tolérance aux pannes et monitoring en temps réel.

##  Fonctionnalités Implémentées

- **Apprentissage Fédéré** : FedAvg avec pondération selon la taille des datasets
- **Tolérance aux pannes** :
  - Quorum minimum
  - Heartbeats
  - Retry avec backoff exponentiel
  - Checkpointing
  - Détection des gradients byzantins (norme L2)
- **Simulation de pannes** (déconnexion, perte de paquets, crash serveur)
- **Synchronisation** : Horloges logiques de Lamport
- **Monitoring** : Temps réel avec Loguru
- **Déploiement** : Docker + docker-compose

##  Lancement Rapide

```bash
# 1. Cloner le repo
git clone <ton-repo>
cd fl-distributed-system

# 2. Lancer le système
docker-compose up --build
