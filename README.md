# KakuUnlock Suite v5.0.0

Ferramenta Open Source para automacao, diagnostico e bypass de FRP em dispositivos MediaTek e Qualcomm.

## AVISO CRITICO (Samsung One UI 8+)
A Samsung removeu a funcionalidade de desbloqueio de bootloader no firmware One UI 8. Tentar rodar o comando de unlock (`seccfg unlock`) em aparelhos como o Galaxy A15 tem 99% de chance de causar um brick permanente. O KakuUnlock prioriza o **Modo Read-Only (Leitura e Backup)** para manter seu aparelho seguro.

## O que esta incluso?
- **APK Trigger**: Reinicia o celular direto pro modo BROM via root.
- **PC Automator (Python) v5.0**: Menu interativo com Backup Total, EFS/IMEI, Checksum SHA256, Diagnostico ADB e extracao de particoes.
- **Drivers e Payloads**: Todos os drivers USB e o arquivo DA original.

## Como usar (Windows)
1. Baixe o zip do projeto (Code > Download ZIP).
2. Instale os drivers presentes em `drivers/windows`.
3. Rode o `KakuTest.bat` na pasta `pc_automator`.
4. Escolha a opcao desejada no menu. (Os logs serao salvos na pasta `logs` e os backups na pasta `backups`).

## Como usar (Linux/Termux)
1. `sudo ./install_rules.sh` (para configurar o USB).
2. `pip install -r requirements.txt`.
3. `python3 kaku_auto.py`.

**Aviso:** Use em dispositivos proprios. A ferramenta opera no modo read-only por padrao.
