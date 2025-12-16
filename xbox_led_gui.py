import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import time
import threading
import winreg
import json
import locale

# Dil Dosyası
TRANS = {
    "EN": {
        "title": "Xbox Controller LED Off",
        "desc": "This tool turns off the controller light completely.\n(Uses Steam in the background to apply settings)",
        "warn": "IMPORTANT: Controller must be connected via CABLE.\nTo turn light back on, simply replug the controller.",
        "btn_off": "TURN OFF LED",
        "btn_process": "Turning Off LED...",
        "btn_success": "Successfully Closed (Exit)",
        "status_ready": "Ready.",
        "status_steam_missing": "ERROR: Steam not found!",
        "err_title": "Steam Required",
        "err_msg": "STEAM IS REQUIRED FOR THIS PROGRAM TO WORK.\n\nWhy?\nWindows driver blocks LED control.\nThis program uses Steam mechanism to bypass it.\n\nPlease install Steam and try again.",
        "status_check": "Checking Steam...",
        "status_setting": "Applying setting (Off)...",
        "status_closing_driver": "Preparing driver (Closing Steam)...",
        "status_sending": "Sending LED command (Silent)...",
        "status_processing": "Processing... ({}s)",
        "status_cleaning": "Cleaning up (Closing Steam)...",
        "status_done": "SUCCESS! LED Turned Off."
    },
    "TR": {
        "title": "Xbox Kontrolcü Işığını Kapat",
        "desc": "Bu araç kontrolcünün ışığını tamamen kapatır.\n(Arkaplanda Steam'i kullanarak ayar yapar)",
        "warn": "ÖNEMLİ: Kontrolcü KABLO ile bağlı olmalıdır.\nIşığı geri açmak için çıkarıp takmanız yeterlidir.",
        "btn_off": "LED'İ KAPAT",
        "btn_process": "LED Kapatılıyor...",
        "btn_success": "Başarıyla Kapandı (Çıkış)",
        "status_ready": "Hazır.",
        "status_steam_missing": "HATA: Bilgisayarda Steam bulunamadı!",
        "err_title": "Steam Gerekli",
        "err_msg": "BU PROGRAMIN ÇALIŞMASI İÇİN STEAM GEREKLİDİR.\n\nNeden?\nWindows'un kendi sürücüsü LED kontrolüne izin vermez.\nBu program, Steam'in sürücü altyapısını kullanarak bu engeli aşar.\n\nLütfen Steam'i yükleyip tekrar deneyin.",
        "status_check": "Steam kontrol ediliyor...",
        "status_setting": "Ayar (Kapalı) sisteme işleniyor...",
        "status_closing_driver": "Sürücü hazırlanıyor (Steam Kapatılıyor)...",
        "status_sending": "LED komutu gönderiliyor (Sessiz)...",
        "status_processing": "İşleniyor... ({}sn)",
        "status_cleaning": "Temizlik yapılıyor (Steam Kapatılıyor)...",
        "status_done": "BAŞARILI! Işık Kapatıldı."
    }
}

CONFIG_FILE = "config.json"

class XboxLedApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Xbox LED Tool")
        self.root.geometry("420x280")
        self.root.resizable(False, False)
        
        # Dil Yükle
        self.lang = self.load_config() 
        
        # Stil
        style = ttk.Style()
        style.configure("TButton", font=("Segoe UI", 11, "bold"))
        style.configure("TLabel", font=("Segoe UI", 10))
        
        # --- Dil Seçici (Sağ Üst) ---
        self.top_frame = ttk.Frame(root)
        self.top_frame.pack(fill="x", padx=10, pady=5)
        
        # Dil Butonu (EN / TR)
        self.lang_btn = ttk.Button(self.top_frame, text=self.get_lang_btn_text(), command=self.toggle_language, width=5)
        self.lang_btn.pack(side="right")
        
        # --- Ana İçerik ---
        
        # Başlık
        self.title_label = ttk.Label(root, text="", font=("Segoe UI", 14, "bold"))
        self.title_label.pack(pady=(5, 10))
        
        # Açıklama
        self.desc_label = ttk.Label(root, text="", justify="center")
        self.desc_label.pack(pady=5)
        
        # Uyarılar
        self.warn_label = ttk.Label(root, text="", foreground="#555", justify="center", font=("Segoe UI", 9, "italic"))
        self.warn_label.pack(pady=10)
        
        # Buton Frame
        btn_frame = ttk.Frame(root)
        btn_frame.pack(pady=10, fill="x")
        
        # Kapatma Butonu
        self.apply_btn = ttk.Button(btn_frame, text="", command=self.start_apply_thread)
        self.apply_btn.pack(pady=5, ipadx=30, ipady=10)
        
        # Durum
        self.status_var = tk.StringVar(value="")
        self.status_label = ttk.Label(root, textvariable=self.status_var, font=("Segoe UI", 9))
        self.status_label.pack(side="bottom", pady=10)
        
        # Metinleri Güncelle
        self.update_ui_text()
        
        # Başlangıç Kontrolü
        self.check_steam_installation()

    def load_config(self):
        # Sistem Dilini Algıla
        sys_lang = "EN"
        try:
            loc = locale.getdefaultlocale()
            if loc and loc[0] and loc[0].lower().startswith("tr"):
                sys_lang = "TR"
        except:
            pass

        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    data = json.load(f)
                    return data.get("lang", sys_lang)
            except:
                pass
        return sys_lang

    def save_config(self, lang):
        try:
            with open(CONFIG_FILE, "w") as f:
                json.dump({"lang": lang}, f)
        except:
            pass

    def get_lang_btn_text(self):
        return "TR" if self.lang == "EN" else "EN" # Şu anki buysa, değiştirme butonu diğeri olsun

    def toggle_language(self):
        self.lang = "TR" if self.lang == "EN" else "EN"
        self.save_config(self.lang)
        self.lang_btn.config(text=self.get_lang_btn_text())
        self.update_ui_text()
        
    def t(self, key):
        return TRANS[self.lang].get(key, key)

    def update_ui_text(self):
        self.root.title(self.t("title"))
        self.title_label.config(text=self.t("title"))
        self.desc_label.config(text=self.t("desc"))
        self.warn_label.config(text=self.t("warn"))
        
        # Butonun o anki durumuna göre metni güncelle
        if self.apply_btn['state'] == 'disabled':
            # Eğer işlem yapılıyorsa elleme (Thread güncelliyor) veya bitmişse
            pass
        else:
            self.apply_btn.config(text=self.t("btn_off"))

    def check_steam_installation(self):
        steam_path = self.get_steam_path()
        if not steam_path:
            self.apply_btn.config(state="disabled")
            self.status_var.set(self.t("status_steam_missing"))
            self.status_label.config(foreground="red")
            tk.messagebox.showerror(self.t("err_title"), self.t("err_msg"))
        
    def start_apply_thread(self):
        # Butonu kilitle ve metni değiştir
        self.apply_btn.config(state="disabled", text=self.t("btn_process"))
        t = threading.Thread(target=self.run_process)
        t.daemon = True
        t.start()

    def get_steam_path(self):
        try:
            hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\WOW6432Node\\Valve\\Steam")
            val, _ = winreg.QueryValueEx(hkey, "InstallPath")
            exe = os.path.join(val, "steam.exe")
            if os.path.exists(exe): return exe
        except:
            pass
        
        defaults = [
            r"C:\Program Files (x86)\Steam\steam.exe",
            r"C:\Program Files\Steam\steam.exe"
        ]
        for p in defaults:
            if os.path.exists(p): return p
        return None

    def run_process(self):
        try:
            # Hedef: Tamamen kapalı (0.0)
            brightness_str = "0.0"
            
            self.update_status(self.t("status_check"), "blue")
            steam_exe = self.get_steam_path()
            if not steam_exe:
                self.update_status(self.t("status_steam_missing"), "red")
                self.reset_ui(error=True)
                return
            
            self.update_status(self.t("status_setting"), "blue")
            # 1. SETX ile Kalıcı Yap
            subprocess.run(["SETX", "SDL_JOYSTICK_HIDAPI_XBOX_ONE_HOME_LED", brightness_str], 
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
            
            # 2. Geçici
            os.environ["SDL_JOYSTICK_HIDAPI_XBOX_ONE_HOME_LED"] = brightness_str
            
            # Steam'i kapat
            self.update_status(self.t("status_closing_driver"), "orange")
            subprocess.run(["taskkill", "/f", "/im", "steam.exe"], 
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
            time.sleep(2)
            
            # Steam'i sessiz aç
            self.update_status(self.t("status_sending"), "green")
            subprocess.Popen([steam_exe, "-silent"], creationflags=subprocess.CREATE_NO_WINDOW)
            
            # Bekle
            for i in range(15, 0, -1):
                self.update_status(self.t("status_processing").format(i), "green")
                time.sleep(1)
                
            # Kapat
            self.update_status(self.t("status_cleaning"), "orange")
            subprocess.run(["taskkill", "/f", "/im", "steam.exe"], 
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
            
            self.update_status(self.t("status_done"), "green")
            self.root.after(0, self.set_exit_mode)
            
        except Exception as e:
            self.update_status(f"Error: {e}", "red")
            self.root.after(0, self.reset_ui)

    def update_status(self, text, color):
        self.status_var.set(text)
        self.status_label.config(foreground=color)
        self.root.update_idletasks()

    def set_exit_mode(self):
        self.apply_btn.config(state="normal", text=self.t("btn_success"), command=self.root.destroy)

    def reset_ui(self, error=False):
        if not error:
            self.apply_btn.config(state="normal", text=self.t("btn_off")) 

if __name__ == "__main__":
    root = tk.Tk()
    app = XboxLedApp(root)
    
    # Pencereyi ekranın ortasına al
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws/2) - (420/2)
    y = (hs/2) - (280/2)
    root.geometry('%dx%d+%d+%d' % (420, 280, x, y))
    
    root.mainloop()
