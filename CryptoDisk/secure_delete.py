#!/usr/bin/env python3

import os
import random
import secrets
from pathlib import Path
import platform

class SecureDelete:
    def __init__(self):
        self.system = platform.system()
        self.use_gutmann = True
        self.use_dod = True
        self.use_nist = True
        
        self.gutmann_patterns = [
            b'\x55', b'\xAA', b'\x92\x49\x24', b'\x49\x24\x92', b'\x24\x92\x49',
            b'\x00', b'\x11', b'\x22', b'\x33', b'\x44', b'\x55', b'\x66', b'\x77',
            b'\x88', b'\x99', b'\xAA', b'\xBB', b'\xCC', b'\xDD', b'\xEE', b'\xFF',
            b'\x92\x49\x24', b'\x49\x24\x92', b'\x24\x92\x49', b'\x6D\xB6\xDB',
            b'\xB6\xDB\x6D', b'\xDB\x6D\xB6', None, b'\x92\x49\x24', b'\x49\x24\x92',
            b'\x24\x92\x49', b'\x6D\xB6\xDB', b'\xB6\xDB\x6D', b'\xDB\x6D\xB6',
            None, None
        ]
        
    def set_methods(self, gutmann=True, dod=True, nist=True):
        self.use_gutmann = gutmann
        self.use_dod = dod
        self.use_nist = nist
        
    def secure_delete_file(self, file_path):
        file_path = Path(file_path)
        if not file_path.exists():
            return False
            
        file_size = file_path.stat().st_size
        
        try:
            if self.use_nist:
                self._nist_overwrite(file_path, file_size)
                
            if self.use_dod:
                self._dod_overwrite(file_path, file_size)
                
            if self.use_gutmann:
                self._gutmann_overwrite(file_path, file_size)
                
            renamed_path = self._rename_file_randomly(file_path)
            renamed_path.unlink()
            return True
            
        except Exception as e:
            print(f"Error during secure deletion: {e}")
            try:
                file_path.unlink()
            except:
                pass
            return False
            
    def _nist_overwrite(self, file_path, file_size):
        with open(file_path, 'r+b') as f:
            random_data = secrets.token_bytes(min(file_size, 1024 * 1024))
            
            for offset in range(0, file_size, len(random_data)):
                f.seek(offset)
                remaining = min(len(random_data), file_size - offset)
                if remaining < len(random_data):
                    f.write(random_data[:remaining])
                else:
                    f.write(random_data)
            f.flush()
            if self.system != "Windows":
                os.fsync(f.fileno())
                
    def _dod_overwrite(self, file_path, file_size):
        patterns = [b'\x00', b'\xFF', None]
        
        for pattern in patterns:
            with open(file_path, 'r+b') as f:
                if pattern is None:
                    data = secrets.token_bytes(min(file_size, 1024 * 1024))
                else:
                    data = pattern * min(file_size, 1024 * 1024)
                    
                for offset in range(0, file_size, len(data)):
                    f.seek(offset)
                    remaining = min(len(data), file_size - offset)
                    if remaining < len(data):
                        if pattern is None:
                            f.write(data[:remaining])
                        else:
                            f.write(pattern * remaining)
                    else:
                        f.write(data)
                f.flush()
                if self.system != "Windows":
                    os.fsync(f.fileno())
                    
    def _gutmann_overwrite(self, file_path, file_size):
        for pattern in self.gutmann_patterns:
            with open(file_path, 'r+b') as f:
                if pattern is None:
                    data = secrets.token_bytes(min(file_size, 1024 * 1024))
                else:
                    if len(pattern) == 1:
                        data = pattern * min(file_size, 1024 * 1024)
                    else:
                        repeat_count = min(file_size, 1024 * 1024) // len(pattern) + 1
                        data = (pattern * repeat_count)[:min(file_size, 1024 * 1024)]
                        
                for offset in range(0, file_size, len(data)):
                    f.seek(offset)
                    remaining = min(len(data), file_size - offset)
                    if remaining < len(data):
                        if pattern is None:
                            f.write(data[:remaining])
                        else:
                            if len(pattern) == 1:
                                f.write(pattern * remaining)
                            else:
                                repeat_count = remaining // len(pattern) + 1
                                write_data = (pattern * repeat_count)[:remaining]
                                f.write(write_data)
                    else:
                        f.write(data)
                f.flush()
                if self.system != "Windows":
                    os.fsync(f.fileno())
                    
    def _rename_file_randomly(self, file_path):
        original_dir = file_path.parent
        original_name = file_path.name
        
        for i in range(3):
            random_name = self._generate_random_filename(len(original_name))
            new_path = original_dir / random_name
            
            try:
                file_path.rename(new_path)
                file_path = new_path
            except:
                break
                
        return file_path
        
    def _generate_random_filename(self, length):
        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        return ''.join(secrets.choice(chars) for _ in range(length))
        
    def secure_delete_directory(self, dir_path):
        dir_path = Path(dir_path)
        if not dir_path.exists() or not dir_path.is_dir():
            return False
            
        try:
            for item in dir_path.rglob('*'):
                if item.is_file():
                    self.secure_delete_file(item)
                    
            for item in sorted(dir_path.rglob('*'), key=lambda x: len(str(x)), reverse=True):
                if item.is_dir():
                    try:
                        item.rmdir()
                    except:
                        pass
                        
            dir_path.rmdir()
            return True
            
        except Exception as e:
            print(f"Error during directory secure deletion: {e}")
            return False
            
    def get_overwrite_info(self):
        methods = []
        total_passes = 0
        
        if self.use_nist:
            methods.append("NIST 800-88 (1 pass)")
            total_passes += 1
            
        if self.use_dod:
            methods.append("DoD 5220.22-M (3 passes)")
            total_passes += 3
            
        if self.use_gutmann:
            methods.append("Gutmann Method (35 passes)")
            total_passes += 35
            
        return methods, total_passes