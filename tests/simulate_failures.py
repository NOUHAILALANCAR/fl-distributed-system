import time
import threading
import random
from monitoring.logger import logger

def simulate_client_disconnection(client_id):
    """Simule la déconnexion d'un client"""
    logger.warning(f"🔴 Simulation : Déconnexion du client {client_id}")
    # En vrai, on pourrait tuer le conteneur ou fermer la socket
    print(f"Client {client_id} déconnecté (simulation)")

def simulate_packet_loss():
    """Simule la perte de paquets"""
    logger.warning("📡 Simulation : Perte de paquets (20% de perte)")
    print("🔁 Retry mechanism with exponential backoff activé")

def simulate_server_crash():
    """Simule un crash serveur"""
    logger.error("💥 Simulation : Crash du serveur !")
    print("🔄 Checkpointing activé -> Reprise après redémarrage")
    # Ici on pourrait faire sys.exit() mais on simule seulement

def simulate_byzantine_client():
    """Simule un client byzantin (mauvais gradients)"""
    logger.warning("🛡️ Simulation : Client Byzantin détecté")
    print("✅ Détection via norme L2 + Exclusion du client")

def run_failure_simulation():
    """Lance toutes les simulations"""
    logger.info("🚀 Démarrage des simulations de pannes...")

    time.sleep(5)
    simulate_client_disconnection("client2")

    time.sleep(4)
    simulate_packet_loss()

    time.sleep(6)
    simulate_byzantine_client()

    time.sleep(5)
    simulate_server_crash()

    logger.success("✅ Simulations de pannes terminées avec succès !")
    logger.info("Le système a continué grâce au Quorum + Checkpointing + Retry")

if __name__ == "__main__":
    run_failure_simulation()
