#!/usr/bin/env python3

from pathlib import Path
import os
import sys

print('=== DIAGNÓSTICO CRYPTODISK ===')
print()

# Verificar pasta de instalação
install_dir = Path(os.environ.get('APPDATA', '')) / 'CryptoDisk'
print(f'Pasta de instalação: {install_dir}')
print(f'Existe? {install_dir.exists()}')

if install_dir.exists():
    print('Arquivos encontrados:')
    for file in install_dir.iterdir():
        print(f'  - {file.name}')
else:
    print('  - Pasta de instalação NÃO encontrada!')
print()

# Verificar Desktop
desktop = Path.home() / 'Desktop'
print(f'Desktop: {desktop}')
print(f'Existe? {desktop.exists()}')

if desktop.exists():
    print('Arquivos relacionados ao CryptoDisk no Desktop:')
    cryptodisk_files = []
    
    for file in desktop.iterdir():
        if 'cryptodisk' in file.name.lower():
            cryptodisk_files.append(file.name)
    
    if cryptodisk_files:
        for file in cryptodisk_files:
            print(f'  - {file}')
    else:
        print('  - Nenhum arquivo CryptoDisk encontrado no Desktop')
else:
    print('  - Desktop NÃO encontrado!')

print()

# Verificar pasta CryptoDisk específica
cryptodisk_folder = desktop / 'CryptoDisk'
print('Pasta CryptoDisk no Desktop:')
print(f'  Localização: {cryptodisk_folder}')
print(f'  Existe? {cryptodisk_folder.exists()}')

if cryptodisk_folder.exists():
    try:
        files_in_folder = list(cryptodisk_folder.iterdir())
        if files_in_folder:
            print('  Conteúdo da pasta:')
            for file in files_in_folder:
                print(f'    - {file.name}')
        else:
            print('  - Pasta vazia')
    except:
        print('  - Erro ao acessar pasta')

print()
print('=== CRIANDO ARQUIVOS FALTANTES ===')

# Criar pasta CryptoDisk no Desktop
try:
    cryptodisk_folder.mkdir(exist_ok=True)
    print(f'✅ Criada/verificada pasta: {cryptodisk_folder}')
except Exception as e:
    print(f'❌ Erro ao criar pasta: {e}')

# Criar arquivo .bat no Desktop
if install_dir.exists():
    try:
        batch_content = f'''@echo off
echo Iniciando CryptoDisk...
cd /d "{install_dir}"
"{sys.executable}" "main.py"
echo.
echo Pressione qualquer tecla para fechar...
pause >nul
'''
        
        batch_path = desktop / 'CryptoDisk.bat'
        with open(batch_path, 'w', encoding='utf-8') as f:
            f.write(batch_content)
        
        print(f'✅ Criado atalho: {batch_path}')
        
    except Exception as e:
        print(f'❌ Erro ao criar atalho .bat: {e}')
else:
    print('❌ Não é possível criar atalho - pasta de instalação não existe')

# Criar atalho Python direto
try:
    python_script = desktop / 'CryptoDisk.py'
    script_content = f'''#!/usr/bin/env python3
import sys
from pathlib import Path

install_dir = Path(r"{install_dir}")
main_script = install_dir / "main.py"

if main_script.exists():
    import subprocess
    subprocess.run([sys.executable, str(main_script)])
else:
    print("CryptoDisk não encontrado!")
    print(f"Procurando em: {{main_script}}")
    input("Pressione Enter para fechar...")
'''
    
    with open(python_script, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print(f'✅ Criado atalho Python: {python_script}')
    
except Exception as e:
    print(f'❌ Erro ao criar atalho Python: {e}')

print()
print('=== INSTRUÇÕES ===')
print('Agora você deve ter no Desktop:')
print('1. Pasta "CryptoDisk" - para arrastar arquivos')
print('2. Arquivo "CryptoDisk.bat" - clique duplo para abrir')
print('3. Arquivo "CryptoDisk.py" - alternativa ao .bat')
print()
print('Para testar, clique duplo no arquivo CryptoDisk.bat')
print('Se não funcionar, execute: python CryptoDisk.py')