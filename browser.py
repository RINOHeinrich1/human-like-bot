import os
import subprocess
import platform
import sys
from logger import setup_logger

logger = setup_logger()

def open_chrome_with_url(url, fullscreen=True):
    system = platform.system()

    try:
        if system == "Windows":
            paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
            ]
            for path in paths:
                if os.path.exists(path):
                    args = [path]
                    args.append('--lang=fr')  # <-- ajout de la langue française
                    if fullscreen:
                        args.append('--start-fullscreen')
                    args.append(url)
                    subprocess.Popen(args)
                    return
            logger.error("Chrome non trouvé sur Windows.")
            sys.exit(1)

        elif system == "Linux":
            user_data_dir = "/app/chrome-profile"
            os.makedirs(user_data_dir, exist_ok=True)

            args = [
                'google-chrome',
                '--no-sandbox',
                f'--user-data-dir={user_data_dir}',
                '--lang=fr'  # <-- ajout de la langue française
            ]
            if fullscreen:
                args.append('--start-fullscreen')
            args.append(url)
            subprocess.Popen(args)

        elif system == "Darwin":
            # macOS ne gère pas --lang directement via open
            # Tu peux configurer la langue via les préférences système macOS ou dans Chrome manuellement
            subprocess.Popen(['open', '-a', 'Google Chrome', url])
            # Sinon, il faudrait un script AppleScript pour forcer la langue

        else:
            logger.error(f"Système non supporté : {system}")
            sys.exit(1)

    except Exception as e:
        logger.error(f"Erreur lors de l'ouverture de Chrome : {e}")
        sys.exit(1)
