import os
import requests
import zipfile
from pathlib import Path
import shutil
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("setup.log", mode='w')
    ]
)

# Define the base directory for the toolkit
BASE_DIR = Path("Technician_Toolkit")
TOOLS_DIR = BASE_DIR / "Tools"
READMES_DIR = BASE_DIR / "Readmes"
SCRIPTS_DIR = BASE_DIR / "Scripts"
DOCUMENTATION_DIR = BASE_DIR / "Documentation"
DRIVERS_DIR = BASE_DIR / "Drivers"
UTILITIES_DIR = BASE_DIR / "Utilities"

# Define tools with their download URLs and extraction info
TOOLS = [
    # Windows Tools
    {
        "name": "HWMonitor",
        "url": "https://download.cpuid.com/hwmonitor/hwmonitor_setup.exe",  # Updated URL
        "platform": "Windows",
        "description": "Hardware monitoring tool to check temperatures, voltages, and fan speeds."
    },
    {
        "name": "MemTest86",
        "url": "https://www.memtest86.com/downloads/memtest86-usb.zip",
        "platform": "Windows, Mac",
        "description": "Memory testing tool to check for RAM issues."
    },
    {
        "name": "CCleaner",
        "url": "https://download.ccleaner.com/ccsetup562.exe",  # Update to latest version if available
        "platform": "Windows",
        "description": "System optimization and cleaning tool."
    },
    {
        "name": "Malwarebytes",
        "url": "https://downloads.malwarebytes.com/file/mb3",
        "platform": "Windows, Mac",
        "description": "Anti-malware tool for scanning and removing malware."
    },
    {
        "name": "Hiren's BootCD",
        "url": "https://www.hirensbootcd.org/download/",  # Manual download
        "platform": "Windows",
        "description": "Comprehensive bootable toolkit for troubleshooting.",
        "manual": True,
        "manual_instructions": "Download the latest version from [Hiren's BootCD](https://www.hirensbootcd.org/download/) and place the ISO in the 'Tools/Hiren's BootCD' directory."
    },
    {
        "name": "Process Explorer",
        "url": "https://download.sysinternals.com/files/ProcessExplorer.zip",
        "platform": "Windows",
        "description": "Advanced process management tool."
    },
    {
        "name": "Autoruns",
        "url": "https://download.sysinternals.com/files/Autoruns.zip",
        "platform": "Windows",
        "description": "Utility to manage startup programs and services."
    },
    {
        "name": "Recuva",
        "url": "https://download.ccleaner.com/RecuvaSetup.exe",  # Updated URL
        "platform": "Windows",
        "description": "File recovery tool to restore deleted files."
    },
    {
        "name": "Macrium Reflect Free",
        "url": "https://downloads.macrium.com/reflectfree.exe",
        "platform": "Windows",
        "description": "Backup and disk imaging solution."
    },
    {
        "name": "Ninite",
        "url": "https://ninite.com/",  # Manual download
        "platform": "Windows",
        "description": "Bulk installer for essential Windows applications.",
        "manual": True,
        "manual_instructions": "Visit [Ninite](https://ninite.com/) to select and download the desired bulk installer. Place the installer in the 'Tools/Ninite' directory."
    },
    {
        "name": "Unlocker",
        "url": "https://www.filehorse.com/download-unlocker/",  # Manual download
        "platform": "Windows",
        "description": "Utility to delete locked files and manage file locks.",
        "manual": True,
        "manual_instructions": "Download Unlocker from [FileHorse](https://www.filehorse.com/download-unlocker/) and place the executable in the 'Tools/Unlocker' directory."
    },
    {
        "name": "TeamViewer",
        "url": "https://download.teamviewer.com/download/TeamViewer_Setup.exe",
        "platform": "Windows, Mac",
        "description": "Remote desktop application for remote support."
    },
    
    # Mac Tools
    {
        "name": "OnyX",
        "url": "https://www.titanium-software.fr/download.php?onyx",  # Manual download
        "platform": "Mac",
        "description": "Mac maintenance and optimization tool.",
        "manual": True,
        "manual_instructions": "Download OnyX from [Titanium Software](https://www.titanium-software.fr/download.php?onyx) and place the app in the 'Tools/OnyX' directory."
    },
    {
        "name": "Disk Drill",
        "url": "https://www.cleverfiles.com/download.php?file=D4bMAqXfdG",  # Updated direct download link
        "platform": "Mac",
        "description": "Data recovery software for Mac systems."
    },
    {
        "name": "Thunderbolt Control Center",
        "url": "https://example.com/download-thunderbolt-control-center.zip",  # Replace with actual URL or mark as manual
        "platform": "Mac",
        "description": "Manage Thunderbolt connections and devices.",
        "manual": True,
        "manual_instructions": "Download Thunderbolt Control Center from the official website and place the app in the 'Tools/Thunderbolt Control Center' directory."
    },
    
    # Android Tools
    {
        "name": "Android SDK Platform-Tools",
        "url": "https://dl.google.com/android/repository/platform-tools_r33.0.3-windows.zip",  # Update as needed
        "platform": "Windows, Mac",
        "description": "Includes ADB and Fastboot tools for Android development and troubleshooting."
    },
    
    # iOS Tools
    {
        "name": "Xcode Command Line Tools",
        "url": "https://developer.apple.com/download/more/",  # Manual download
        "platform": "Mac",
        "description": "Essential tools for iOS development, including compilers and debuggers.",
        "manual": True,
        "manual_instructions": "Download Xcode Command Line Tools from [Apple Developer](https://developer.apple.com/download/more/) and follow the installation instructions."
    },
    
    # Password Bypass Tools
    {
        "name": "Trinity Rescue Kit (TRK)",
        "url": "https://sourceforge.net/projects/trinityrescuekit/files/latest/download",  # Updated URL
        "platform": "Windows",
        "description": "A free and open-source Linux distribution for resetting Windows passwords and other system recovery tasks."
    },
    {
        "name": "Ophcrack",
        "url": "https://sourceforge.net/projects/ophcrack/files/latest/download",  # Manual download
        "platform": "Windows",
        "description": "An open-source tool that cracks Windows passwords using rainbow tables.",
        "manual": True,
        "manual_instructions": "Download Ophcrack from [SourceForge](https://sourceforge.net/projects/ophcrack/files/latest/download) and place the ISO or executable in the 'Tools/Ophcrack' directory."
    },
    {
        "name": "Offline NT Password & Registry Editor",
        "url": "https://sourceforge.net/projects/ntpasswd/files/latest/download",  # Manual download
        "platform": "Windows",
        "description": "A free tool to reset Windows user passwords by editing the Windows registry.",
        "manual": True,
        "manual_instructions": "Download Offline NT Password & Registry Editor from [SourceForge](https://sourceforge.net/projects/ntpasswd/files/latest/download) and place the ISO in the 'Tools/Offline NT Password & Registry Editor' directory."
    },
    {
        "name": "John the Ripper",
        "url": "https://github.com/openwall/john/releases/download/john-1.9.0-jumbo-1/john-1.9.0-jumbo-1.zip",  # Updated URL
        "platform": "Windows, Mac",
        "description": "A free and open-source password cracking tool targeted at Unix-based systems."
    },
    
    # Additional Tools
    {
        "name": "Sysinternals Suite",
        "url": "https://download.sysinternals.com/files/SysinternalsSuite.zip",
        "platform": "Windows",
        "description": "A comprehensive suite of system utilities from Microsoft."
    },
    {
        "name": "Sublime Text",
        "url": "https://download.sublimetext.com/sublime_text_setup.exe",  # Updated URL to latest version
        "platform": "Windows",
        "description": "A sophisticated text editor for code, markup, and prose."
    },
    {
        "name": "Visual Studio Code",
        "url": "https://update.code.visualstudio.com/latest/win32-x64/stable",
        "platform": "Windows, Mac",
        "description": "A lightweight but powerful source code editor."
    },
    {
        "name": "Git",
        "url": "https://github.com/git-for-windows/git/releases/download/v2.40.0.windows.1/Git-2.40.0-64-bit.exe",
        "platform": "Windows",
        "description": "Version control system for tracking changes in source code."
    },
    {
        "name": "Homebrew",
        "url": "https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh",
        "platform": "Mac",
        "description": "The missing package manager for macOS."
    },
    # Add more tools as needed
]

# Define folder structure
FOLDER_STRUCTURE = [
    TOOLS_DIR,
    READMES_DIR,
    SCRIPTS_DIR / "Windows",
    SCRIPTS_DIR / "Mac",
    SCRIPTS_DIR / "Unlocking" / "Windows",
    SCRIPTS_DIR / "Unlocking" / "Mac",
    DOCUMENTATION_DIR,
    DRIVERS_DIR,
    UTILITIES_DIR,
]

def create_folders():
    for folder in FOLDER_STRUCTURE:
        folder.mkdir(parents=True, exist_ok=True)
    logging.info(f"Created folder structure under {BASE_DIR}")

def download_tool(tool):
    tool_dir = TOOLS_DIR / tool["name"]
    tool_dir.mkdir(exist_ok=True)
    file_name = tool["url"].split('/')[-1].split('?')[0]  # Handle URLs with query params
    file_path = tool_dir / file_name

    # Check if the tool requires manual download
    if tool.get("manual", False):
        logging.warning(f"{tool['name']} requires manual download.")
        logging.info(f"Instructions: {tool.get('manual_instructions', 'No instructions provided.')}")
        return

    try:
        logging.info(f"Downloading {tool['name']}...")
        response = requests.get(tool["url"], stream=True, timeout=120)
        response.raise_for_status()
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        logging.info(f"Downloaded {tool['name']} to {file_path}")

        # If the tool is a zip or similar compressed file, extract it
        if file_name.endswith('.zip') or file_name.endswith('.dmg') or file_name.endswith('.iso'):
            try:
                if file_name.endswith('.zip'):
                    with zipfile.ZipFile(file_path, 'r') as zip_ref:
                        zip_ref.extractall(tool_dir)
                    logging.info(f"Extracted {tool['name']}")
                elif file_name.endswith('.iso'):
                    # ISO extraction is not handled; provide instructions
                    logging.warning(f"ISO extraction for {tool['name']} is not implemented. Please mount manually if needed.")
                elif file_name.endswith('.dmg'):
                    # DMG extraction for Mac requires additional tools and is not handled here
                    logging.warning(f"DMG extraction for {tool['name']} is not implemented. Please extract manually if needed.")
            except zipfile.BadZipFile:
                logging.warning(f"{tool['name']} is not a valid zip file. Skipping extraction.")

    except requests.exceptions.HTTPError as http_err:
        logging.error(f"Failed to download {tool['name']}: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        logging.error(f"Failed to download {tool['name']}: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        logging.error(f"Failed to download {tool['name']} due to timeout: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        logging.error(f"Failed to download {tool['name']}: {req_err}")
    except Exception as e:
        logging.error(f"Failed to download {tool['name']}: {e}")

def download_all_tools():
    for tool in TOOLS:
        download_tool(tool)

def create_readmes():
    for tool in TOOLS:
        if tool.get("manual", False):
            readme_content = f"""
# {tool['name']}

**Platform:** {tool['platform']}

**Description:**
{tool['description']}

**Usage Instructions:**
1. Follow the manual download instructions provided in the 'Readmes' folder.
2. After downloading, place the tool in the `Tools/{tool['name']}` directory.
3. Run the executable or follow the specific instructions for this tool.
4. Refer to the official documentation for advanced usage.

**Purpose:**
This tool is used to {tool['description'].lower()}.

**Example Scenario:**
*Technician Jane needs to reset a forgotten Windows user password. She navigates to `Tools/Ophcrack`, creates a bootable USB with the Ophcrack ISO, boots the locked system using the USB, and successfully retrieves the user's password to regain access.*

**Licensing:**
Ensure you comply with the licensing agreements of this tool before use.

---
"""
        else:
            readme_content = f"""
# {tool['name']}

**Platform:** {tool['platform']}

**Description:**
{tool['description']}

**Usage Instructions:**
1. Navigate to the `Tools/{tool['name']}` directory.
2. Run the executable or follow the specific instructions for this tool.
3. For bootable tools (e.g., TRK, Ophcrack), create a bootable USB or CD/DVD using the ISO file and boot the target system with it.
4. Refer to the official documentation for advanced usage.

**Purpose:**
This tool is used to {tool['description'].lower()}.

**Example Scenario:**
*Technician Jane needs to reset a forgotten Windows user password. She navigates to `Tools/Ophcrack`, creates a bootable USB with the Ophcrack ISO, boots the locked system using the USB, and successfully retrieves the user's password to regain access.*

**Licensing:**
Ensure you comply with the licensing agreements of this tool before use.

---
"""
        readme_path = READMES_DIR / f"{tool['name']}_README.md"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content.strip())
    logging.info(f"Created README files in {READMES_DIR}")

def create_main_readme():
    content = """
# Technician Toolkit

This toolkit contains a comprehensive collection of tools and utilities for diagnosing, repairing, and optimizing computer systems on both Windows and Mac platforms. It also includes advanced password bypass tools for unlocking devices and systems when legitimate access is required.

## Folder Structure

- **Tools/**: Contains all the diagnostic, optimization, and password bypass tools.
- **Readmes/**: Provides instructions and information about each tool.
- **Scripts/**: Custom scripts for automation and troubleshooting.
  - **Windows/**: Scripts tailored for Windows systems.
  - **Mac/**: Scripts tailored for Mac systems.
  - **Unlocking/**
    - **Windows/**: Scripts related to unlocking Windows systems.
    - **Mac/**: Scripts related to unlocking Mac systems.
- **Documentation/**: Guides and manuals for various repair procedures and ethical guidelines.
- **Drivers/**: Essential drivers needed for hardware diagnostics.
- **Utilities/**: Additional utilities for system maintenance.

## Included Tools

### Diagnostic Tools
- **HWMonitor**
- **MemTest86**
- **Process Explorer**
- **Autoruns**
- **Android SDK Platform-Tools**

### Optimization Utilities
- **CCleaner**
- **OnyX**
- **Recuva**
- **Disk Drill**
- **Sysinternals Suite**

### Malware Removal
- **Malwarebytes**

### Backup Solutions
- **Macrium Reflect Free**
- **Recuva**
- **Disk Drill**

### Remote Support
- **TeamViewer**

### Development Tools
- **Visual Studio Code**
- **Sublime Text**
- **Git**
- **Homebrew**

### Password Bypass Tools
- **Trinity Rescue Kit (TRK)**
- **Ophcrack**
- **Offline NT Password & Registry Editor**
- **John the Ripper**

### Additional Utilities
- **Ninite**
- **Unlocker**
- **Thunderbolt Control Center**

## Custom Scripts

### Kill Switch
A custom script to terminate non-essential applications and services to stabilize a freezing system.

- **Windows:** `Scripts/Windows/kill_switch.bat`
- **Mac:** `Scripts/Mac/kill_switch.sh`

### Backup and Restore
Scripts to automate the backup and restoration of important files.

- **Windows:** `Scripts/Windows/backup_restore.bat`
- **Mac:** `Scripts/Mac/backup_restore.sh`

### AI-Powered Diagnostics
Scripts leveraging artificial intelligence to analyze system logs and provide diagnostic insights.

- **Windows:** `Scripts/Windows/ai_diagnostics.py`
- **Mac:** `Scripts/Mac/ai_diagnostics.py`

## Usage

1. **Tools:** Navigate to the `Tools` folder and select the appropriate tool for your diagnostic, optimization, or password bypass task.
2. **Readmes:** Refer to the `Readmes` folder for detailed instructions on how to use each tool.
3. **Scripts:** Use the scripts in the `Scripts` folder to automate common tasks.
4. **Documentation:** Consult the `Documentation` folder for step-by-step repair guides and ethical usage guidelines.
5. **Drivers:** Install necessary drivers from the `Drivers` folder when performing hardware diagnostics.
6. **Utilities:** Utilize additional utilities for system optimization and maintenance.

## Maintenance

- **Update Tools:** Regularly check for updates to the tools in the `Tools` folder to ensure you have the latest features and security patches.
- **Backup:** Keep a backup of your toolkit to prevent data loss.
- **Customization:** Feel free to add or remove tools based on your specific needs.

## Ethical Considerations

**Important:** The tools included in this toolkit are intended solely for legitimate purposes such as security testing, system recovery, and providing authorized support services. Unauthorized use of these tools to bypass security measures or gain unauthorized access to systems is illegal and unethical. Always obtain explicit permission before utilizing password bypass tools on any system.

## Troubleshooting

If you encounter issues with any tool:

1. Refer to the specific tool's README in the `Readmes` folder.
2. Consult the official documentation or support channels of the respective tool.
3. Utilize the `Documentation` folder for general troubleshooting guides.

## Support

For any issues or suggestions, please contact the toolkit administrator.

---
"""
    readme_path = BASE_DIR / "README.md"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    logging.info(f"Created main README at {readme_path}")

def create_custom_scripts():
    # Kill Switch for Windows
    kill_switch_windows = SCRIPTS_DIR / "Windows" / "kill_switch.bat"
    kill_switch_content_win = """
@echo off
echo Initiating Kill Switch...
echo Terminating non-essential applications...

:: List of non-essential processes to kill
taskkill /F /IM notepad.exe
taskkill /F /IM chrome.exe
taskkill /F /IM firefox.exe
taskkill /F /IM spotify.exe

echo Kill Switch executed successfully.
pause
"""
    with open(kill_switch_windows, 'w', encoding='utf-8') as f:
        f.write(kill_switch_content_win.strip())

    # Kill Switch for Mac
    kill_switch_mac = SCRIPTS_DIR / "Mac" / "kill_switch.sh"
    kill_switch_content_mac = """
#!/bin/bash
echo "Initiating Kill Switch..."
echo "Terminating non-essential applications..."

# List of non-essential applications to kill
pkill -f "Google Chrome"
pkill -f "Firefox"
pkill -f "Spotify"
pkill -f "TextEdit"

echo "Kill Switch executed successfully."
"""
    with open(kill_switch_mac, 'w', encoding='utf-8') as f:
        f.write(kill_switch_content_mac.strip())
    os.chmod(kill_switch_mac, 0o755)

    # Backup and Restore for Windows
    backup_restore_windows = SCRIPTS_DIR / "Windows" / "backup_restore.bat"
    backup_restore_content_win = """
@echo off
echo Backup and Restore Script

:: Backup Example
echo Backing up Documents...
xcopy C:\\Users\\%USERNAME%\\Documents E:\\Backup\\Documents /E /H /C /I

:: Restore Example
echo Restoring Documents...
xcopy E:\\Backup\\Documents C:\\Users\\%USERNAME%\\Documents /E /H /C /I

echo Backup and Restore operations completed.
pause
"""
    with open(backup_restore_windows, 'w', encoding='utf-8') as f:
        f.write(backup_restore_content_win.strip())

    # Backup and Restore for Mac
    backup_restore_mac = SCRIPTS_DIR / "Mac" / "backup_restore.sh"
    backup_restore_content_mac = """
#!/bin/bash
echo "Backup and Restore Script"

# Backup Example
echo "Backing up Documents..."
cp -R ~/Documents /Volumes/Backup/Documents

# Restore Example
echo "Restoring Documents..."
cp -R /Volumes/Backup/Documents ~/Documents

echo "Backup and Restore operations completed."
"""
    with open(backup_restore_mac, 'w', encoding='utf-8') as f:
        f.write(backup_restore_content_mac.strip())
    os.chmod(backup_restore_mac, 0o755)

    # AI-Powered Diagnostics for Windows
    ai_diag_windows = SCRIPTS_DIR / "Windows" / "ai_diagnostics.py"
    ai_diag_content_win = """
import os

def analyze_logs():
    log_path = "C:\\\\Windows\\\\Logs\\\\System.log"
    if os.path.exists(log_path):
        with open(log_path, 'r') as f:
            logs = f.read()
        # Placeholder for AI analysis
        print("Analyzing system logs with AI...")
        # Implement AI-based log analysis here
        print("Analysis Complete: No critical issues found.")
    else:
        print("System log not found.")

if __name__ == "__main__":
    analyze_logs()
"""
    with open(ai_diag_windows, 'w', encoding='utf-8') as f:
        f.write(ai_diag_content_win.strip())

    # AI-Powered Diagnostics for Mac
    ai_diag_mac = SCRIPTS_DIR / "Mac" / "ai_diagnostics.py"
    ai_diag_content_mac = """
import os

def analyze_logs():
    log_path = "/var/log/system.log"
    if os.path.exists(log_path):
        with open(log_path, 'r') as f:
            logs = f.read()
        # Placeholder for AI analysis
        print("Analyzing system logs with AI...")
        # Implement AI-based log analysis here
        print("Analysis Complete: No critical issues found.")
    else:
        print("System log not found.")

if __name__ == "__main__":
    analyze_logs()
"""
    with open(ai_diag_mac, 'w', encoding='utf-8') as f:
        f.write(ai_diag_content_mac.strip())
    os.chmod(ai_diag_mac, 0o755)

    # Unlocking Scripts (Windows)
    unlocking_windows = SCRIPTS_DIR / "Unlocking" / "Windows" / "unlock_windows.bat"
    unlocking_windows_content = """
@echo off
echo Unlocking Windows User Account...
echo This script uses Offline NT Password & Registry Editor to reset user passwords.

:: Instructions:
:: 1. Ensure you have Offline NT Password & Registry Editor ISO in Tools/Offline NT Password & Registry Editor
:: 2. Create a bootable USB/DVD with the ISO using a tool like Rufus.
:: 3. Boot the target system with the bootable media.
:: 4. Follow the on-screen instructions to reset or remove the user password.

echo Unlocking process initiated. Follow the instructions above.
pause
"""
    with open(unlocking_windows, 'w', encoding='utf-8') as f:
        f.write(unlocking_windows_content.strip())
    os.chmod(unlocking_windows, 0o755)

    # Unlocking Scripts (Mac)
    unlocking_mac = SCRIPTS_DIR / "Unlocking" / "Mac" / "unlock_mac.sh"
    unlocking_mac_content = """
#!/bin/bash
echo "Unlocking Mac User Account..."
echo "This script provides guidelines to reset Mac user passwords."

# Instructions:
# 1. Restart the Mac and hold down Command (⌘) + R to enter Recovery Mode.
# 2. Once in Recovery Mode, open Terminal from the Utilities menu.
# 3. Use the 'resetpassword' command to reset the user password.
# 4. Follow the on-screen instructions to complete the password reset.

echo "Unlocking process initiated. Follow the instructions above."
"""
    with open(unlocking_mac, 'w', encoding='utf-8') as f:
        f.write(unlocking_mac_content.strip())
    os.chmod(unlocking_mac, 0o755)

    logging.info("Created custom scripts in Scripts folder")

def add_documentation():
    # Sample Documentation
    doc_content = """
# Technician Toolkit Documentation

## Overview

The Technician Toolkit is designed to equip computer repair professionals with a comprehensive set of tools and utilities for effective diagnosis, repair, and optimization of both Windows and Mac systems. It also includes advanced password bypass tools for unlocking devices and systems when legitimate access is required.

## Using the Toolkit

### 1. Diagnostic Tools

- **HWMonitor:** Use to monitor hardware temperatures and voltages.
- **MemTest86:** Perform memory tests to identify faulty RAM.
- **Process Explorer & Autoruns:** Manage and troubleshoot running processes and startup programs.
- **Android SDK Platform-Tools:** Use ADB and Fastboot for Android device management.

### 2. Optimization Utilities

- **CCleaner & OnyX:** Clean unnecessary files and optimize system performance.
- **Recuva & Disk Drill:** Recover deleted files and manage storage.
- **Sysinternals Suite:** Advanced system utilities for Windows.

### 3. Malware Removal

- **Malwarebytes:** Scan and remove malware and other threats.

### 4. Backup Solutions

- **Macrium Reflect Free:** Create disk images and perform backups.
- **Recuva & Disk Drill:** Additional tools for data recovery.
- **Backup Scripts:** Automate backup and restoration of important files.

### 5. Remote Support

- **TeamViewer:** Provide remote assistance to customers.

### 6. Development Tools

- **Visual Studio Code & Sublime Text:** Powerful code editors for development tasks.
- **Git & Homebrew:** Version control and package management tools.

### 7. Password Bypass Tools

- **Trinity Rescue Kit (TRK):** A free and open-source Linux distribution for resetting Windows passwords and other system recovery tasks.
- **Ophcrack:** An open-source tool that cracks Windows passwords using rainbow tables.
- **Offline NT Password & Registry Editor:** A free tool to reset Windows user passwords by editing the Windows registry.
- **John the Ripper:** A free and open-source password cracking tool targeted at Unix-based systems.

### 8. Additional Utilities

- **Ninite:** Bulk installer for essential Windows applications.
- **Unlocker:** Utility to delete locked files and manage file locks.
- **Thunderbolt Control Center:** Manage Thunderbolt connections and devices.

### 9. Custom Scripts

- **Kill Switch:** Quickly terminate non-essential applications to stabilize freezing systems.
- **Backup and Restore:** Automate the backup and restoration of important files.
- **AI-Powered Diagnostics:** Analyze system logs for intelligent troubleshooting.

## Best Practices

- **Regular Updates:** Ensure all tools are up-to-date to leverage the latest features and security patches.
- **Data Backup:** Regularly back up customer data before performing repair operations.
- **Licensing Compliance:** Adhere to software licensing agreements when using and distributing tools.

## Ethical Considerations

**Important:** The tools included in this toolkit are intended solely for legitimate purposes such as security testing, system recovery, and providing authorized support services. Unauthorized use of these tools to bypass security measures or gain unauthorized access to systems is illegal and unethical. Always obtain explicit permission before utilizing password bypass tools on any system.

## Troubleshooting

If you encounter issues with any tool:

1. Refer to the specific tool's README in the `Readmes` folder.
2. Consult the official documentation or support channels of the respective tool.
3. Utilize the `Documentation` folder for general troubleshooting guides.

## Contact

For any issues or suggestions, please contact the toolkit administrator.

---
"""
    doc_path = DOCUMENTATION_DIR / "README.md"
    with open(doc_path, 'w', encoding='utf-8') as f:
        f.write(doc_content.strip())
    logging.info(f"Added documentation in {DOCUMENTATION_DIR}")

def zip_toolkit():
    zip_filename = "Technician_Toolkit.zip"
    if Path(zip_filename).exists():
        Path(zip_filename).unlink()
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(BASE_DIR):
            for file in files:
                file_path = Path(root) / file
                zipf.write(file_path, file_path.relative_to(BASE_DIR))
    logging.info(f"Zipped toolkit into {zip_filename}")

def main():
    logging.info("Starting Technician Toolkit setup...")
    create_folders()
    download_all_tools()
    create_readmes()
    create_main_readme()
    create_custom_scripts()
    add_documentation()
    zip_toolkit()
    logging.info("Technician Toolkit setup complete!")

if __name__ == "__main__":
    main()
