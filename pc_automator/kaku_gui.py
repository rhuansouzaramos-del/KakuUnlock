import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import threading
import os
import sys

class KakuUnlockGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("KakuUnlock Suite v6.0 - Elite")
        self.root.geometry("800x600")
        self.root.configure(bg="#1e1e1e")

        # Variáveis
        self.device_model = tk.StringVar(value="Desconectado")

        # Abas
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        self.tab_brom = ttk.Frame(self.notebook)
        self.tab_adb = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_brom, text='Modo BROM (MTK)')
        self.notebook.add(self.tab_adb, text='Modo ADB (Android)')

        # --- ABA BROM ---
        frame_info = tk.Frame(self.tab_brom, bg="#1e1e1e")
        frame_info.pack(fill='x', pady=5)
        tk.Label(frame_info, text="Dispositivo:", bg="#1e1e1e", fg="white").pack(side='left')
        tk.Label(frame_info, textvariable=self.device_model, bg="#1e1e1e", fg="#00ff00", font=("Arial", 10, "bold")).pack(side='left', padx=5)

        frame_btns = tk.Frame(self.tab_brom, bg="#1e1e1e")
        frame_btns.pack(fill='x', pady=10)
        
        btn_style = {"bg": "#333333", "fg": "white", "font": ("Arial", 10), "width": 25, "pady": 5}
        
        tk.Button(frame_btns, text="1. Identificar Chip (Auto)", command=lambda: self.run_cmd("mtk da --loader ../payloads/DA_auth.bin printgpt", "Identificar"), **btn_style).pack(side='left', padx=5)
        tk.Button(frame_btns, text="2. Backup Total", command=lambda: self.run_cmd("mtk da --loader ../payloads/DA_auth.bin rl ../backups/backup_total", "Backup Total"), **btn_style).pack(side='left', padx=5)
        tk.Button(frame_btns, text="3. Extrair boot.img", command=lambda: self.run_cmd("mtk da --loader ../payloads/DA_auth.bin r boot ../backups/boot.img", "Extrair Boot"), **btn_style).pack(side='left', padx=5)

        # --- ABA ADB ---
        frame_adb_btns = tk.Frame(self.tab_adb, bg="#1e1e1e")
        frame_adb_btns.pack(fill='x', pady=10)
        tk.Button(frame_adb_btns, text="Auto-Identify (ADB)", command=self.auto_identify_adb, **btn_style).pack(side='left', padx=5)
        tk.Button(frame_adb_btns, text="Bypass FRP", command=self.bypass_frp, **btn_style).pack(side='left', padx=5)

        # --- TERMINAL LOG ---
        self.log_area = scrolledtext.ScrolledText(root, bg="black", fg="#00ff00", font=("Consolas", 9))
        self.log_area.pack(fill='both', expand=True, padx=10, pady=10)

        self.log("KakuUnlock GUI v6.0 Iniciada. Aguardando dispositivo...")

    def log(self, msg):
        self.log_area.insert(tk.END, msg + "\n")
        self.log_area.see(tk.END)

    def run_cmd(self, cmd, action_name):
        self.log(f"\n[*] Executando: {action_name}...")
        def thread_task():
            try:
                # Simulação se o mtkclient não estiver instalado no diretório local
                if not os.path.exists("mtkclient/mtk"):
                    self.log("[!] mtkclient não encontrado localmente. Certifique-se de rodar dentro da pasta pc_automator e ter clonado o mtkclient.")
                    self.log("[*] Baixando mtkclient...")
                    subprocess.run(["git", "clone", "https://github.com/bkerler/mtkclient.git"], check=True)
                    subprocess.run(["pip", "install", "-r", "mtkclient/requirements.txt"], check=True)
                
                process = subprocess.Popen(cmd, shell=True, cwd="mtkclient", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                for line in process.stdout:
                    self.root.after(0, self.log, line.strip())
                process.wait()
                self.root.after(0, self.log, f"[+] {action_name} finalizado.")
            except Exception as e:
                self.root.after(0, self.log, f"[-] Erro: {e}")
        threading.Thread(target=thread_task, daemon=True).start()

    def auto_identify_adb(self):
        self.log("\n[*] Lendo informações do sistema via ADB...")
        def task():
            try:
                model = subprocess.check_output("adb shell getprop ro.product.model", shell=True, text=True).strip()
                android = subprocess.check_output("adb shell getprop ro.build.version.release", shell=True, text=True).strip()
                self.root.after(0, self.device_model.set, f"{model} (Android {android})")
                self.root.after(0, self.log, f"[+] Modelo: {model} | Android: {android}")
            except Exception as e:
                self.root.after(0, self.log, f"[-] ADB não conectado ou sem permissão.")
        threading.Thread(target=task, daemon=True).start()

    def bypass_frp(self):
        self.log("\n[*] Iniciando Bypass de FRP...")
        def task():
            try:
                subprocess.run("adb shell settings put global device_provisioned 1", shell=True, check=True)
                subprocess.run("adb shell settings put secure user_setup_complete 1", shell=True, check=True)
                subprocess.run("adb shell am start -n com.android.settings/.Settings", shell=True, check=True)
                self.root.after(0, self.log, "[+] Bypass de FRP concluído! Configurações aberta.")
            except Exception as e:
                self.root.after(0, self.log, f"[-] Erro no FRP: {e}")
        threading.Thread(target=task, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = KakuUnlockGUI(root)
    root.mainloop()
