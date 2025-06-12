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

def scroll_and_click_all_instances(image_path, max_scrolls=20, scroll_amount=-300, interval=0.5, confidence=0.8):
    """
    Scrolle l'écran et clique sur toutes les occurrences de l'image trouvées.
    Évite de cliquer plusieurs fois sur la même.
    """
    print(f"🔄 Scroll pour cliquer sur toutes les occurrences de {image_path}...")
    clicked_positions = set()
    total_clicked = 0

    for i in range(max_scrolls):
        try:
            locations = list(pyautogui.locateAllOnScreen(image_path, confidence=confidence))
        except Exception as e:
            print(f"⚠️ Erreur locateAllOnScreen : {e}")
            locations = []

        new_clicks = 0
        for location in locations:
            center = pyautogui.center(location)
            pos_key = (center.x, center.y)

            if pos_key not in clicked_positions:
                pyautogui.moveTo(center.x, center.y, duration=0.3)
                pyautogui.click()
                clicked_positions.add(pos_key)
                total_clicked += 1
                new_clicks += 1
                print(f"✅ Clic sur {pos_key}")
                time.sleep(0.4)  # Laisse LinkedIn charger les pop-ups

        if new_clicks == 0:
            # Aucun nouveau bouton trouvé, continue de scroller
            pyautogui.scroll(scroll_amount)
            time.sleep(interval)
        else:
            print(f"🔁 {new_clicks} nouvelle(s) occurrence(s) cliquée(s) à l'étape {i+1}.")

    print(f"🎯 {total_clicked} bouton(s) cliqué(s) au total.")
    return total_clicked

def type_search_query(query):
    print(f"⌨️ Taper la recherche : {query}")
    pyautogui.write(query, interval=0.1)
    pyautogui.press('enter')
    print("🔎 Recherche lancée.")
    
def click_all_instances_of_image(image_path, confidence=0.8):
    """
    Clique sur toutes les instances visibles de l'image à l'écran.
    """
    print(f"🔍 Recherche de toutes les occurrences de {image_path}...")
    try:
        locations = list(pyautogui.locateAllOnScreen(image_path, confidence=confidence))
    except Exception as e:
        print(f"❌ Erreur pendant locateAllOnScreen : {e}")
        return 0

    if not locations:
        print("❌ Aucune occurrence trouvée.")
        return 0

    count = 0
    for location in locations:
        center = pyautogui.center(location)
        pyautogui.moveTo(center.x, center.y, duration=0.3)
        pyautogui.click()
        print(f"✅ Cliquez sur une occurrence à {center}")
        count += 1
        time.sleep(0.5)  # Petite pause pour éviter les blocages

    print(f"✅ {count} bouton(s) 'Se connecter' cliqué(s).")
    return count
def se_connecter_sans_note(
    image_connect_path,
    image_envoyer_path,
    image_personne_suivant_path,
    max_scrolls=20,
    scroll_amount=-80,
    interval=0.5,
    confidence=0.8,
    initial_wait=3,
    wait_after_personne_suivant=3,
):
    """
    Clique sur tous les boutons 'Se connecter' visibles, puis sur 'Envoyer' sans note.
    Si plus aucun nouveau bouton n'est trouvé, clique sur 'personne_suivant'.
    """
    print(f"⏳ Attente initiale ({initial_wait}s) pour laisser la page charger...")
    time.sleep(initial_wait)

    print(f"🔄 Début du scroll pour cliquer sur {image_connect_path} et envoyer sans note...")
    clicked_positions = set()
    total_connect_clicked = 0
    total_envoyer_clicked = 0

    for i in range(max_scrolls):
        try:
            locations = list(pyautogui.locateAllOnScreen(image_connect_path, confidence=confidence))
        except Exception as e:
            print(f"⚠️ Erreur locateAllOnScreen : {e}")
            locations = []

        new_clicks = 0
        for location in locations:
            center = pyautogui.center(location)
            pos_key = (center.x, center.y)

            if pos_key not in clicked_positions:
                pyautogui.moveTo(center.x, center.y, duration=0.3)
                pyautogui.click()
                clicked_positions.add(pos_key)
                total_connect_clicked += 1
                new_clicks += 1
                print(f"✅ 'Se connecter' cliqué à {pos_key}")
                time.sleep(2)  # attendre que la popup se charge un peu plus longtemps

                if click_on_image(image_envoyer_path, timeout=6):
                    total_envoyer_clicked += 1
                    time.sleep(1)
                else:
                    print("❌ Bouton 'Envoyer' non trouvé après 'Se connecter'.")

        if new_clicks == 0:
            print(f"🔍 Aucun nouveau bouton trouvé, scroll...")
            pyautogui.scroll(scroll_amount)
            time.sleep(interval)

            if click_on_image(image_personne_suivant_path, timeout=4):
                print("➡️ Bouton 'personne suivant' cliqué.")
                time.sleep(wait_after_personne_suivant)
        else:
            print(f"🔁 {new_clicks} nouveau(x) clic(s) à l'étape {i+1}.")

    print(f"🎯 Total 'Se connecter' cliqués : {total_connect_clicked}")
    print(f"📤 Total 'Envoyer' sans note : {total_envoyer_clicked}")
    return total_connect_clicked, total_envoyer_clicked

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
se_connecter='images/se_connecter.png'
envoyer_sans_note='images/envoyer_sans_note.png'
personne_suivant='images/personne_suivant.png'
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
    se_connecter_sans_note(se_connecter,envoyer_sans_note,personne_suivant,interval=3)
    #scroll_and_click_on_image(image_voir_tous, max_scrolls=5)
else:
    print("❌ Barre de recherche introuvable.")
