#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import sys
import threading
import time
from pathlib import Path
import shutil
from tkinterdnd2 import DND_FILES, TkinterDnD
from crypto_engine import CryptoEngine
from secure_delete import SecureDelete
import platform
import argparse
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class CryptoDiskFolderHandler(FileSystemEventHandler):
    def __init__(self, app):
        self.app = app
        
    def on_created(self, event):
        if not event.is_directory:
            file_path = Path(event.src_path)
            if not file_path.suffix == '.crypted' and file_path.name != '.gitkeep':
                self.app.process_dropped_file(str(file_path))

class CryptoDisk:
    def __init__(self, background_mode=False):
        self.system = platform.system()
        self.background_mode = background_mode
        self.setup_paths()
        self.crypto = CryptoEngine()
        self.secure_delete = SecureDelete()
        self.load_settings()
        
        if not background_mode:
            self.setup_gui()
        else:
            print("CryptoDisk running in background mode...")
            
        self.setup_folder_monitoring()
        
    def setup_paths(self):
        if self.system == "Windows":
            self.desktop = Path.home() / "Desktop"
        else:
            self.desktop = Path.home() / "Desktop"
            if not self.desktop.exists():
                self.desktop = Path.home()
        
        self.cryptodisk_folder = self.desktop / "CryptoDisk"
        self.cryptodisk_folder.mkdir(exist_ok=True)
        
        self.app_dir = Path(__file__).parent
        self.icon_path = self.app_dir / "icon.ico"
        self.settings_file = self.app_dir / "settings.json"
        
    def load_settings(self):
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    self.secure_delete.set_methods(
                        gutmann=settings.get('gutmann', True),
                        dod=settings.get('dod', True),
                        nist=settings.get('nist', True)
                    )
        except:
            pass
            
    def save_settings(self):
        try:
            settings = {
                'gutmann': self.secure_delete.use_gutmann,
                'dod': self.secure_delete.use_dod,
                'nist': self.secure_delete.use_nist
            }
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f)
        except:
            pass
        
    def setup_gui(self):
        self.root = TkinterDnD.Tk()
        self.root.title("CryptoDisk - Secure File Destruction")
        self.root.geometry("600x400")
        self.root.configure(bg='#2b2b2b')
        
        if self.icon_path.exists():
            try:
                if self.system == "Windows":
                    self.root.iconbitmap(str(self.icon_path))
                else:
                    icon_img = tk.PhotoImage(file=str(self.icon_path))
                    self.root.iconphoto(True, icon_img)
            except:
                pass
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', background='#2b2b2b', foreground='#ffffff', font=('Arial', 16, 'bold'))
        style.configure('Info.TLabel', background='#2b2b2b', foreground='#cccccc', font=('Arial', 10))
        style.configure('Custom.TButton', font=('Arial', 12, 'bold'))
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title_label = ttk.Label(main_frame, text="CryptoDisk", style='Title.TLabel')
        title_label.pack(pady=(0, 10))
        
        info_label = ttk.Label(main_frame, 
                              text="Secure file destruction with military-grade overwriting",
                              style='Info.TLabel')
        info_label.pack(pady=(0, 20))
        
        self.drop_frame = tk.Frame(main_frame, bg='#404040', relief='ridge', bd=2)
        self.drop_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        self.drop_frame.drop_target_register(DND_FILES)
        self.drop_frame.dnd_bind('<<Drop>>', self.on_drop)
        
        drop_label = tk.Label(self.drop_frame, 
                             text="Drag files here to encrypt and queue for secure deletion\n\n" +
                                  "Files will be:\n" +
                                  "• Encrypted with AES-256\n" +
                                  "• Renamed randomly\n" +
                                  "• Queued for secure overwriting",
                             bg='#404040', fg='#ffffff', font=('Arial', 12),
                             justify=tk.CENTER)
        drop_label.pack(expand=True)
        
        self.file_list = tk.Listbox(main_frame, bg='#353535', fg='#ffffff', 
                                   font=('Consolas', 9), height=8)
        self.file_list.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        self.empty_button = ttk.Button(button_frame, text="Empty CryptoDisk", 
                                      command=self.empty_cryptodisk, style='Custom.TButton')
        self.empty_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.add_button = ttk.Button(button_frame, text="Add Files", 
                                    command=self.add_files, style='Custom.TButton')
        self.add_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.settings_button = ttk.Button(button_frame, text="Settings", 
                                         command=self.show_settings, style='Custom.TButton')
        self.settings_button.pack(side=tk.RIGHT)
        
        self.status_var = tk.StringVar(value="Ready - Monitoring CryptoDisk folder")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, style='Info.TLabel')
        status_label.pack(pady=(10, 0))
        
        self.update_file_list()
        
    def setup_folder_monitoring(self):
        self.observer = Observer()
        handler = CryptoDiskFolderHandler(self)
        self.observer.schedule(handler, str(self.cryptodisk_folder), recursive=False)
        self.observer.start()
        
    def process_dropped_file(self, file_path):
        threading.Thread(target=self._process_file_thread, args=(file_path,), daemon=True).start()
        
    def _process_file_thread(self, file_path):
        try:
            if not self.background_mode:
                self.status_var.set(f"Processing: {Path(file_path).name}")
            
            original_path = Path(file_path)
            if not original_path.exists():
                return
                
            random_name = self.crypto.generate_random_name()
            encrypted_path = self.cryptodisk_folder / f"{random_name}.crypted"
            
            self.crypto.encrypt_file(str(original_path), str(encrypted_path))
            self.secure_delete.secure_delete_file(str(original_path))
            
            if not self.background_mode:
                self.root.after(0, self.update_file_list)
                self.status_var.set("Ready - Monitoring CryptoDisk folder")
                
        except Exception as e:
            if not self.background_mode:
                messagebox.showerror("Error", f"Failed to process {file_path}: {str(e)}")
        
    def on_drop(self, event):
        files = self.root.tk.splitlist(event.data)
        self.process_files(files)
        
    def add_files(self):
        files = filedialog.askopenfilenames(title="Select files to add to CryptoDisk")
        if files:
            self.process_files(files)
            
    def process_files(self, files):
        for file_path in files:
            self.process_dropped_file(file_path)
        
    def empty_cryptodisk(self):
        files = list(self.cryptodisk_folder.glob("*.crypted"))
        if not files:
            messagebox.showinfo("Info", "CryptoDisk is already empty")
            return
            
        result = messagebox.askyesno("Confirm Deletion", 
                                   f"This will permanently destroy {len(files)} files using military-grade overwriting.\n\n" +
                                   "This action CANNOT be undone!\n\nContinue?")
        if not result:
            return
            
        threading.Thread(target=self._empty_cryptodisk_thread, args=(files,), daemon=True).start()
        
    def _empty_cryptodisk_thread(self, files):
        for i, file_path in enumerate(files, 1):
            try:
                self.status_var.set(f"Securely deleting {i}/{len(files)}: {file_path.name}")
                self.secure_delete.secure_delete_file(str(file_path))
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
                
        self.status_var.set("Ready - CryptoDisk emptied successfully")
        self.root.after(0, self.update_file_list)
        
    def update_file_list(self):
        self.file_list.delete(0, tk.END)
        files = list(self.cryptodisk_folder.glob("*.crypted"))
        for file_path in files:
            size = file_path.stat().st_size
            size_str = self.format_size(size)
            self.file_list.insert(tk.END, f"{file_path.name} ({size_str})")
            
    def format_size(self, size_bytes):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"
        
    def show_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("CryptoDisk Settings")
        settings_window.geometry("400x300")
        settings_window.configure(bg='#2b2b2b')
        
        if self.icon_path.exists():
            try:
                if self.system == "Windows":
                    settings_window.iconbitmap(str(self.icon_path))
            except:
                pass
        
        ttk.Label(settings_window, text="Secure Deletion Methods:", 
                 style='Title.TLabel').pack(pady=10)
        
        methods_frame = ttk.Frame(settings_window)
        methods_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.gutmann_var = tk.BooleanVar(value=self.secure_delete.use_gutmann)
        ttk.Checkbutton(methods_frame, text="Gutmann Method (35 passes)", 
                       variable=self.gutmann_var).pack(anchor='w', pady=5)
        
        self.dod_var = tk.BooleanVar(value=self.secure_delete.use_dod)
        ttk.Checkbutton(methods_frame, text="DoD 5220.22-M (3 passes)", 
                       variable=self.dod_var).pack(anchor='w', pady=5)
        
        self.nist_var = tk.BooleanVar(value=self.secure_delete.use_nist)
        ttk.Checkbutton(methods_frame, text="NIST 800-88 (1 pass)", 
                       variable=self.nist_var).pack(anchor='w', pady=5)
        
        ttk.Button(settings_window, text="Apply Settings", 
                  command=lambda: self.apply_settings(settings_window)).pack(pady=20)
        
    def apply_settings(self, window):
        self.secure_delete.set_methods(
            gutmann=self.gutmann_var.get(),
            dod=self.dod_var.get(),
            nist=self.nist_var.get()
        )
        self.save_settings()
        window.destroy()
        messagebox.showinfo("Settings", "Settings applied successfully")
        
    def run(self):
        if not self.background_mode:
            self.root.mainloop()
        else:
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("CryptoDisk background service stopped")
                
    def stop(self):
        if hasattr(self, 'observer'):
            self.observer.stop()
            self.observer.join()

def delete_file_directly(file_path):
    try:
        secure_delete = SecureDelete()
        
        original_path = Path(file_path)
        if not original_path.exists():
            return
            
        if secure_delete.secure_delete_file(str(original_path)):
            try:
                original_path.unlink(missing_ok=True)
            except:
                pass
        
    except Exception as e:
        pass

def main():
    parser = argparse.ArgumentParser(description='CryptoDisk - Secure File Destruction')
    parser.add_argument('--delete', metavar='FILE', help='Delete file directly without GUI')
    parser.add_argument('--background', action='store_true', help='Run in background mode')
    parser.add_argument('--empty', action='store_true', help='Empty CryptoDisk folder')
    parser.add_argument('--settings', action='store_true', help='Show settings in terminal')
    parser.add_argument('--set-gutmann', choices=['on', 'off'], help='Enable/disable Gutmann method')
    parser.add_argument('--set-dod', choices=['on', 'off'], help='Enable/disable DoD method')
    parser.add_argument('--set-nist', choices=['on', 'off'], help='Enable/disable NIST method')
    
    args = parser.parse_args()
    
    if args.delete:
        delete_file_directly(args.delete)
        return
        
    if args.empty:
        desktop = Path.home() / "Desktop"
        cryptodisk_folder = desktop / "CryptoDisk"
        files = list(cryptodisk_folder.glob("*.crypted"))
        
        if not files:
            print("CryptoDisk is already empty")
            return
            
        print(f"Found {len(files)} files to delete")
        confirm = input(f"Delete {len(files)} files permanently? (y/N): ")
        
        if confirm.lower() == 'y':
            secure_delete = SecureDelete()
            for i, file_path in enumerate(files, 1):
                print(f"Deleting {i}/{len(files)}: {file_path.name}")
                secure_delete.secure_delete_file(str(file_path))
            print("CryptoDisk emptied successfully")
        return
        
    app = CryptoDisk(background_mode=args.background)
    
    if args.settings or args.set_gutmann or args.set_dod or args.set_nist:
        app.load_settings()
        
        if args.set_gutmann:
            app.secure_delete.use_gutmann = args.set_gutmann == 'on'
        if args.set_dod:
            app.secure_delete.use_dod = args.set_dod == 'on'
        if args.set_nist:
            app.secure_delete.use_nist = args.set_nist == 'on'
            
        if args.set_gutmann or args.set_dod or args.set_nist:
            app.save_settings()
            print("Settings updated")
            
        if args.settings:
            methods, total_passes = app.secure_delete.get_overwrite_info()
            print("Current Settings:")
            for method in methods:
                print(f"  - {method}")
            print(f"Total passes: {total_passes}")
        return
        
    try:
        app.run()
    finally:
        app.stop()

if __name__ == "__main__":
    main()