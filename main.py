from browser import open_chrome_with_url
from config import IMAGES, URL_LINKEDIN
from automation import *
from logger import setup_logger
import time
import pyautogui
logger = setup_logger()

def verifier_connexion():
    logger.info("Vérification de l'état de connexion...")
    try:
        if pyautogui.locateOnScreen(IMAGES["compte_connecte"], confidence=0.8):
            logger.info("Déjà connecté.")
            return True
    except Exception as e:
        logger.warning(f"Erreur détection connexion : {e}")
    return False


# ==========================
# Script principal
# ==========================
url = "https://www.linkedin.com/home"
def main():
    open_chrome_with_url(URL_LINKEDIN)
    time.sleep(5)
    if not verifier_connexion():
        if click_on_image(IMAGES["connexion"]):
            if not click_on_image(IMAGES["mon_compte"]):
                logger.error("Connexion échouée.")
                return
    if click_on_image(IMAGES["barre_recherche"], timeout=10):
        copy_paste_search_query("Chasseur de tête Toulouse")
        if not click_on_image(IMAGES["filtre_personnes"], timeout=10):
            logger.error("❌ Filtre 'Personnes' introuvable.")
        else:
            time.sleep(3)  # attendre un peu le filtrage

        # Boucle pour traiter plusieurs pages
        while True:
            se_connecter_sans_note(
                IMAGES["se_connecter"],
                IMAGES["envoyer_sans_note"],
                IMAGES["limite_invitations_hebdo"],
                IMAGES["limite_invitations_mensuels"],
                IMAGES["ok_limite"],
                interval=3
            )

            if click_on_image(IMAGES["personne_suivant"], timeout=5):
                logger.info("➡️ Bouton 'personne suivant' cliqué. Passage à la page suivante...")
                time.sleep(3)  # attendre le chargement de la nouvelle page
            else:
                logger.info("⛔️ Plus de page suivante trouvée.")
                break
    else:
        logger.error("❌ Barre de recherche introuvable.")

if __name__ == "__main__":
    main()