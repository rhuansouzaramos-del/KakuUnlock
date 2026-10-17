import subprocess
import os
import sys
from rich.console import Console
from rich.panel import Panel

console = Console()

def run(cmd):
    console.print(Panel(f"[bold blue]Executando:[/] {cmd}", style="blue"))
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        console.print(result.stdout)
    if result.stderr:
        console.print(f"[red]{result.stderr}[/red]")
    return result.returncode

console.print(Panel("[bold green]KakuUnlock — Teste Real Read-Only (Windows)[/bold green]", style="green"))
console.print("[*] Lendo tabela de partições (printgpt)...")

# No Windows, os comandos mudam um pouco
rc = run("cd mtkclient && python mtk printgpt")
if rc != 0:
    console.print("[red]Falha ao ler partições. Verifique o driver (WinUSB) e o modo BROM.[/red]")
    sys.exit(1)

console.print("[*] Extraindo partição boot (read-only)...")
run("cd mtkclient && python mtk r boot boot.img")

# Checagem do arquivo
boot_path = os.path.join("mtkclient", "boot.img")
if os.path.exists(boot_path):
    size = os.path.getsize(boot_path)
    console.print(f"[green]Sucesso! boot.img criado ({size} bytes)[/green]")
else:
    console.print("[red]boot.img não foi criado. Algo falhou.[/red]")
