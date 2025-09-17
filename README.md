# 🔐 CryptoDisk - Military-Grade Secure File Destruction

<div align="center">

![CryptoDisk Logo](https://img.shields.io/badge/CryptoDisk-Secure%20Deletion-red?style=for-the-badge&logo=shield&logoColor=white)

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey?style=flat-square)](https://github.com)
[![Security](https://img.shields.io/badge/Security-Military%20Grade-red?style=flat-square&logo=lock)](https://github.com)

**Professional-grade secure file destruction with AES-256 encryption and military overwriting standards**

[📥 Download](#installation) • [🚀 Quick Start](#quick-start) • [📖 Documentation](#documentation) • [⚙️ Configuration](#configuration)

</div>

---

## 🌟 Features

<table>
<tr>
<td width="50%">

### 🛡️ **Security Features**
- **AES-256 Encryption** before deletion
- **Gutmann Method** (35-pass overwrite)
- **DoD 5220.22-M** (3-pass overwrite)
- **NIST 800-88** (1-pass overwrite)
- **File name randomization**
- **Zero forensic recovery**

</td>
<td width="50%">

### 🎯 **User Experience**
- **Drag & Drop** interface
- **Right-click context menu**
- **Auto-monitoring** folder
- **Silent operation** (no console windows)
- **Cross-platform** support
- **Background service** mode

</td>
</tr>
</table>

---

## 📷 Screenshots

<div align="center">
<table>
<tr>
<td align="center">
<h4>🖥️ Main Interface</h4>
<img src="https://via.placeholder.com/300x200/2b2b2b/ffffff?text=CryptoDisk+GUI" alt="Main Interface" width="300"/>
</td>
<td align="center">
<h4>🖱️ Context Menu</h4>
<img src="https://via.placeholder.com/300x200/f0f0f0/333333?text=Right+Click+Menu" alt="Context Menu" width="300"/>
</td>
</tr>
</table>
</div>

---

## 🚀 Quick Start

### Windows Installation

```batch
# Download and run installer
python working_installer.py

# Or install without GUI
python working_installer.py --install
```

### Linux Installation

```bash
# GUI Installation
python working_installer.py

# Command Line Installation
python install_linux.py --install

# Install with all options
python install_linux.py --install --startup
```

### 🎯 Instant Usage

1. **Right-click any file** → Select **"Delete with CryptoDisk"**
2. **Drag files** to the **CryptoDisk folder** on Desktop
3. **Launch app** to manage settings and bulk operations

---

## 📦 Installation

### Prerequisites

```bash
# Python 3.8 or higher
python --version

# Install dependencies
pip install -r requirements.txt
```

### Windows Setup

<details>
<summary><b>🪟 Windows Installation Guide</b></summary>

#### Method 1: Automatic Installer (Recommended)
```batch
# Run as Administrator for full integration
python working_installer.py
```

#### Method 2: Manual Installation
```batch
# Clone repository
git clone https://github.com/yourusername/cryptodisk.git
cd cryptodisk

# Install dependencies
pip install -r requirements.txt

# Run installer
python working_installer.py --install --no-gui
```

#### Features Installed:
- ✅ Desktop shortcut
- ✅ Right-click context menu
- ✅ CryptoDisk monitoring folder
- ✅ Optional system startup
- ✅ Windows registry integration

</details>

### Linux Setup

<details>
<summary><b>🐧 Linux Installation Guide</b></summary>

#### Method 1: Interactive Installer
```bash
python working_installer.py
```

#### Method 2: Command Line Installer
```bash
# Basic installation
python install_linux.py --install

# Full installation with autostart
python install_linux.py --install --startup

# Installation without context menu
python install_linux.py --install --no-context-menu
```

#### Features Installed:
- ✅ Desktop shortcut (.desktop file)
- ✅ Applications menu entry
- ✅ Nautilus context menu
- ✅ CryptoDisk monitoring folder
- ✅ Optional autostart service
- ✅ System integration

</details>

---

## 🛠️ Usage

### 🖱️ Right-Click Deletion

Simply right-click any file or folder and select **"Delete with CryptoDisk"**

```
File.txt → Right Click → "Delete with CryptoDisk" → ✅ Securely Deleted
```

### 📁 Drag & Drop

1. Files dragged to **CryptoDisk folder** are automatically processed
2. Files are encrypted, renamed, and queued for secure deletion
3. Use **"Empty CryptoDisk"** button to permanently destroy queued files

### 💻 Command Line Usage

#### Windows
```batch
# Delete single file
python main.py --delete "C:\path\to\file.txt"

# Empty CryptoDisk folder
python main.py --empty

# Run in background
python main.py --background

# Configure settings
python main.py --set-gutmann off --set-dod on
```

#### Linux
```bash
# Delete single file
python install_linux.py --delete /path/to/file

# Empty CryptoDisk folder
python install_linux.py --empty

# Show current settings
python install_linux.py --settings

# Configure methods
python install_linux.py --set-gutmann on --set-nist off
```

---

## ⚙️ Configuration

### 🔧 Security Methods

<table>
<tr>
<th>Method</th>
<th>Passes</th>
<th>Description</th>
<th>Security Level</th>
</tr>
<tr>
<td><strong>NIST 800-88</strong></td>
<td>1</td>
<td>Random data overwrite</td>
<td>🟢 Standard</td>
</tr>
<tr>
<td><strong>DoD 5220.22-M</strong></td>
<td>3</td>
<td>Military standard (0x00, 0xFF, Random)</td>
<td>🟡 High</td>
</tr>
<tr>
<td><strong>Gutmann Method</strong></td>
<td>35</td>
<td>Maximum security overwrite patterns</td>
<td>🔴 Maximum</td>
</tr>
</table>

### ⚡ Performance vs Security

```
NIST Only:     🔵🔵⚪⚪⚪ (Fastest, Good Security)
DoD + NIST:    🔵🔵🔵⚪⚪ (Balanced)
All Methods:   🔵🔵🔵🔵🔵 (Slowest, Maximum Security)
```

---

## 🎛️ Settings Management

### GUI Settings
- Launch CryptoDisk app
- Click **"Settings"** button
- Toggle security methods
- Click **"Apply Settings"**

### Command Line Settings

#### Linux
```bash
# View current settings
python install_linux.py --settings

# Enable/disable methods
python install_linux.py --set-gutmann on
python install_linux.py --set-dod off
python install_linux.py --set-nist on
```

#### Windows
```batch
# Through main application
python main.py --set-gutmann on --set-dod on --set-nist on
```

---

## 🔒 Security Technical Details

### Encryption Process
1. **AES-256-CBC** encryption with random key
2. **PBKDF2-HMAC-SHA256** key derivation (100,000 iterations)
3. **Random salt** generation (256-bit)
4. **Metadata encryption** with original file information

### Overwrite Process
1. **Multiple pass overwriting** with specific patterns
2. **File name randomization** (multiple rounds)
3. **File system metadata clearing**
4. **Final deletion** from file system

### Security Standards Compliance
- ✅ **NIST SP 800-88** Revision 1
- ✅ **DoD 5220.22-M** Standards
- ✅ **Gutmann Method** Implementation
- ✅ **FIPS 140-2** Compatible algorithms

---

## 🚫 Uninstallation

### Windows
```batch
# GUI uninstaller
python working_installer.py

# Command line uninstall
python working_installer.py --uninstall
```

### Linux
```bash
# GUI uninstaller
python working_installer.py

# Command line uninstall
python install_linux.py --uninstall
```

**What gets removed:**
- All application files
- Registry entries (Windows)
- Desktop shortcuts
- Context menu entries
- Autostart entries
- Configuration files

**What stays:**
- CryptoDisk folder (with any remaining files)
- Python installation
- User documents

---

## 🆘 Troubleshooting

### Common Issues

<details>
<summary><b>❌ "Context menu not appearing"</b></summary>

**Windows:**
```batch
# Run installer as Administrator
python working_installer.py
```

**Linux:**
```bash
# Update desktop database
update-desktop-database ~/.local/share/applications
```
</details>

<details>
<summary><b>❌ "Permission denied" errors</b></summary>

**Windows:**
- Run Command Prompt as Administrator
- Check file is not in use by another program

**Linux:**
```bash
# Check file permissions
ls -la filename
chmod 644 filename  # Make writable
```
</details>

<details>
<summary><b>❌ "Dependencies not found"</b></summary>

```bash
# Reinstall dependencies
pip uninstall tkinterdnd2 cryptography watchdog
pip install -r requirements.txt
```
</details>

<details>
<summary><b>❌ "Console window appears (Windows)"</b></summary>

Ensure installer used `pythonw.exe`:
```batch
# Reinstall to fix
python working_installer.py --uninstall
python working_installer.py --install
```
</details>

### Getting Help

1. **Check logs** in installation directory
2. **Run diagnostics**: `python diagnostic.py`
3. **Verify installation**: Check if files exist in install directory
4. **Reinstall**: Uninstall completely, then reinstall

---

## 🔧 Development

### Project Structure
```
cryptodisk/
├── main.py                 # Main application
├── crypto_engine.py        # Encryption engine  
├── secure_delete.py        # Secure deletion methods
├── context_menu.py         # OS integration
├── working_installer.py    # Windows/Linux installer
├── install_linux.py        # Linux CLI installer
├── requirements.txt        # Python dependencies
├── icon.ico               # Windows icon
├── icon.png               # Linux icon
└── README.md              # This file
```

### Dependencies
- **tkinterdnd2**: Drag and drop support
- **cryptography**: AES encryption implementation
- **watchdog**: File system monitoring
- **pywin32**: Windows integration (Windows only)

### Contributing
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## ⚖️ Legal & Security

### ⚠️ Important Disclaimers

> **WARNING**: This tool permanently destroys data. Deleted files CANNOT be recovered. Use with extreme caution.

### Legal Notice
- **Use responsibly**: Only delete files you own
- **Backup important data**: Always keep backups elsewhere
- **Compliance**: Ensure usage complies with local laws
- **No warranty**: Software provided "as is"

### Security Note
This tool implements industry-standard secure deletion methods. However:
- **SSD considerations**: Modern SSDs may retain data in spare areas
- **System limitations**: Some file systems may cache data
- **Memory dumps**: Sensitive data may exist in RAM/swap files

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

---

## 🙏 Acknowledgments

- **Peter Gutmann** - Gutmann secure deletion method
- **NIST** - SP 800-88 Guidelines for Media Sanitization  
- **DoD** - 5220.22-M Security Requirements
- **Python Cryptography Team** - Excellent cryptography library
- **Open Source Community** - Various libraries and tools used

---

<div align="center">

### 🌟 Star this repository if it helped you secure your data!

[![GitHub stars](https://img.shields.io/github/stars/yourusername/cryptodisk?style=social)](https://github.com/yourusername/cryptodisk/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/yourusername/cryptodisk?style=social)](https://github.com/yourusername/cryptodisk/network)

**Made with ❤️ for digital privacy and security**

</div>
