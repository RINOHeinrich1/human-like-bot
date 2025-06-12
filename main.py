import pyautogui
import subprocess
import time
import platform
import os
import sys

def open_chrome_with_url(url):
    system = platform.system()

    if system == "Windows":
        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        if not os.path.exists(chrome_path):
            chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        if not os.path.exists(chrome_path):
            print("❌ Chrome non trouvé sur Windows.")
            sys.exit(1)
        subprocess.Popen([chrome_path, url])

    elif system == "Linux":
        try:
            subprocess.Popen(['google-chrome', url])
        except FileNotFoundError:
            try:
                subprocess.Popen(['chromium-browser', url])
            except FileNotFoundError:
                print("❌ Chrome ou Chromium non trouvé sur Linux.")
                sys.exit(1)

    elif system == "Darwin":  # macOS
        subprocess.Popen(['open', '-a', 'Google Chrome', url])

    else:
        print(f"❌ Système non supporté : {system}")
        sys.exit(1)

def click_on_image(image_path, timeout=10, interval=0.5):
    """
    Attend dynamiquement l'apparition de l'image jusqu'à timeout (en secondes).
    """
    print(f"⏳ Recherche de {image_path} pendant maximum {timeout} secondes...")

    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=0.8)
        except pyautogui.ImageNotFoundException:
            # Gestion spécifique si jamais la version de pyautogui le lève
            location = None
        except Exception as e:
            print(f"❌ Erreur inattendue pendant locateOnScreen : {e}")
            location = None

        if location:
            center = pyautogui.center(location)
            pyautogui.moveTo(center.x, center.y, duration=0.5)
            pyautogui.click()
            print(f"✅ {image_path} cliqué.")
            return True

        time.sleep(interval)

    print(f"❌ {image_path} non trouvé après {timeout} secondes.")
    return False
def scroll_and_click_on_image(image_path, max_scrolls=20, scroll_amount=-300, interval=0.5):
    """
    Scrolle l'écran jusqu'à trouver et cliquer sur l'image. scroll_amount < 0 = vers le bas.
    """
    print(f"🔄 Scrolling pour trouver {image_path}...")

    for i in range(max_scrolls):
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=0.8)
        except Exception as e:
            print(f"⚠️ Erreur locateOnScreen: {e}")
            location = None

        if location:
            center = pyautogui.center(location)
            pyautogui.moveTo(center.x, center.y, duration=0.3)
            pyautogui.click()
            print(f"✅ {image_path} trouvé et cliqué après {i + 1} scrolls.")
            return True

        pyautogui.scroll(scroll_amount)
        time.sleep(interval)

    print(f"❌ {image_path} non trouvé après {max_scrolls} scrolls.")
    return False

def type_search_query(query):
    print(f"⌨️ Taper la recherche : {query}")
    pyautogui.write(query, interval=0.1)
    pyautogui.press('enter')
    print("🔎 Recherche lancée.")

# ==========================
# Script principal
# ==========================
url = "https://www.linkedin.com/home"
image_connexion = 'images/bouton_connexion.png'
image_mon_compte = 'images/mon_compte.png'
image_barre_recherche = 'images/barre_de_recherche.png'
image_voir_tous = 'images/voir_tous_les_resultats.png'
image_compte_connecte = 'images/compte_connecte.png'  # à capturer quand déjà connecté
filtre_personnes='images/filtre_personnes.png'
# Ouvre Chrome avec LinkedIn
open_chrome_with_url(url)

# Attend que la page charge
time.sleep(5)

# Vérifie si l'utilisateur est déjà connecté
try:
    print("🔍 Vérification de l'état de connexion...")
    compte_actif = pyautogui.locateOnScreen(image_compte_connecte, confidence=0.8)
except Exception as e:
    print(f"⚠️ Erreur pendant la détection de connexion : {e}")
    compte_actif = None

if compte_actif:
    print("✅ Déjà connecté, passage direct à la recherche.")
else:
    if click_on_image(image_connexion, timeout=10):
        if not click_on_image(image_mon_compte, timeout=10):
            print("❌ Échec de la connexion ou bouton 'Mon compte' introuvable.")
            sys.exit(1)

# Barre de recherche + requête
if click_on_image(image_barre_recherche, timeout=10):
    type_search_query("AMOA france")
   # time.sleep(2)
    if (not click_on_image(filtre_personnes,timeout=10)):
        print("❌ filtre introuvable.")
    #scroll_and_click_on_image(image_voir_tous, max_scrolls=5)
else:
    print("❌ Barre de recherche introuvable.")
