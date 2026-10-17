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
MTK_VID = 0x0e8d
BROM_PIDS = [0x0003, 0x2000, 0x2001]
PAYLOAD_DA = "../payloads/DA_auth.bin"
APK_FRP = "FRP_Bypass.apk"

def check_env():
    if not os.path.exists(PAYLOAD_DA):
        console.print(f"[-] ERRO: Payload DA nao encontrado em {PAYLOAD_DA}", style="bold red")
        sys.exit(1)
    if not os.path.exists("mtkclient"):
        console.print("[*] Baixando o motor mtkclient...", style="yellow")
        subprocess.run(["git", "clone", "https://github.com/bkerler/mtkclient.git"])
        subprocess.run(["pip", "install", "-r", "mtkclient/requirements.txt"])

def check_device():
    for pid in BROM_PIDS:
        if usb.core.find(idVendor=MTK_VID, idProduct=pid):
            return True
    return False

def run_cmd(cmd, title):
    console.print(Panel(f"[bold blue]Executando:[/] {title}", style="blue"))
    try:
        result = subprocess.run(cmd, shell=True, check=True)
        if result.returncode == 0:
            console.print(f"[green]OK {title} concluido com sucesso![/green]")
        return True
    except subprocess.CalledProcessError:
        console.print(f"[bold red]FALHA ao executar: {title}[/bold red]")
        return False

def menu_brom():
    console.print(Panel("[bold cyan]MODO BROM (MTK)[/bold cyan]\nO celular deve estar desligado e conectado via USB."))
    console.print("1. [green]Leitura Segura[/green] (Ler tabela de particoes)")
    console.print("2. [green]Backup Total[/green] (Dump de todas as particoes)")
    console.print("3. [green]Backup EFS/IMEI[/green] (Salvar dados da antena)")
    console.print("4. [green]Extrair boot.img[/green] (Ler a particao de boot)")
    console.print("5. [yellow]Limpar FRP[/yellow] (Apagar particao FRP)")
    console.print("6. [bold red]Desbloquear Bootloader[/bold red] (PERIGOSO no One UI 8)")
    console.print("0. Voltar")
    
    opcao = Prompt.ask("\nEscolha uma opcao", choices=["0","1","2","3","4","5","6"])
    
    if opcao == '1':
        run_cmd(f"cd mtkclient && python3 mtk da --loader ../{PAYLOAD_DA} printgpt", "Leitura de Particoes")
    elif opcao == '2':
        run_cmd(f"cd mtkclient && python3 mtk da --loader ../{PAYLOAD_DA} rl backup_kaku", "Backup Total")
    elif opcao == '3':
        run_cmd(f"cd mtkclient && python3 mtk da --loader ../{PAYLOAD_DA} r efs efs_backup.bin", "Backup EFS/IMEI")
    elif opcao == '4':
        run_cmd(f"cd mtkclient && python3 mtk da --loader ../{PAYLOAD_DA} r boot boot.img", "Extracao do boot.img")
    elif opcao == '5':
        run_cmd(f"cd mtkclient && python3 mtk da --loader ../{PAYLOAD_DA} e frp", "Limpeza de FRP")
    elif opcao == '6':
        console.print("[bold red]AVISO: Desbloquear o bootloader em Samsung One UI 8 pode brickar o aparelho permanentemente![/bold red]")
        if Prompt.ask("Tem certeza que deseja continuar?", choices=["s","n"]) == "s":
            run_cmd(f"cd mtkclient && python3 mtk da --loader ../{PAYLOAD_DA} seccfg unlock", "Desbloqueio de Bootloader")

def menu_adb():
    console.print(Panel("[bold green]MODO ADB (Android Ligado)[/bold green]\nDepuracao USB deve estar ativa."))
    console.print("1. [green]Bypass de FRP[/green] (Contornar tela de conta Google)")
    console.print("2. [green]Desativar Knox[/green] (Remover travas de seguranca)")
    console.print("3. [green]Extrair APK[/green] (Puxar app instalado)")
    console.print("4. [green]Reboot Recovery[/green]")
    console.print("0. Voltar")
    
    opcao = Prompt.ask("\nEscolha uma opcao", choices=["0","1","2","3","4"])
    
    if opcao == '1':
        if os.path.exists(APK_FRP):
            subprocess.run(["adb", "install", APK_FRP])
            subprocess.run(["adb", "shell", "settings", "put", "global", "device_provisioned", "1"])
            subprocess.run(["adb", "shell", "settings", "put", "secure", "user_setup_complete", "1"])
            subprocess.run(["adb", "shell", "am", "start", "-n", "com.android.settings/.Settings"])
            console.print("[green]FRP contornado![/green]")
        else:
            console.print("[red]APK de FRP nao encontrado![/red]")
    elif opcao == '2':
        subprocess.run(["adb", "shell", "pm", "uninstall", "-k", "--user", "0", "com.samsung.android.kgclient"])
        subprocess.run(["adb", "shell", "pm", "uninstall", "-k", "--user", "0", "com.samsung.android.knox.attestation"])
        console.print("[green]Knox neutralizado.[/green]")
    elif opcao == '3':
        pkg = Prompt.ask("Digite o pacote do app (ex: com.instagram.android)")
        run_cmd(f"adb shell pm path {pkg}", "Localizando APK")
    elif opcao == '4':
        run_cmd("adb reboot recovery", "Reiniciando Recovery")

def main():
    check_env()
    while True:
        console.print(Panel("[bold magenta]KakuUnlock Automator v4.0[/bold magenta]\n[dim]Open Source MTK Tool by rhuansouzaramos-del[/dim]", border_style="magenta"))
        console.print("1. Modo BROM (MTK Desligado)")
        console.print("2. Modo ADB (Android Ligado)")
        console.print("0. Sair")
        
        escolha = Prompt.ask("\nEscolha o modo", choices=["0","1","2"])
        
        if escolha == '1':
            if check_device():
                menu_brom()
            else:
                console.print("[red]Dispositivo nao detectado. Coloque no modo BROM.[/red]")
        elif escolha == '2':
            menu_adb()
        elif escolha == '0':
            break

if __name__ == "__main__":
    main()
