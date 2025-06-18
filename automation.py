from logger import setup_logger
import time
import pyautogui
import keyboard
import pyperclip
import os
from datetime import datetime
def take_screenshot():
    logger = setup_logger()
    try:
        os.makedirs("screenshots", exist_ok=True)
        filename = f"screenshots/screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        logger.info(f"📸 Capture d'écran enregistrée dans {filename}")
        print(f"📸 Capture d'écran enregistrée dans {filename}")
    except Exception as e:
        logger.error(f"❌ Erreur lors de la capture d'écran avec pyautogui : {e}")
        print(f"❌ Erreur lors de la capture d'écran avec pyautogui : {e}")

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

def type_search_query_with_keyboard(query):
    print(f"⌨️ Taper la recherche (avec accents) : {query}")
    keyboard.write(query, delay=0.1)
    keyboard.press_and_release('enter')
    print("🔎 Recherche lancée.")
       
def copy_paste(query):
    print(f"⌨️ Taper la recherche (avec accents) : {query}")
    pyperclip.copy(query)  # Copie dans le presse-papier
    pyautogui.hotkey("ctrl", "v")  # Colle (pour Windows/Linux)
    pyautogui.press("enter")
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
    limite_invitations_hebdomadaire_path,
    limite_invitation_mensuels_path,
    ok_limite_invitations_hebdomadaire,
    max_scrolls=5,
    scroll_amount=-5,
    interval=0.5,
    confidence=0.8,
    initial_wait=3,
):
    """
    Clique sur tous les boutons 'Se connecter' visibles, puis sur 'Envoyer' sans note.
    Si l'invitation est limitée, clique sur 'OK' et continue.
    """
    print(f"⏳ Attente initiale ({initial_wait}s) pour laisser la page charger...")
    time.sleep(initial_wait)

    print(f"🔄 Début du scroll pour cliquer sur {image_connect_path} et envoyer sans note...")
    clicked_positions = set()
    total_connect_clicked = 0
    total_envoyer_clicked = 0
    logger = setup_logger()  # ✅ appel au logger importé

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
                time.sleep(2)  # attendre que la popup se charge

                # Vérifie si la limite est atteinte (gestion d'erreur ajoutée ici)
                try:
                    limite_visible = pyautogui.locateOnScreen(limite_invitations_hebdomadaire_path, confidence=confidence)
                except Exception as e:
                    print(f"⚠️ Erreur locateOnScreen (limite invitations) : {e}")
                    limite_visible = None

                if limite_visible:
                    print("⚠️ Limite d'invitations atteinte détectée.")
                    if click_on_image(ok_limite_invitations_hebdomadaire, timeout=5):
                        print("✅ Bouton 'OK' cliqué après limite atteinte.")
                        continue  # Passe au suivant sans essayer 'Envoyer'
                    else:
                        print("❌ Bouton 'OK' non trouvé après détection de la limite.")
                        continue

                # Sinon, cliquer sur 'Envoyer'
                if click_on_image(image_envoyer_path, timeout=6):
                    total_envoyer_clicked += 1
                    time.sleep(1)
                else:
                    print("❌ Bouton 'Envoyer' non trouvé après 'Se connecter'.")

        if new_clicks == 0:
            print(f"🔍 Aucun nouveau bouton trouvé, scroll...")
            pyautogui.scroll(scroll_amount)
            time.sleep(interval)
        else:
            print(f"🔁 {new_clicks} nouveau(x) clic(s) à l'étape {i+1}.")

    print(f"🎯 Total 'Se connecter' cliqués : {total_connect_clicked}")
    print(f"📤 Total 'Envoyer' sans note : {total_envoyer_clicked}")
    return total_connect_clicked, total_envoyer_clicked
