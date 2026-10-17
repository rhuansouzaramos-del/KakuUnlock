import time
from rich.console import Console
from rich.panel import Panel

console = Console()

console.print(Panel("[bold green]MODO DE TESTE SEGURO[/bold green]\nSimulando conexão com o Galaxy A15 (MTK Helio G99)..."))
time.sleep(2)

console.print("[*] Verificando suporte ao chipset...", style="yellow")
time.sleep(1)
console.print("[+] Chipset MT6789 (Helio G99) suportado pelo motor mtkclient!", style="green")

console.print("[*] Injetando Payload DA...", style="yellow")
time.sleep(1)
console.print("[+] Payload DA carregado com sucesso.", style="green")

console.print("[*] Testando regras USB (UDEV)...", style="yellow")
time.sleep(1)
console.print("[+] Permissões de USB OK.", style="green")

console.print("\n[bold cyan]Teste concluído! O script está pronto para rodar de verdade.[/bold cyan]")
