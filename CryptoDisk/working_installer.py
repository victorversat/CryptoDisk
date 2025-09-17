#!/usr/bin/env python3

import tkinter as tk
from tkinter import messagebox
import sys
import os
import platform
import subprocess
from pathlib import Path
import shutil
import argparse

class WorkingInstaller:
    def __init__(self, gui_mode=True):
        self.system = platform.system()
        self.app_dir = Path(__file__).parent.resolve()
        self.gui_mode = gui_mode
        
        if self.system == "Windows":
            self.install_dir = Path(os.environ.get('APPDATA', '')) / "CryptoDisk"
        else:
            self.install_dir = Path.home() / ".local" / "share" / "CryptoDisk"
            
        if gui_mode:
            self.create_window()
        
    def create_window(self):
        self.root = tk.Tk()
        self.root.title("CryptoDisk Installer")
        self.root.geometry("500x600")
        self.root.configure(bg='white')
        
        main_container = tk.Frame(self.root, bg='white')
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        header_frame = tk.Frame(main_container, bg='#1e3a8a', height=80)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        header_frame.pack_propagate(False)
        
        title = tk.Label(header_frame, text="CryptoDisk Installer", 
                        bg='#1e3a8a', fg='white', font=('Arial', 18, 'bold'))
        title.place(relx=0.5, rely=0.3, anchor='center')
        
        subtitle = tk.Label(header_frame, text="Secure File Destruction System", 
                           bg='#1e3a8a', fg='#bfdbfe', font=('Arial', 11))
        subtitle.place(relx=0.5, rely=0.7, anchor='center')
        
        info_frame = tk.Frame(main_container, bg='#f8fafc', relief='solid', bd=1)
        info_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        info_text = tk.Text(info_frame, bg='#f8fafc', fg='#334155', font=('Arial', 10),
                           wrap=tk.WORD, relief='flat', padx=15, pady=15, height=12)
        info_text.pack(fill=tk.BOTH, expand=True)
        
        features = """FEATURES:
• Military-grade file deletion (AES-256 encryption)
• Multiple secure overwrite methods (Gutmann, DoD, NIST)  
• Drag & drop interface for easy use
• Context menu integration (right-click any file)
• Cross-platform support (Windows/Linux)
• Automatic file monitoring in CryptoDisk folder

WHAT WILL BE INSTALLED:
• Main CryptoDisk application files
• Desktop shortcut (.lnk file)
• Context menu registry entries
• CryptoDisk folder on Desktop
• Python dependencies (if missing)"""

        info_text.insert('1.0', features)
        info_text.config(state='disabled')
        
        options_frame = tk.LabelFrame(main_container, text="Installation Options", 
                                     bg='white', fg='#1e40af', font=('Arial', 11, 'bold'),
                                     padx=10, pady=10)
        options_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.context_menu_var = tk.BooleanVar(value=True)
        self.desktop_var = tk.BooleanVar(value=True)
        self.startup_var = tk.BooleanVar(value=False)
        
        cb1 = tk.Checkbutton(options_frame, 
                            text="Add context menu (right-click integration)",
                            variable=self.context_menu_var, bg='white', fg='#374151',
                            font=('Arial', 10), activebackground='white')
        cb1.pack(anchor='w', pady=2)
        
        cb2 = tk.Checkbutton(options_frame,
                            text="Create desktop shortcut",
                            variable=self.desktop_var, bg='white', fg='#374151',
                            font=('Arial', 10), activebackground='white')
        cb2.pack(anchor='w', pady=2)
        
        cb3 = tk.Checkbutton(options_frame,
                            text="Start with system (background monitoring)",
                            variable=self.startup_var, bg='white', fg='#374151',
                            font=('Arial', 10), activebackground='white')
        cb3.pack(anchor='w', pady=2)
        
        button_frame = tk.Frame(main_container, bg='white')
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        install_btn = tk.Button(button_frame, text="INSTALL CRYPTODISK",
                               command=self.install_cryptodisk,
                               bg='#059669', fg='white', font=('Arial', 12, 'bold'),
                               relief='flat', padx=30, pady=12, cursor='hand2',
                               activebackground='#047857')
        install_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        uninstall_btn = tk.Button(button_frame, text="UNINSTALL",
                                 command=self.uninstall_cryptodisk,
                                 bg='#dc2626', fg='white', font=('Arial', 12, 'bold'),
                                 relief='flat', padx=30, pady=12, cursor='hand2',
                                 activebackground='#b91c1c')
        uninstall_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        close_btn = tk.Button(button_frame, text="CLOSE",
                             command=self.root.destroy,
                             bg='#6b7280', fg='white', font=('Arial', 12, 'bold'),
                             relief='flat', padx=30, pady=12, cursor='hand2',
                             activebackground='#4b5563')
        close_btn.pack(side=tk.RIGHT)
        
        self.status_var = tk.StringVar(value="Ready to install CryptoDisk")
        status_frame = tk.Frame(main_container, bg='#f1f5f9', relief='solid', bd=1)
        status_frame.pack(fill=tk.X)
        
        status_label = tk.Label(status_frame, textvariable=self.status_var,
                               bg='#f1f5f9', fg='#475569', font=('Arial', 9),
                               pady=8)
        status_label.pack()
        
    def update_status(self, message):
        if self.gui_mode:
            self.status_var.set(message)
            self.root.update_idletasks()
        print(f"Status: {message}")
        
    def install_cryptodisk(self, context_menu=True, desktop=True, startup=False):
        if self.gui_mode:
            context_menu = self.context_menu_var.get()
            desktop = self.desktop_var.get()
            startup = self.startup_var.get()
            
        try:
            self.update_status("Starting installation...")
            
            self.update_status("Creating installation directory...")
            self.install_dir.mkdir(parents=True, exist_ok=True)
            print(f"Install directory: {self.install_dir}")
            
            self.update_status("Copying application files...")
            required_files = ["main.py", "crypto_engine.py", "secure_delete.py", "context_menu.py"]
            
            copied_files = []
            for filename in required_files:
                source = self.app_dir / filename
                destination = self.install_dir / filename
                
                if source.exists():
                    shutil.copy2(source, destination)
                    copied_files.append(filename)
                    print(f"Copied: {filename}")
                else:
                    print(f"Missing file: {filename}")
            
            print(f"Copied {len(copied_files)} files: {copied_files}")
            
            icon_files = ["icon.ico", "icon.png"]
            for icon_file in icon_files:
                source = self.app_dir / icon_file
                destination = self.install_dir / icon_file
                if source.exists():
                    shutil.copy2(source, destination)
                    print(f"Copied icon: {icon_file}")
            
            self.update_status("Creating CryptoDisk folder on Desktop...")
            desktop_cryptodisk = Path.home() / "Desktop" / "CryptoDisk"
            desktop_cryptodisk.mkdir(exist_ok=True)
            print(f"Created Desktop folder: {desktop_cryptodisk}")
            
            if desktop:
                self.update_status("Creating desktop shortcut...")
                shortcut_created = self.create_desktop_shortcut()
                if shortcut_created:
                    print("Desktop shortcut created successfully")
                else:
                    print("Desktop shortcut creation failed")
            
            if context_menu:
                self.update_status("Installing context menu integration...")
                context_menu_installed = self.setup_context_menu()
                if context_menu_installed:
                    print("Context menu installed successfully")
                else:
                    print("Context menu installation failed")
            
            if startup and self.system == "Windows":
                self.update_status("Setting up system startup...")
                startup_setup = self.setup_startup_entry()
                if startup_setup:
                    print("Startup entry created successfully")
                else:
                    print("Startup entry creation failed")
            
            self.update_status("Checking Python dependencies...")
            self.verify_dependencies()
            
            self.update_status("Installation completed successfully!")
            
            result_message = f"CryptoDisk has been installed successfully!\n\n"
            result_message += f"Installation location: {self.install_dir}\n"
            result_message += f"Desktop folder: {Path.home() / 'Desktop' / 'CryptoDisk'}\n\n"
            result_message += "You can now:\n"
            result_message += "• Use the desktop shortcut to launch CryptoDisk\n"
            if context_menu:
                result_message += "• Right-click any file and select 'Delete with CryptoDisk'\n"
            result_message += "• Drag files to the CryptoDisk folder on your desktop"
            
            if self.gui_mode:
                messagebox.showinfo("Installation Complete", result_message)
            else:
                print(result_message)
                
            return True
            
        except Exception as error:
            self.update_status("Installation failed!")
            error_message = f"Installation failed with error:\n\n{str(error)}\n\n"
            error_message += f"Install directory: {self.install_dir}\n"
            error_message += "Please check file permissions and try again."
            
            if self.gui_mode:
                messagebox.showerror("Installation Error", error_message)
            else:
                print(error_message)
            print(f"Installation error: {error}")
            return False
    
    def create_desktop_shortcut(self):
        try:
            if self.system == "Windows":
                desktop_path = Path.home() / "Desktop"
                shortcut_path = desktop_path / "CryptoDisk.lnk"
                
                vbs_script = f'''
Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = "{shortcut_path}"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "{sys.executable}"
oLink.Arguments = """"{self.install_dir / "main.py"}""""
oLink.WorkingDirectory = "{self.install_dir}"
oLink.Description = "CryptoDisk - Secure File Deletion"
oLink.IconLocation = "{self.install_dir / "icon.ico"}"
oLink.Save
'''
                
                vbs_path = self.install_dir / "create_shortcut.vbs"
                with open(vbs_path, 'w') as f:
                    f.write(vbs_script)
                
                result = subprocess.run(['cscript', '//nologo', str(vbs_path)], 
                                      capture_output=True, text=True)
                
                vbs_path.unlink()
                
                if result.returncode == 0 and shortcut_path.exists():
                    print(f"Shortcut created at: {shortcut_path}")
                    return True
                else:
                    print(f"VBS script failed: {result.stderr}")
                    return self.create_batch_shortcut()
            else:
                return self.create_linux_shortcut()
                
        except Exception as e:
            print(f"Shortcut creation error: {e}")
            return False
    
    def create_batch_shortcut(self):
        try:
            desktop_path = Path.home() / "Desktop"
            batch_path = desktop_path / "CryptoDisk.bat"
            
            batch_content = f'''@echo off
cd /d "{self.install_dir}"
"{sys.executable}" "main.py"
pause
'''
            
            with open(batch_path, 'w') as f:
                f.write(batch_content)
            
            print(f"Batch shortcut created at: {batch_path}")
            return True
            
        except Exception as e:
            print(f"Batch shortcut creation error: {e}")
            return False
    
    def create_linux_shortcut(self):
        try:
            icon_png = self.install_dir / "icon.png"
            icon_path = str(icon_png) if icon_png.exists() else ""
            
            desktop_content = f'''[Desktop Entry]
Version=1.0
Type=Application
Name=CryptoDisk
Comment=Secure File Destruction
Exec={sys.executable} "{self.install_dir / "main.py"}"
Icon={icon_path}
Terminal=false
Categories=Utility;Security;System;
StartupNotify=true
'''
            
            desktop_path = Path.home() / "Desktop"
            desktop_shortcut = desktop_path / "CryptoDisk.desktop"
            
            with open(desktop_shortcut, 'w') as f:
                f.write(desktop_content)
            desktop_shortcut.chmod(0o755)
            
            applications_dir = Path.home() / ".local" / "share" / "applications"
            applications_dir.mkdir(parents=True, exist_ok=True)
            app_shortcut = applications_dir / "CryptoDisk.desktop"
            
            with open(app_shortcut, 'w') as f:
                f.write(desktop_content)
            app_shortcut.chmod(0o755)
            
            subprocess.run(["update-desktop-database", str(applications_dir)], 
                         capture_output=True)
            
            print(f"Linux shortcuts created")
            return True
            
        except Exception as e:
            print(f"Linux shortcut creation error: {e}")
            return False
    
    def setup_context_menu(self):
        try:
            if self.system == "Windows":
                import winreg as reg
                
                pythonw_exe = Path(sys.executable).parent / "pythonw.exe"
                python_path = str(pythonw_exe) if pythonw_exe.exists() else sys.executable
                
                script_path = self.install_dir / "main.py"
                icon_path = self.install_dir / "icon.ico"
                
                key_path = r"*\shell\CryptoDisk"
                command_path = r"*\shell\CryptoDisk\command"
                
                with reg.CreateKey(reg.HKEY_CLASSES_ROOT, key_path) as key:
                    reg.SetValue(key, "", reg.REG_SZ, "Delete with CryptoDisk")
                    if icon_path.exists():
                        reg.SetValueEx(key, "Icon", 0, reg.REG_SZ, str(icon_path))
                    
                with reg.CreateKey(reg.HKEY_CLASSES_ROOT, command_path) as key:
                    command = f'"{python_path}" "{script_path}" --delete "%1"'
                    reg.SetValue(key, "", reg.REG_SZ, command)
                
                folder_key_path = r"Directory\shell\CryptoDisk"
                folder_command_path = r"Directory\shell\CryptoDisk\command"
                
                with reg.CreateKey(reg.HKEY_CLASSES_ROOT, folder_key_path) as key:
                    reg.SetValue(key, "", reg.REG_SZ, "Delete with CryptoDisk")
                    if icon_path.exists():
                        reg.SetValueEx(key, "Icon", 0, reg.REG_SZ, str(icon_path))
                    
                with reg.CreateKey(reg.HKEY_CLASSES_ROOT, folder_command_path) as key:
                    command = f'"{python_path}" "{script_path}" --delete "%1"'
                    reg.SetValue(key, "", reg.REG_SZ, command)
                
            else:
                icon_png = self.install_dir / "icon.png"
                icon_path = str(icon_png) if icon_png.exists() else ""
                
                desktop_file_content = f"""[Desktop Entry]
Type=Action
Name=Delete with CryptoDisk
Icon={icon_path}
Profiles=profile-zero;

[X-Action-Profile profile-zero]
Exec={sys.executable} {self.install_dir / "main.py"} --delete %f
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
    "{sys.executable}" "{self.install_dir / "main.py"}" --delete "$file" &
done
wait
"""
                
                nautilus_script_path = nautilus_scripts_dir / "Delete with CryptoDisk"
                with open(nautilus_script_path, 'w') as f:
                    f.write(nautilus_script_content)
                nautilus_script_path.chmod(0o755)
                
                subprocess.run(["update-desktop-database", str(applications_dir)], 
                             capture_output=True)
            
            print("Context menu registry entries created")
            return True
                
        except Exception as e:
            print(f"Context menu setup failed: {e}")
            return False
    
    def setup_startup_entry(self):
        try:
            import winreg as reg
            startup_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
            
            with reg.OpenKey(reg.HKEY_CURRENT_USER, startup_key, 0, reg.KEY_SET_VALUE) as key:
                startup_command = f'"{sys.executable}" "{self.install_dir / "main.py"}" --background'
                reg.SetValueEx(key, "CryptoDisk", 0, reg.REG_SZ, startup_command)
            
            print("Startup registry entry created")
            return True
                
        except Exception as e:
            print(f"Startup setup failed: {e}")
            return False
    
    def verify_dependencies(self):
        required_packages = ["tkinterdnd2", "cryptography", "watchdog"]
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            if self.gui_mode:
                result = messagebox.askyesno("Missing Dependencies",
                                           f"The following Python packages are required:\n\n" +
                                           f"{', '.join(missing_packages)}\n\n" +
                                           f"Would you like to install them automatically?")
            else:
                result = True
                print(f"Installing missing packages: {', '.join(missing_packages)}")
                
            if result:
                try:
                    for package in missing_packages:
                        self.update_status(f"Installing {package}...")
                        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                        print(f"Installed package: {package}")
                except Exception as e:
                    error_msg = f"Could not install dependencies automatically.\n\n" + \
                               f"Please run this command manually:\n" + \
                               f"pip install {' '.join(missing_packages)}"
                    if self.gui_mode:
                        messagebox.showwarning("Dependency Installation Failed", error_msg)
                    else:
                        print(error_msg)
                    print(f"Dependency installation failed: {e}")
    
    def uninstall_cryptodisk(self):
        if self.gui_mode:
            confirm = messagebox.askyesno("Confirm Uninstall",
                                        "Are you sure you want to uninstall CryptoDisk?\n\n" +
                                        "This will remove all installed files and registry entries.\n" +
                                        "Files in the CryptoDisk folder will NOT be deleted.")
        else:
            confirm = True
            print("Uninstalling CryptoDisk...")
        
        if not confirm:
            return False
        
        try:
            self.update_status("Uninstalling CryptoDisk...")
            
            if self.system == "Windows":
                self.update_status("Removing context menu...")
                try:
                    import winreg as reg
                    reg.DeleteKey(reg.HKEY_CLASSES_ROOT, r"*\shell\CryptoDisk\command")
                    reg.DeleteKey(reg.HKEY_CLASSES_ROOT, r"*\shell\CryptoDisk")
                    reg.DeleteKey(reg.HKEY_CLASSES_ROOT, r"Directory\shell\CryptoDisk\command")
                    reg.DeleteKey(reg.HKEY_CLASSES_ROOT, r"Directory\shell\CryptoDisk")
                    print("Context menu entries removed")
                except Exception as e:
                    print(f"Context menu removal failed: {e}")
                
                self.update_status("Removing startup entry...")
                try:
                    startup_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
                    with reg.OpenKey(reg.HKEY_CURRENT_USER, startup_key, 0, reg.KEY_SET_VALUE) as key:
                        reg.DeleteValue(key, "CryptoDisk")
                    print("Startup entry removed")
                except Exception as e:
                    print(f"Startup removal failed: {e}")
            else:
                try:
                    local_share = Path.home() / ".local" / "share"
                    applications_dir = local_share / "applications"
                    nautilus_scripts_dir = local_share / "nautilus" / "scripts"
                    
                    files_to_remove = [
                        applications_dir / "cryptodisk-context.desktop",
                        applications_dir / "CryptoDisk.desktop",
                        nautilus_scripts_dir / "Delete with CryptoDisk"
                    ]
                    
                    for file_path in files_to_remove:
                        try:
                            file_path.unlink()
                            print(f"Removed: {file_path}")
                        except FileNotFoundError:
                            pass
                        except Exception as e:
                            print(f"Failed to remove {file_path}: {e}")
                            
                    subprocess.run(["update-desktop-database", str(applications_dir)], 
                                 capture_output=True)
                except Exception as e:
                    print(f"Linux cleanup failed: {e}")
            
            self.update_status("Removing desktop shortcuts...")
            desktop_path = Path.home() / "Desktop"
            shortcuts = ["CryptoDisk.lnk", "CryptoDisk.bat", "CryptoDisk.desktop"]
            
            for shortcut in shortcuts:
                shortcut_path = desktop_path / shortcut
                try:
                    shortcut_path.unlink()
                    print(f"Removed shortcut: {shortcut}")
                except FileNotFoundError:
                    pass
                except Exception as e:
                    print(f"Failed to remove {shortcut}: {e}")
            
            self.update_status("Removing installation files...")
            if self.install_dir.exists():
                shutil.rmtree(self.install_dir)
                print(f"Removed installation directory: {self.install_dir}")
            
            self.update_status("Uninstallation completed!")
            success_msg = "CryptoDisk has been uninstalled successfully!"
            if self.gui_mode:
                messagebox.showinfo("Uninstall Complete", success_msg)
            else:
                print(success_msg)
                
            return True
            
        except Exception as error:
            self.update_status("Uninstallation failed!")
            error_msg = f"Uninstallation failed:\n\n{str(error)}"
            if self.gui_mode:
                messagebox.showerror("Uninstall Error", error_msg)
            else:
                print(error_msg)
            print(f"Uninstallation error: {error}")
            return False
    
    def run(self):
        if self.gui_mode:
            self.root.mainloop()

def main():
    parser = argparse.ArgumentParser(description='CryptoDisk Installer')
    parser.add_argument('--install', action='store_true', help='Install CryptoDisk without GUI')
    parser.add_argument('--uninstall', action='store_true', help='Uninstall CryptoDisk without GUI')
    parser.add_argument('--no-context-menu', action='store_true', help='Skip context menu installation')
    parser.add_argument('--no-desktop', action='store_true', help='Skip desktop shortcut creation')
    parser.add_argument('--startup', action='store_true', help='Add to system startup')
    
    args = parser.parse_args()
    
    if args.install or args.uninstall:
        installer = WorkingInstaller(gui_mode=False)
        
        if args.install:
            context_menu = not args.no_context_menu
            desktop = not args.no_desktop
            startup = args.startup
            
            success = installer.install_cryptodisk(
                context_menu=context_menu,
                desktop=desktop,
                startup=startup
            )
            sys.exit(0 if success else 1)
            
        elif args.uninstall:
            success = installer.uninstall_cryptodisk()
            sys.exit(0 if success else 1)
    else:
        installer = WorkingInstaller(gui_mode=True)
        installer.run()

if __name__ == "__main__":
    main()