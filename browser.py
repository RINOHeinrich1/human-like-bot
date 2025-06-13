import subprocess
import platform
import os
import sys
from logger import setup_logger

logger = setup_logger()

def open_chrome_with_url(url):
    system = platform.system()

    try:
        if system == "Windows":
            paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
            ]
            for path in paths:
                if os.path.exists(path):
                    subprocess.Popen([path, url])
                    return
            logger.error("Chrome non trouvé sur Windows.")
            sys.exit(1)

        elif system == "Linux":
            subprocess.Popen(['google-chrome', url])
        elif system == "Darwin":
            subprocess.Popen(['open', '-a', 'Google Chrome', url])
        else:
            logger.error(f"Système non supporté : {system}")
            sys.exit(1)
    except Exception as e:
        logger.error(f"Erreur lors de l'ouverture de Chrome : {e}")
        sys.exit(1)
