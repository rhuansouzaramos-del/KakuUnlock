#!/usr/bin/env python3
import usb.core
import time
import subprocess
import os
import sys
from rich.console import Console
from rich.panel import Panel

console = Console()
MTK_VID = 0x0e8d
BROM_PIDS = [0x0003, 0x2000, 0x2001]
PAYLOAD_DA = "../payloads/DA_auth.bin"
APK_FRP = "FRP_Bypass.apk"

def check_device():
    for pid in BROM_PIDS:
        if usb.core.find(idVendor=MTK_VID, idProduct=pid):
            return True
    return False

def run_cmd(cmd, title):
    console.print(f"[*] Executando: {title}...", style="yellow")
    try:
        subprocess.run(cmd, check=True)
        console.print(f"[+] {title} concluído com sucesso!", style="green")
    except subprocess.CalledProcessError:
        console.print(f"[-] Falha ao executar {title}.", style="red")

def menu_brom():
    console.print(Panel("[bold cyan]MODO BROM (MTK)[/bold cyan]\nO celular precisa estar desligado e conectado no USB."))
    console.print("1. Desbloquear Bootloader (seccfg unlock)")
    console.print("2. Limpar FRP (Apagar partição frp)")
    console.print("3. Reparar IMEI / Baseband (Apagar NVram)")
    console.print("4. Dump Completo (Backup de todas as partições)")
    console.print("5. Backup EFS (Salvar IMEI)")
    console.print("6. Reboot Recovery")
    console.print("0. Voltar")
    
    opcao = input("\nEscolha uma opção: ")
    
    if opcao == '1':
        run_cmd(["python3", "-m", "mtkclient", "da", "--loader", PAYLOAD_DA, "seccfg", "unlock"], "Desbloqueio de Bootloader")
    elif opcao == '2':
        run_cmd(["python3", "-m", "mtkclient", "da", "--loader", PAYLOAD_DA, "e", "frp"], "Limpeza de FRP")
    elif opcao == '3':
        run_cmd(["python3", "-m", "mtkclient", "da", "--loader", PAYLOAD_DA, "e", "nvram"], "Reparo de IMEI")
        run_cmd(["python3", "-m", "mtkclient", "da", "--loader", PAYLOAD_DA, "e", "nvdata"], "Reparo de Nvdata")
    elif opcao == '4':
        run_cmd(["python3", "-m", "mtkclient", "da", "--loader", PAYLOAD_DA, "rl", "backup_kaku"], "Dump Completo")
    elif opcao == '5':
        run_cmd(["python3", "-m", "mtkclient", "da", "--loader", PAYLOAD_DA, "r", "efs", "efs_backup.bin"], "Backup EFS")
    elif opcao == '6':
        run_cmd(["python3", "-m", "mtkclient", "da", "--loader", PAYLOAD_DA, "reset"], "Reboot")

def menu_adb():
    console.print(Panel("[bold green]MODO ADB (Android Ligado)[/bold green]\nCelular precisa estar ligado com Depuração USB ativa."))
    console.print("1. Bypass de FRP via Alliance Shield")
    console.print("2. Desinstalar Knox / Apps de Segurança (Samsung)")
    console.print("3. Extrair APK de App instalado")
    console.print("4. Remover Conta Google (sem root)")
    console.print("5. Reboot Recovery via ADB")
    console.print("0. Voltar")
    
    opcao = input("\nEscolha uma opção: ")
    
    if opcao == '1':
        console.print("[*] Iniciando bypass de FRP...", style="yellow")
        if os.path.exists(APK_FRP):
            subprocess.run(["adb", "install", APK_FRP])
            cmds = [
                ["adb", "shell", "settings", "put", "global", "device_provisioned", "1"],
                ["adb", "shell", "settings", "put", "secure", "user_setup_complete", "1"],
                ["adb", "shell", "am", "start", "-n", "com.android.settings/.Settings"]
            ]
            for c in cmds: subprocess.run(c)
            console.print("[+] FRP contornado. Alliance Shield instalado.", style="green")
        else:
            console.print(f"[-] Arquivo {APK_FRP} não encontrado!", style="red")
            
    elif opcao == '2':
        console.print("[*] Desativando Knox...", style="yellow")
        subprocess.run(["adb", "shell", "pm", "uninstall", "-k", "--user", "0", "com.samsung.android.kgclient"])
        subprocess.run(["adb", "shell", "pm", "uninstall", "-k", "--user", "0", "com.samsung.android.knox.attestation"])
        console.print("[+] Knox neutralizado.", style="green")
        
    elif opcao == '3':
        pkg = input("Digite o pacote do app (ex: com.instagram.android): ")
        run_cmd(["adb", "shell", "pm", "path", pkg], f"Localizando APK de {pkg}")

    elif opcao == '4':
        console.print("[*] Removendo conta Google via ADB (pode falhar em versões novas)...", style="yellow")
        subprocess.run(["adb", "shell", "pm", "clear", "com.google.android.gms"])
        subprocess.run(["adb", "shell", "pm", "clear", "com.google.android.gsf"])
        console.print("[+] Tentativa de remoção concluída.", style="green")

    elif opcao == '5':
        run_cmd(["adb", "reboot", "recovery"], "Reboot para Recovery")

def main():
    while True:
        console.print(Panel("[bold green]KakuUnlock Automator v3.0[/bold green]\nFerramenta Open Source de Unlock MTK"))
        console.print("1. Modo BROM (MTK)")
        console.print("2. Modo ADB (Android)")
        console.print("0. Sair")
        
        escolha = input("\nEscolha o modo: ")
        if escolha == '1':
            if check_device():
                menu_brom()
            else:
                console.print("[-] Celular não detectado no modo BROM.", style="red")
        elif escolha == '2':
            menu_adb()
        elif escolha == '0':
            break

if __name__ == "__main__":
    main()
