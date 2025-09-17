#!/usr/bin/env python3

import platform
import os
import sys
import subprocess
from pathlib import Path
import winreg as reg

class ContextMenuIntegration:
    def __init__(self):
        self.system = platform.system()
        self.app_dir = Path(__file__).parent.resolve()
        self.main_script = self.app_dir / "main.py"
        if self.system == "Windows":
            pythonw_exe = Path(sys.executable).parent / "pythonw.exe"
            self.python_exe = str(pythonw_exe) if pythonw_exe.exists() else sys.executable
        else:
            self.python_exe = sys.executable
        self.icon_path = self.app_dir / "icon.ico"
        
    def install_context_menu(self):
        if self.system == "Windows":
            return self._install_windows_context_menu()
        else:
            return self._install_linux_context_menu()
            
    def uninstall_context_menu(self):
        if self.system == "Windows":
            return self._uninstall_windows_context_menu()
        else:
            return self._uninstall_linux_context_menu()
            
    def _install_windows_context_menu(self):
        try:
            key_path = r"*\shell\CryptoDisk"
            command_path = r"*\shell\CryptoDisk\command"
            
            with reg.CreateKey(reg.HKEY_CLASSES_ROOT, key_path) as key:
                reg.SetValue(key, "", reg.REG_SZ, "Delete with CryptoDisk")
                if self.icon_path.exists():
                    reg.SetValueEx(key, "Icon", 0, reg.REG_SZ, str(self.icon_path))
                
            with reg.CreateKey(reg.HKEY_CLASSES_ROOT, command_path) as key:
                command = f'"{self.python_exe}" "{self.main_script}" --delete "%1"'
                reg.SetValue(key, "", reg.REG_SZ, command)
                
            folder_key_path = r"Directory\shell\CryptoDisk"
            folder_command_path = r"Directory\shell\CryptoDisk\command"
            
            with reg.CreateKey(reg.HKEY_CLASSES_ROOT, folder_key_path) as key:
                reg.SetValue(key, "", reg.REG_SZ, "Delete with CryptoDisk")
                if self.icon_path.exists():
                    reg.SetValueEx(key, "Icon", 0, reg.REG_SZ, str(self.icon_path))
                
            with reg.CreateKey(reg.HKEY_CLASSES_ROOT, folder_command_path) as key:
                command = f'"{self.python_exe}" "{self.main_script}" --delete "%1"'
                reg.SetValue(key, "", reg.REG_SZ, command)
                
            return True
            
        except Exception as e:
            print(f"Error installing Windows context menu: {e}")
            return False
            
    def _uninstall_windows_context_menu(self):
        try:
            try:
                reg.DeleteKey(reg.HKEY_CLASSES_ROOT, r"*\shell\CryptoDisk\command")
                reg.DeleteKey(reg.HKEY_CLASSES_ROOT, r"*\shell\CryptoDisk")
            except:
                pass
                
            try:
                reg.DeleteKey(reg.HKEY_CLASSES_ROOT, r"Directory\shell\CryptoDisk\command")
                reg.DeleteKey(reg.HKEY_CLASSES_ROOT, r"Directory\shell\CryptoDisk")
            except:
                pass
                
            return True
            
        except Exception as e:
            print(f"Error uninstalling Windows context menu: {e}")
            return False
            
    def _install_linux_context_menu(self):
        try:
            desktop_file_content = f"""[Desktop Entry]
Type=Action
Name=Delete with CryptoDisk
Icon={self.app_dir}/icon.png
Profiles=profile-zero;

[X-Action-Profile profile-zero]
Exec={self.python_exe} {self.main_script} --delete %f
MimeTypes=application/octet-stream;text/plain;image/jpeg;image/png;video/mp4;audio/mpeg;application/pdf;text/html;
"""

            local_share = Path.home() / ".local" / "share"
            applications_dir = local_share / "applications"
            nautilus_scripts_dir = local_share / "nautilus" / "scripts"
            
            applications_dir.mkdir(parents=True, exist_ok=True)
            nautilus_scripts_dir.mkdir(parents=True, exist_ok=True)
            
            desktop_file_path = applications_dir / "cryptodisk-context.desktop"
            with open(desktop_file_path, 'w') as f:
                f.write(desktop_file_content)
            desktop_file_path.chmod(0o755)
            
            nautilus_script_content = f"""#!/bin/bash
for file in "$@"; do
    "{self.python_exe}" "{self.main_script}" --delete "$file" &
done
wait
"""
            
            nautilus_script_path = nautilus_scripts_dir / "Delete with CryptoDisk"
            with open(nautilus_script_path, 'w') as f:
                f.write(nautilus_script_content)
            nautilus_script_path.chmod(0o755)
            
            subprocess.run(["update-desktop-database", str(applications_dir)], 
                         capture_output=True)
            
            return True
            
        except Exception as e:
            print(f"Error installing Linux context menu: {e}")
            return False
            
    def _uninstall_linux_context_menu(self):
        try:
            local_share = Path.home() / ".local" / "share"
            applications_dir = local_share / "applications"
            nautilus_scripts_dir = local_share / "nautilus" / "scripts"
            
            desktop_file_path = applications_dir / "cryptodisk-context.desktop"
            nautilus_script_path = nautilus_scripts_dir / "Delete with CryptoDisk"
            
            try:
                desktop_file_path.unlink()
            except:
                pass
                
            try:
                nautilus_script_path.unlink()
            except:
                pass
                
            subprocess.run(["update-desktop-database", str(applications_dir)], 
                         capture_output=True)
            
            return True
            
        except Exception as e:
            print(f"Error uninstalling Linux context menu: {e}")
            return False
            
    def create_desktop_shortcut(self):
        if self.system == "Windows":
            return self._create_windows_shortcut()
        else:
            return self._create_linux_shortcut()
            
    def _create_windows_shortcut(self):
        try:
            import win32com.client
            
            desktop = Path.home() / "Desktop"
            shortcut_path = desktop / "CryptoDisk.lnk"
            
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(str(shortcut_path))
            shortcut.Targetpath = self.python_exe
            shortcut.Arguments = f'"{self.main_script}"'
            shortcut.WorkingDirectory = str(self.app_dir)
            if self.icon_path.exists():
                shortcut.IconLocation = str(self.icon_path)
            shortcut.Description = "CryptoDisk - Secure File Destruction"
            shortcut.save()
            
            return True
            
        except Exception as e:
            print(f"Error creating Windows shortcut: {e}")
            return False
            
    def _create_linux_shortcut(self):
        try:
            icon_png = self.app_dir / "icon.png"
            icon_path = str(icon_png) if icon_png.exists() else ""
            
            desktop_content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=CryptoDisk
Comment=Secure File Destruction
Exec={self.python_exe} "{self.main_script}"
Icon={icon_path}
Terminal=false
Categories=Utility;Security;System;
StartupNotify=true
"""
            
            desktop = Path.home() / "Desktop"
            shortcut_path = desktop / "CryptoDisk.desktop"
            
            with open(shortcut_path, 'w') as f:
                f.write(desktop_content)
            shortcut_path.chmod(0o755)
            
            applications_dir = Path.home() / ".local" / "share" / "applications"
            applications_dir.mkdir(parents=True, exist_ok=True)
            app_shortcut = applications_dir / "CryptoDisk.desktop"
            
            with open(app_shortcut, 'w') as f:
                f.write(desktop_content)
            app_shortcut.chmod(0o755)
            
            subprocess.run(["update-desktop-database", str(applications_dir)], 
                         capture_output=True)
            
            return True
            
        except Exception as e:
            print(f"Error creating Linux shortcut: {e}")
            return False