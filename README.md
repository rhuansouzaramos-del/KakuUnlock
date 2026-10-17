# KakuUnlock Suite v6.0.0

Ferramenta Open Source para automacao, diagnostico e bypass de FRP em dispositivos MediaTek e Qualcomm.

## AVISO CRITICO (Samsung One UI 8+)
A Samsung removeu a funcionalidade de desbloqueio de bootloader no firmware One UI 8. Tentar rodar o comando de unlock (`seccfg unlock`) em aparelhos como o Galaxy A15 tem 99% de chance de causar um brick permanente. O KakuUnlock prioriza o **Modo Read-Only (Leitura e Backup)** para manter seu aparelho seguro.

## 🚀 Novidades da v6.0.0 (GUI Edition)
- **Interface Gráfica (Tkinter):** Fim do terminal preto. Botoes clicaveis para todas as funcoes de BROM e ADB.
- **Auto-Identify:** O script le o modelo do celular e a versao do Android automaticamente via ADB.
- **Logs em Tempo Real:** Acompanhe a execucao do `mtkclient` linha por linha na propria janela.
- **Bypass de FRP (1 Clique):** Botao dedicado para pular a tela de conta Google.

## Como usar (Windows)
1. Baixe o codigo fonte (ZIP).
2. Instale os drivers em `drivers/windows`.
3. Instale as dependencias: `pip install pyusb rich`
4. Baixe o `mtkclient`: `git clone https://github.com/bkerler/mtkclient.git`
5. Execute: `python pc_automator/kaku_gui.py`

**Aviso:** Use em dispositivos proprios. A ferramenta opera no modo read-only por padrao.
