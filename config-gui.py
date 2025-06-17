import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageGrab, ImageTk
import os

CONFIG_FILE = "config.py"
IMAGE_DIR = "images"
os.makedirs(IMAGE_DIR, exist_ok=True)

IMAGE_KEYS = [
    "connexion", "mon_compte", "barre_recherche", "compte_connecte",
    "filtre_personnes", "se_connecter", "envoyer_sans_note",
    "personne_suivant", "limite_invitations_hebdo",
    "limite_invitations_mensuels", "ok_limite","email_preconfiguree","password_preconfiguree","email_non_configuree",
    "password_non_configuree"
]

class ZoneSelector:
    def __init__(self, callback):
        self.callback = callback
        self.root = tk.Toplevel()
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 1.0)

        self.screenshot = ImageGrab.grab()
        self.tk_img = ImageTk.PhotoImage(self.screenshot)

        self.canvas = tk.Canvas(self.root, cursor="cross")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)

        self.overlay = self.canvas.create_rectangle(
            0, 0, self.screenshot.width, self.screenshot.height,
            fill='black', stipple='gray25'
        )
        self.canvas.tag_lower(self.overlay)

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
        x1, y1 = int(min(self.start_x, end_x)), int(min(self.start_y, end_y))
        x2, y2 = int(max(self.start_x, end_x)), int(max(self.start_y, end_y))
        self.callback((x1, y1, x2, y2))


class ConfigCaptureApp:
    def __init__(self, master):
        self.master = master
        master.title("🛠️ Configuration LinkedIn")
        master.geometry("500x600")
        master.configure(padx=20, pady=20)

        self.config = self.load_config()
        self.create_form()

    def create_form(self):
        style = ttk.Style()
        style.configure("TLabel", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10, "bold"))

        ttk.Label(self.master, text="🔗 URL LinkedIn", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 2))
        self.url_entry = ttk.Entry(self.master, width=60)
        self.url_entry.insert(0, self.config.get("URL_LINKEDIN", "https://www.linkedin.com/home"))
        self.url_entry.pack(pady=(0, 10))
        ttk.Label(self.master, text="🔍 Profile recherchée", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 2))
        self.search_query_entry = ttk.Entry(self.master, width=60)
        self.search_query_entry.insert(0, self.config.get("SEARCH_QUERY", ""))
        self.search_query_entry.pack(pady=(0, 10))
        ttk.Label(self.master, text="📧 Email", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 2))
        self.email_entry = ttk.Entry(self.master, width=60)
        self.email_entry.insert(0, self.config.get("CREDENTIALS", {}).get("email", ""))
        self.email_entry.pack(pady=(0, 10))

        ttk.Label(self.master, text="🔒 Mot de passe", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 2))
        self.password_entry = ttk.Entry(self.master, width=60, show="*")
        self.password_entry.insert(0, self.config.get("CREDENTIALS", {}).get("password", ""))
        self.password_entry.pack(pady=(0, 10))

        ttk.Label(self.master, text="🔁 MAX_SCROLL", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 2))
        self.scroll_entry = ttk.Entry(self.master, width=10)
        self.scroll_entry.insert(0, str(self.config.get("MAX_SCROLL", 20)))
        self.scroll_entry.pack(pady=(0, 15))

        # Nouvelle case à cocher pour EMAIL_LOGIN
        self.email_login_var = tk.BooleanVar(value=self.config.get("EMAIL_LOGIN", True))
        self.email_login_check = ttk.Checkbutton(
            self.master,
            text="✅ Connexion avec email",
            variable=self.email_login_var
        )
        self.email_login_check.pack(pady=(0, 10))

        ttk.Label(self.master, text="🖼️ Clé d'image à associer", font=("Segoe UI", 10, "bold")).pack(pady=(10, 5))
        self.key_var = tk.StringVar(value=IMAGE_KEYS[0])
        self.dropdown = ttk.OptionMenu(self.master, self.key_var, IMAGE_KEYS[0], *IMAGE_KEYS)
        self.dropdown.pack(pady=(0, 15))

        ttk.Separator(self.master, orient="horizontal").pack(fill="x", pady=10)

        btn_frame = ttk.Frame(self.master)
        btn_frame.pack(pady=10)

        self.capture_btn = ttk.Button(btn_frame, text="📸 Nouvelle capture", command=self.start_capture)
        self.capture_btn.grid(row=0, column=0, padx=5)

        self.save_btn = ttk.Button(btn_frame, text="💾 Enregistrer", command=self.save_config)
        self.save_btn.grid(row=0, column=1, padx=5)

        self.quit_btn = ttk.Button(btn_frame, text="❌ Quitter", command=self.master.quit)
        self.quit_btn.grid(row=0, column=2, padx=5)

    def load_config(self):
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("config", CONFIG_FILE)
            config_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(config_module)
            return {
                "URL_LINKEDIN": getattr(config_module, "URL_LINKEDIN", ""),
                "CREDENTIALS": getattr(config_module, "CREDENTIALS", {}),
                "MAX_SCROLL": getattr(config_module, "MAX_SCROLL", 20),
                "EMAIL_LOGIN": getattr(config_module, "EMAIL_LOGIN", True),
                "SEARCH_QUERY": getattr(config_module, "SEARCH_QUERY", ""),
                "IMAGES": getattr(config_module, "IMAGES", {})
            }
        except Exception:
            return {}

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
        self.config.setdefault("IMAGES", {})[key] = filepath
        self.save_config(save_message=False)
        messagebox.showinfo("Succès", f"Image enregistrée : {filepath}")

    def save_config(self, save_message=True):
        url = self.url_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        try:
            max_scroll = int(self.scroll_entry.get())
        except ValueError:
            messagebox.showerror("Erreur", "MAX_SCROLL doit être un entier.")
            return

        self.config["URL_LINKEDIN"] = url
        self.config["CREDENTIALS"] = {"email": email, "password": password}
        self.config["MAX_SCROLL"] = max_scroll
        self.config["EMAIL_LOGIN"] = self.email_login_var.get()
        search_query = self.search_query_entry.get()
        self.config["SEARCH_QUERY"] = search_query

        with open(CONFIG_FILE, "w") as f:
            f.write(f'URL_LINKEDIN = "{url}"\n\nn')
            f.write("CREDENTIALS = {\n")
            f.write(f'    "email": "{email}",\n')
            f.write(f'    "password": "{password}"\n')
            f.write("}\n\n")
            f.write(f"MAX_SCROLL = {max_scroll}\n\n")
            f.write(f"EMAIL_LOGIN = {self.config['EMAIL_LOGIN']}\n\n")
            f.write("IMAGES = {\n")
            f.write(f'SEARCH_QUERY = "{search_query}"\n\n')

            for k, v in self.config.get("IMAGES", {}).items():
                f.write(f'    "{k}": "{v}",\n')
            f.write("}\n")

        if save_message:
            messagebox.showinfo("Succès", "Configuration enregistrée.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ConfigCaptureApp(root)
    root.mainloop()
