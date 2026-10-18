#!/usr/bin/env python3
import usb.core
import time
import subprocess
import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()
MTK_VID = 0xae8d
BROM-PIDS = [0x0003, 0x2000, 0x2001]
PAYLOAD_DA = "../payloads/DA_auth.bin"
BACKUP_DIR = "../backups"
LOG_DIR = "../logs"
TOOLS_DIR = "../tools"

def check_env():
    os.makedirs(BACKUP_DIR, exist_ok=True)
    os.makedirs$LOG_DIR, exist_ok=True)
    os.makedirs(TOOLS_DIR, exist_ok=True)
    if not os.path.exists(PAYLOAD_DA):
        console.print("[-] ERRO: Payload DA nao encontrado.", style="bold red")
        sys.exit(1)

def check_device():
    for pid in BROM_PIDS:
        if usb.core.find(idVendor=MTK_VID, idProduct=pid):
            return True
    return False

def run_cmd(cmd, title):
    console.print(Panel("[bold blue]Executando:[/] " + title, style="blue"))
    try:
        log_path = os.path.join(LOG_DIR, title.replace(' ', '_').lower() + ".log")
        with open(log_path, "w") as log_file:
            result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            log_file.write(result.stdout)
            console.print(result.stdout)
        return True
    except subprocess.CalledProcessError:
        console.print("FALHA ao executar: " + title, style="bold red")
        return False

def menu_brom():
    console.print(Panel("[bold cyan]MODO BROM (MTK)[/bold cyan]"))
    console.print("1. Leitura Segura\n2. Backup Total\n3. Extrair boot.img\n4. Tentar Exploits (Kamakiri/Carbonara)\n0. Voltar")
    opcao = Prompt.ask("Escolha uma opcao", choices=["0","1","2","3","4"])
    if opcao == '1':
        run_cmd("cd mtkclient && python3 mtk da --loader ../" + PAYLOAD_DA + " printgpt", "Leitura")
    elif opcao == '2':
        run_cmd("cd mtkclient && python3 mtk da --loader ../" + PAYLOAD_DA + " rl ../backups/backup_total", "Backup Total")
    elif opcao == '3':
        run_cmd("cd mtkclient && python3 mtk da --loader ../" + PAYLOAD_DA + " r boot ../backups/boot.img", "Boot.img")
    elif opcao == '4':
        run_cmd("cd mtkclient && python3 mtk payload --exploit kamakiri", "Kamakiri Exploit")
        run_cmd("cd mtkclient && python3 mtk payload --exploit carbonara", "Carbonara Exploit")

def menu_pentest():
    console.print(Panel("[bold green]PENTEST & REVERSE ENGINEERING[/bold green]"))
    console.print("1. Bypass SSL Pinning (Frida)\n2. Dump de APK\n3. Decompilar APK (JADX)\n4. Espelhar Tela (Scrcpy)\n0. Voltar")
    opcao = Prompt.ask("Escolha uma opcao", choices=["0","1","2","3","4"])
    if opcao == '1':
        try:
            frida_version = subprocess.check_output("frida --version", shell=True, text=True).strip()
            url = "https://github.com/frida/frida/releases/download/" + frida_version + "/frida-server-" + frida_version + "-android-arm64.xz"
            run_cmd("wget " + url + " -O frida-server.xz && unxz -f frida-server.xz", "Baixar Frida Server")
            run_cmd("adb push frida-server /data/local/tmp/ && adb shell 'chmod 755 /data/local/tmp/frida-server'", "Enviar Frida")
            subprocess.Popen("adb shell '/data/local/tmp/frida-server &'", shell=True)
            time.sleep(2)
            run_cmd("frida -U -f com.android.settings -l " + TOOLS_DIR + "/ssl_bypass.js", "Injetar Bypass SSL")
        except Exception as e:
            console.print("Erro Frida: " + str(e), style="red")
    elif opcao == '2':
        pkg = Prompt.ask("Digite o pacote (ex: com.instagram.android)")
        run_cmd("adb shell pm path " + pkg, "Localizar APK")
    elif opcao == '3':
        apk = Prompt.ask("Digite o caminho do APK")
        run_cmd(TOOLS_DIR + "/jadx/bin/jadx -d output_" + apk.replace(".apk","") + " " + apk, "Decompilar JADX")
    elif opcao == '4':
        run_cmd("scrcpy", "Espelhamento")

def main():
    check_env()
    while True:
        console.print(Panel("[bold magenta]KakuUnlock Ultimate v7.0[/bold magenta]", border_style="magenta"))
        console.print("1. Modo BROM (MTK Desligado)\n2. Pentest & RE (ADB)\n0. Sair")
        escolha = Prompt.ask("Escolha o modo", choices=["0","1","2"])
        if escolha == '1':
            if check_device():
                menu_brom()
            else:
                console.print("Dispositivo nao detectado no BROM.", style="red")
        elif escolha == '2':
            menu_pentest()
        elif escolha == '0':
            break

if __name__ == "__main__":
    main()
