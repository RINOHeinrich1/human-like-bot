import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageGrab, ImageTk
import os

CONFIG_FILE = "config.py"
IMAGE_DIR = "images"
os.makedirs(IMAGE_DIR, exist_ok=True)

IMAGE_KEYS = [
    "connexion",
    "mon_compte",
    "barre_recherche",
    "compte_connecte",
    "filtre_personnes",
    "se_connecter",
    "envoyer_sans_note",
    "personne_suivant",
    "limite_invitations_hebdo",
    "ok_limite"
]

class ZoneSelector:
    def __init__(self, callback):
        self.callback = callback
        self.root = tk.Toplevel()
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 1.0)  # opaque pour que l’image soit bien visible

        # Capture d’écran au lancement
        self.screenshot = ImageGrab.grab()
        self.tk_img = ImageTk.PhotoImage(self.screenshot)

        self.canvas = tk.Canvas(self.root, cursor="cross")
        self.canvas.pack(fill="both", expand=True)

        # Afficher la capture d’écran en fond
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)

        # Ajouter un calque semi-transparent noir pour assombrir légèrement l’écran
        self.overlay = self.canvas.create_rectangle(
            0, 0, self.screenshot.width, self.screenshot.height,
            fill='black', stipple='gray25'
        )
        self.canvas.tag_lower(self.overlay)  # mettre sous les autres éléments

        self.rect = None
        self.start_x = self.start_y = 0

        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def on_press(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline="red", width=2
        )

    def on_drag(self, event):
        cur_x, cur_y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_release(self, event):
        end_x, end_y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        self.root.destroy()

        x1 = int(min(self.start_x, end_x))
        y1 = int(min(self.start_y, end_y))
        x2 = int(max(self.start_x, end_x))
        y2 = int(max(self.start_y, end_y))

        self.callback((x1, y1, x2, y2))


class ConfigCaptureApp:
    def __init__(self, master):
        self.master = master
        master.title("Capture configuration")

        self.key_var = tk.StringVar(value=IMAGE_KEYS[0])
        self.label = ttk.Label(master, text="Clé à associer :")
        self.label.pack(pady=5)

        self.dropdown = ttk.OptionMenu(master, self.key_var, IMAGE_KEYS[0], *IMAGE_KEYS)
        self.dropdown.pack(pady=5)

        self.capture_btn = ttk.Button(master, text="Nouvelle capture", command=self.start_capture)
        self.capture_btn.pack(pady=10)

        self.quit_btn = ttk.Button(master, text="Quitter", command=master.quit)
        self.quit_btn.pack(pady=5)

    def start_capture(self):
        self.master.withdraw()
        self.selector = ZoneSelector(self.on_capture_done)

    def on_capture_done(self, box):
        self.master.deiconify()

        try:
            image = ImageGrab.grab(bbox=box)
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur de capture : {e}")
            return

        key = self.key_var.get()
        filepath = os.path.join(IMAGE_DIR, f"{key}.png")
        image.save(filepath)
        self.update_config_py(key, filepath)
        messagebox.showinfo("Succès", f"Image capturée et enregistrée : {filepath}")

    def update_config_py(self, key, filepath):
        if not os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "w") as f:
                f.write("URL_LINKEDIN = \"https://www.linkedin.com/home\"\n\n")
                f.write("IMAGES = {\n}\n")

        with open(CONFIG_FILE, 'r') as f:
            lines = f.readlines()

        found = False
        for i, line in enumerate(lines):
            if f'"{key}"' in line:
                lines[i] = f'    "{key}": "{filepath}",\n'
                found = True

        if not found:
            for i, line in enumerate(lines):
                if line.strip().endswith("}"):
                    lines.insert(i, f'    "{key}": "{filepath}",\n')
                    break

        with open(CONFIG_FILE, 'w') as f:
            f.writelines(lines)

if __name__ == "__main__":
    root = tk.Tk()
    app = ConfigCaptureApp(root)
    root.mainloop()
