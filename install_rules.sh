#!/bin/bash
echo "[*] Instalando regras UDEV do KakuUnlock..."
cat << 'RULE' > /etc/udev/rules.d/99-kakuunlock.rules
SUBSYSTEM=="usb", ATTR{idVendor}=="0e8d", MODE="0666", GROUP="plugdev"
SUBSYSTEM=="usb", ATTR{idVendor}=="05c6", ATTR{idProduct}=="9008", MODE="0666", GROUP="plugdev"
SUBSYSTEM=="usb", ATTR{idVendor}=="04e8", MODE="0666", GROUP="plugdev"
RULE
udevadm control --reload-rules
udevadm trigger
echo "[+] Regras UDEV instaladas."
