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

console.print(Panel("[bold green]KakuUnlock — Teste Real Read-Only[/bold green]", style="green"))
console.print("[*] Lendo tabela de partições (printgpt)...")

rc = run("cd ~/mtkclient && python3 mtk printgpt")
if rc != 0:
    console.print("[red]Falha ao ler partições. Verifique o modo BROM e o cabo.[/red]")
    sys.exit(1)

console.print("[*] Extraindo partição boot (read-only)...")
run("cd ~/mtkclient && python3 mtk r boot boot.img")

if os.path.exists(os.path.expanduser("~/mtkclient/boot.img")):
    size = os.path.getsize(os.path.expanduser("~/mtkclient/boot.img"))
    console.print(f"[green]Sucesso! boot.img criado ({size} bytes)[/green]")
else:
    console.print("[red]boot.img não foi criado. Algo falhou.[/red]")
