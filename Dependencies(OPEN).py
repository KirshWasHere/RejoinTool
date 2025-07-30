import sys
import subprocess
import webbrowser
import time

REQUIRED_LIBRARIES = {
    "licensing": "licensing",
    "psutil": "psutil",
    "keyboard": "keyboard",
    "requests": "requests",
    "win32gui": "pywin32",
    "mss": "mss",
    "cv2": "opencv-python",
    "numpy": "numpy",
    "selenium": "selenium"

}

def check_and_install_libraries():
    print("─" * 60)
    print("Checking for required libraries...")
    
    missing_packages = []
    for import_name, package_name in REQUIRED_LIBRARIES.items():
        try:
            __import__(import_name)
            print(f"[ ✓ ] Found: {package_name}")
        except ImportError:
            print(f"[ X ] Missing: {package_name}")
            missing_packages.append(package_name)
    
    print("─" * 60)

    if missing_packages:
        print("Attempting to install missing libraries...")
        
        for package in set(missing_packages):
            print(f"\nAttempting to install '{package}'...")
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", package],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                print(f"Successfully installed '{package}'.")
            except subprocess.CalledProcessError:
                print(f"ERROR: Failed to install '{package}'.")
                print("Please try to install it manually by running:")
                print(f"  pip install {package}")
        
        print("\nAll missing libraries have been processed.")
        print("Please restart the main application for the changes to take effect.")
    else:
        print("All required libraries are already installed.")

def open_discord_invite():
    url = "https://discord.gg/2RQ4myfUBg"
    print(f"\nJoin for Updates\n-> {url}")
    webbrowser.open(url)

if __name__ == "__main__":
    check_and_install_libraries()
    print("\nDependency check complete.")
    
    print("Opening Discord Invite link in 3 seconds...")
    time.sleep(3)
    
    open_discord_invite()
    
    input("\nPress Enter to exit.")