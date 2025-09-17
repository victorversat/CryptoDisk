#!/usr/bin/env python3

import os
import secrets
import string
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import json
from pathlib import Path

class CryptoEngine:
    def __init__(self):
        self.key_size = 32
        self.iv_size = 16
        self.salt_size = 32
        self.iterations = 100000
        
    def generate_random_name(self, length=16):
        chars = string.ascii_lowercase + string.digits
        return ''.join(secrets.choice(chars) for _ in range(length))
        
    def generate_key_from_password(self, password, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=self.key_size,
            salt=salt,
            iterations=self.iterations,
        )
        return kdf.derive(password.encode())
        
    def encrypt_file(self, input_file, output_file, password=None):
        if password is None:
            password = self.generate_random_password()
            
        salt = os.urandom(self.salt_size)
        iv = os.urandom(self.iv_size)
        key = self.generate_key_from_password(password, salt)
        
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        
        input_path = Path(input_file)
        original_size = input_path.stat().st_size
        
        metadata = {
            'original_name': input_path.name,
            'original_size': original_size,
            'password': password,
            'timestamp': str(input_path.stat().st_mtime)
        }
        
        with open(input_file, 'rb') as infile, open(output_file, 'wb') as outfile:
            outfile.write(salt)
            outfile.write(iv)
            
            metadata_json = json.dumps(metadata).encode()
            metadata_size = len(metadata_json)
            outfile.write(metadata_size.to_bytes(4, byteorder='big'))
            
            encrypted_metadata = encryptor.update(self.pad_data(metadata_json))
            outfile.write(encrypted_metadata)
            
            while True:
                chunk = infile.read(8192)
                if not chunk:
                    break
                    
                if len(chunk) < 8192:
                    chunk = self.pad_data(chunk)
                    
                encrypted_chunk = encryptor.update(chunk)
                outfile.write(encrypted_chunk)
                
            final_chunk = encryptor.finalize()
            if final_chunk:
                outfile.write(final_chunk)
                
    def decrypt_file(self, input_file, output_file, password):
        with open(input_file, 'rb') as infile:
            salt = infile.read(self.salt_size)
            iv = infile.read(self.iv_size)
            metadata_size = int.from_bytes(infile.read(4), byteorder='big')
            
            key = self.generate_key_from_password(password, salt)
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
            decryptor = cipher.decryptor()
            
            encrypted_metadata = infile.read(self.pad_size(metadata_size))
            decrypted_metadata = decryptor.update(encrypted_metadata)
            metadata_json = self.unpad_data(decrypted_metadata)[:metadata_size]
            metadata = json.loads(metadata_json.decode())
            
            with open(output_file, 'wb') as outfile:
                bytes_written = 0
                target_size = metadata['original_size']
                
                while bytes_written < target_size:
                    chunk = infile.read(8192)
                    if not chunk:
                        break
                        
                    decrypted_chunk = decryptor.update(chunk)
                    
                    remaining = target_size - bytes_written
                    if remaining < len(decrypted_chunk):
                        decrypted_chunk = decrypted_chunk[:remaining]
                        
                    outfile.write(decrypted_chunk)
                    bytes_written += len(decrypted_chunk)
                    
                final_chunk = decryptor.finalize()
                if final_chunk and bytes_written < target_size:
                    remaining = target_size - bytes_written
                    if remaining > 0:
                        outfile.write(final_chunk[:remaining])
                        
        return metadata
        
    def pad_data(self, data):
        padding_length = 16 - (len(data) % 16)
        padding = bytes([padding_length] * padding_length)
        return data + padding
        
    def unpad_data(self, data):
        padding_length = data[-1]
        return data[:-padding_length]
        
    def pad_size(self, size):
        return ((size + 15) // 16) * 16
        
    def generate_random_password(self, length=32):
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(secrets.choice(chars) for _ in range(length))
        
    def secure_random_bytes(self, size):
        return os.urandom(size)
        
    def get_file_metadata(self, encrypted_file, password):
        try:
            with open(encrypted_file, 'rb') as infile:
                salt = infile.read(self.salt_size)
                iv = infile.read(self.iv_size)
                metadata_size = int.from_bytes(infile.read(4), byteorder='big')
                
                key = self.generate_key_from_password(password, salt)
                cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
                decryptor = cipher.decryptor()
                
                encrypted_metadata = infile.read(self.pad_size(metadata_size))
                decrypted_metadata = decryptor.update(encrypted_metadata)
                metadata_json = self.unpad_data(decrypted_metadata)[:metadata_size]
                return json.loads(metadata_json.decode())
        except:
            return None