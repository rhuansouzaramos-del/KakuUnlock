#!/usr/bin/env python3
import usb.core
import time
import subprocess
import os
import sys
import hashlib
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()
MTK_VID = 0x0e8d
BROM_PIDS = [0x0003, 0x2000, 0x2001]
PAYLOAD_DA = "../payloads/DA_auth.bin"
APK_FRP = "FRP_Bypass.apk"
BACKUP_DIR = "../backups"
LOG_DIR = "../logs"

def check_env():
    os.makedirs(BACKUP_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)
    
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

def generate_checksum(filepath):
    if not os.path.exists(filepath):
        return
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    hash_file = filepath + ".sha256"
    with open(hash_file, "w") as f:
        f.write(sha256_hash.hexdigest())
    console.print(f"[green]Checksum SHA256 gerado: {hash_file}[/green]")

def run_cmd(cmd, title):
    console.print(Panel(f"[bold blue]Executando:[/] {title}", style="blue"))
    try:
        # Redireciona logs para arquivo
        log_path = os.path.join(LOG_DIR, f"{title.replace(' ', '_').lower()}.log")
        with open(log_path, "w") as log_file:
            result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            log_file.write(result.stdout)
            console.print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]FALHA ao executar: {title}[/bold red]")
        console.print(f"[red]Erro: Verifique se o cabo USB esta conectado e o celular no modo BROM.[/red]")
        return False
    except Exception as e:
        console.print(f"[bold red]Erro inesperado: {e}[/bold red]")
        return False

def menu_brom():
    console.print(Panel("[bold cyan]MODO BROM (MTK)[/bold cyan]\nO celular deve estar desligado e conectado via USB."))
    console.print("1. [green]Leitura Segura[/green] (Ler tabela de particoes)")
    console.print("2. [green]Backup Total[/green] (Dump de todas as particoes)")
    console.print("3. [green]Backup EFS/IMEI[/green] (Salvar dados da antena)")
    console.print("4. [green]Extrair boot.img + Checksum[/green]")
    console.print("5. [yellow]Limpar FRP[/yellow] (Apagar particao FRP)")
    console.print("6. [bold red]Desbloquear Bootloader[/bold red] (PERIGOSO no One UI 8)")
    console.print("0. Voltar")
    
    opcao = Prompt.ask("\nEscolha uma opcao", choices=["0","1","2","3","4","5","6"])
    
    if opcao == '1':
        run_cmd(f"cd mtkclient && python3 mtk da --loader ../{PAYLOAD_DA} printgpt", "Leitura de Particoes")
    elif opcao == '2':
        run_cmd(f"cd mtkclient && python3 mtk da --loader ../{PAYLOAD_DA} rl ../backups/backup_total", "Backup Total")
    elif opcao == '3':
        run_cmd(f"cd mtkclient && python3 mtk da --loader ../{PAYLOAD_DA} r efs ../backups/efs_backup.bin", "Backup EFS/IMEI")
        generate_checksum(os.path.join(BACKUP_DIR, "efs_backup.bin"))
    elif opcao == '4':
        run_cmd(f"cd mtkclient && python3 mtk da --loader ../{PAYLOAD_DA} r boot ../backups/boot.img", "Extracao do boot.img")
        generate_checksum(os.path.join(BACKUP_DIR, "boot.img"))
    elif opcao == '5':
        run_cmd(f"cd mtkclient && python3 mtk da --loader ../{PAYLOAD_DA} e frp", "Limpeza de FRP")
    elif opcao == '6':
        console.print("[bold red]AVISO: Desbloquear o bootloader em Samsung One UI 8 pode brickar o aparelho![/bold red]")
        if Prompt.ask("Tem certeza?", choices=["s","n"]) == "s":
            run_cmd(f"cd mtkclient && python3 mtk da --loader ../{PAYLOAD_DA} seccfg unlock", "Desbloqueio de Bootloader")

def menu_adb():
    console.print(Panel("[bold green]MODO ADB (Android Ligado)[/bold green]\nDepuracao USB deve estar ativa."))
    console.print("1. [green]Diagnostico do Sistema[/green] (Modelo, Android, Kernel)")
    console.print("2. [green]Bypass de FRP[/green] (Contornar conta Google)")
    console.print("3. [green]Desativar Knox[/green]")
    console.print("4. [green]Reboot Recovery[/green]")
    console.print("0. Voltar")
    
    opcao = Prompt.ask("\nEscolha uma opcao", choices=["0","1","2","3","4"])
    
    if opcao == '1':
        console.print("[*] Puxando dados do sistema...", style="yellow")
        run_cmd("adb shell getprop ro.product.model", "Modelo do Aparelho")
        run_cmd("adb shell getprop ro.build.version.release", "Versao do Android")
        run_cmd("adb shell getprop ro.build.fingerprint", "Fingerprint da Build")
        run_cmd("adb shell dmesg | tail -n 20", "Ultimos Logs do Kernel (dmesg)")
    elif opcao == '2':
        if os.path.exists(APK_FRP):
            subprocess.run(["adb", "install", APK_FRP])
            run_cmd("adb shell settings put global device_provisioned 1", "Configurar Provisionamento")
            run_cmd("adb shell settings put secure user_setup_complete 1", "Pular Setup Wizard")
            run_cmd("adb shell am start -n com.android.settings/.Settings", "Abrir Configuracoes")
        else:
            console.print("[red]APK de FRP nao encontrado![/red]")
    elif opcao == '3':
        run_cmd("adb shell pm uninstall -k --user 0 com.samsung.android.kgclient", "Remover Knox Client")
        run_cmd("adb shell pm uninstall -k --user 0 com.samsung.android.knox.attestation", "Remover Knox Attestation")
    elif opcao == '4':
        run_cmd("adb reboot recovery", "Reiniciando Recovery")

def main():
    check_env()
    while True:
        console.print(Panel("[bold magenta]KakuUnlock Automator v5.0[/bold magenta]\n[dim]Open Source MTK Tool by rhuansouzaramos-del[/dim]", border_style="magenta"))
        console.print("1. Modo BROM (MTK Desligado)")
        console.print("2. Modo ADB (Android Ligado)")
        console.print("0. Sair")
        
        escolha = Prompt.ask("\nEscolha o modo", choices=["0","1","2"])
        
        if escolha == '1':
            if check_device():
                menu_brom()
            else:
                console.print("[red]Dispositivo nao detectado no BROM. Verifique o cabo.[/red]")
        elif escolha == '2':
            menu_adb()
        elif escolha == '0':
            break

if __name__ == "__main__":
    main()
