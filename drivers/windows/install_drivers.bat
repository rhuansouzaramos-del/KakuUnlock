@echo off
echo ========================================================
echo KakuUnlock - Instalador de Drivers USB
echo ========================================================
echo [*] Extraindo e instalando MediaTek...
tar -xf "Mediatek_Driver_Auto_Installer_v5.2307_(by_gsmofficial.com).zip"
start /wait Mediatek_Driver_Auto_Installer*/Install_Drivers.exe /S

echo [*] Extraindo Qualcomm...
tar -xf "Qualcomm_USB_Driver_v1.0.10065.1  (by_gsmofficial.com).rar"
start /wait Qualcomm_USB_Driver*/Setup.exe /S

echo [*] Extraindo ADB/Fastboot...
tar -xf "adb_and_fastboot_driver_1.4.3_(by_gsmofficial.com).zip"
start /wait adb_and_fastboot_driver*/install.bat

echo [+] Drivers instalados!
pause
