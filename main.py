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

def click_on_image(image_path, delay=5, max_attempts=10):
    print(f"⏳ Attente {delay} sec avant de chercher {image_path}...")
    time.sleep(delay)

    for attempt in range(max_attempts):
        print(f"🔍 Tentative {attempt + 1}/{max_attempts} : recherche de {image_path}...")
        location = pyautogui.locateOnScreen(image_path, confidence=0.8)
        if location:
            center = pyautogui.center(location)
            pyautogui.moveTo(center.x, center.y, duration=0.5)
            pyautogui.click()
            print(f"✅ {image_path} cliqué.")
            return True
        time.sleep(1)

    print(f"❌ {image_path} non trouvé après {max_attempts} tentatives.")
    return False

# ==========================
# Script principal
# ==========================
url = "https://www.linkedin.com/home"
image_connexion = 'images/bouton_connexion.png'
image_mon_compte = 'images/mon_compte.png'

open_chrome_with_url(url)

if click_on_image(image_connexion, delay=7):
    # Attendre le chargement après clic sur connexion
    time.sleep(5)
    click_on_image(image_mon_compte, delay=2)
