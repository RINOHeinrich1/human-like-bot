from browser import open_chrome_with_url
from config import IMAGES, URL_LINKEDIN,CREDENTIALS,MAX_SCROLL,EMAIL_LOGIN,SEARCH_QUERY
from automation import *
from logger import setup_logger
import time
import pyautogui
import webbrowser
logger = setup_logger()

def verifier_connexion(timeout=10, interval=0.5):
    """
    Vérifie la présence de l'image 'compte_connecte' à l'écran avec un timeout.
    
    Args:
        timeout (int): Durée maximale en secondes pour attendre l'apparition de l'image.
        interval (float): Intervalle en secondes entre chaque tentative.

    Returns:
        bool: True si l'image est détectée dans le délai imparti, sinon False.
    """
    logger.info(f"⏳ Vérification de l'état de connexion pendant maximum {timeout} secondes...")
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            location = pyautogui.locateOnScreen(IMAGES["compte_connecte"], confidence=0.8)
        except pyautogui.ImageNotFoundException:
            location = None
        except Exception as e:
            logger.warning(f"❌ Erreur pendant locateOnScreen : {e}")
            location = None

        if location:
            logger.info("✅ Déjà connecté.")
            return True

        time.sleep(interval)

    logger.warning("❌ Non connecté après le délai imparti.")
    return False


# ==========================
# Script principal
# ==========================
url = "https://www.linkedin.com/home"
def main():
    open_chrome_with_url(URL_LINKEDIN)
    time.sleep(5)
    if not verifier_connexion():
            # Rediriger vers la bonne URL si EMAIL_LOGIN est True
                if EMAIL_LOGIN:
                    webbrowser.open("https://www.linkedin.com/checkpoint/lg/sign-in-another-account")
                    logger.info("Redirection vers la page de connexion email spécifique.")
                    time.sleep(5)  # laisse le temps de charger la page

                    # === CHAMP EMAIL ===
                    if click_on_image(IMAGES.get("email_preconfiguree"),10):
                        logger.info("Champ email préconfiguré détecté.")
                        pyautogui.hotkey("ctrl", "a")
                        time.sleep(0.2)
                        copy_paste(CREDENTIALS["email"])
                        pyautogui.press("esc")
                        time.sleep(3)
                        copy_paste(CREDENTIALS["password"])
                        
                        
                    elif click_on_image(IMAGES.get("email_non_configuree"),10):
                        logger.info("Champ email non préconfiguré détecté.")
                        copy_paste(CREDENTIALS["email"])
                        logger.info("Champ mot de passe non préconfiguré détecté.")
                        copy_paste(CREDENTIALS["password"])
                        pyautogui.press("esc")
                    else:
                        logger.error("Champ email non détecté.")
                        return

                    time.sleep(5)
                else:
                    # Après saisie, cliquer sur le bouton connexion
                    if click_on_image(IMAGES.get("connexion"),10):
                        time.sleep(2)
                        if not click_on_image(IMAGES.get("mon_compte"),10):
                            logger.error("Connexion échouée.")
                            return
                    else:
                        logger.error("Bouton connexion non détecté.")
                        return

    if click_on_image(IMAGES["barre_recherche"], timeout=10):
        copy_paste(SEARCH_QUERY)
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
                max_scrolls=MAX_SCROLL,
                interval=3
            )
            result = click_on_image(IMAGES["personne_suivant"], timeout=5)
            #print(f"🎯 Résultat click_on_image: {result}")
            if result:
                logger.info("➡️ Bouton 'personne suivant' cliqué. Passage à la page suivante...")
                time.sleep(3)
            else:
                logger.info("⛔️ Plus de page suivante trouvée. Il se peut que votre limite mensuels soit atteint opter pour linkedin premium")
                break
    else:
        logger.error("❌ Barre de recherche introuvable.")

if __name__ == "__main__":
    main()