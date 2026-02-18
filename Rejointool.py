import sys
import subprocess
import os
import time
import ctypes
import threading
import json
import re
import datetime
import atexit
import random
import winreg
if sys.platform == 'win32':
    import msvcrt
    os.system('chcp 65001 > nul')
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, 'runas', sys.executable, ' '.join(sys.argv), None, 1)
        sys.exit(0)
os.system('')
os.environ['PATH'] = os.path.dirname(sys.executable) + os.pathsep + os.environ['PATH']
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
REQUIRED_LIBRARIES = {'rich': 'rich', 'psutil': 'psutil', 'requests': 'requests', 'win32gui': 'pywin32', 'selenium': 'selenium', 'webdriver_manager': 'webdriver-manager', 'mss': 'mss', 'cv2': 'opencv-python', 'numpy': 'numpy', 'keyboard': 'keyboard', 'cryptography': 'cryptography', 'rich_pixels': 'rich-pixels'}
CHROME_PROFILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chrome_data')

def clear_screen():
    subprocess.run('cls' if sys.platform == 'win32' else 'clear', shell=True)

def print_header(title):
    print('=' * 60)
    print(f'| {title:^56} |')
    print('=' * 60)
    print()

def check_and_install_libraries(libraries_to_check):
    print_header('Checking Required Libraries')
    packages_to_check = set(libraries_to_check.values())
    missing_packages = []
    for (import_name, package_name) in libraries_to_check.items():
        try:
            __import__(import_name)
            print(f'[+] Found: {package_name}')
        except ImportError:
            if package_name not in missing_packages:
                print(f'[X] Missing: {package_name}')
                missing_packages.append(package_name)
    print('-' * 60)
    if not missing_packages:
        return True
    print_header('Installing Missing Libraries')
    for package in missing_packages:
        print(f"Installing {package}...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', package], check=True, capture_output=True, text=True)
            print(f"Installed {package}")
        except subprocess.CalledProcessError as e:
            print('\n' + '=' * 20 + ' ERROR ' + '=' * 20)
            print(f"Failed to install '{package}'.")
            print('Install manually:')
            print(f'pip install {package}')
            print('\n--- PIP Error Output ---')
            print(e.stderr)
            print('=' * 47)
            return False
    print('\n' + '=' * 60)
    print('[+] All dependencies have been installed.')
    print('\nRestart the tool.')
    print('\nThis window will close in 10 seconds...')
    time.sleep(10)
    sys.exit(0)
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service as ChromeService
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException
    from webdriver_manager.chrome import ChromeDriverManager
    import requests
    import win32event
    import win32api
    import psutil
    import win32gui
    import win32con
    import win32process
    import win32com.client
    from win32com.shell import shell, shellcon
    import cv2
    import numpy as np
    from mss import mss
    import keyboard
    from cryptography.fernet import Fernet
    import base64
    import hashlib
    import uuid
    from rich_pixels import Pixels
except ImportError as e:
    print(f'A critical library is missing or failed to import: {e}')
    print('Restart the tool.')
    input('Press Enter to exit.')
    sys.exit(1)
print('-' * 50)
print('Checking optional features...')

def check_feature(module_name, feature_name):
    try:
        module = __import__(module_name)
        globals()[module_name] = module
        print(f"Enabled: '{feature_name}'")
        return True
    except ImportError:
        print(f"Disabled: '{feature_name}' (module '{module_name}' is missing).")
        return False
DESKTOP_MODE_ENABLED = check_feature('psutil', 'Monitor and Scanning')
SHARE_LINK_RESOLUTION_ENABLED = check_feature('requests', '67')
if sys.platform == 'win32':
    ADVANCED_WINDOWS_INTEGRATION_ENABLED = check_feature('win32gui', 'Web Roblox')
    if ADVANCED_WINDOWS_INTEGRATION_ENABLED:
        import win32gui
        import win32con
        import win32process
        import win32com.client
        from win32com.shell import shell, shellcon
else:
    ADVANCED_WINDOWS_INTEGRATION_ENABLED = False
print('-' * 50)
time.sleep(3)
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.layout import Layout
    from rich.live import Live
    from rich.text import Text
    from rich.prompt import Prompt, Confirm
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
    from rich.align import Align
    from rich.style import Style
    from rich import box
    from rich.columns import Columns
    from rich.padding import Padding
    rich_console = Console()
    RICH_ENABLED = True
    print('Enabled: Rich ui')
except ImportError:
    rich_console = None
    RICH_ENABLED = False
    print('Disabled: Rich ui, Using Normal')
print('-' * 50)
time.sleep(1)
BACKGROUND_SPAMMER_ENABLED = False
DEFAULT_SPAM_MESSAGES = ['RejoinTool Session Manager! rejointool,xyz/hi', 'RejoinTool Auto Rejoin! rejointool,xyz/hi', 'RejoinTool Session Control! rejointool,xyz/hi', 'RejoinTool Session Tool! rejointool,xyz/hi', 'RejoinTool Game Manager! rejointool,xyz/hi']
BACKGROUND_SPAM_INTERVAL = 600
BACKGROUND_SPAM_STARTUP_DELAY = 5
BACKGROUND_SPAM_MESSAGE_COUNT = 2
BACKGROUND_SPAM_MESSAGE_DELAY = 2
EMULATOR_BACKGROUND_SPAMMER_ENABLED = False
EMULATOR_SPAM_INTERVAL = 600
EMULATOR_SPAM_STARTUP_DELAY = 30
EMULATOR_SPAM_MESSAGE_COUNT = 2
EMULATOR_SPAM_MESSAGE_DELAY = 3
EMULATOR_SPAM_RETRY_DELAY = 30
ROBLOX_PROCESS_NAME = 'RobloxPlayerBeta.exe'
VALID_PROCESS_STATES = ['running', 'sleeping', 'disk-sleep']
DESKTOP_MONITORING_INTERVAL = 5
DEBUG_MONITORING_INTERVAL = 0.1
FREEZE_CHECK_INTERVAL = 120
SINGLETON_MUTEX_NAME = 'ROBLOX_singletonMutex'
UI_WIDTH = 96
CONSOLE_UPDATE_INTERVAL = 1.5
mutex_handle = None

def acquire_singleton_mutex():
    global mutex_handle
    try:
        mutex_handle = win32event.CreateMutex(None, True, SINGLETON_MUTEX_NAME)
        if win32api.GetLastError() == 183:
            print_centered(colorize('ERROR: Mutex already exists!', C.RED))
            print_centered(colorize('Another multi-instance tool or Roblox might be running.', C.ORANGE))
            print_centered(colorize('Close other tools/Roblox', C.ORANGE))
            print_centered(colorize('If you are sure no other instances are running, try restarting your computer.', C.ORANGE))
            win32api.CloseHandle(mutex_handle)
            mutex_handle = None
            return False
        print_centered(colorize('Mutex acquired', C.GREEN))
        return True
    except Exception as e:
        print_centered(colorize(f'A critical error occurred while creating the mutex: {e}', C.RED))
        return False

def release_singleton_mutex():
    if mutex_handle:
        print_centered(colorize('\nReleasing mutex...', C.DIM))
        try:
            win32event.ReleaseMutex(mutex_handle)
            win32api.CloseHandle(mutex_handle)
        except Exception as e:
            log_event(f'Could not cleanly release mutex: {e}', 'WARN', 'system')
atexit.register(release_singleton_mutex)

def show_splash_screen():
    """Display startup logo"""
    try:
        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Error Template', 'logo.png')
        if os.path.exists(logo_path) and RICH_ENABLED:
            rich_console.clear()
            pixels = Pixels.from_image_path(logo_path, resize=(80, 40))
            rich_console.print(Align.center(pixels))
            rich_console.print()
            rich_console.print(Align.center(f"[{current_rich_theme['primary']}]Thanks for using RejoinTool[/{current_rich_theme['primary']}]"))
            rich_console.print(Align.center(f"[{current_rich_theme['dim']}]Press any key to continue...[/{current_rich_theme['dim']}]"))
            if sys.platform == 'win32':
                import msvcrt
                msvcrt.getch()
            else:
                input()
    except Exception as e:
        pass

def find_roblox_hwnd(pid):

    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
            (_, found_pid) = win32process.GetWindowThreadProcessId(hwnd)
            if found_pid == pid:
                hwnds.append(hwnd)
        return True
    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds[0] if hwnds else None

def find_visual_error(hwnd, templates_dir, confidence_threshold=0.9):
    if not hwnd or not win32gui.IsWindow(hwnd) or (not win32gui.IsWindowVisible(hwnd)):
        return False
    try:
        (left, top, right, bottom) = win32gui.GetWindowRect(hwnd)
        width = right - left
        height = bottom - top
        if width <= 0 or height <= 0:
            return False
        monitor = {'top': top, 'left': left, 'width': width, 'height': height}
        with mss() as sct:
            screen_image = np.array(sct.grab(monitor))
        screen_gray = cv2.cvtColor(screen_image, cv2.COLOR_BGR2GRAY)
        all_png_paths = []
        for (root, _, files) in os.walk(templates_dir):
            for file in files:
                if file.lower().endswith('.png'):
                    all_png_paths.append(os.path.join(root, file))
        if not all_png_paths:
            return False
        for template_path in all_png_paths:
            try:
                template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
                if template is None:
                    continue
                result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
                (_, max_val, _, _) = cv2.minMaxLoc(result)
                if max_val >= confidence_threshold:
                    return True
            except cv2.error:
                continue
            except Exception:
                continue
        return False
    except Exception:
        return False

def detect_freeze(hwnd, freeze_threshold=0.98, check_interval=10, consecutive_checks=3, is_emulator=False):
    """
    Detect if Roblox window is frozen by comparing consecutive screenshots.

    Args:
        hwnd: Window handle
        freeze_threshold: Similarity threshold (0.98 = 98% similar means frozen)
        check_interval: Seconds between screenshot comparisons
        consecutive_checks: Number of consecutive similar screenshots to confirm freeze
        is_emulator: Whether this is running in an emulator (affects detection logic)

    Returns:
        bool: True if freeze detected, False otherwise
    """
    if not hwnd or not win32gui.IsWindow(hwnd) or (not win32gui.IsWindowVisible(hwnd)):
        return False
    try:
        (left, top, right, bottom) = win32gui.GetWindowRect(hwnd)
        width = right - left
        height = bottom - top
        if width <= 0 or height <= 0:
            return False
        monitor = {'top': top, 'left': left, 'width': width, 'height': height}
        if is_emulator:
            freeze_threshold = min(freeze_threshold, 0.95)
            consecutive_checks = max(consecutive_checks, 3)
            check_interval = max(check_interval, 8)
        with mss() as sct:
            initial_image = np.array(sct.grab(monitor))
        if is_emulator:
            scale_factor = 0.5
            (height, width) = initial_image.shape[:2]
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            initial_image = cv2.resize(initial_image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        initial_gray = cv2.cvtColor(initial_image, cv2.COLOR_BGR2GRAY)
        similar_count = 0
        total_checks = 0
        max_total_checks = consecutive_checks * 2
        for i in range(max_total_checks):
            time.sleep(check_interval)
            if not win32gui.IsWindow(hwnd) or not win32gui.IsWindowVisible(hwnd):
                return False
            with mss() as sct:
                current_image = np.array(sct.grab(monitor))
            if is_emulator:
                (height, width) = current_image.shape[:2]
                new_width = int(width * scale_factor)
                new_height = int(height * scale_factor)
                current_image = cv2.resize(current_image, (new_width, new_height), interpolation=cv2.INTER_AREA)
            current_gray = cv2.cvtColor(current_image, cv2.COLOR_BGR2GRAY)
            try:
                mse = np.mean((initial_gray.astype(float) - current_gray.astype(float)) ** 2)
                similarity_mse = 1.0 - mse / 255.0 ** 2
                try:
                    from skimage.metrics import structural_similarity as ssim
                    similarity_ssim = ssim(initial_gray, current_gray)
                except ImportError:
                    similarity_ssim = similarity_mse
                hist1 = cv2.calcHist([initial_gray], [0], None, [256], [0, 256])
                hist2 = cv2.calcHist([current_gray], [0], None, [256], [0, 256])
                hist_similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
                hist_similarity = max(0, hist_similarity)
                if is_emulator:
                    combined_similarity = similarity_mse * 0.3 + similarity_ssim * 0.3 + hist_similarity * 0.4
                else:
                    combined_similarity = similarity_mse * 0.4 + similarity_ssim * 0.4 + hist_similarity * 0.2
                total_checks += 1
                if combined_similarity >= freeze_threshold:
                    similar_count += 1
                    if is_emulator:
                        log_event(f'Freeze check {total_checks}: Similarity {combined_similarity:.3f} >= {freeze_threshold} (Emulator)', 'DEBUG', 'freeze_detection')
                else:
                    similar_count = 0
                    initial_gray = current_gray
                    if is_emulator:
                        log_event(f'Freeze check {total_checks}: Movement detected, similarity {combined_similarity:.3f} < {freeze_threshold} (Emulator)', 'DEBUG', 'freeze_detection')
                if similar_count >= consecutive_checks:
                    log_event(f'Freeze detected after {total_checks} checks with {similar_count} consecutive similar screenshots (similarity: {combined_similarity:.3f})', 'WARN', 'freeze_detection')
                    return True
            except Exception as e:
                log_event(f'Freeze detection error: {e}', 'ERROR', 'freeze_detection')
                return False
        if total_checks >= consecutive_checks:
            log_event(f'No freeze detected after {total_checks} checks (Emulator: {is_emulator})', 'DEBUG', 'freeze_detection')
            return False
        return False
    except Exception as e:
        log_event(f'Freeze detection failed: {e}', 'ERROR', 'freeze_detection')
        return False
if getattr(sys, 'frozen', False):
    base_path = os.path.dirname(sys.executable)
else:
    base_path = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILENAME = os.path.join(base_path, 'universal_config.json')
CRITICAL_LOG_FILENAME = os.path.join(base_path, 'critical_error_log.txt')

class C:
    RESET = '\x1b[0m'
    BOLD = '\x1b[1m'
    DIM = '\x1b[2m'
    BLUE = '\x1b[38;5;111m'
    CYAN = '\x1b[38;5;141m'
    MAGENTA = '\x1b[38;5;141m'
    ORANGE = '\x1b[38;5;179m'
    GREEN = '\x1b[38;5;78m'
    RED = '\x1b[38;5;167m'
    BRIGHT_RED = '\x1b[38;5;196m'
    GREY = '\x1b[38;5;244m'
    WHITE = '\x1b[38;5;252m'
    YELLOW = '\x1b[38;5;226m'
COLOR_MAP = {'Cyan': '\x1b[38;5;141m', 'Magenta': '\x1b[38;5;201m', 'Blue': '\x1b[38;5;111m', 'Orange': '\x1b[38;5;208m', 'Green': '\x1b[38;5;78m', 'White': '\x1b[38;5;252m'}
RICH_THEMES = {'Default': {'name': 'Default', 'primary': 'cyan', 'secondary': 'bright_yellow', 'success': 'green', 'error': 'red', 'warning': 'yellow', 'info': 'blue', 'dim': 'dim white', 'box_style': box.ROUNDED}, 'Cyberpunk': {'name': 'Cyberpunk', 'primary': 'bright_cyan', 'secondary': 'magenta', 'success': 'bright_green', 'error': 'bright_red', 'warning': 'yellow', 'info': 'blue', 'dim': 'dim cyan', 'box_style': box.HEAVY}, 'Matrix': {'name': 'Matrix', 'primary': 'bright_green', 'secondary': 'green', 'success': 'bright_green', 'error': 'red', 'warning': 'yellow', 'info': 'cyan', 'dim': 'dim green', 'box_style': box.DOUBLE}, 'Neon': {'name': 'Neon', 'primary': 'bright_magenta', 'secondary': 'bright_cyan', 'success': 'bright_green', 'error': 'bright_red', 'warning': 'bright_yellow', 'info': 'bright_blue', 'dim': 'magenta', 'box_style': box.DOUBLE_EDGE}, 'Minimalist': {'name': 'Minimalist', 'primary': 'white', 'secondary': 'bright_white', 'success': 'green', 'error': 'red', 'warning': 'yellow', 'info': 'blue', 'dim': 'dim white', 'box_style': box.SIMPLE}}
THEMES = {'Default': {'name': 'Default', 'header': ['╔', '═', '╗', '║', '╚', '═', '╝', '╟', '╢', '╠', '╣'], 'colors': {'CYAN': COLOR_MAP['Cyan'], 'ORANGE': '\x1b[38;5;179m', 'BRIGHT_RED': '\x1b[38;5;196m'}}, 'Modern': {'name': 'Modern', 'header': ['╭', '─', '╮', '│', '╰', '─', '╯', '├', '┤', '├', '┤'], 'colors': {'CYAN': COLOR_MAP['Blue'], 'ORANGE': '\x1b[38;5;208m', 'BRIGHT_RED': '\x1b[38;5;197m'}}, 'Minimalist': {'name': 'Minimalist', 'header': ['+', '-', '+', '|', '+', '-', '+', '|', '|', '|', '|'], 'colors': {'CYAN': COLOR_MAP['White'], 'ORANGE': '\x1b[38;5;248m', 'BRIGHT_RED': '\x1b[38;5;1m'}}, 'Neon': {'name': 'Neon', 'header': ['▓', '█', '▓', '█', '▓', '█', '▓', '█', '█', '█', '█'], 'colors': {'CYAN': '\x1b[38;5;51m', 'ORANGE': '\x1b[38;5;201m', 'BRIGHT_RED': '\x1b[38;5;198m'}}, 'Glitch': {'name': 'Glitch', 'header': ['#', '=', '#', '|', '#', '=', '#', '|', '|', '|', '|'], 'colors': {'CYAN': '\x1b[38;5;123m', 'ORANGE': '\x1b[38;5;208m', 'BRIGHT_RED': '\x1b[38;5;9m'}}, 'Matrix': {'name': 'Matrix', 'header': ['+', '-', '+', '|', '+', '-', '+', '|', '|', '|', '|'], 'colors': {'CYAN': '\x1b[38;5;46m', 'ORANGE': '\x1b[38;5;226m', 'BRIGHT_RED': '\x1b[38;5;196m'}}, 'Vaporwave': {'name': 'Vaporwave', 'header': ['~', '-', '~', '|', '~', '-', '~', '|', '|', '|', '|'], 'colors': {'CYAN': '\x1b[38;5;129m', 'ORANGE': '\x1b[38;5;201m', 'BRIGHT_RED': '\x1b[38;5;198m'}}, 'KirshStyle': {'name': 'KirshStyle', 'header': ['╭', '─', '╮', '│', '╰', '─', '╯', '├', '┤', '├', '┤'], 'colors': {'CYAN': COLOR_MAP['White'], 'ORANGE': '\x1b[38;5;250m', 'BRIGHT_RED': '\x1b[38;5;240m'}}, 'Cyberpunk': {'name': 'Cyberpunk', 'header': ['>>', '=', '<<', '║', '>>', '=', '<<', '╠', '╣', '╬', '╩'], 'colors': {'CYAN': '\x1b[38;5;39m', 'ORANGE': '\x1b[38;5;208m', 'BRIGHT_RED': '\x1b[38;5;196m'}}, 'Retro': {'name': 'Retro', 'header': ['#', '-', '#', '|', '#', '-', '#', '+', '+', '+', '+'], 'colors': {'CYAN': '\x1b[38;5;103m', 'ORANGE': '\x1b[38;5;172m', 'BRIGHT_RED': '\x1b[38;5;124m'}}}
current_rich_theme = RICH_THEMES['Default']
(H_TOP_LEFT, H_TOP, H_TOP_RIGHT, H_SIDE, H_BOT_LEFT, H_BOT, H_BOT_RIGHT, H_MID_LEFT, H_MID_RIGHT, H_T_MID, H_T_MID_DOWN) = (' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ')
UI_WIDTH = 96
ROBLOX_PROCESS_NAME = 'RobloxPlayerBeta.exe'
ROBLOX_PACKAGE_NAME = 'com.roblox.client'
ROBLOX_ACTIVITY_NAME = 'com.roblox.client.ActivityProtocolLaunch'
GAMES_DB = {'Jailbreak': 606849621, 'Adopt Me!': 920587237, 'Blox Fruits': 2753915549, 'Pet Simulator 99': 8737899170, 'Da Hood': 2788229376, 'Blade Ball': 13772394625, 'DIG': 126244816328678}
SESSION_STATUS = {}
STATUS_LOCK = threading.RLock()
MONITORING_ACTIVE = True
TOGGLE_REQUESTED = False
EXIT_TO_MENU_REQUESTED = False
DEBUG_MODE_ACTIVE = False
DEBUG_LOG = []

def clean_cookie(raw_cookie):
    if not isinstance(raw_cookie, str):
        return ''
    if '|_' in raw_cookie:
        try:
            potential_key = raw_cookie.split('|_')[-1]
            final_key = potential_key.split(';')[0]
            return final_key
        except IndexError:
            pass
    if '.ROBLOSECURITY=' in raw_cookie:
        try:
            potential_key = raw_cookie.split('.ROBLOSECURITY=')[1]
            final_key = potential_key.split(';')[0]
            return final_key
        except IndexError:
            pass
    return raw_cookie.strip().split(';')[0]

def get_machine_encryption_key():
    """Generate machine-specific encryption key"""
    try:
        machine_id = str(uuid.getnode())
        
        key_material = hashlib.sha256(machine_id.encode()).digest()
        
        return base64.urlsafe_b64encode(key_material)
    except Exception as e:
        print(f"Warning: Could not generate machine key, using fallback: {e}")
        fallback = hashlib.sha256(b"RejoinToolFallbackKey2025").digest()
        return base64.urlsafe_b64encode(fallback)

def encrypt_cookie(cookie_string):
    """Encrypt cookie"""
    try:
        if not cookie_string:
            return ""
        
        cipher = Fernet(get_machine_encryption_key())
        encrypted_bytes = cipher.encrypt(cookie_string.encode('utf-8'))
        return encrypted_bytes.decode('utf-8')
    except Exception as e:
        print(f"Encryption error: {e}")
        return cookie_string 

def decrypt_cookie(encrypted_cookie):
    """Decrypt cookie"""
    try:
        if not encrypted_cookie:
            return ""
        
        if encrypted_cookie.startswith('_|WARNING:'):
            return encrypted_cookie
        
        cipher = Fernet(get_machine_encryption_key())
        decrypted_bytes = cipher.decrypt(encrypted_cookie.encode('utf-8'))
        return decrypted_bytes.decode('utf-8')
    except Exception as e:
        print(f"Decryption failed (might be old format): {e}")
        return encrypted_cookie

def load_roblox_accounts():
    """Load accounts"""
    config = load_config()
    encrypted_accounts = config.get('roblox_accounts', {})
    
    decrypted_accounts = {}
    for username, encrypted_cookie in encrypted_accounts.items():
        decrypted_accounts[username] = decrypt_cookie(encrypted_cookie)
    
    return decrypted_accounts

def save_roblox_accounts(accounts_data):
    """Save accounts"""
    config = load_config()
    encrypted_accounts = {}
    for username, cookie in accounts_data.items():
        encrypted_accounts[username] = encrypt_cookie(cookie)
    
    config['roblox_accounts'] = encrypted_accounts
    save_config(config)

def get_roblox_user_info(cookie):
    url = 'https://users.roblox.com/v1/users/authenticated'
    headers = {'Cookie': f'.ROBLOSECURITY={cookie}', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'id' in data and 'name' in data:
                return data.get('name')
            else:
                return None
    except (requests.RequestException, json.JSONDecodeError):
        return None
    return None

def add_accounts_from_cookie():
    draw_header('BULK ADD FROM COOKIE')
    print_centered('Paste your .ROBLOSECURITY cookies below.')
    print_centered(colorize('You can paste the full string from browser tools or just the value.', C.GREY))
    print_centered('One cookie per line. Press Enter on an empty line when you are finished.')
    print()
    cookies_to_process = []
    while True:
        try:
            line = input(f'{C.DIM}> {C.RESET}')
            if not line.strip():
                break
            cookies_to_process.append(line)
        except EOFError:
            break
    if not cookies_to_process:
        print_centered(colorize('No cookies entered. Returning to menu.', C.CYAN))
        time.sleep(2)
        return
    print_centered(f'\nFound {len(cookies_to_process)} cookies to process.')
    if get_input('Continue? (y/n)', C.ORANGE).lower() != 'y':
        return
    saved_accounts = load_roblox_accounts()
    success_count = 0
    fail_count = 0
    draw_header(f'VALIDATING {len(cookies_to_process)} COOKIES')
    for (i, raw_cookie) in enumerate(cookies_to_process):
        cookie_for_validation = clean_cookie(raw_cookie)
        print_centered(f'({i + 1}/{len(cookies_to_process)}) Validating...')
        username = get_roblox_user_info(cookie_for_validation)
        if username:
            message = 'updated' if username in saved_accounts else 'added'
            print_centered(colorize(f" Success! Account '{username}' {message}.", C.GREEN))
            saved_accounts[username] = raw_cookie.strip()
            success_count += 1
        else:
            print_centered(colorize(f' Failed. The provided cookie is invalid or expired.', C.RED))
            fail_count += 1
        time.sleep(0.5)
    save_roblox_accounts(saved_accounts)
    draw_header('BULK ADD COMPLETE')
    print_centered(colorize(f'Added: {success_count}', C.GREEN))
    print_centered(colorize(f'Failed: {fail_count}', C.RED))
    input('\nPress Enter to return to the account manager...')

def launch_private_server_browser(place_id, link_code, cookie, session_key):
    """Launch private server using headless browser method for reliable joining"""
    driver = None
    try:
        log_event('Starting browser-based private server launch...', 'INFO', session_key)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(f'user-data-dir={CHROME_PROFILE_PATH}')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-logging')
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_argument('--window-size=1000,700')
        chrome_options.add_argument('--disable-features=ExternalProtocolPrompt')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        prefs = {'protocol_handler.excluded_schemes': {'roblox-player': False, 'roblox': False}}
        chrome_options.add_experimental_option('prefs', prefs)
        service = ChromeService(ChromeDriverManager().install())
        service.creation_flags = subprocess.CREATE_NO_WINDOW
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(20)
        log_event('Injecting authentication cookie...', 'INFO', session_key)
        driver.get('https://www.roblox.com')
        time.sleep(1)
        driver.delete_all_cookies()
        clean_cookie_value = clean_cookie(cookie)
        driver.add_cookie({'name': '.ROBLOSECURITY', 'value': clean_cookie_value, 'domain': '.roblox.com', 'path': '/', 'secure': True, 'httpOnly': True})
        private_server_url = f'https://www.roblox.com/games/{place_id}/?privateServerLinkCode={link_code}'
        log_event('Loading private server...', 'INFO', session_key)
        driver.get(private_server_url)
        time.sleep(5)
        log_event('Launching Roblox...', 'INFO', session_key)
        roblox_launched = False
        for attempt in range(15):
            try:
                if sys.platform == 'win32':
                    import win32gui

                    def find_roblox_windows(hwnd, windows):
                        if win32gui.IsWindowVisible(hwnd):
                            window_text = win32gui.GetWindowText(hwnd)
                            class_name = win32gui.GetClassName(hwnd)
                            if 'Roblox' in window_text and window_text != 'Roblox' or 'ROBLOXCORPORATION.ROBLOX' in class_name or window_text.startswith('Roblox -'):
                                windows.append((hwnd, window_text))
                        return True
                    roblox_windows = []
                    win32gui.EnumWindows(find_roblox_windows, roblox_windows)
                    if roblox_windows:
                        log_event(f'Roblox launched! Found {len(roblox_windows)} window(s).', 'SUCCESS', session_key)
                        roblox_launched = True
                        break
            except Exception as e:
                log_event(f'Error checking windows: {e}', 'WARN', session_key)
            time.sleep(1)
        if not roblox_launched:
            log_event("Roblox didn't launch within timeout", 'WARN', session_key)
        return True
    except Exception as e:
        log_event(f'Browser launch failed: {str(e)[:100]}...', 'ERROR', session_key)
        return False
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass
        log_event('Browser closed', 'INFO', session_key)

def selenium_fallback_launch(cookie, place_id='123341190296245'):
    """Better authentication method using browser-based launch"""
    driver = None
    try:
        log_event(' Using browser-based Roblox launch (better method)...', 'INFO', 'system')
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(f'user-data-dir={CHROME_PROFILE_PATH}')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-logging')
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_argument('--window-size=1000,700')
        chrome_options.add_argument('--disable-features=ExternalProtocolPrompt')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        prefs = {'protocol_handler.excluded_schemes': {'roblox-player': False, 'roblox': False}}
        chrome_options.add_experimental_option('prefs', prefs)
        service = ChromeService(ChromeDriverManager().install())
        service.creation_flags = subprocess.CREATE_NO_WINDOW
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(15)
        log_event(' Setting up authentication...', 'INFO', 'system')
        driver.get('https://www.roblox.com')
        time.sleep(1)
        driver.delete_all_cookies()
        driver.add_cookie({'name': '.ROBLOSECURITY', 'value': cookie, 'domain': '.roblox.com', 'path': '/', 'secure': True, 'httpOnly': True})
        game_url = f'https://www.roblox.com/games/{place_id}'
        log_event(f'Loading game {place_id}...', 'INFO', 'system')
        driver.get(game_url)
        time.sleep(3)
        log_event('Finding play button...', 'INFO', 'system')
        play_button_found = False
        play_selectors = ["//button[contains(@class, 'btn-full-width') and contains(text(), 'Play')]", "//button[contains(@class, 'btn-primary-md') and contains(text(), 'Play')]", "//button[@id='game-start-button']", "//button[contains(@class, 'play-button')]", "//a[contains(@class, 'btn-full-width')]", "//button[contains(text(), 'Play')]", "//div[contains(@class, 'game-play-button')]//button", "//span[text()='Play']//parent::button"]
        for selector in play_selectors:
            try:
                play_button = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, selector)))
                driver.execute_script('arguments[0].scrollIntoView(true);', play_button)
                time.sleep(0.5)
                driver.execute_script('arguments[0].click();', play_button)
                log_event('Clicked play', 'SUCCESS', 'system')
                play_button_found = True
                break
            except (TimeoutException, Exception):
                continue
        if not play_button_found:
            log_event(' Play button not found, trying protocol launch...', 'WARN', 'system')
            driver.get(f'roblox://placeId={place_id}')
        log_event('Launching Roblox...', 'INFO', 'system')
        roblox_launched = False
        for attempt in range(20):
            try:
                if sys.platform == 'win32':
                    import win32gui

                    def find_roblox_windows(hwnd, windows):
                        if win32gui.IsWindowVisible(hwnd):
                            window_text = win32gui.GetWindowText(hwnd)
                            class_name = win32gui.GetClassName(hwnd)
                            if 'Roblox' in window_text and window_text != 'Roblox' or 'ROBLOXCORPORATION.ROBLOX' in class_name or window_text.startswith('Roblox -'):
                                windows.append((hwnd, window_text))
                        return True
                    roblox_windows = []
                    win32gui.EnumWindows(find_roblox_windows, roblox_windows)
                    if roblox_windows:
                        log_event(f' Roblox launched! Found {len(roblox_windows)} window(s). Closing immediately.', 'SUCCESS', 'system')
                        for (hwnd, title) in roblox_windows:
                            log_event(f'Closing: {title}', 'INFO', 'system')
                            win32gui.PostMessage(hwnd, 16, 0, 0)
                        roblox_launched = True
                        break
            except Exception as e:
                log_event(f'Error checking windows: {e}', 'WARN', 'system')
            time.sleep(1)
            if attempt % 5 == 0 and attempt > 0:
                log_event(f'Still waiting... ({attempt}/20)', 'INFO', 'system')
        if not roblox_launched:
            log_event(" Roblox didn't launch within timeout, but authentication was successful", 'WARN', 'system')
        return True
    except Exception as e:
        log_event(f' Browser launch failed: {str(e)[:100]}...', 'ERROR', 'system')
        return False
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass
        log_event(' Browser-based launch completed', 'INFO', 'system')

def get_auth_ticket(cookie):
    url = 'https://auth.roblox.com/v1/authentication-ticket'
    headers = {'Cookie': f'.ROBLOSECURITY={cookie}', 'Referer': 'https://www.roblox.com/games', 'Content-Type': 'application/json'}
    session = requests.Session()
    try:
        response = session.post(url, headers=headers)
        csrf_token = response.headers.get('x-csrf-token')
        if not csrf_token:
            return None
        headers['X-CSRF-TOKEN'] = csrf_token
        response = session.post(url, headers=headers)
        if response.status_code == 200 and 'rbx-authentication-ticket' in response.headers:
            return response.headers['rbx-authentication-ticket']
    except requests.RequestException:
        return None
    return None

def manage_roblox_accounts():
    while True:
        draw_header('ROBLOX ACCOUNT MANAGER')
        accounts = load_roblox_accounts()
        saved_accounts = list(accounts.keys())
        if not saved_accounts:
            print_centered(colorize('No Roblox accounts saved.', C.ORANGE))
        else:
            for (i, username) in enumerate(saved_accounts):
                print_centered(f"{colorize(f'[{i + 1}]', C.GREY)} {C.WHITE}{username}{C.RESET}")
        print()
        options = ['Add a new account', 'Delete an account', colorize('Cookie Extractor (SavedACCS)', C.ORANGE), 'Back to Main Menu']
        choice = get_choice('Select an option', options)
        if choice == 1:
            # Only cookie import method available, note: removed all other methods since roblox/david baszucki is on drugs and updated them for no fucking reason.
            add_accounts_from_cookie()
        elif choice == 2:
            if not saved_accounts:
                print_centered(colorize('No accounts to delete.', C.ORANGE))
                time.sleep(2)
                continue
            delete_options = [f'{name}' for name in saved_accounts]
            delete_options.append('Cancel')
            del_choice = get_choice('Select account to delete', delete_options)
            if del_choice and del_choice <= len(saved_accounts):
                username_to_del = saved_accounts[del_choice - 1]
                if get_input(f'Delete {username_to_del}? (y/n)', C.BRIGHT_RED).lower() == 'y':
                    del accounts[username_to_del]
                    save_roblox_accounts(accounts)
                    print_centered(colorize(f'Account {username_to_del} deleted.', C.GREEN))
                else:
                    print_centered(colorize('Deletion cancelled.', C.CYAN))
                time.sleep(2)
        elif choice == 3:
            if not saved_accounts:
                print_centered(colorize('No accounts to extract a cookie from.', C.ORANGE))
                time.sleep(2)
                continue
            extract_options = [f'{name}' for name in saved_accounts]
            extract_options.append('Cancel')
            extract_choice = get_choice('Select account to extract cookie from', extract_options)
            if extract_choice and extract_choice <= len(saved_accounts):
                username_to_extract = saved_accounts[extract_choice - 1]
                cookie_to_extract = accounts[username_to_extract]
                draw_header(f'COOKIE FOR: {username_to_extract}')
                print_centered(colorize('Your .ROBLOSECURITY cookie is below:', C.CYAN))
                print()
                print(cookie_to_extract)
                print()
                input(colorize('\nPress Enter to return to the account manager...', C.DIM))
            else:
                continue
        elif choice == 4:
            return

def get_visible_length(s):
    return len(re.sub('\\x1B\\[[0-?]*[ -/]*[@-~]', '', s))

def colorize(text, color):
    return f'{color}{text}{C.RESET}'

def print_centered(text_line=''):
    """Print centered text - uses Rich if available"""
    if RICH_ENABLED and (not re.search('\\x1B\\[[0-?]*[ -/]*[@-~]', text_line)):
        rich_console.print(Align.center(text_line))
    else:
        try:
            console_width = os.get_terminal_size().columns
        except OSError:
            console_width = UI_WIDTH
        padding = ' ' * ((console_width - get_visible_length(text_line)) // 2)
        print(padding + text_line)

def show_success(message):
    """Show success message with Rich"""
    if RICH_ENABLED:
        rich_console.print(f"[{current_rich_theme['success']}]✓[/{current_rich_theme['success']}] {message}")
    else:
        print_centered(colorize(f'[+] {message}', C.GREEN))

def show_error(message):
    """Show error message with Rich"""
    if RICH_ENABLED:
        rich_console.print(f"[{current_rich_theme['error']}]✗[/{current_rich_theme['error']}] {message}")
    else:
        print_centered(colorize(f'[X] {message}', C.RED))

def show_warning(message):
    """Show warning message with Rich"""
    if RICH_ENABLED:
        rich_console.print(f"[{current_rich_theme['warning']}]⚠[/{current_rich_theme['warning']}] {message}")
    else:
        print_centered(colorize(f'[!] {message}', C.ORANGE))

def show_info(message):
    """Show info message with Rich"""
    if RICH_ENABLED:
        rich_console.print(f"[{current_rich_theme['info']}]ℹ[/{current_rich_theme['info']}] {message}")
    else:
        print_centered(colorize(f'[i] {message}', C.BLUE))

def log_event(message, level='INFO', session_key='desktop'):
    global DEBUG_LOG
    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
    log_entry = f'[{timestamp}] [{level}] [{session_key}] {message}'
    DEBUG_LOG.append(log_entry)
    level_color_map = {'INFO': C.CYAN, 'SUCCESS': C.GREEN, 'ERROR': C.RED, 'WARN': C.ORANGE, 'DEBUG': C.MAGENTA}
    with STATUS_LOCK:
        if session_key in SESSION_STATUS:
            status_message = colorize(message, level_color_map.get(level, C.GREY))
            if level == 'SUCCESS':
                status_message = colorize('Running', C.GREEN)
            SESSION_STATUS[session_key]['status'] = status_message

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except AttributeError:
        return False

def save_config(data):
    try:
        with open(CONFIG_FILENAME, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        print_centered(colorize('CRITICAL ERROR: Could not save config file!', C.RED))
        input('Press Enter to exit...')
        sys.exit(1)

def load_config():
    default_config = {'profiles': {}, 'roblox_accounts': {}, 'last_used_profile': None, 'settings': {'theme_name': 'Default', 'theme_color_override': None}}
    if not os.path.exists(CONFIG_FILENAME):
        save_config(default_config)
        return default_config
    try:
        with open(CONFIG_FILENAME, 'r', encoding='utf-8') as f:
            content = f.read()
            config = json.loads(content) if content else default_config
            for (key, value) in default_config.items():
                if key not in config:
                    config[key] = value
            if 'settings' not in config:
                config['settings'] = default_config['settings']
            for (key, value) in default_config['settings'].items():
                if key not in config['settings']:
                    config['settings'][key] = value
            return config
    except (json.JSONDecodeError, FileNotFoundError):
        save_config(default_config)
        return default_config

def apply_theme(config):
    global H_TOP_LEFT, H_TOP, H_TOP_RIGHT, H_SIDE, H_BOT_LEFT, H_BOT, H_BOT_RIGHT, H_MID_LEFT, H_MID_RIGHT, H_T_MID, H_T_MID_DOWN, current_rich_theme
    theme_name = config.get('settings', {}).get('theme_name', 'Default')
    theme = THEMES.get(theme_name, THEMES['Default'])
    C.CYAN = theme['colors'].get('CYAN')
    C.ORANGE = theme['colors'].get('ORANGE')
    C.BRIGHT_RED = theme['colors'].get('BRIGHT_RED')
    if theme_name in RICH_THEMES:
        current_rich_theme = RICH_THEMES[theme_name]
    else:
        current_rich_theme = RICH_THEMES['Default']
    override_color_name = config.get('settings', {}).get('theme_color_override')
    if override_color_name and override_color_name in COLOR_MAP:
        C.CYAN = COLOR_MAP[override_color_name]
    (H_TOP_LEFT, H_TOP, H_TOP_RIGHT, H_SIDE, H_BOT_LEFT, H_BOT, H_BOT_RIGHT, H_MID_LEFT, H_MID_RIGHT, H_T_MID, H_T_MID_DOWN) = theme['header']

def draw_header(title):
    """Draw header using Rich library"""
    if not RICH_ENABLED:
        draw_header_legacy(title)
        return
    rich_console.clear()
    panel = Panel(Align.center(f'[bold]{title}[/bold]'), style=current_rich_theme['primary'], box=current_rich_theme['box_style'], padding=(1, 2))
    rich_console.print(panel)
    rich_console.print()

def draw_header_legacy(title):
    """Legacy ANSI header"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print_centered(f'{C.GREY}{H_TOP_LEFT}{H_TOP * (UI_WIDTH - 2)}{H_TOP_RIGHT}{C.RESET}')
    print_centered(f'{C.GREY}{H_SIDE}{C.RESET}{colorize(title.center(UI_WIDTH - 2), C.BOLD + C.CYAN)}{C.GREY}{H_SIDE}{C.RESET}')
    print_centered(f'{C.GREY}{H_BOT_LEFT}{H_BOT * (UI_WIDTH - 2)}{H_BOT_RIGHT}{C.RESET}')
    print()

def get_input(prompt, color=C.BLUE):
    """Get user input using Rich library"""
    if not RICH_ENABLED:
        console_width = os.get_terminal_size().columns
        formatted_prompt = f'{C.DIM}> {C.RESET}{colorize(prompt, color)}{C.DIM} >> {C.RESET}'
        padding = ' ' * ((console_width - get_visible_length(formatted_prompt)) // 2)
        return input(padding + formatted_prompt)
    try:
        return Prompt.ask(f"[{current_rich_theme['info']}]{prompt}[/{current_rich_theme['info']}]")
    except (EOFError, KeyboardInterrupt):
        return ''

def get_choice(prompt, options):
    """Get user choice using Rich library"""
    if not RICH_ENABLED:
        return get_choice_legacy(prompt, options)
    table = Table(show_header=False, box=box.SIMPLE, padding=(0, 2))
    table.add_column('Option', style=f"dim {current_rich_theme['primary']}", width=8)
    table.add_column('Description', style='white')
    for (i, option) in enumerate(options, 1):
        table.add_row(f'[{i}]', option)
    rich_console.print(table)
    rich_console.print()
    try:
        choice = Prompt.ask(f"[{current_rich_theme['info']}]{prompt}[/{current_rich_theme['info']}]", default='1')
        return int(choice) if choice.isdigit() else None
    except (ValueError, EOFError, KeyboardInterrupt):
        return None

def get_choice_legacy(prompt, options):
    """Legacy ANSI choice menu"""
    for (i, option) in enumerate(options, 1):
        print_centered(f"{colorize(f'[{i}]', C.GREY)} {C.WHITE}{option}{C.RESET}")
    print()
    try:
        choice = get_input(prompt)
        return int(choice) if choice.isdigit() else None
    except (ValueError, EOFError):
        return None

def draw_dashboard(start_time, duration_hours, profile):
    """Draw dashboard using Rich library for modern UI"""
    if not RICH_ENABLED:
        draw_dashboard_legacy(start_time, duration_hours, profile)
        return
    rich_console.clear()
    if duration_hours > 0:
        elapsed = time.time() - start_time
        remaining = duration_hours * 3600 - elapsed
        if remaining < 0:
            remaining = 0
        (h, rem) = divmod(int(remaining), 3600)
        (m, s) = divmod(rem, 60)
        time_text = f'Time Remaining: {h:02d}:{m:02d}:{s:02d}'
        time_style = current_rich_theme['warning']
    else:
        elapsed = time.time() - start_time
        (h, rem) = divmod(int(elapsed), 3600)
        (m, s) = divmod(rem, 60)
        time_text = f'Session Duration: {h:02d}:{m:02d}:{s:02d}'
        time_style = current_rich_theme['info']
    header = Panel(Align.center(f"[bold {current_rich_theme['secondary']}]ROBLOX REJOIN TOOL - LIVE DASHBOARD[/bold {current_rich_theme['secondary']}]\n[{time_style}]{time_text}[/{time_style}]"), box=current_rich_theme['box_style'], style=current_rich_theme['primary'], padding=(0, 2))
    table = Table(box=box.ROUNDED, show_header=True, header_style=f"bold {current_rich_theme['primary']}", border_style=current_rich_theme['dim'])
    table.add_column('Instance', style=current_rich_theme['info'], width=20, no_wrap=True)
    table.add_column('Status', width=30)
    table.add_column('Crashes', justify='center', width=8)
    table.add_column('Restarts', justify='center', width=8)
    table.add_column('Next Restart', justify='center', width=12)
    table.add_column('Auto-R', justify='center', width=6)
    with STATUS_LOCK:
        if not SESSION_STATUS:
            table.add_row(f"[{current_rich_theme['dim']}]No active sessions[/{current_rich_theme['dim']}]", '', '', '', '', '')
        else:
            for (key, data) in sorted(SESSION_STATUS.items()):
                instance_name = data.get('instance_name', 'Unknown')
                status = data.get('status', 'Unknown')
                crashes = str(data.get('crashes', 0))
                restarts = str(data.get('restarts', 0))
                status_clean = re.sub('\\x1B\\[[0-?]*[ -/]*[@-~]', '', str(status))
                if 'running' in status_clean.lower() or 'success' in status_clean.lower():
                    status_text = f"[{current_rich_theme['success']}]{status_clean}[/{current_rich_theme['success']}]"
                elif 'error' in status_clean.lower() or 'crash' in status_clean.lower():
                    status_text = f"[{current_rich_theme['error']}]{status_clean}[/{current_rich_theme['error']}]"
                elif 'initializing' in status_clean.lower() or 'waiting' in status_clean.lower():
                    status_text = f"[{current_rich_theme['warning']}]{status_clean}[/{current_rich_theme['warning']}]"
                else:
                    status_text = status_clean
                next_restart = 'N/A'
                if data.get('restarter_enabled') and data.get('next_restart_time', 0) > 0:
                    remaining_seconds = data['next_restart_time'] - time.time()
                    if remaining_seconds > 0:
                        (mins, secs) = divmod(int(remaining_seconds), 60)
                        next_restart = f'{mins:02d}:{secs:02d}'
                    else:
                        next_restart = f"[{current_rich_theme['warning']}]Now[/{current_rich_theme['warning']}]"
                auto_r = 'ON' if data.get('restarter_enabled') else 'OFF'
                auto_r_styled = f"[{current_rich_theme['success']}]{auto_r}[/{current_rich_theme['success']}]" if data.get('restarter_enabled') else f"[{current_rich_theme['error']}]{auto_r}[/{current_rich_theme['error']}]"
                table.add_row(instance_name, status_text, crashes, restarts, next_restart, auto_r_styled)
    footer = Panel(Align.center(f"[{current_rich_theme['dim']}]CTRL+T: Toggle Restart | CTRL+X: Menu | CTRL+G: Debug | CTRL+C: Exit\nMade by Isaac (Kirsh)[/{current_rich_theme['dim']}]"), box=box.SIMPLE, style=current_rich_theme['dim'])
    rich_console.print(header)
    rich_console.print(table)
    rich_console.print(footer)

def draw_dashboard_legacy(start_time, duration_hours, profile):
    """Legacy ANSI dashboard (fallback when Rich is not available)"""
    os.system('cls' if os.name == 'nt' else 'clear')
    title = '* LIVE DASHBOARD'
    print_centered(f'{C.GREY}{H_TOP_LEFT}{H_TOP * (UI_WIDTH - 2)}{H_TOP_RIGHT}{C.RESET}')
    print_centered(f'{C.GREY}{H_SIDE}{C.RESET}{colorize(title.center(UI_WIDTH - 2), C.BOLD + C.BRIGHT_RED)}{C.GREY}{H_SIDE}{C.RESET}')
    if duration_hours > 0:
        elapsed = time.time() - start_time
        remaining = duration_hours * 3600 - elapsed
        if remaining < 0:
            remaining = 0
        (h, rem) = divmod(remaining, 3600)
        (m, s) = divmod(rem, 60)
        time_str = f'Time Remaining: {int(h):02}:{int(m):02}:{int(s):02}'
        print_centered(f'{C.GREY}{H_MID_LEFT}{H_TOP * (UI_WIDTH - 2)}{H_MID_RIGHT}{C.RESET}')
        print_centered(f'{C.GREY}{H_SIDE}{C.RESET}{colorize(time_str.center(UI_WIDTH - 2), C.ORANGE)}{C.GREY}{H_SIDE}{C.RESET}')
    print_centered(f'{C.GREY}{H_T_MID}{H_BOT * (UI_WIDTH - 2)}{H_T_MID_DOWN}{C.RESET}')
    with STATUS_LOCK:
        if not SESSION_STATUS:
            print_centered(f"{C.GREY}{H_SIDE}{C.RESET}{colorize('No sessions being monitored.'.center(UI_WIDTH - 2), C.ORANGE)}{C.GREY}{H_SIDE}{C.RESET}")
        else:
            col_widths = {'inst': 20, 'stat': 30, 'crash': 7, 'restart': 8, 'next_r': 8, 'r_on': 5}
            separator = f' {C.GREY}|{C.WHITE} '
            header_titles = ['INSTANCE', 'STATUS', 'CRASH', 'RESTARTS', 'NEXT R', 'R']
            header_keys = ['inst', 'stat', 'crash', 'restart', 'next_r', 'r_on']
            header_cells = []
            for (i, title) in enumerate(header_titles):
                key = header_keys[i]
                content = f' {title}'
                padding = col_widths[key] - len(content)
                header_cells.append(f"{content}{' ' * padding}")
            full_header = separator.join(header_cells)
            print_centered(f'{C.GREY}{H_SIDE}{C.WHITE}{C.BOLD}{full_header}{C.RESET}{C.GREY}{H_SIDE}{C.RESET}')
            sessions_to_draw = list(SESSION_STATUS.items())
            for (key, data) in sorted(sessions_to_draw):
                try:
                    data_cells = []
                    instance_name_display = data.get('instance_name', 'Unknown')
                    max_inst_len = col_widths['inst'] - 1
                    if get_visible_length(instance_name_display) > max_inst_len:
                        instance_name_display = instance_name_display[:max_inst_len - 3] + '...'
                    content = f' {instance_name_display}'
                    padding = col_widths['inst'] - get_visible_length(content)
                    data_cells.append(f"{content}{' ' * padding}")
                    content = f" {data.get('status', colorize('Error', C.RED))}"
                    padding = col_widths['stat'] - get_visible_length(content)
                    data_cells.append(f"{content}{' ' * padding}")
                    content = f" {data.get('crashes', '?')}"
                    padding = col_widths['crash'] - get_visible_length(content)
                    data_cells.append(f"{content}{' ' * padding}")
                    content = f" {data.get('restarts', '?')}"
                    padding = col_widths['restart'] - get_visible_length(content)
                    data_cells.append(f"{content}{' ' * padding}")
                    next_r_countdown = 'N/A'
                    if data.get('restarter_enabled') and data.get('next_restart_time', 0) > 0:
                        remaining_seconds = data['next_restart_time'] - time.time()
                        if remaining_seconds > 0:
                            (m, s) = divmod(remaining_seconds, 60)
                            next_r_countdown = f'{int(m):02}:{int(s):02}'
                        else:
                            next_r_countdown = 'Now...'
                    content = f' {next_r_countdown}'
                    padding = col_widths['next_r'] - get_visible_length(content)
                    data_cells.append(f"{content}{' ' * padding}")
                    r_on_text = 'ON' if data.get('restarter_enabled') else 'OFF'
                    r_on_color = C.GREEN if data.get('restarter_enabled') else C.RED
                    content = f' {colorize(r_on_text, r_on_color)}'
                    padding = col_widths['r_on'] - get_visible_length(content)
                    data_cells.append(f"{content}{' ' * padding}")
                    full_line = separator.join(data_cells)
                    print_centered(f'{C.GREY}{H_SIDE}{C.WHITE}{full_line}{C.GREY}{H_SIDE}{C.RESET}')
                except Exception as e:
                    error_message = f" Error rendering {data.get('instance_name', key)}: {e}"
                    error_line = colorize(error_message.ljust(UI_WIDTH - 4), C.BRIGHT_RED)
                    print_centered(f'{C.GREY}{H_SIDE}{error_line}{C.GREY}{H_SIDE}{C.RESET}')
    print_centered(f'{C.GREY}{H_BOT_LEFT}{H_BOT * (UI_WIDTH - 2)}{H_BOT_RIGHT}{C.RESET}')
    print()
    if sys.platform == 'win32':
        print_centered(colorize("'CTRL+T' Scheduled R | 'CTRL+X' Menu | 'CTRL+G' Debug | 'CTRL+C' Exit", C.DIM + C.GREY))
    else:
        print_centered(colorize('Monitoring is active. Press Ctrl+C to exit.', C.DIM + C.GREY))
    print_centered(colorize('Made by Isaac, also known as Kirsh', C.DIM + C.CYAN))

def draw_debug_dashboard(debug_log):
    """Draw debug dashboard using Rich library"""
    if not RICH_ENABLED:
        draw_debug_dashboard_legacy(debug_log)
        return
    rich_console.clear()
    log_text = '\n'.join(debug_log[-30:]) if debug_log else f"[{current_rich_theme['dim']}]No debug logs yet[/{current_rich_theme['dim']}]"
    panel = Panel(log_text, title='[bold magenta]Debug Log[/bold magenta]', subtitle=f"[{current_rich_theme['dim']}]Showing last 30 entries[/{current_rich_theme['dim']}]", box=box.ROUNDED, style='magenta', padding=(1, 2))
    rich_console.print(panel)
    rich_console.print()
    if sys.platform == 'win32':
        rich_console.print(f"[{current_rich_theme['dim']}]HOTKEYS: CTRL+G: Toggle Debug | CTRL+X: Menu | CTRL+C: Exit[/{current_rich_theme['dim']}]", justify='center')
    else:
        rich_console.print(f"[{current_rich_theme['dim']}]Debug mode is active. Press Ctrl+C to exit.[/{current_rich_theme['dim']}]", justify='center')
    rich_console.print(f"[{current_rich_theme['dim']}]Made by Isaac (Kirsh)[/{current_rich_theme['dim']}]", justify='center')

def draw_debug_dashboard_legacy(debug_log):
    """Legacy ANSI debug dashboard"""
    os.system('cls' if os.name == 'nt' else 'clear')
    title = '* DEBUG MODE *'
    print_centered(f'{C.GREY}{H_TOP_LEFT}{H_TOP * (UI_WIDTH - 2)}{H_TOP_RIGHT}{C.RESET}')
    print_centered(f'{C.GREY}{H_SIDE}{C.RESET}{colorize(title.center(UI_WIDTH - 2), C.BOLD + C.MAGENTA)}{C.GREY}{H_SIDE}{C.RESET}')
    print_centered(f'{C.GREY}{H_T_MID}{H_BOT * (UI_WIDTH - 2)}{H_T_MID_DOWN}{C.RESET}')
    for entry in debug_log[-20:]:
        print_centered(f'{C.GREY}{H_SIDE}{C.RESET} {entry.ljust(UI_WIDTH - 4)} {C.GREY}{H_SIDE}{C.RESET}')
    print_centered(f'{C.GREY}{H_BOT_LEFT}{H_BOT * (UI_WIDTH - 2)}{H_BOT_RIGHT}{C.RESET}')
    print()
    if sys.platform == 'win32':
        print_centered(colorize("HOTKEYS (window must be focused): 'CTRL+G' Toggle Debug | 'CTRL+X' Menu | 'CTRL+C' Exit", C.DIM + C.GREY))
    else:
        print_centered(colorize('Debug mode is active. Press Ctrl+C to exit.', C.DIM + C.GREY))
    print_centered(colorize('Made by Isaac, also known as Kirsh', C.DIM + C.CYAN))
MUMU_PROCESS_NAMES = ['MuMuVMM Headless Frontend.exe', 'MuMuPlayer.exe', 'NemuHeadless.exe', 'MuMuVMM Interface.exe', 'NemuPlayer.exe']
MUMU_DIR_NAMES = ['mumu', 'nemu', 'mumuplayer']
LDPLAYER_PROCESS_NAMES = ['dnplayer.exe', 'ldplayer.exe', 'Ld9BoxHeadless.exe']
LDPLAYER_DIR_NAMES = ['ldplayer', 'dnplayer', 'xuanzhi']
BLUESTACKS_PROCESS_NAMES = ['HD-Player.exe', 'BlueStacks.exe', 'Bluestacks.exe', 'BlueStacksX.exe']

def _get_mumu_from_path(base_path):
    if not base_path or not os.path.exists(base_path):
        return None
    possible_adb_locations = [os.path.join('nx_main', 'adb.exe'), os.path.join('vmonitor', 'bin', 'adb.exe'), os.path.join('shell', 'adb.exe')]
    found_adb_path = None
    for rel_path in possible_adb_locations:
        potential_path = os.path.join(base_path, rel_path)
        if os.path.exists(potential_path):
            found_adb_path = potential_path
            break
    vms_path = os.path.join(base_path, 'vms')
    if found_adb_path and os.path.exists(vms_path):
        log_event(f'Found valid MuMu path: {base_path}', 'INFO')
        log_event(f'Using ADB at: {found_adb_path}', 'INFO')
        return (base_path, found_adb_path, vms_path)
    return None

def _scan_directory_for_mumu(directory):
    log_event(f'Scanning directory: {directory}', 'INFO')
    if not directory or not os.path.exists(directory):
        return None
    try:
        for dirname in os.listdir(directory):
            if any((name_part in dirname.lower() for name_part in MUMU_DIR_NAMES)):
                path_to_check = os.path.join(directory, dirname)
                result = _get_mumu_from_path(path_to_check)
                if result:
                    return result
    except (IOError, PermissionError):
        pass
    return None

def get_mumu_paths():
    if sys.platform != 'win32':
        return (None, None, None)
    if DESKTOP_MODE_ENABLED:
        try:
            log_event('Scanning for MuMu process...', 'INFO')
            for proc in psutil.process_iter(['name', 'exe']):
                if proc.info['name'] in MUMU_PROCESS_NAMES:
                    proc_path = proc.info['exe']
                    install_path_options = [os.path.dirname(proc_path), os.path.dirname(os.path.dirname(proc_path))]
                    for install_path in install_path_options:
                        result = _get_mumu_from_path(install_path)
                        if result:
                            return result
        except (psutil.NoSuchProcess, psutil.AccessDenied, TypeError) as e:
            log_event(f'psutil scan failed: {e}', 'WARN')
    try:
        log_event('Checking shortcuts...', 'INFO')
        shell_obj = win32com.client.Dispatch('WScript.Shell')
        shortcut_locations = [shell.SHGetFolderPath(0, shellcon.CSIDL_COMMON_DESKTOPDIRECTORY, None, 0), shell.SHGetFolderPath(0, shellcon.CSIDL_DESKTOPDIRECTORY, None, 0), shell.SHGetFolderPath(0, shellcon.CSIDL_COMMON_STARTMENU, None, 0), shell.SHGetFolderPath(0, shellcon.CSIDL_STARTMENU, None, 0)]
        for loc in set(shortcut_locations):
            for (root, _, files) in os.walk(loc):
                for file in files:
                    if file.lower().endswith('.lnk'):
                        if any((name_part in file.lower() for name_part in MUMU_DIR_NAMES)):
                            try:
                                shortcut_path = os.path.join(root, file)
                                target_path = shell_obj.CreateShortCut(shortcut_path).TargetPath
                                if any((proc_name.lower() in target_path.lower() for proc_name in MUMU_PROCESS_NAMES)):
                                    install_path_options = [os.path.dirname(target_path), os.path.dirname(os.path.dirname(target_path))]
                                    for install_path in install_path_options:
                                        result = _get_mumu_from_path(install_path)
                                        if result:
                                            return result
                            except Exception:
                                continue
    except Exception as e:
        log_event(f'Shortcut scan failed: {e}', 'WARN')
    try:
        import winreg
        log_event('Checking registry...', 'INFO')
        uninstall_key_path = 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall'
        key_handles = [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]
        for handle in key_handles:
            with winreg.OpenKey(handle, uninstall_key_path) as uninstall_key:
                for i in range(winreg.QueryInfoKey(uninstall_key)[0]):
                    try:
                        subkey_name = winreg.EnumKey(uninstall_key, i)
                        if any((name_part in subkey_name.lower() for name_part in MUMU_DIR_NAMES)):
                            with winreg.OpenKey(uninstall_key, subkey_name) as app_key:
                                (install_path, _) = winreg.QueryValueEx(app_key, 'InstallLocation')
                                result = _get_mumu_from_path(install_path)
                                if result:
                                    return result
                    except (FileNotFoundError, OSError):
                        continue
    except (FileNotFoundError, ImportError) as e:
        log_event(f'Registry scan failed: {e}', 'WARN')
    log_event('Attempting to find MuMu via common directories...', 'INFO')
    common_dirs = [os.getenv('ProgramFiles'), os.getenv('ProgramFiles(x86)'), os.getenv('ProgramData'), os.getenv('LOCALAPPDATA'), os.path.join(os.getenv('SystemDrive'), '\\'), os.path.expanduser('~'), os.path.join(os.path.expanduser('~'), 'Desktop')]
    common_dirs.extend([os.path.join(d, 'Netease') for d in common_dirs if d])
    for directory in set((d for d in common_dirs if d)):
        result = _scan_directory_for_mumu(directory)
        if result:
            return result
    log_event('All methods failed to find MuMu Player installation.', 'ERROR')
    return (None, None, None)

def find_active_mumu_emulators():
    (mumu_dir, adb_path, vms_path) = get_mumu_paths()
    if not vms_path:
        print_centered(colorize('[X] CRITICAL: MuMu Player VMS directory not found.', C.RED))
        return []
    print_centered(colorize('--- Scanning MuMu Instances (via log file method) ---', C.CYAN))
    active_emulators_list = []
    try:
        instance_folders = os.listdir(vms_path)
    except FileNotFoundError:
        print_centered(colorize(f'[X] VMS path not found at: {vms_path}', C.RED))
        return []
    for folder_name in instance_folders:
        (port, name) = (None, f'Instance ({folder_name})')
        is_active = False
        try:
            log_path = os.path.join(vms_path, folder_name, 'logs', 'VBox.log')
            if os.path.exists(log_path):
                with open(log_path, 'r', encoding='utf-8', errors='ignore') as file:
                    if 'stopped' not in file.read():
                        is_active = True
            else:
                continue
            if not is_active:
                continue
            shell_cfg_path = os.path.join(vms_path, folder_name, 'configs', 'vm_config.json')
            if os.path.exists(shell_cfg_path):
                with open(shell_cfg_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    port = data.get('vm', {}).get('nat', {}).get('port_forward', {}).get('adb', {}).get('host_port')
            extra_cfg_path = os.path.join(vms_path, folder_name, 'configs', 'extra_config.json')
            if os.path.exists(extra_cfg_path):
                with open(extra_cfg_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    name = data.get('playerName', name)
            if port:
                print_centered(colorize(f"[+] Found Active MuMu Instance: '{name}' on port {port}", C.GREEN))
                active_emulators_list.append({'port': str(port), 'name': name, 'type': 'mumu'})
        except Exception as e:
            log_event(f"Error scanning mumu instance folder '{folder_name}': {e}", 'WARN', 'detector')
            continue
    if not active_emulators_list:
        print_centered(colorize('-> No active MuMu instances found using log file method.', C.ORANGE))
    return active_emulators_list

def _validate_ld_path(path):
    if not path or not os.path.exists(path):
        return None
    vms_path = os.path.join(path, 'vms')
    console_path = os.path.join(path, 'dnconsole.exe')
    if os.path.exists(vms_path) and os.path.exists(console_path):
        log_event(f'Validated LDPlayer installation at: {path}', 'SUCCESS', 'ld_detector')
        return (path, os.path.join(path, 'adb.exe'), vms_path)
    return None

def get_ldplayer_paths():
    log_event('Attempting to find LDPlayer installation path...', 'INFO', 'ld_detector')
    if DESKTOP_MODE_ENABLED:
        log_event('Scanning running processes for LDPlayer...', 'INFO', 'ld_detector')
        for proc in psutil.process_iter(['name', 'exe']):
            try:
                if proc.info['name'] in LDPLAYER_PROCESS_NAMES:
                    proc_path = proc.info['exe']
                    install_path = os.path.dirname(proc_path)
                    result = _validate_ld_path(install_path)
                    if result:
                        return result
            except (psutil.NoSuchProcess, psutil.AccessDenied, TypeError):
                continue
    else:
        log_event('psutil library not found. Skipping process scan.', 'WARN', 'ld_detector')
    log_event('Process scan failed or unavailable. Falling back to drive scan...', 'INFO', 'ld_detector')
    drive_letters = []
    try:
        proc = subprocess.run(['wmic', 'logicaldisk', 'get', 'name'], capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
        drive_letters = [line.strip() for line in proc.stdout.splitlines() if ':' in line]
        log_event(f"Found drives to scan: {', '.join(drive_letters)}", 'INFO', 'ld_detector')
    except (subprocess.CalledProcessError, FileNotFoundError):
        log_event('Could not get drive list via WMIC, using common drive letters.', 'WARN', 'ld_detector')
        drive_letters = ['C:\\', 'D:\\', 'E:\\', 'F:\\']
    search_paths = [os.getenv('ProgramFiles'), os.getenv('ProgramFiles(x86)')]
    search_paths.extend(drive_letters)
    for path in set((p for p in search_paths if p and os.path.exists(p))):
        log_event(f'Scanning directory: {path}', 'DEBUG', 'ld_detector')
        try:
            for dirname in os.listdir(path):
                if any((name_part in dirname.lower() for name_part in LDPLAYER_DIR_NAMES)):
                    potential_path = os.path.join(path, dirname)
                    result = _validate_ld_path(potential_path)
                    if result:
                        return result
        except (IOError, PermissionError):
            continue
    log_event('All detection methods failed. Could not find LDPlayer installation path.', 'ERROR', 'ld_detector')
    return (None, None, None)

def find_active_ldplayer_emulators():
    (ldplayer_dir, _, _) = get_ldplayer_paths()
    if not ldplayer_dir:
        print_centered(colorize('[X] CRITICAL: LDPlayer directory not found.', C.RED))
        return []
    print_centered(colorize('--- Scanning LDPlayer Instances ---', C.CYAN))
    active_emulators = []
    try:
        console_path = os.path.join(ldplayer_dir, 'dnconsole.exe')
        if not os.path.exists(console_path):
            log_event("'dnconsole.exe' not found.", 'ERROR', 'ld_detector')
            return []
        list_result = subprocess.run([console_path, 'list2'], capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW, cwd=ldplayer_dir)
        running_instances = []
        lines = list_result.stdout.strip().splitlines()
        for line in lines:
            parts = line.split(',')
            if len(parts) >= 5 and parts[4] == '1':
                try:
                    running_instances.append({'index': int(parts[0]), 'name': parts[1]})
                except (ValueError, IndexError):
                    continue
        if not running_instances:
            log_event('dnconsole reports no instances are running.', 'INFO', 'ld_detector')
            return []
        for instance in running_instances:
            instance_name = instance['name']
            instance_index = instance['index']
            try:
                adb_result = subprocess.run([console_path, 'adb', '--index', str(instance_index), '--command', 'get-serialno'], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW, cwd=ldplayer_dir, timeout=10)
                output_text = adb_result.stdout + adb_result.stderr
                match = re.search('emulator-(\\d+)', output_text)
                if match:
                    console_port = int(match.group(1))
                    adb_port = console_port + 1
                    print_centered(colorize(f"[+] Found Active LDPlayer Instance: '{instance_name}' on port {adb_port}", C.GREEN))
                    active_emulators.append({'port': str(adb_port), 'name': instance_name, 'index': instance_index, 'type': 'ldplayer'})
                else:
                    log_event(f"Could not determine port for '{instance_name}'", 'ERROR', 'ld_detector')
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
                log_event(f'Failed to run dnconsole adb command for instance {instance_index}: {e}', 'ERROR', 'ld_detector')
                continue
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        log_event(f'Failed to run dnconsole list2 command: {e}', 'ERROR', 'ld_detector')
        return []
    if not active_emulators:
        print_centered(colorize('-> No active LDPlayer instances could be fully verified.', C.ORANGE))
    return active_emulators

def get_bluestacks_paths():
    log_event('Searching for BlueStacks installation...', 'INFO', 'bs_detector')
    if not DESKTOP_MODE_ENABLED:
        log_event('psutil not found, cannot scan processes. This may reduce detection accuracy.', 'WARN', 'bs_detector')
        return (None, None)
    for proc in psutil.process_iter(['name', 'exe']):
        try:
            if proc.info['name'] in BLUESTACKS_PROCESS_NAMES:
                install_path = os.path.dirname(proc.info['exe'])
                adb_path = os.path.join(install_path, 'HD-Adb.exe')
                if os.path.exists(adb_path):
                    log_event(f'Found BlueStacks process. Path: {install_path}', 'SUCCESS', 'bs_detector')
                    return (install_path, adb_path)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    log_event('Could not find a running BlueStacks process.', 'ERROR', 'bs_detector')
    return (None, None)

def find_active_bluestacks_emulators():
    print_centered(colorize('--- Scanning BlueStacks Instances ---', C.CYAN))
    (install_dir, adb_path) = get_bluestacks_paths()
    if not adb_path:
        return []
    config_file_path = os.path.join(os.getenv('ProgramData'), 'BlueStacks_nxt', 'bluestacks.conf')
    if not os.path.exists(config_file_path):
        log_event(f'BlueStacks config file not found at: {config_file_path}', 'ERROR', 'bs_detector')
        return []
    all_configured_ports = {}
    try:
        with open(config_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                match = re.search('bst\\.instance\\.([^. ]+)\\.adb_port="(\\d+)"', line)
                if match:
                    all_configured_ports[match.group(1)] = match.group(2)
    except Exception as e:
        log_event(f'Error parsing BlueStacks config file: {e}', 'ERROR', 'bs_detector')
        return []
    active_emulators = []
    try:
        command = [adb_path, 'devices']
        result = subprocess.run(command, capture_output=True, text=True, timeout=10, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
        adb_output = result.stdout
        for (name, port_str) in all_configured_ports.items():
            port = int(port_str)
            console_port = port - 1
            is_connected = f'127.0.0.1:{port}' in adb_output or f'emulator-{console_port}' in adb_output
            is_device_ready = 'device' in adb_output
            if is_connected and is_device_ready:
                print_centered(colorize(f"[+] Found Active BlueStacks Instance: '{name}' on port {port}", C.GREEN))
                active_emulators.append({'port': str(port), 'name': f'BlueStacks - {name}', 'type': 'bluestacks'})
    except Exception as e:
        log_event(f'An error occurred while running ADB for BlueStacks: {e}', 'ERROR', 'bs_detector')
    if not active_emulators:
        print_centered(colorize('-> No active BlueStacks instances found.', C.ORANGE))
    return active_emulators

def find_active_emulator_instances(mode):
    if mode == 'mumu':
        return find_active_mumu_emulators()
    elif mode == 'ldplayer':
        return find_active_ldplayer_emulators()
    elif mode == 'bluestacks':
        return find_active_bluestacks_emulators()
    return []

def get_emulator_adb_path(mode):
    if mode == 'mumu':
        (_, adb_path, _) = get_mumu_paths()
        return adb_path
    elif mode == 'ldplayer':
        (_, adb_path, _) = get_ldplayer_paths()
        return adb_path
    elif mode == 'bluestacks':
        (_, adb_path) = get_bluestacks_paths()
        return adb_path
    return None

def run_adb_command(adb_path, port, command, timeout=10):
    full_command = [adb_path, '-s', f'127.0.0.1:{port}', 'shell'] + command
    try:
        return subprocess.run(full_command, capture_output=True, text=True, timeout=timeout, check=True, encoding='utf-8', errors='ignore', creationflags=subprocess.CREATE_NO_WINDOW)
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as e:
        log_event(f'ADB command failed: {e}', 'ERROR', str(port))
        return None

def launch_roblox_instance(profile, target, adb_path=None):
    session_key = str(target)
    log_event('--> Launching', 'INFO', session_key)
    place_id = profile.get('place_id')
    link_code = profile.get('private_server_link_code')
    roblox_account_cookie = profile.get('roblox_cookie')
    if link_code:
        log_event(f'Private server detected - Place ID: {place_id}, Link Code: {link_code[:20]}...', 'INFO', session_key)
    else:
        log_event(f'Public server launch - Place ID: {place_id}', 'INFO', session_key)
    if not place_id:
        log_event('Cannot launch: Place ID is missing.', 'ERROR', session_key)
        return
    if profile.get('mode') == 'desktop':
        if not DESKTOP_MODE_ENABLED:
            log_event('Cannot launch: Desktop mode disabled.', 'ERROR', session_key)
            return
        if not roblox_account_cookie:
            log_event('Cannot launch: Roblox account cookie is missing for desktop mode.', 'ERROR', session_key)
            return
        if link_code:
            log_event('Using browser-based launch for private server...', 'INFO', session_key)
            success = launch_private_server_browser(place_id, link_code, roblox_account_cookie, session_key)
            if success:
                log_event('Private server browser launch completed!', 'INFO', session_key)
            else:
                log_event('Private server browser launch failed!', 'ERROR', session_key)
            return
        auth_ticket = get_auth_ticket(clean_cookie(roblox_account_cookie))
        if not auth_ticket:
            log_event('Could not get auth ticket for desktop launch. The cookie might be invalid or expired.', 'ERROR', session_key)
            return
        browser_tracker_id = random.randint(100000000000, 999999999999)
        placelauncher_url = f'https%3A%2F%2Fassetgame.roblox.com%2Fgame%2FPlaceLauncher.ashx%3Frequest%3DRequestGame%26browserTrackerId%3D{browser_tracker_id}%26placeId%3D{place_id}%26isPlayTogetherGame%3Dfalse'
        launch_url = f'roblox-player:1+launchmode:play+gameinfo:{auth_ticket}+launchtime:{int(time.time() * 1000)}+placelauncherurl:{placelauncher_url}+browsertrackerid:{browser_tracker_id}+robloxLocale:en_us+gameLocale:en_us+channel:+LaunchExp:InApp'
        try:
            os.startfile(launch_url)
            log_event('Roblox launch command sent!', 'INFO', session_key)
        except Exception as e:
            log_event(f'Error launching Roblox: {e}', 'ERROR', session_key)
    elif profile.get('mode') in ['mumu', 'ldplayer', 'bluestacks']:
        if not adb_path:
            log_event('Cannot launch: ADB path missing.', 'ERROR', session_key)
            return
        if link_code:
            log_event('VIP server links are not directly launchable on emulators. Launching standard game.', 'WARN', session_key)
        uri = f'roblox://placeId={place_id}'
        launch_command = ['am', 'start', '-n', f'{ROBLOX_PACKAGE_NAME}/{ROBLOX_ACTIVITY_NAME}', '-a', 'android.intent.action.VIEW', '-d', uri]
        run_adb_command(adb_path, session_key, launch_command)

def find_new_roblox_pid(existing_pids):
    for _ in range(20):
        try:
            current_pids = {p.pid for p in psutil.process_iter(['name']) if p.info['name'] == ROBLOX_PROCESS_NAME}
            new_pids = current_pids - existing_pids
            if new_pids:
                return new_pids.pop()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
        time.sleep(1)
    return None

def configure_scheduled_restart():
    """Configure scheduled restart settings for a session"""
    config = load_config()
    restart_defaults = config.get('settings', {}).get('scheduled_restart_defaults', {})
    default_enabled = restart_defaults.get('enabled', False)
    default_interval = restart_defaults.get('interval', 60)
    draw_header('SCHEDULED RESTART')
    if default_interval < 1:
        d_text = f'{int(default_interval * 60)}s'
    elif abs(default_interval - round(default_interval)) < 0.01:
        d_text = f'{int(round(default_interval))}m'
    else:
        d_text = f'{default_interval:.2f}m'
    status_text = 'Enabled' if default_enabled else 'Disabled'
    print_centered(f'Default: {colorize(status_text, C.CYAN)} ({d_text})')
    print()
    options = ['Use Default Settings', 'Enable (20 minutes)', 'Enable (30 minutes)', 'Enable (45 minutes)', 'Enable (1 hour)', 'Enable (2 hours)', 'Enable (4 hours)', 'Enable (Testing - 30 seconds)', 'Enable (Custom Interval)', 'Disable Restart']
    choice = get_choice('Select option', options)
    if choice == 1:
        return (default_enabled, default_interval)
    elif choice == 10:
        return (False, default_interval)
    interval_map = {2: 20, 3: 30, 4: 45, 5: 60, 6: 120, 7: 240, 8: 0.5}
    if choice in interval_map:
        return (True, interval_map[choice])
    elif choice == 9:
        while True:
            try:
                val = get_input('Enter interval in minutes')
                if not val:
                    return (default_enabled, default_interval)
                new_interval = float(val)
                if new_interval <= 0:
                    print_centered(colorize('Must be positive.', C.RED))
                    continue
                if new_interval < 20:
                    print_centered(colorize('Minimum is 20 minutes.', C.RED))
                    continue
                return (True, new_interval)
            except ValueError:
                print_centered(colorize('Invalid number.', C.RED))
    return (default_enabled, default_interval)

def check_emulator(port, adb_path, profile):
    emul = port
    adb = adb_path
    log_event('Connecting via ADB...', 'INFO', str(port))
    subprocess.run([adb, 'connect', f'127.0.0.1:{emul}'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0)
    time.sleep(2)
    launch_roblox_instance(profile, port, adb_path=adb)
    with STATUS_LOCK:
        if str(port) in SESSION_STATUS:
            SESSION_STATUS[str(port)]['crashes'] = 0
    time.sleep(10)
    check_emulator.last_freeze_check = time.time()
    debug_window_title = f"Debug View - {SESSION_STATUS.get(str(port), {}).get('instance_name', port)}"
    debug_window_active = False
    while MONITORING_ACTIVE:
        emulator_name = SESSION_STATUS.get(str(port), {}).get('instance_name', '')
        hwnd = None
        if emulator_name:
            hwnd = win32gui.FindWindow(None, emulator_name)
        current_time = time.time()
        last_debug_update = getattr(check_emulator, 'last_debug_update', 0)
        if DEBUG_MODE_ACTIVE and current_time - last_debug_update >= 1.0:
            try:
                if hwnd and win32gui.IsWindow(hwnd) and win32gui.IsWindowVisible(hwnd):
                    (left, top, right, bottom) = win32gui.GetWindowRect(hwnd)
                    width = right - left
                    height = bottom - top
                    if width > 0 and height > 0:
                        monitor = {'top': top, 'left': left, 'width': width, 'height': height}
                        with mss() as sct:
                            debug_image = np.array(sct.grab(monitor))
                        scale_percent = 50
                        new_width = int(debug_image.shape[1] * scale_percent / 100)
                        new_height = int(debug_image.shape[0] * scale_percent / 100)
                        resized_image = cv2.resize(debug_image, (new_width, new_height), interpolation=cv2.INTER_AREA)
                        cv2.imshow(debug_window_title, resized_image)
                        debug_window_active = True
                        cv2.waitKey(1)
                        check_emulator.last_debug_update = current_time
                elif debug_window_active:
                    cv2.destroyWindow(debug_window_title)
                    debug_window_active = False
            except Exception:
                if debug_window_active:
                    cv2.destroyWindow(debug_window_title)
                    debug_window_active = False
        elif not DEBUG_MODE_ACTIVE:
            if debug_window_active:
                cv2.destroyWindow(debug_window_title)
                debug_window_active = False
        if find_visual_error(hwnd, base_path):
            log_event(f'Detected Disconnect for {emulator_name}. Relaunching...', 'WARN', str(port))
            run_adb_command(adb, emul, ['am', 'force-stop', ROBLOX_PACKAGE_NAME])
            time.sleep(2)
            launch_roblox_instance(profile, port, adb_path=adb)
            time.sleep(10)
            continue
        current_time = time.time()
        last_freeze_check = getattr(check_emulator, 'last_freeze_check', 0)
        freeze_check_interval = profile.get('freeze_check_interval_main', 120)
        if profile.get('freeze_detection_enabled', True) and current_time - last_freeze_check >= freeze_check_interval:
            freeze_threshold = profile.get('freeze_threshold', 0.98)
            freeze_interval = profile.get('freeze_check_interval', 5)
            freeze_checks = profile.get('freeze_consecutive_checks', 2)
            if detect_freeze(hwnd, freeze_threshold=freeze_threshold, check_interval=freeze_interval, consecutive_checks=freeze_checks, is_emulator=True):
                log_event(f'Detected Freeze for {emulator_name}. Relaunching...', 'WARN', str(port))
                run_adb_command(adb, emul, ['am', 'force-stop', ROBLOX_PACKAGE_NAME])
                time.sleep(2)
                launch_roblox_instance(profile, port, adb_path=adb)
                time.sleep(10)
                continue
            check_emulator.last_freeze_check = current_time
        try:
            ps_result = run_adb_command(adb, emul, ['ps'])
            if ps_result and ROBLOX_PACKAGE_NAME in ps_result.stdout:
                log_event('Running', 'SUCCESS', str(port))
                time.sleep(0.1 if DEBUG_MODE_ACTIVE else 5)
            else:
                log_event('Roblox not found. Relaunching...', 'WARN', str(port))
                with STATUS_LOCK:
                    session_data = SESSION_STATUS.get(str(port))
                    if session_data:
                        session_data['crashes'] += 1
                        if session_data.get('restarter_enabled') and profile.get('restarter_interval', 0) > 0:
                            cooldown_minutes = profile.get('restarter_interval', 0)
                            session_data['next_restart_time'] = time.time() + cooldown_minutes * 60
                            log_event('Crash detected. Scheduled restart timer reset.', 'INFO', str(port))
                run_adb_command(adb, emul, ['am', 'force-stop', ROBLOX_PACKAGE_NAME])
                time.sleep(2)
                launch_roblox_instance(profile, port, adb_path=adb)
                time.sleep(10)
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            log_event('Emulator offline. Retrying connection...', 'ERROR', str(port))
            subprocess.run([adb, 'connect', f'127.0.0.1:{emul}'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0)
            time.sleep(15)
        except Exception as e:
            log_event(f'An unexpected error occurred: {e}', 'ERROR', str(port))
            time.sleep(15)
    if not MONITORING_ACTIVE:
        if debug_window_active:
            cv2.destroyWindow(debug_window_title)

def check_desktop_by_pid(profile, session_key):
    pid = profile.get('pid')
    if not pid:
        log_event('Monitoring thread started without a PID!', 'ERROR', session_key)
        return
    with STATUS_LOCK:
        if session_key in SESSION_STATUS and SESSION_STATUS[session_key].get('crashes') == -1:
            SESSION_STATUS[session_key]['crashes'] = 0
    debug_window_title = f'Debug View - {session_key}'
    debug_window_active = False
    while MONITORING_ACTIVE:
        hwnd = find_roblox_hwnd(pid)
        is_crashed = False
        current_time = time.time()
        last_debug_update = getattr(check_desktop_by_pid, 'last_debug_update', 0)
        if DEBUG_MODE_ACTIVE and current_time - last_debug_update >= 1.0:
            try:
                if hwnd and win32gui.IsWindow(hwnd) and win32gui.IsWindowVisible(hwnd):
                    (left, top, right, bottom) = win32gui.GetWindowRect(hwnd)
                    width = right - left
                    height = bottom - top
                    if width > 0 and height > 0:
                        monitor = {'top': top, 'left': left, 'width': width, 'height': height}
                        with mss() as sct:
                            debug_image = np.array(sct.grab(monitor))
                        scale_percent = 50
                        new_width = int(debug_image.shape[1] * scale_percent / 100)
                        new_height = int(debug_image.shape[0] * scale_percent / 100)
                        resized_image = cv2.resize(debug_image, (new_width, new_height), interpolation=cv2.INTER_AREA)
                        cv2.imshow(debug_window_title, resized_image)
                        debug_window_active = True
                        cv2.waitKey(1)
                        check_desktop_by_pid.last_debug_update = current_time
                elif debug_window_active:
                    cv2.destroyWindow(debug_window_title)
                    debug_window_active = False
            except Exception:
                if debug_window_active:
                    cv2.destroyWindow(debug_window_title)
                    debug_window_active = False
        elif not DEBUG_MODE_ACTIVE:
            if debug_window_active:
                cv2.destroyWindow(debug_window_title)
                debug_window_active = False
        if find_visual_error(hwnd, base_path):
            log_event(f'Visual error detected for PID {pid}. Relaunching...', 'WARN', session_key)
            try:
                psutil.Process(pid).kill()
            except psutil.NoSuchProcess:
                pass
            is_crashed = True
        current_time = time.time()
        last_freeze_check = getattr(check_desktop_by_pid, 'last_freeze_check', 0)
        freeze_check_interval = profile.get('freeze_check_interval_main', 120)
        if profile.get('freeze_detection_enabled', True) and current_time - last_freeze_check >= freeze_check_interval:
            freeze_threshold = profile.get('freeze_threshold', 0.98)
            freeze_interval = profile.get('freeze_check_interval', 5)
            freeze_checks = profile.get('freeze_consecutive_checks', 2)
            if detect_freeze(hwnd, freeze_threshold=freeze_threshold, check_interval=freeze_interval, consecutive_checks=freeze_checks):
                log_event(f'Freeze detected for PID {pid}. Relaunching...', 'WARN', session_key)
                try:
                    psutil.Process(pid).kill()
                except psutil.NoSuchProcess:
                    pass
                is_crashed = True
            check_desktop_by_pid.last_freeze_check = current_time
        if not is_crashed:
            try:
                if psutil.pid_exists(pid):
                    proc = psutil.Process(pid)
                    if proc.name() == ROBLOX_PROCESS_NAME:
                        status = proc.status()
                        if status in [psutil.STATUS_RUNNING, psutil.STATUS_SLEEPING, psutil.STATUS_DISK_SLEEP]:
                            log_event('Running', 'SUCCESS', session_key)
                            time.sleep(0.1 if DEBUG_MODE_ACTIVE else 5)
                            continue
                        else:
                            log_event(f'Process in invalid state: {status}', 'WARN', session_key)
                is_crashed = True
            except psutil.NoSuchProcess:
                is_crashed = True
            except Exception as e:
                log_event(f'Monitoring error for PID {pid}: {e}', 'ERROR', session_key)
                time.sleep(5)
                continue
        if is_crashed:
            log_event(f'Crash detected (PID {pid}). Relaunching...', 'ERROR', session_key)
            with STATUS_LOCK:
                session_data = SESSION_STATUS.get(session_key)
                if session_data:
                    session_data['crashes'] += 1
                    if session_data.get('restarter_enabled') and profile.get('restarter_interval', 0) > 0:
                        cooldown_minutes = profile.get('restarter_interval', 0)
                        session_data['next_restart_time'] = time.time() + cooldown_minutes * 60
                        log_event('Crash detected. Scheduled restart timer reset.', 'INFO', session_key)
            if not profile.get('roblox_cookie'):
                log_event('Cannot relaunch: No account associated with this existing instance.', 'ERROR', session_key)
                break
            existing_pids = {p.pid for p in psutil.process_iter(['name']) if p.info['name'] == ROBLOX_PROCESS_NAME}
            launch_roblox_instance(profile, session_key)
            log_event('Waiting for new process...', 'INFO', session_key)
            new_pid = find_new_roblox_pid(existing_pids)
            if new_pid:
                pid = new_pid
                profile['pid'] = new_pid
                log_event(f'Now monitoring new PID: {pid}', 'INFO', session_key)
                with STATUS_LOCK:
                    if session_key in SESSION_STATUS:
                        SESSION_STATUS[session_key]['pid'] = new_pid
                time.sleep(5)
            else:
                log_event('Relaunch failed. Could not find new process.', 'ERROR', session_key)
                time.sleep(10)
    if not MONITORING_ACTIVE:
        if debug_window_active:
            cv2.destroyWindow(debug_window_title)
        return
        log_event(f'Crash detected (PID {pid}). Relaunching...', 'ERROR', session_key)
        with STATUS_LOCK:
            session_data = SESSION_STATUS.get(session_key)
            if session_data:
                session_data['crashes'] += 1
                if session_data.get('restarter_enabled') and profile.get('restarter_interval', 0) > 0:
                    cooldown_minutes = profile.get('restarter_interval', 0)
                    session_data['next_restart_time'] = time.time() + cooldown_minutes * 60
                    log_event('Crash detected. Scheduled restart timer reset.', 'INFO', session_key)
        if not profile.get('roblox_cookie'):
            log_event('Cannot relaunch: No account associated with this existing instance.', 'ERROR', session_key)
            return
        existing_pids = {p.pid for p in psutil.process_iter(['name']) if p.info['name'] == ROBLOX_PROCESS_NAME}
        launch_roblox_instance(profile, session_key)
        log_event('Waiting for new process...', 'INFO', session_key)
        new_pid = find_new_roblox_pid(existing_pids)
        if new_pid:
            pid = new_pid
            profile['pid'] = new_pid
            log_event(f'Now monitoring new PID: {pid}', 'INFO', session_key)
            with STATUS_LOCK:
                if session_key in SESSION_STATUS:
                    SESSION_STATUS[session_key]['pid'] = new_pid
            time.sleep(5)
        else:
            log_event('Relaunch failed. Could not find new process.', 'ERROR', session_key)
            time.sleep(10)

def emulator_session_restarter(port, cooldown_minutes, profile, adb_path):
    while MONITORING_ACTIVE:
        time.sleep(1)
        if not MONITORING_ACTIVE:
            break
        should_restart = False
        with STATUS_LOCK:
            session_data = SESSION_STATUS.get(str(port))
            if not session_data or not session_data.get('restarter_enabled'):
                if session_data:
                    session_data['next_restart_time'] = 0
                continue
            if session_data.get('next_restart_time', 0) == 0:
                session_data['next_restart_time'] = time.time() + cooldown_minutes * 60
            if time.time() >= session_data.get('next_restart_time', float('inf')):
                should_restart = True
                session_data['restarts'] += 1
                session_data['next_restart_time'] = time.time() + cooldown_minutes * 60
        if should_restart:
            log_event('Scheduled restart...', 'INFO', str(port))
            run_adb_command(adb_path, str(port), ['am', 'force-stop', ROBLOX_PACKAGE_NAME])
            time.sleep(5)
            launch_roblox_instance(profile, str(port), adb_path=adb_path)

def desktop_session_restarter(profile, cooldown_minutes, session_key):
    while MONITORING_ACTIVE:
        time.sleep(1)
        if not MONITORING_ACTIVE:
            break
        should_restart = False
        with STATUS_LOCK:
            session_data = SESSION_STATUS.get(session_key)
            if not session_data or not session_data.get('restarter_enabled'):
                if session_data:
                    session_data['next_restart_time'] = 0
                continue
            if session_data.get('next_restart_time', 0) == 0:
                session_data['next_restart_time'] = time.time() + cooldown_minutes * 60
            if time.time() >= session_data.get('next_restart_time', float('inf')):
                should_restart = True
                session_data['restarts'] += 1
                session_data['next_restart_time'] = time.time() + cooldown_minutes * 60
        if should_restart:
            log_event('Scheduled restart...', 'INFO', session_key)
            try:
                pid_to_kill = None
                with STATUS_LOCK:
                    if session_key in SESSION_STATUS:
                        pid_to_kill = SESSION_STATUS[session_key].get('pid')
                if pid_to_kill and psutil.pid_exists(pid_to_kill):
                    log_event(f'Killing PID {pid_to_kill} for scheduled restart.', 'INFO', session_key)
                    psutil.Process(pid_to_kill).kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

def troubleshoot_connection():
    draw_header('CONNECTION TROUBLESHOOTER')
    print_centered('This wizard will attempt to fix common emulator connection issues.')
    emulator_choice = get_choice('Which emulator are you troubleshooting?', ['MuMu Player', 'LDPlayer', 'BlueStacks', 'Cancel'])
    if not emulator_choice or emulator_choice > 3:
        return
    if emulator_choice == 1:
        mode = 'mumu'
    elif emulator_choice == 2:
        mode = 'ldplayer'
    elif emulator_choice == 3:
        mode = 'bluestacks'
    adb_path = get_emulator_adb_path(mode)
    if not adb_path:
        print_centered(colorize(f'[X] Could not find adb.exe for {mode.capitalize()}. Cannot proceed.', C.RED))
        input('\nPress Enter to return to menu...')
        return
    print_centered(colorize('\n--- Step 1: Resetting ADB Server ---', C.CYAN))
    try:
        subprocess.run([adb_path, 'kill-server'], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
        time.sleep(1)
        result = subprocess.run([adb_path, 'start-server'], capture_output=True, text=True, timeout=5, creationflags=subprocess.CREATE_NO_WINDOW)
        if 'successfully' in result.stdout:
            print_centered(colorize('[+] ADB server reset successfully.', C.GREEN))
        else:
            print_centered(colorize('[!] ADB server may not have started correctly.', C.ORANGE))
    except Exception as e:
        print_centered(colorize(f'[X] Failed to reset ADB server: {e}', C.RED))
    print()
    print_centered(colorize('--- Step 2: Checking Administrator Rights ---', C.CYAN))
    if is_admin():
        print_centered(colorize('[+] Script is running as Administrator.', C.GREEN))
    else:
        print_centered(colorize('[!] WARNING: Script is NOT running as Administrator.', C.ORANGE))
        print_centered(colorize('This is a common cause of issues. Please restart the script by', C.ORANGE))
        print_centered(colorize("right-clicking it and selecting 'Run as administrator'.", C.ORANGE))
    print()
    print_centered(colorize('--- Step 3: Final Connection Check ---', C.CYAN))
    try:
        result = subprocess.run([adb_path, 'devices'], capture_output=True, text=True, timeout=5, creationflags=subprocess.CREATE_NO_WINDOW)
        print_centered("Result of 'adb devices':")
        for line in result.stdout.strip().splitlines():
            print_centered(colorize(line, C.WHITE))
    except Exception as e:
        print_centered(colorize(f'[X] Could not run final check: {e}', C.RED))
    print()
    input(colorize('Troubleshooting complete. Press Enter to return to the menu...', C.DIM))

def request_toggle():
    global TOGGLE_REQUESTED
    TOGGLE_REQUESTED = True

def request_exit_to_menu():
    global EXIT_TO_MENU_REQUESTED
    EXIT_TO_MENU_REQUESTED = True

def request_debug_toggle():
    global DEBUG_MODE_ACTIVE
    DEBUG_MODE_ACTIVE = not DEBUG_MODE_ACTIVE

def handle_toggle_restart_menu():
    global SESSION_STATUS
    os.system('cls' if os.name == 'nt' else 'clear')
    draw_header('TOGGLE SCHEDULED RESTART')
    with STATUS_LOCK:
        sessions = list(SESSION_STATUS.items())
    if not sessions:
        print_centered('No active sessions to toggle.')
        time.sleep(2)
        return
    options = []
    for (key, data) in sessions:
        status = colorize('Enabled', C.GREEN) if data.get('restarter_enabled') else colorize('Disabled', C.RED)
        options.append(f"{data['instance_name']} (Currently: {status})")
    options.append('Cancel')
    choice = get_choice('Select a session to toggle restart for:', options)
    if choice is not None and 1 <= choice <= len(sessions):
        (session_key_to_toggle, session_data_to_toggle) = sessions[choice - 1]
        with STATUS_LOCK:
            current_status = SESSION_STATUS[session_key_to_toggle].get('restarter_enabled', False)
            SESSION_STATUS[session_key_to_toggle]['restarter_enabled'] = not current_status
            new_status_text = 'ENABLED' if not current_status else 'DISABLED'
            color = C.GREEN if not current_status else C.RED
            instance_name = session_data_to_toggle['instance_name']
            print_centered(colorize(f'Scheduled restarts {new_status_text} for {instance_name}.', color))
        time.sleep(1.5)

def end_session_after_duration(duration_hours):
    if duration_hours > 0:
        time.sleep(duration_hours * 3600)
        global MONITORING_ACTIVE
        MONITORING_ACTIVE = False
        print_centered(colorize('\nSession duration complete. Exiting.', C.GREEN))
        os._exit(0)

def confirm_launch_with_warning():
    draw_header('(!) IMPORTANT ACCOUNT WARNING (!)')
    print_centered(colorize('You are about to launch a session.', C.ORANGE))
    print_centered(colorize('If you are using an executor or other third-party tools,', C.GREY))
    print_centered(colorize('it is STRONGLY recommended to use an alternate account.', C.GREY))
    print()
    print_centered(colorize('Using such software can put your account at risk.', C.WHITE))
    print_centered(colorize('The developers are not responsible for any action taken against your account.', C.WHITE))
    print()
    choice = get_input('Are you sure you want to continue? (y/n)', C.BRIGHT_RED).lower()
    if choice == 'y':
        return True
    else:
        print_centered(colorize('Launch aborted by user.', C.CYAN))
        time.sleep(2)
        return False

def launch_monitor_all_dashboard():
    draw_header('MONITOR ALL - PLATFORM SELECTION')
    platform_options = {'mumu': 'MuMu Player', 'ldplayer': 'LDPlayer', 'bluestacks': 'BlueStacks'}
    if DESKTOP_MODE_ENABLED:
        platform_options['desktop'] = 'Normal Roblox (Desktop)'
        platform_options['existing'] = colorize('Monitor Existing Instances', C.YELLOW)
    selected_platforms = []
    while True:
        draw_header('SELECT PLATFORMS TO MONITOR')
        print_centered('Select which platforms you want to include in this session.')
        choices = []
        for (key, name) in platform_options.items():
            status = colorize(' (Selected)', C.GREEN) if key in selected_platforms else ''
            choices.append(f'{name}{status}')
        choices.append('Continue to Configuration')
        choices.append('Cancel')
        choice = get_choice('Choose an option', choices)
        if choice is None:
            continue
        if 1 <= choice <= len(platform_options):
            platform_key = list(platform_options.keys())[choice - 1]
            EMULATOR_TYPES = {'mumu', 'ldplayer', 'bluestacks'}
            is_new_selection_emulator = platform_key in EMULATOR_TYPES
            selected_emulator_type = None
            for p_key in selected_platforms:
                if p_key in EMULATOR_TYPES:
                    selected_emulator_type = p_key
                    break
            if is_new_selection_emulator and selected_emulator_type and (platform_key != selected_emulator_type):
                draw_header('EMULATOR CONFLICT')
                print_centered(colorize('You can only monitor one type of emulator at a time due to ADB limitations.', C.RED))
                print_centered(colorize(f"You have already selected '{platform_options[selected_emulator_type]}'.", C.ORANGE))
                print_centered(colorize('Please deselect it before choosing another emulator type.', C.ORANGE))
                time.sleep(4)
                continue
            if platform_key in selected_platforms:
                selected_platforms.remove(platform_key)
            else:
                selected_platforms.append(platform_key)
        elif choice == len(choices) - 1:
            if not selected_platforms:
                print_centered(colorize('You must select at least one platform to monitor.', C.RED))
                time.sleep(2)
            else:
                break
        elif choice == len(choices):
            return
    if any((p in selected_platforms for p in ['mumu', 'ldplayer', 'bluestacks'])):
        draw_header('ATTENTION')
        print_centered(colorize('Please ensure all emulators you wish to monitor are OPEN and RUNNING.', C.ORANGE))
        print_centered(colorize('The script will now scan for active instances.', C.GREY))
        print()
        get_input('Press Enter to continue...')
    profiles_to_launch = []
    for platform_mode in selected_platforms:
        if platform_mode in ['mumu', 'ldplayer', 'bluestacks']:
            active_emulators = find_active_emulator_instances(platform_mode)
            if not active_emulators:
                print_centered(colorize(f'No active {platform_mode.capitalize()} instances found. Skipping.', C.ORANGE))
                time.sleep(2)
                continue
            for emul in active_emulators:
                instance_name = emul['name']
                config_context_title = f'CONFIGURE: {instance_name}'
                (place_id, link_code) = select_game(context_title=config_context_title)
                if place_id is None:
                    print_centered(colorize('No game selected. This instance will not be monitored.', C.ORANGE))
                    time.sleep(2)
                    continue
                (restarter_on, interval) = configure_scheduled_restart()
                config = load_config()
                freeze_defaults = config.get('settings', {}).get('freeze_detection_defaults', {})
                freeze_enabled = freeze_defaults.get('enabled', False)
                freeze_interval = freeze_defaults.get('interval', 30)
                profile = {'profile_name': f'MonAll - {instance_name}', 'mode': platform_mode, 'instance_target': emul, 'place_id': place_id, 'private_server_link_code': link_code, 'restarter_on': restarter_on, 'restarter_interval': interval, 'freeze_detection_enabled': freeze_enabled, 'freeze_check_interval_main': freeze_interval}
                profiles_to_launch.append(profile)
        elif platform_mode == 'desktop':
            accounts = load_roblox_accounts()
            if not accounts:
                print_centered(colorize('No Roblox accounts found. Please add an account first.', C.RED))
                time.sleep(3)
                continue
            draw_header('SELECT DESKTOP INSTANCES')
            num_instances_str = get_input('How many new desktop instances do you want to launch?')
            try:
                num_instances = int(num_instances_str)
                if num_instances <= 0:
                    raise ValueError
            except (ValueError, TypeError):
                print_centered(colorize('Invalid number.', C.RED))
                time.sleep(2)
                continue
            for i in range(num_instances):
                instance_num = i + 1
                draw_header(f'CONFIGURE DESKTOP INSTANCE {instance_num}/{num_instances}')
                account_names = list(accounts.keys())
                account_options = [f'{name}' for name in account_names]
                account_choice = get_choice(f'Select Roblox account for instance {instance_num}', account_options + ['Cancel'])
                if not account_choice or account_choice > len(account_names):
                    print_centered(colorize('Cancelled instance configuration.', C.CYAN))
                    time.sleep(2)
                    continue
                selected_account_name = account_names[account_choice - 1]
                (place_id, link_code) = select_game(context_title=f'CONFIGURE: Desktop - {selected_account_name}')
                if place_id is None:
                    print_centered(colorize('No game selected. Skipping instance.', C.ORANGE))
                    time.sleep(2)
                    continue
                (restarter_on, interval) = configure_scheduled_restart()
                config = load_config()
                freeze_defaults = config.get('settings', {}).get('freeze_detection_defaults', {})
                freeze_enabled = freeze_defaults.get('enabled', False)
                freeze_interval = freeze_defaults.get('interval', 30)
                profile = {'profile_name': f'MonAll - {selected_account_name}', 'mode': 'desktop', 'place_id': place_id, 'private_server_link_code': link_code, 'restarter_on': restarter_on, 'restarter_interval': interval, 'roblox_account_name': selected_account_name, 'roblox_cookie': accounts[selected_account_name], 'freeze_detection_enabled': freeze_enabled, 'freeze_check_interval_main': freeze_interval}
                profiles_to_launch.append(profile)
        elif platform_mode == 'existing':
            profiles_to_launch.extend(scan_and_configure_existing_instances())
    if profiles_to_launch:
        if not confirm_launch_with_warning():
            return
        launch_monitor(profiles_to_launch)
    else:
        print_centered(colorize('No instances were configured for monitoring.', C.ORANGE))
        time.sleep(3)

def launch_monitor(profiles):
    global SESSION_STATUS, MONITORING_ACTIVE, TOGGLE_REQUESTED, EXIT_TO_MENU_REQUESTED, DEBUG_MODE_ACTIVE
    MONITORING_ACTIVE = True
    SESSION_STATUS = {}
    if BACKGROUND_SPAMMER_ENABLED:
        background_spammer_daemon = threading.Thread(target=background_auto_spammer, daemon=True)
        background_spammer_daemon.start()
        debug_log_only('Background auto spammer started with profile monitoring', 'INFO')
    else:
        debug_log_only('Background auto spammer is disabled in configuration', 'INFO')
    emulator_profiles = [p for p in profiles if isinstance(p, dict) and p.get('mode') in ['mumu', 'ldplayer', 'bluestacks']]
    if emulator_profiles and EMULATOR_BACKGROUND_SPAMMER_ENABLED:
        emulator_mode = emulator_profiles[0].get('mode')
        active_emulators = find_active_emulator_instances(emulator_mode)
        adb_path = get_emulator_adb_path(emulator_mode)
        if active_emulators and adb_path:
            emulator_spammer_daemon = threading.Thread(target=emulator_background_auto_spammer, args=(active_emulators, adb_path), daemon=True)
            emulator_spammer_daemon.start()
            debug_log_only(f'Emulator background spammer started for {len(active_emulators)} {emulator_mode} instance(s)', 'INFO')
        else:
            debug_log_only('Emulator background spammer enabled but no active emulators found', 'WARN')
    elif emulator_profiles and (not EMULATOR_BACKGROUND_SPAMMER_ENABLED):
        debug_log_only('Emulator background spammer is disabled in configuration', 'INFO')
    EMULATOR_TYPES = {'mumu', 'ldplayer', 'bluestacks'}
    found_emulator_types = set()
    if isinstance(profiles, list):
        for p in profiles:
            if p.get('mode') in EMULATOR_TYPES:
                found_emulator_types.add(p.get('mode'))
    if len(found_emulator_types) > 1:
        draw_header('!! LAUNCH ABORTED !!')
        print_centered(colorize('ADB CONFLICT DETECTED', C.BRIGHT_RED))
        print_centered(colorize('Cannot monitor multiple emulator types in the same session.', C.ORANGE))
        print_centered(colorize(f"Detected types: {', '.join((t.capitalize() for t in found_emulator_types))}", C.WHITE))
        print_centered(colorize('Please launch sessions for different emulators separately.', C.ORANGE))
        input('\nPress Enter to return to the menu...')
        return
    if not isinstance(profiles, list):
        profiles = [profiles]
    TOGGLE_REQUESTED = False
    EXIT_TO_MENU_REQUESTED = False
    DEBUG_MODE_ACTIVE = False

    def console_input_handler():
        global MONITORING_ACTIVE, TOGGLE_REQUESTED, EXIT_TO_MENU_REQUESTED, DEBUG_MODE_ACTIVE
        if sys.platform != 'win32':
            return
        while MONITORING_ACTIVE:
            try:
                if msvcrt.kbhit():
                    key = msvcrt.getch()
                    if key == b'\x14':
                        request_toggle()
                    elif key == b'\x18':
                        request_exit_to_menu()
                    elif key == b'\x07':
                        request_debug_toggle()
                    elif key == b'\x03':
                        print_centered(colorize('\nShutting down...', C.ORANGE))
                        MONITORING_ACTIVE = False
                        break
            except (IOError, OSError):
                break
            except Exception:
                break
            time.sleep(1.0)
    if sys.platform == 'win32':
        input_thread = threading.Thread(target=console_input_handler, daemon=True)
        input_thread.start()
    draw_header('SESSION DURATION')
    config = load_config()
    session_defaults = config.get('settings', {}).get('session_defaults', {})
    duration_hours = session_defaults.get('duration', 0)
    if duration_hours == 0:
        print_centered(colorize('Using default: Unlimited session', C.GREEN))
    else:
        print_centered(colorize(f'Using default: {duration_hours} hours', C.GREEN))
    print()
    override = get_input('Override default duration? (y/n)').lower() == 'y'
    if override:
        while True:
            try:
                duration_str = get_input('Enter session duration in hours (0 for unlimited)')
                duration_hours = float(duration_str)
                if duration_hours >= 0:
                    break
            except (ValueError, TypeError):
                print_centered(colorize('Invalid input. Please enter a number.', C.RED))
    start_time = time.time()
    if duration_hours > 0:
        threading.Thread(target=end_session_after_duration, args=(duration_hours,), daemon=True).start()
    all_launched_pids = {p.pid for p in psutil.process_iter(['name']) if p.info['name'] == ROBLOX_PROCESS_NAME}
    desktop_instance_count = 0
    for profile in profiles:
        mode = profile['mode']
        (session_key, instance_name) = ('', '')
        if mode in ['mumu', 'ldplayer', 'bluestacks']:
            emul = profile.get('instance_target')
            if not emul:
                continue
            (session_key, instance_name) = (str(emul['port']), emul['name'])
        elif mode == 'desktop':
            desktop_instance_count += 1
            instance_name = profile.get('roblox_account_name', f'Desktop {desktop_instance_count}')
            session_key = f"desktop_{instance_name}_{profile.get('pid', desktop_instance_count)}"
        with STATUS_LOCK:
            SESSION_STATUS[session_key] = {'profile_name': profile['profile_name'], 'instance_name': instance_name, 'status': colorize('Initializing...', C.CYAN), 'crashes': -1, 'restarts': 0, 'restarter_enabled': profile.get('restarter_on', False), 'next_restart_time': 0}
        if mode in ['mumu', 'ldplayer', 'bluestacks']:
            adb_path = get_emulator_adb_path(mode)
            if not adb_path:
                log_event(f'Could not find {mode.capitalize()} ADB path. Skipping.', 'ERROR', session_key)
                continue
            threading.Thread(target=check_emulator, args=(session_key, adb_path, profile), daemon=True).start()
        elif mode == 'desktop' and DESKTOP_MODE_ENABLED:
            if 'pid' in profile and profile['pid'] is not None:
                log_event(f"Monitoring existing PID {profile['pid']} for {instance_name}", 'INFO', 'system')
                threading.Thread(target=check_desktop_by_pid, args=(profile, session_key), daemon=True).start()
            else:
                launch_roblox_instance(profile, session_key)
                log_event(f'Waiting for new process for {instance_name}...', 'INFO', 'system')
                new_pid = find_new_roblox_pid(all_launched_pids)
                if not new_pid:
                    log_event(f'Could not find process for {instance_name}. Skipping.', 'ERROR', session_key)
                    continue
                all_launched_pids.add(new_pid)
                profile['pid'] = new_pid
                with STATUS_LOCK:
                    if session_key in SESSION_STATUS:
                        SESSION_STATUS[session_key]['pid'] = new_pid
                threading.Thread(target=check_desktop_by_pid, args=(profile, session_key), daemon=True).start()
        if profile.get('restarter_on') and profile.get('restarter_interval', 0) > 0:
            restarter_func = desktop_session_restarter if mode == 'desktop' else emulator_session_restarter
            args = (profile, profile['restarter_interval'], session_key) if mode == 'desktop' else (session_key, profile['restarter_interval'], profile, get_emulator_adb_path(mode))
            threading.Thread(target=restarter_func, args=args, daemon=True).start()
        print_centered(colorize('Waiting 5s...', C.DIM + C.GREY))
        time.sleep(5)
    try:
        dummy_profile_for_dashboard_title = profiles[0] if profiles else {}
        while MONITORING_ACTIVE:
            if EXIT_TO_MENU_REQUESTED:
                print_centered(colorize('\nExiting to menu...', C.ORANGE))
                time.sleep(1.5)
                MONITORING_ACTIVE = False
                continue
            if TOGGLE_REQUESTED:
                handle_toggle_restart_menu()
                TOGGLE_REQUESTED = False
            if DEBUG_MODE_ACTIVE:
                draw_debug_dashboard(DEBUG_LOG)
            else:
                draw_dashboard(start_time, duration_hours, dummy_profile_for_dashboard_title)
            time.sleep(1.5)
    except KeyboardInterrupt:
        print_centered(colorize('\nOperation cancelled by user.', C.ORANGE))
        MONITORING_ACTIVE = False
        time.sleep(2)
        sys.exit(0)
    except Exception as e:
        MONITORING_ACTIVE = False
        print_centered(colorize(f'\nUNEXPECTED ERROR IN UI THREAD: {e}', C.BRIGHT_RED))
        log_event(f'Dashboard crashed with error: {e}', level='ERROR', session_key='system')
        input('Press Enter to exit...')
    finally:
        EXIT_TO_MENU_REQUESTED = False
        TOGGLE_REQUESTED = False

def resolve_share_link(share_url):
    """
    Resolve new Roblox share link format using Selenium with authentication.
    New format: https://www.roblox.com/share?code=xxxxx&type=Server
    Returns: (place_id, link_code) or (None, None) if failed
    """
    driver = None
    try:
        if not re.search('roblox\\.com/share\\?code=([a-f0-9]+)&type=Server', share_url, re.IGNORECASE):
            return (None, None)
        print_centered(colorize('Detected new share link format.', C.CYAN))
        print_centered(colorize('Resolving link...', C.DIM))
        accounts = load_roblox_accounts()
        if not accounts:
            print_centered(colorize('No accounts configured. Cannot resolve new share links.', C.RED))
            print_centered(colorize('Please add an account first, or use the old link format.', C.ORANGE))
            time.sleep(3)
            return (None, None)
        account_name = list(accounts.keys())[0]
        account_cookie = accounts[account_name]
        print_centered(colorize(f"Using {account_name} to resolve...", C.CYAN))
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(f'user-data-dir={CHROME_PROFILE_PATH}')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-logging')
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-features=ExternalProtocolPrompt')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        prefs = {'protocol_handler.excluded_schemes': {'roblox-player': False, 'roblox': False}}
        chrome_options.add_experimental_option('prefs', prefs)
        service = ChromeService(ChromeDriverManager().install())
        service.creation_flags = subprocess.CREATE_NO_WINDOW
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(20)
        print_centered(colorize('Injecting auth...', C.DIM))
        driver.get('https://www.roblox.com')
        time.sleep(1)
        driver.delete_all_cookies()
        clean_cookie_value = clean_cookie(account_cookie)
        driver.add_cookie({'name': '.ROBLOSECURITY', 'value': clean_cookie_value, 'domain': '.roblox.com', 'path': '/', 'secure': True, 'httpOnly': True})
        print_centered(colorize(' Navigating to share link...', C.DIM))
        driver.get(share_url)
        time.sleep(3)
        final_url = driver.current_url
        print_centered(colorize(f' Redirect complete', C.DIM))
        place_id = None
        link_code = None
        place_id_match = re.search('/games/(\\d+)/', final_url)
        link_code_match = re.search('privateServerLinkCode=([\\w\\d\\-=_]+)', final_url)
        if place_id_match and link_code_match:
            place_id = int(place_id_match.group(1))
            link_code = link_code_match.group(1)
            print_centered(colorize(f'Successfully resolved share link!', C.GREEN))
            print_centered(colorize(f'Place ID: {place_id}', C.GREEN))
            print_centered(colorize(f'Link Code: {link_code[:15]}...', C.GREEN))
            time.sleep(2)
            return (place_id, link_code)
        else:
            print_centered(colorize('Could not extract game details from redirected URL.', C.RED))
            print_centered(colorize(f'Final URL: {final_url[:80]}...', C.DIM))
            time.sleep(3)
            return (None, None)
    except Exception as e:
        print_centered(colorize(f'Error resolving share link: {e}', C.RED))
        time.sleep(2)
        return (None, None)
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

def select_game(context_title=None):
    if context_title:
        header_title = f'{context_title} - GAME'
    else:
        header_title = 'SELECT A GAME'
    draw_header(header_title)
    game_list = list(GAMES_DB.keys())
    options = game_list + ['Enter a Custom Place ID', 'Enter a Private Server Link', 'Back']
    while True:
        CREDIT_TEXT = colorize('Made by Isaac, also known as Kirsh', C.DIM + C.CYAN)
        print()
        print_centered(CREDIT_TEXT)
        choice = get_choice('Choose a game or option', options)
        if choice is None:
            draw_header(header_title)
            continue
        if 1 <= choice <= len(game_list):
            return (GAMES_DB[game_list[choice - 1]], None)
        elif choice == len(game_list) + 1:
            draw_header(header_title)
            try:
                return (int(get_input('Enter Custom Roblox PlaceID')), None)
            except (ValueError, TypeError):
                draw_header(header_title)
                print_centered(colorize('Invalid ID. Please enter numbers only.', C.RED))
                time.sleep(2)
                draw_header(header_title)
        elif choice == len(game_list) + 2:
            draw_header(header_title)
            if not SHARE_LINK_RESOLUTION_ENABLED:
                print_centered(colorize("This feature requires the 'requests' library.", C.RED))
                print_centered(colorize("Please run 'pip install requests' and restart the script.", C.ORANGE))
                time.sleep(4)
                draw_header(header_title)
                continue
            try:
                url = get_input('Paste the full Private Server Link')
                (place_id, link_code) = (None, None)
                print_centered(colorize('Resolving link...', C.DIM))
                match = re.search('roblox\\.com/games/(\\d+)/.*?privateServerLinkCode=([\\w\\d\\-=_]+)', url)
                if match:
                    place_id = int(match.group(1))
                    link_code = match.group(2)
                    print_centered(colorize(f'[+] Detected Place ID: {place_id}', C.GREEN))
                    print_centered(colorize(f'[+] Detected Link Code: {link_code[:15]}...', C.GREEN))
                    time.sleep(2)
                    return (place_id, link_code)
                if re.search('roblox\\.com/share\\?code=([a-f0-9]+)&type=Server', url, re.IGNORECASE):
                    (place_id, link_code) = resolve_share_link(url)
                    if place_id and link_code:
                        return (place_id, link_code)
                    else:
                        draw_header(header_title)
                        print_centered(colorize('Failed to resolve new share link format.', C.RED))
                        time.sleep(3)
                        draw_header(header_title)
                        continue
                try:
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
                    response = requests.get(url, allow_redirects=True, timeout=10, headers=headers)
                    response.raise_for_status()
                    place_id_match = re.search('/games/(\\d+)/', response.url)
                    link_code_match = re.search('privateServerLinkCode=([\\w\\d\\-=_]+)', response.url)
                    if place_id_match and link_code_match:
                        place_id = int(place_id_match.group(1))
                        link_code = link_code_match.group(1)
                except requests.RequestException as e:
                    draw_header(header_title)
                    print_centered(colorize(f'Failed to resolve link: {e}', C.RED))
                    time.sleep(3)
                    draw_header(header_title)
                    continue
                if place_id and link_code:
                    print_centered(colorize(f'[+] Detected Place ID: {place_id}', C.GREEN))
                    print_centered(colorize(f'[+] Detected Link Code: {link_code[:15]}...', C.GREEN))
                    time.sleep(2)
                    return (place_id, link_code)
                else:
                    draw_header(header_title)
                    print_centered(colorize('Invalid link. Could not extract game details.', C.RED))
                    time.sleep(3)
                    draw_header(header_title)
            except Exception as e:
                draw_header(header_title)
                print_centered(colorize(f'An unexpected error occurred: {e}', C.RED))
                time.sleep(2)
                draw_header(header_title)
        elif choice == len(options):
            return (None, None)

def create_or_edit_profile(config, profile_name=None):
    (is_editing, settings) = (profile_name is not None, config['profiles'].get(profile_name, {}) if profile_name else {})
    CREDIT_TEXT = colorize('Made by Isaac, also known as Kirsh', C.DIM + C.CYAN)
    draw_header(f'EDITING: {profile_name}' if is_editing else 'CREATE NEW PROFILE')
    if not is_editing:
        while 'mode' not in settings:
            draw_header('SELECT PROFILE MODE')
            mode_options = ['MuMu Player (Emulator)', 'LDPlayer (Emulator)', 'BlueStacks (Emulator)']
            if DESKTOP_MODE_ENABLED:
                mode_options.append('Normal Roblox (Desktop)')
            else:
                mode_options.append(colorize('Normal Roblox (Desktop) - [DISABLED, psutil not found]', C.GREY))
            mode_options.append('Cancel')
            print()
            print_centered(CREDIT_TEXT)
            mode_choice = get_choice('What will this profile manage?', mode_options)
            if mode_choice == 1:
                settings['mode'] = 'mumu'
            elif mode_choice == 2:
                settings['mode'] = 'ldplayer'
            elif mode_choice == 3:
                settings['mode'] = 'bluestacks'
            elif mode_choice == 4 and DESKTOP_MODE_ENABLED:
                settings['mode'] = 'desktop'
            elif mode_choice == 4 and (not DESKTOP_MODE_ENABLED):
                print_centered(colorize("Please install 'psutil' to enable this mode.", C.RED))
                time.sleep(3)
            elif mode_choice == len(mode_options):
                return
            else:
                continue
    draw_header(f"PROFILE SETTINGS: {profile_name or 'New'}")
    current_game_display = f"ID: {settings.get('place_id', 'Not Set')}"
    if settings.get('private_server_link_code'):
        current_game_display += ' (Private Link)'
    if not is_editing or get_input(f'Current Game: {current_game_display}. Change? (y/n)', C.ORANGE).lower() == 'y':
        (new_place_id, new_link_code) = select_game()
        if new_place_id is not None:
            (settings['place_id'], settings['private_server_link_code']) = (new_place_id, new_link_code)
        elif not is_editing:
            return
    if not settings.get('place_id'):
        print_centered(colorize('No game selected. Aborting profile creation.', C.RED))
        time.sleep(2)
        return
    if settings.get('mode') == 'desktop':
        accounts = load_roblox_accounts()
        if not accounts:
            print_centered(colorize('No Roblox accounts found. You must add accounts in the manager first.', C.RED))
            time.sleep(3)
            return
        account_names = list(accounts.keys())
        selected_accounts = settings.get('accounts', []) if is_editing else []
        while True:
            draw_header(f"PROFILE: {profile_name or 'New'} - SELECT ACCOUNTS")
            print_centered('Select which accounts to associate with this profile.')
            for (i, acc_name) in enumerate(account_names):
                status = colorize(' [Selected]', C.GREEN) if acc_name in selected_accounts else ''
                print_centered(f'[{i + 1}] {acc_name}{status}')
            print()
            print_centered("Enter numbers to toggle selection (e.g., 1,3). Type 'done' to finish.")
            choice_str = get_input('Selection')
            if choice_str.lower() == 'done':
                if not selected_accounts:
                    print_centered(colorize('You must select at least one account.', C.RED))
                    time.sleep(2)
                    continue
                else:
                    break
            try:
                for sel_idx in [int(i.strip()) for i in choice_str.split(',') if i.strip().isdigit()]:
                    if 1 <= sel_idx <= len(account_names):
                        acc_name_to_toggle = account_names[sel_idx - 1]
                        if acc_name_to_toggle in selected_accounts:
                            selected_accounts.remove(acc_name_to_toggle)
                        else:
                            selected_accounts.append(acc_name_to_toggle)
            except ValueError:
                print_centered(colorize('Invalid input.', C.RED))
                time.sleep(2)
        settings['accounts'] = selected_accounts
    (settings['restarter_on'], settings['restarter_interval']) = configure_scheduled_restart()
    current_freeze_enabled = settings.get('freeze_detection_enabled', True)
    if is_editing:
        change_freeze = get_input('Change Freeze Detection settings? (y/n)', C.ORANGE).lower() == 'y'
        if change_freeze:
            freeze_enabled = get_input('Enable Freeze Detection? (y/n)', C.BLUE).lower() == 'y'
            settings['freeze_detection_enabled'] = freeze_enabled
            if freeze_enabled:
                try:
                    freeze_interval = int(get_input('Freeze Check Interval (10-120 seconds, default 30)'))
                    if 10 <= freeze_interval <= 120:
                        settings['freeze_check_interval_main'] = freeze_interval
                    else:
                        print_centered(colorize('Invalid interval. Using default 30 seconds.', C.RED))
                        settings['freeze_check_interval_main'] = 30
                        time.sleep(1)
                except (ValueError, TypeError):
                    print_centered(colorize('Invalid input. Using default 30 seconds.', C.RED))
                    settings['freeze_check_interval_main'] = 30
                    time.sleep(1)
    else:
        config = load_config()
        freeze_defaults = config.get('settings', {}).get('freeze_detection_defaults', {})
        settings['freeze_detection_enabled'] = freeze_defaults.get('enabled', False)
        settings['freeze_check_interval_main'] = freeze_defaults.get('interval', 30)
    if settings.get('freeze_detection_enabled', True):
        current_freeze_interval = settings.get('freeze_check_interval_main', 120)
        try:
            new_interval = int(get_input(f'Freeze Check Interval (currently {current_freeze_interval} seconds, enter 10-120)'))
            if 10 <= new_interval <= 120:
                settings['freeze_check_interval_main'] = new_interval
            else:
                print_centered(colorize('Invalid interval. Using default 120 seconds.', C.RED))
                settings['freeze_check_interval_main'] = 120
        except (ValueError, TypeError):
            print_centered(colorize('Invalid input. Using default 120 seconds.', C.RED))
            settings['freeze_check_interval_main'] = 120
    if not is_editing:
        while True:
            draw_header('SAVE PROFILE')
            profile_name_input = get_input('Enter a name for this profile')
            if profile_name_input and profile_name_input not in config['profiles']:
                profile_name = profile_name_input
                break
            elif not profile_name_input:
                print_centered(colorize('Name cannot be empty.', C.RED))
            else:
                print_centered(colorize('A profile with this name already exists.', C.RED))
    config['profiles'][profile_name] = settings
    save_config(config)
    print_centered(colorize(f"Profile '{profile_name}' ({settings['mode']}) saved!", C.GREEN))
    time.sleep(2)

def manage_profiles():
    while True:
        config = load_config()
        apply_theme(config)
        draw_header('PROFILE MANAGER')
        profiles = config.get('profiles', {})
        profile_names = list(profiles.keys())
        if not profile_names:
            print_centered(colorize('No profiles found.', C.ORANGE))
            no_profile_options = ['Create a new profile', 'Back to Main Menu']
            choice = get_choice('What would you like to do?', no_profile_options)
            if choice == 1:
                create_or_edit_profile(config)
                continue
            else:
                return
        display_options = []
        for name in profile_names:
            mode = profiles[name].get('mode', 'N/A').capitalize()
            acc_count_str = ''
            if mode == 'Desktop':
                acc_count = len(profiles[name].get('accounts', []))
                acc_count_str = f' - {acc_count} account(s)' if acc_count > 0 else ' - No accounts'
            display_options.append(f'{name} {C.DIM}({mode}{acc_count_str}){C.RESET}')
        options = ['Launch a Profile', 'Create New Profile', 'Edit a Profile', 'Delete a Profile', colorize('Troubleshoot Connection', C.CYAN), 'Back to Main Menu']
        CREDIT_TEXT = colorize('Made by Isaac, also known as Kirsh', C.DIM + C.CYAN)
        print()
        print_centered(CREDIT_TEXT)
        choice = get_choice('Select an option', options)
        if not choice:
            continue
        if choice == 1:
            launch_choice = get_choice('Choose profile to launch', display_options + ['Cancel'])
            if launch_choice and launch_choice <= len(profile_names):
                profile_to_launch_name = profile_names[launch_choice - 1]
                profile_data = profiles[profile_to_launch_name]
                if not confirm_launch_with_warning():
                    continue
                manage_profiles_launch_logic(profile_data, profile_to_launch_name)
        elif choice == 2:
            create_or_edit_profile(config)
        elif choice == 3:
            edit_choice = get_choice('Choose profile to edit', display_options + ['Cancel'])
            if edit_choice and edit_choice <= len(profile_names):
                create_or_edit_profile(config, profile_names[edit_choice - 1])
        elif choice == 4:
            delete_choice = get_choice('Choose profile to delete', display_options + ['Cancel'])
            if delete_choice and delete_choice <= len(profile_names):
                profile_to_delete = profile_names[delete_choice - 1]
                if get_input(f"Delete '{profile_to_delete}'? (y/n)", C.BRIGHT_RED).lower() == 'y':
                    del config['profiles'][profile_to_delete]
                    if config.get('last_used_profile') == profile_to_delete:
                        config['last_used_profile'] = None
                    save_config(config)
        elif choice == 5:
            troubleshoot_connection()
        elif choice == 6:
            return

def show_about_section():
    draw_header('ABOUT REJOINTOOL')
    print_centered(colorize('Multi-threaded session manager for Roblox instances.', C.WHITE))
    print()
    print_centered(colorize('--- ENGINE & CORE ---', C.CYAN))
    print_centered('- Multi-threaded session management for multiple instances')
    print_centered('- Desktop & Emulator support (MuMu, LDPlayer, BlueStacks)')
    print_centered('- PID-based monitoring for desktop, ADB for emulators')
    print_centered('- Secure account management with encrypted cookie storage')
    print_centered('- Scheduled restart system for session stability')
    print_centered('- Auto-detection of emulator installation paths')
    print()
    print_centered(colorize('--- USER INTERFACE ---', C.CYAN))
    print_centered('- Rich text-based UI with live dashboard')
    print_centered('- Real-time status, crash count, restart tracking')
    print_centered('- Debug Mode (CTRL+G) for verbose event logs')
    print_centered('- 12 unique themes with color customization')
    print_centered('- Hotkeys: CTRL+T (toggle restart), CTRL+X (menu), CTRL+G (debug)')
    print()
    print_centered(colorize('--- CONFIGURATION ---', C.CYAN))
    print_centered('- Profile system for quick setup and launching')
    print_centered('- All settings saved in universal_config.json')
    print_centered('- Per-profile restart intervals and settings')
    print_centered('- Last used profile quick-launch option')
    print()
    print_centered(colorize('--- INFO & CREDITS ---', C.CYAN))
    print_centered(f"{colorize('Developed by:', C.WHITE)} {colorize('Isaac (Kirsh)', C.ORANGE)}")
    print_centered(f"{colorize('Website:', C.WHITE)} {colorize('https://Rejointool.xyz/hi', C.ORANGE)}")
    print_centered(f"{colorize('License:', C.WHITE)} {colorize('MIT License', C.ORANGE)}")
    print()
    print_centered(colorize('--- DISCLAIMER ---', C.CYAN))
    print_centered(colorize('Use alternate accounts when using executors/third-party tools.', C.YELLOW))
    print_centered(colorize('Not responsible for any bans. Use at your own risk.', C.GREY))
    print()
    input(colorize('\nPress Enter to return to the main menu...', C.DIM))

def show_settings_menu():
    while True:
        config = load_config()
        apply_theme(config)
        draw_header('SETTINGS')
        current_theme_name = config.get('settings', {}).get('theme_name', 'Default')
        print_centered(f'Current Theme: {colorize(current_theme_name, C.CYAN)}')
        current_color_override = config.get('settings', {}).get('theme_color_override')
        if current_color_override:
            print_centered(f'Color Override: {colorize(current_color_override, COLOR_MAP.get(current_color_override, C.WHITE))}')
        else:
            print_centered('Color Override: None')
        freeze_defaults = config.get('settings', {}).get('freeze_detection_defaults', {})
        freeze_enabled = freeze_defaults.get('enabled', False)
        freeze_interval = freeze_defaults.get('interval', 30)
        freeze_status = colorize('Enabled', C.GREEN) if freeze_enabled else colorize('Disabled', C.RED)
        print_centered(f'Freeze Detection Default: {freeze_status} ({freeze_interval}s)')
        restart_defaults = config.get('settings', {}).get('scheduled_restart_defaults', {})
        restart_enabled = restart_defaults.get('enabled', False)
        restart_interval = restart_defaults.get('interval', 60)
        restart_status = colorize('Enabled', C.GREEN) if restart_enabled else colorize('Disabled', C.RED)
        print_centered(f'Scheduled Restart Default: {restart_status} ({restart_interval}min)')
        session_defaults = config.get('settings', {}).get('session_defaults', {})
        session_duration = session_defaults.get('duration', 0)
        session_text = 'Unlimited' if session_duration == 0 else f'{session_duration}h'
        print_centered(f'Default Session Duration: {colorize(session_text, C.CYAN)}')
        print()
        options = ['Change Theme', 'Change Accent Color', 'Freeze Detection Defaults', 'Scheduled Restart Defaults', 'Session Duration Default', 'Back to Main Menu']
        choice = get_choice('Select an option', options)
        if choice == 1:
            theme_names = list(THEMES.keys())
            theme_choice = get_choice('Select a new theme', theme_names + ['Cancel'])
            if theme_choice and theme_choice <= len(theme_names):
                config['settings']['theme_name'] = theme_names[theme_choice - 1]
                save_config(config)
                print_centered(colorize(f"Theme set to '{config['settings']['theme_name']}'.", C.GREEN))
                time.sleep(1)
        elif choice == 2:
            color_names = list(COLOR_MAP.keys())
            color_options = [colorize(name, color) for (name, color) in COLOR_MAP.items()]
            color_choice = get_choice('Select a new accent color', color_options + ['Remove Override', 'Cancel'])
            if color_choice and color_choice <= len(color_names):
                config['settings']['theme_color_override'] = color_names[color_choice - 1]
                save_config(config)
            elif color_choice == len(color_names) + 1:
                config['settings']['theme_color_override'] = None
                save_config(config)
                print_centered(colorize('Accent color override removed.', C.GREEN))
                time.sleep(1)
        elif choice == 3:
            configure_freeze_detection_defaults(config)
        elif choice == 4:
            configure_scheduled_restart_defaults(config)
        elif choice == 5:
            configure_session_duration_default(config)
        elif choice == 6:
            break

def configure_freeze_detection_defaults(config):
    """Configure default freeze detection settings"""
    draw_header('FREEZE DETECTION DEFAULTS')
    print_centered('These settings will be used as defaults when creating new profiles.')
    print()
    freeze_defaults = config.get('settings', {}).get('freeze_detection_defaults', {})
    current_enabled = freeze_defaults.get('enabled', False)
    current_interval = freeze_defaults.get('interval', 30)
    print_centered(f"Current: {colorize('Enabled' if current_enabled else 'Disabled', C.CYAN)} with {current_interval}s interval")
    print()
    options = ['Enable by Default', 'Disable by Default', 'Change Default Interval', 'Back']
    choice = get_choice('Select an option', options)
    if choice == 1:
        if 'settings' not in config:
            config['settings'] = {}
        if 'freeze_detection_defaults' not in config['settings']:
            config['settings']['freeze_detection_defaults'] = {}
        config['settings']['freeze_detection_defaults']['enabled'] = True
        save_config(config)
        show_success('Freeze detection will be enabled by default for new profiles')
        time.sleep(1.5)
    elif choice == 2:
        if 'settings' not in config:
            config['settings'] = {}
        if 'freeze_detection_defaults' not in config['settings']:
            config['settings']['freeze_detection_defaults'] = {}
        config['settings']['freeze_detection_defaults']['enabled'] = False
        save_config(config)
        show_success('Freeze detection will be disabled by default for new profiles')
        time.sleep(1.5)
    elif choice == 3:
        try:
            new_interval = int(get_input('Enter default interval in seconds (10-120)'))
            if 10 <= new_interval <= 120:
                if 'settings' not in config:
                    config['settings'] = {}
                if 'freeze_detection_defaults' not in config['settings']:
                    config['settings']['freeze_detection_defaults'] = {}
                config['settings']['freeze_detection_defaults']['interval'] = new_interval
                save_config(config)
                show_success(f'Default interval set to {new_interval} seconds')
                time.sleep(1.5)
            else:
                show_error('Interval must be between 10 and 120 seconds')
                time.sleep(1.5)
        except (ValueError, TypeError):
            show_error('Invalid input. Please enter a number.')
            time.sleep(1.5)

def configure_scheduled_restart_defaults(config):
    """Configure default scheduled restart settings"""
    draw_header('SCHEDULED RESTART DEFAULTS')
    print_centered('These settings will be used as defaults when creating new profiles.')
    print()
    restart_defaults = config.get('settings', {}).get('scheduled_restart_defaults', {})
    current_enabled = restart_defaults.get('enabled', False)
    current_interval = restart_defaults.get('interval', 60)
    if current_interval < 1:
        interval_text = f'{int(current_interval * 60)} seconds'
    elif abs(current_interval - round(current_interval)) < 0.01:
        interval_text = f'{int(round(current_interval))} minutes'
    else:
        interval_text = f'{current_interval:.2f} minutes'
    print_centered(f"Current: {colorize('Enabled' if current_enabled else 'Disabled', C.CYAN)} with {interval_text} interval")
    print()
    options = ['Enable by Default', 'Disable by Default', 'For Testing (30 seconds)', 'Set to 20 minutes', 'Set to 30 minutes', 'Set to 45 minutes', 'Set to 60 minutes', 'Set to 2 hours (120 min)', 'Set to 4 hours (240 min)', 'Set to 6 hours (360 min)', 'Custom Interval (Minutes)', 'Back']
    choice = get_choice('Select an option', options)
    if choice == 1:
        if 'settings' not in config:
            config['settings'] = {}
        if 'scheduled_restart_defaults' not in config['settings']:
            config['settings']['scheduled_restart_defaults'] = {}
        config['settings']['scheduled_restart_defaults']['enabled'] = True
        save_config(config)
        show_success('Scheduled restart will be enabled by default for new profiles')
        time.sleep(1.5)
    elif choice == 2:
        if 'settings' not in config:
            config['settings'] = {}
        if 'scheduled_restart_defaults' not in config['settings']:
            config['settings']['scheduled_restart_defaults'] = {}
        config['settings']['scheduled_restart_defaults']['enabled'] = False
        save_config(config)
        show_success('Scheduled restart will be disabled by default for new profiles')
        time.sleep(1.5)
    else:
        interval_map = {3: 0.5, 4: 20, 5: 30, 6: 45, 7: 60, 8: 120, 9: 240, 10: 360}
        if choice in interval_map:
            new_interval = interval_map[choice]
            if 'settings' not in config:
                config['settings'] = {}
            if 'scheduled_restart_defaults' not in config['settings']:
                config['settings']['scheduled_restart_defaults'] = {}
            config['settings']['scheduled_restart_defaults']['interval'] = new_interval
            save_config(config)
            if new_interval < 1:
                display_text = f'{int(new_interval * 60)} seconds'
            else:
                display_text = f'{new_interval} minutes'
            show_success(f'Default interval set to {display_text}')
            time.sleep(1.5)
        elif choice == 11:
            try:
                new_interval = float(get_input('Enter default interval in minutes'))
                if new_interval <= 0:
                    show_error('Interval must be positive')
                    time.sleep(1.5)
                elif new_interval < 20:
                    show_error("Minimum interval is 20 minutes. Use 'For Testing' option for shorter interval.")
                    time.sleep(2)
                elif new_interval > 1440:
                    show_error('Interval cannot exceed 1440 minutes (24 hours)')
                    time.sleep(1.5)
                else:
                    if 'settings' not in config:
                        config['settings'] = {}
                    if 'scheduled_restart_defaults' not in config['settings']:
                        config['settings']['scheduled_restart_defaults'] = {}
                    config['settings']['scheduled_restart_defaults']['interval'] = new_interval
                    save_config(config)
                    show_success(f'Default interval set to {new_interval} minutes')
                    time.sleep(1.5)
            except (ValueError, TypeError):
                show_error('Invalid input. Please enter a number.')
                time.sleep(1.5)

def configure_session_duration_default(config):
    """Configure default session duration"""
    draw_header('SESSION DURATION DEFAULT')
    print_centered('Set the default session duration for new launches.')
    print()
    session_defaults = config.get('settings', {}).get('session_defaults', {})
    current_duration = session_defaults.get('duration', 0)
    if current_duration == 0:
        duration_text = 'Unlimited'
    elif current_duration < 1:
        minutes = int(current_duration * 60)
        if minutes == 0:
            duration_text = f'{int(current_duration * 3600)} seconds'
        else:
            duration_text = f'{minutes} minutes'
    elif current_duration == 1:
        duration_text = '1 hour'
    elif abs(current_duration - round(current_duration)) < 0.01:
        duration_text = f'{int(round(current_duration))} hours'
    else:
        duration_text = f'{current_duration:.2f} hours'
    print_centered(f'Current: {colorize(duration_text, C.CYAN)}')
    print()
    options = ['Set to Unlimited (0)', 'For Testing (30 seconds)', 'Set to 20 minutes', 'Set to 30 minutes', 'Set to 45 minutes', 'Set to 1 hour', 'Set to 2 hours', 'Set to 4 hours', 'Set to 8 hours', 'Set to 12 hours', 'Set to 24 hours', 'Custom Duration (Minutes)', 'Back']
    choice = get_choice('Select an option', options)
    duration_map = {1: 0, 2: 30 / 3600, 3: 20 / 60, 4: 30 / 60, 5: 45 / 60, 6: 1, 7: 2, 8: 4, 9: 8, 10: 12, 11: 24}
    if choice in duration_map:
        if 'settings' not in config:
            config['settings'] = {}
        if 'session_defaults' not in config['settings']:
            config['settings']['session_defaults'] = {}
        new_duration = duration_map[choice]
        config['settings']['session_defaults']['duration'] = new_duration
        save_config(config)
        if new_duration == 0:
            duration_text = 'unlimited'
        elif new_duration < 1:
            mins = int(new_duration * 60)
            if mins == 0:
                duration_text = f'{int(new_duration * 3600)} seconds'
            else:
                duration_text = f'{mins} minutes'
        else:
            duration_text = f'{new_duration} hours' if new_duration != 1 else '1 hour'
        show_success(f'Default session duration set to {duration_text}')
        time.sleep(1.5)
    elif choice == 12:
        try:
            minutes_input = float(get_input('Enter duration in MINUTES (0 for unlimited)'))
            if minutes_input < 0:
                show_error('Duration cannot be negative')
                time.sleep(1.5)
                return
            if minutes_input == 0:
                new_duration = 0
            elif minutes_input < 20:
                show_error("Minimum duration is 20 minutes. Use 'For Testing' option for shorter duration.")
                time.sleep(2)
                return
            else:
                new_duration = minutes_input / 60
            if new_duration > 168:
                show_error('Duration cannot exceed 168 hours (7 days)')
                time.sleep(1.5)
            else:
                if 'settings' not in config:
                    config['settings'] = {}
                if 'session_defaults' not in config['settings']:
                    config['settings']['session_defaults'] = {}
                config['settings']['session_defaults']['duration'] = new_duration
                save_config(config)
                if new_duration == 0:
                    duration_text = 'unlimited'
                elif new_duration < 1:
                    duration_text = f'{int(new_duration * 60)} minutes'
                else:
                    duration_text = f'{new_duration:.2f} hours'
                show_success(f'Default session duration set to {duration_text}')
                time.sleep(1.5)
        except (ValueError, TypeError):
            show_error('Invalid input. Please enter a number.')
            time.sleep(1.5)

class ServerHopManager:
    """Manages server hopping functionality for chat spammer"""

    def __init__(self, chat_config):
        self.hop_config = chat_config.get('server_hop', {})
        self.enabled = self.hop_config.get('enabled', False)
        self.interval = self.hop_config.get('interval', 15) * 60
        self.max_retries = self.hop_config.get('max_retries', 3)
        self.selected_account = self.hop_config.get('account', None)
        self.last_hop_time = self.hop_config.get('last_hop_time', 0)
        self.retry_count = self.hop_config.get('retry_count', 0)
        self.hop_in_progress = self.hop_config.get('hop_in_progress', False)

    def should_hop(self):
        """Check if it's time to hop servers"""
        if not self.enabled or self.hop_in_progress:
            return False
        current_time = time.time()
        return current_time - self.last_hop_time >= self.interval

    def reset_hop_timer(self, chat_config, config):
        """Reset the hop timer to start counting from now"""
        current_time = time.time()
        self.last_hop_time = current_time
        self.hop_config['last_hop_time'] = current_time
        chat_config['server_hop'] = self.hop_config
        config['chat_spammer'] = chat_config
        save_config(config)
        print_centered(colorize(f' Server hop timer reset. Next hop in {self.interval // 60} minutes.', C.DIM))

    def perform_hop(self, place_id, chat_config, config, account_name, link_code=None):
        """Execute server hop by closing and relaunching Roblox"""
        if self.hop_in_progress:
            return (False, 'Hop already in progress')
        self.hop_in_progress = True
        try:
            print_centered(colorize(' Starting server hop...', C.CYAN))
            print_centered(colorize(' Closing Roblox...', C.ORANGE))
            self.close_roblox_processes()
            time.sleep(3)
            print_centered(colorize(' Relaunching Roblox...', C.GREEN))
            success = self.launch_roblox_for_hop(place_id, account_name, link_code)
            if not success:
                raise Exception('Failed to relaunch Roblox')
            print_centered(colorize(' Waiting for new server...', C.CYAN))
            time.sleep(8)
            self.last_hop_time = time.time()
            self.retry_count = 0
            self.hop_config['last_hop_time'] = self.last_hop_time
            self.hop_config['retry_count'] = self.retry_count
            self.hop_config['hop_in_progress'] = False
            chat_config['server_hop'] = self.hop_config
            config['chat_spammer'] = chat_config
            save_config(config)
            print_centered(colorize(' Server hop completed successfully!', C.GREEN))
            return (True, 'Server hop successful')
        except Exception as e:
            self.retry_count += 1
            error_msg = f'Server hop failed: {e}'
            if self.retry_count < self.max_retries:
                print_centered(colorize(f' {error_msg}', C.RED))
                print_centered(colorize(f' Retrying... ({self.retry_count}/{self.max_retries})', C.ORANGE))
                self.hop_config['retry_count'] = self.retry_count
                self.hop_config['hop_in_progress'] = False
                chat_config['server_hop'] = self.hop_config
                config['chat_spammer'] = chat_config
                save_config(config)
                time.sleep(10)
                return self.perform_hop(place_id, chat_config, config, account_name, link_code)
            else:
                print_centered(colorize(f' {error_msg}', C.RED))
                print_centered(colorize(' Max retries reached. Continuing with current server.', C.ORANGE))
                self.retry_count = 0
                self.hop_config['retry_count'] = 0
                self.hop_config['hop_in_progress'] = False
                chat_config['server_hop'] = self.hop_config
                config['chat_spammer'] = chat_config
                save_config(config)
                return (False, error_msg)
        finally:
            self.hop_in_progress = False

    def close_roblox_processes(self):
        """Close all Roblox processes"""
        try:
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] in ['RobloxPlayerBeta.exe', 'RobloxPlayer.exe']:
                    proc.kill()
                    print_centered(colorize(f'Closed Roblox process (PID: {proc.pid})', C.DIM))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    def launch_roblox_for_hop(self, place_id, account_name, link_code=None):
        """Launch Roblox for server hop using the same logic as initial launch"""
        try:
            accounts = load_roblox_accounts()
            if account_name not in accounts:
                raise Exception(f"Account '{account_name}' not found")
            account_cookie = accounts[account_name]
            if not account_cookie:
                raise Exception(f"No cookie found for account '{account_name}'")
            if link_code:
                print_centered(colorize('Using browser-based launch for private server hop...', C.CYAN))
                success = launch_private_server_browser(place_id, link_code, account_cookie, 'server_hop')
                return success
            auth_ticket = get_auth_ticket(clean_cookie(account_cookie))
            if not auth_ticket:
                raise Exception('Could not get auth ticket')
            browser_tracker_id = random.randint(100000000000, 999999999999)
            placelauncher_url = f'https%3A%2F%2Fassetgame.roblox.com%2Fgame%2FPlaceLauncher.ashx%3Frequest%3DRequestGame%26browserTrackerId%3D{browser_tracker_id}%26placeId%3D{place_id}%26isPlayTogetherGame%3Dfalse'
            launch_url = f'roblox-player:1+launchmode:play+gameinfo:{auth_ticket}+launchtime:{int(time.time() * 1000)}+placelauncherurl:{placelauncher_url}+browsertrackerid:{browser_tracker_id}+robloxLocale:en_us+gameLocale:en_us+channel:+LaunchExp:InApp'
            os.startfile(launch_url)
            return True
        except Exception as e:
            print_centered(colorize(f'Launch failed: {e}', C.RED))
            return False

    def get_next_hop_time(self):
        """Get formatted time until next hop"""
        if not self.enabled:
            return 'Disabled'
        current_time = time.time()
        time_until_hop = self.interval - (current_time - self.last_hop_time)
        if time_until_hop <= 0:
            return 'Ready to hop'
        minutes = int(time_until_hop // 60)
        seconds = int(time_until_hop % 60)
        return f'{minutes}m {seconds}s'

def auto_spammer_thread():
    """Background thread that sends messages every 10 minutes when enabled"""
    while True:
        try:
            time.sleep(600)
            config = load_config()
            chat_config = config.get('chat_spammer', {})
            should_run = chat_config.get('auto_spammer_enabled', True)
            if should_run and chat_config.get('messages', []):
                messages = chat_config['messages']
                import random
                selected_messages = random.sample(messages, min(2, len(messages)))
                log_event(' Auto spammer: Sending 2 messages...', 'INFO', 'system')
                for (i, message) in enumerate(selected_messages):
                    try:
                        if sys.platform == 'win32':
                            import win32gui
                            import keyboard

                            def find_roblox_window(hwnd, windows):
                                if win32gui.IsWindowVisible(hwnd):
                                    window_text = win32gui.GetWindowText(hwnd)
                                    class_name = win32gui.GetClassName(hwnd)
                                    if 'Roblox' in window_text and window_text != 'Roblox' or 'ROBLOXCORPORATION.ROBLOX' in class_name:
                                        windows.append(hwnd)
                                return True
                            roblox_windows = []
                            win32gui.EnumWindows(find_roblox_window, roblox_windows)
                            if roblox_windows:
                                hwnd = roblox_windows[0]
                                win32gui.SetForegroundWindow(hwnd)
                                time.sleep(0.5)
                                keyboard.press_and_release('/')
                                time.sleep(0.2)
                                keyboard.write(message)
                                time.sleep(0.2)
                                keyboard.press_and_release('enter')
                                log_event(f' Auto message {i + 1}/2 sent', 'SUCCESS', 'system')
                                if i < len(selected_messages) - 1:
                                    time.sleep(2)
                            else:
                                log_event(' No Roblox window found for auto spammer', 'WARN', 'system')
                                break
                    except Exception as e:
                        log_event(f' Auto spammer error: {e}', 'ERROR', 'system')
        except Exception as e:
            log_event(f' Auto spammer thread error: {e}', 'ERROR', 'system')
            time.sleep(60)

def debug_log_only(message, level='INFO'):
    """Add message to debug log only, without showing in main console"""
    global DEBUG_LOG
    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
    log_entry = f'[{timestamp}] [{level}] [AUTO-SPAMMER] {message}'
    DEBUG_LOG.append(log_entry)

def background_auto_spammer():
    """Background auto spammer - sends 2 messages immediately, then every 10 minutes, logs to debug only"""
    print('DEBUG: Background auto spammer function called!')
    debug_log_only('Background auto spammer thread started', 'INFO')
    print('DEBUG: Waiting 5 seconds before starting...')
    time.sleep(5)
    print('DEBUG: Starting main loop...')
    first_run = True
    while True:
        try:
            debug_log_only('Starting spam cycle...', 'INFO')
            config = load_config()
            chat_config = config.get('chat_spammer', {})
            messages = chat_config.get('messages', ['RejoinTool Session Manager! rejointool,xyz/hi', 'RejoinTool Auto Rejoin! rejointool,xyz/hi', 'RejoinTool Session Control! rejointool,xyz/hi', 'RejoinTool Session Tool! rejointool,xyz/hi', 'RejoinTool Game Manager! rejointool,xyz/hi'])
            if not messages:
                debug_log_only('No messages found, skipping cycle', 'WARN')
                time.sleep(600)
                continue
            selected_messages = random.sample(messages, min(2, len(messages)))
            debug_log_only(f'Selected 2 messages from {len(messages)} available', 'INFO')
            roblox_hwnd = get_roblox_hwnd()
            if roblox_hwnd and is_in_game(roblox_hwnd):
                debug_log_only('Roblox game detected (in-game) - sending messages...', 'INFO')
                for (i, message) in enumerate(selected_messages):
                    try:
                        success = send_chat_message(roblox_hwnd, message, f'Background-Auto')
                        if success:
                            debug_log_only(f'Message {i + 1}/2 sent: {message[:30]}...', 'SUCCESS')
                        else:
                            debug_log_only(f'Failed to send message {i + 1}/2', 'ERROR')
                        if i < len(selected_messages) - 1:
                            time.sleep(2)
                    except Exception as e:
                        debug_log_only(f'Exception sending message {i + 1}: {e}', 'ERROR')
                debug_log_only('Background spam cycle completed successfully', 'SUCCESS')
            else:
                debug_log_only('No Roblox game running - waiting for game to start...', 'WARN')
            if first_run:
                debug_log_only('First spam cycle completed! Next cycle in 10 minutes...', 'INFO')
                first_run = False
            else:
                debug_log_only('Waiting 10 minutes until next cycle...', 'INFO')
            time.sleep(600)
        except Exception as e:
            debug_log_only(f'Background auto spammer error: {e}', 'ERROR')
            time.sleep(60)

def emulator_background_auto_spammer(emulator_instances, adb_path):
    """Emulator background spammer"""
    debug_log_only('Emulator background auto spammer thread started', 'INFO')
    debug_log_only(f' Waiting {EMULATOR_SPAM_STARTUP_DELAY} seconds for emulators to fully load...', 'INFO')
    time.sleep(EMULATOR_SPAM_STARTUP_DELAY)
    first_run = True
    while True:
        try:
            debug_log_only('Starting emulator spam cycle...', 'INFO')
            config = load_config()
            chat_config = config.get('chat_spammer', {})
            messages = chat_config.get('messages', DEFAULT_SPAM_MESSAGES)
            if not messages:
                debug_log_only('No messages found, skipping emulator cycle', 'WARN')
                time.sleep(EMULATOR_SPAM_RETRY_DELAY)
                continue
            selected_messages = random.sample(messages, min(EMULATOR_SPAM_MESSAGE_COUNT, len(messages)))
            debug_log_only(f'Selected {len(selected_messages)} messages for emulator spam', 'INFO')
            active_emulators = []
            for emulator in emulator_instances:
                port = emulator.get('port')
                name = emulator.get('name', f'Port-{port}')
                try:
                    ps_result = run_adb_command(adb_path, port, ['ps'])
                    if ps_result and 'com.roblox.client' in ps_result.stdout:
                        active_emulators.append({'port': port, 'name': name})
                        debug_log_only(f'Roblox detected on {name} (port {port})', 'INFO')
                    else:
                        debug_log_only(f'No Roblox on {name} (port {port})', 'WARN')
                except Exception as e:
                    debug_log_only(f'Error checking {name}: {e}', 'ERROR')
            emulator_windows = []
            try:
                import win32gui

                def enum_callback(hwnd, windows):
                    try:
                        if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
                            window_text = win32gui.GetWindowText(hwnd)
                            class_name = win32gui.GetClassName(hwnd)
                            is_emulator_window = False
                            for emulator in emulator_instances:
                                emulator_name = emulator.get('name', '')
                                if emulator_name in window_text or any((keyword in window_text.lower() for keyword in ['mumu', 'ldplayer', 'bluestacks', 'nox'])):
                                    is_emulator_window = True
                                    break
                            if 'Roblox' in window_text and window_text != 'Roblox' or 'ROBLOXCORPORATION.ROBLOX' in class_name:
                                is_emulator_window = True
                            if is_emulator_window:
                                windows.append((hwnd, window_text or f'Emulator Window'))
                    except Exception:
                        pass
                    return True
                win32gui.EnumWindows(enum_callback, emulator_windows)
                debug_log_only(f'Found {len(emulator_windows)} potential emulator windows', 'INFO')
            except Exception as e:
                debug_log_only(f'Error finding emulator windows: {e}', 'ERROR')
            if emulator_windows:
                in_game_windows = []
                for (hwnd, window_title) in emulator_windows:
                    if is_in_game(hwnd):
                        in_game_windows.append((hwnd, window_title))
                if in_game_windows:
                    debug_log_only(f'Found {len(in_game_windows)} emulator window(s) in-game - sending messages...', 'INFO')
                    for (i, message) in enumerate(selected_messages):
                        for (hwnd, window_title) in in_game_windows:
                            try:
                                success = send_chat_message(hwnd, message, f'Emulator-{window_title[:20]}')
                                if success:
                                    debug_log_only(f'Message {i + 1}/{len(selected_messages)} sent to {window_title[:25]}...: {message[:30]}...', 'SUCCESS')
                                else:
                                    debug_log_only(f'Failed to send message {i + 1} to {window_title[:25]}...', 'ERROR')
                            except Exception as e:
                                debug_log_only(f'Exception sending to {window_title}: {e}', 'ERROR')
                    if i < len(selected_messages) - 1:
                        time.sleep(EMULATOR_SPAM_MESSAGE_DELAY)
                debug_log_only('Emulator spam cycle completed successfully', 'SUCCESS')
                if first_run:
                    debug_log_only('First emulator spam cycle completed! Next cycle in 10 minutes...', 'INFO')
                    first_run = False
                else:
                    debug_log_only('Waiting 10 minutes until next emulator cycle...', 'INFO')
                time.sleep(EMULATOR_SPAM_INTERVAL)
            else:
                debug_log_only('No active emulators with Roblox found - retrying in 30 seconds...', 'WARN')
                time.sleep(EMULATOR_SPAM_RETRY_DELAY)
        except Exception as e:
            debug_log_only(f'Emulator background spammer error: {e}', 'ERROR')
            time.sleep(EMULATOR_SPAM_RETRY_DELAY)

def manage_chat_spammer():
    """Chat Spammer configuration and management menu"""
    while True:
        config = load_config()
        chat_config = config.get('chat_spammer', {'messages': ['RejoinTool Session Manager! rejointool,xyz/hi', 'RejoinTool Auto Rejoin! rejointool,xyz/hi', 'RejoinTool Session Manager! rejointool,xyz/hi', 'RejoinTool Session Control! rejointool,xyz/hi', 'RejoinTool Session Tool! rejointool,xyz/hi', 'RejoinTool Game Manager! rejointool,xyz/hi'], 'interval': 30, 'message_count': 3, 'delay_between_messages': 2, 'server_hop': {'enabled': False, 'interval': 15, 'max_retries': 3, 'account': None, 'last_hop_time': 0, 'retry_count': 0, 'hop_in_progress': False}})
        draw_header('CHAT SPAMMER CONFIGURATION')
        print_centered(f"Messages: {len(chat_config['messages'])} configured")
        hop_config = chat_config.get('server_hop', {})
        hop_enabled = hop_config.get('enabled', False)
        hop_status_color = C.GREEN if hop_enabled else C.GREY
        hop_status_text = 'ENABLED' if hop_enabled else 'DISABLED'
        print_centered(f'Server Hopping: {colorize(hop_status_text, hop_status_color)}')
        if hop_enabled:
            hop_manager = ServerHopManager(chat_config)
            selected_account = hop_config.get('account', 'Current')
            print_centered(f"Hop Interval: {hop_config.get('interval', 15)} minutes")
            print_centered(f"Hop Account: {colorize(selected_account if selected_account else 'Current', C.CYAN)}")
            print_centered(f'Next Hop: {hop_manager.get_next_hop_time()}')
        print()
        options = ['Settings', 'Start Spammer', 'Back to Main Menu']
        choice = get_choice('Select an option', options)
        if choice == 1:
            chat_spammer_settings_menu(chat_config, config)
        elif choice == 2:
            start_manual_spam_session(chat_config)
        elif choice == 3:
            break

def chat_spammer_settings_menu(chat_config, config):
    """Chat spammer settings submenu"""
    while True:
        draw_header('CHAT SPAMMER SETTINGS')
        print_centered('Configure all chat spammer options:')
        print()
        options = ['Configure Messages', 'Configure Timing', 'Server Hop Settings', 'Test Chat Spammer', 'Back']
        choice = get_choice('Select an option', options)
        if choice == 1:
            configure_chat_messages(chat_config, config)
        elif choice == 2:
            configure_chat_timing(chat_config, config)
        elif choice == 3:
            configure_server_hop_settings(chat_config, config)
        elif choice == 4:
            test_chat_spammer(chat_config)
        elif choice == 5:
            break

def configure_chat_messages(chat_config, config):
    """Configure chat spammer messages"""
    while True:
        draw_header('CHAT MESSAGES CONFIGURATION')
        print_centered('Current Messages:')
        print()
        for (i, message) in enumerate(chat_config['messages'], 1):
            print(f"  {colorize(f'[{i}]', C.CYAN)} {message}")
        print()
        options = ['Add New Message', 'Edit Message', 'Delete Multiple Messages', 'Server Hop Settings', 'Reset to Default Messages', 'Back']
        choice = get_choice('Select an option', options)
        if choice == 1:
            new_message = get_input('Enter new message')
            if new_message.strip():
                chat_config['messages'].append(new_message.strip())
                config['chat_spammer'] = chat_config
                save_config(config)
                print_centered(colorize('Message added successfully.', C.GREEN))
                time.sleep(1)
            else:
                print_centered(colorize('Message cannot be empty.', C.RED))
                time.sleep(1)
        elif choice == 2:
            if not chat_config['messages']:
                print_centered(colorize('No messages to edit.', C.RED))
                time.sleep(1)
                continue
            try:
                msg_num = int(get_input('Enter message number to edit'))
                if 1 <= msg_num <= len(chat_config['messages']):
                    current_msg = chat_config['messages'][msg_num - 1]
                    print_centered(f'Current message: {current_msg}')
                    new_message = get_input('Enter new message (or press Enter to keep current)')
                    if new_message.strip():
                        chat_config['messages'][msg_num - 1] = new_message.strip()
                        config['chat_spammer'] = chat_config
                        save_config(config)
                        print_centered(colorize('Message updated successfully.', C.GREEN))
                        time.sleep(1)
                else:
                    print_centered(colorize('Invalid message number.', C.RED))
                    time.sleep(1)
            except ValueError:
                print_centered(colorize('Please enter a valid number.', C.RED))
                time.sleep(1)
        elif choice == 3:
            if not chat_config['messages']:
                print_centered(colorize('No messages to delete.', C.RED))
                time.sleep(1)
                continue
            delete_multiple_messages(chat_config, config)
        elif choice == 4:
            configure_server_hop_settings(chat_config, config)
        elif choice == 5:
            chat_config['messages'] = ['RejoinTool Session Manager! rejointool,xyz/hi', 'RejoinTool Auto Rejoin! rejointool,xyz/hi', 'RejoinTool Session Manager! rejointool,xyz/hi', 'RejoinTool Session Control! rejointool,xyz/hi', 'RejoinTool Session Tool! rejointool,xyz/hi', 'RejoinTool Game Manager! rejointool,xyz/hi']
            config['chat_spammer'] = chat_config
            save_config(config)
            print_centered(colorize('Messages reset to default.', C.GREEN))
            time.sleep(1)
        elif choice == 6:
            break

def configure_server_hop_settings(chat_config, config):
    """Configure server hopping settings"""
    while True:
        draw_header('SERVER HOP SETTINGS')
        hop_config = chat_config.get('server_hop', {})
        status_color = C.GREEN if hop_config.get('enabled', False) else C.RED
        status_text = 'ENABLED' if hop_config.get('enabled', False) else 'DISABLED'
        print_centered(f'Server Hopping: {colorize(status_text, status_color)}')
        print_centered(f"Hop Interval: {hop_config.get('interval', 15)} minutes")
        print_centered(f"Max Retries: {hop_config.get('max_retries', 3)}")
        selected_account = hop_config.get('account', None)
        if selected_account:
            print_centered(f'Selected Account: {colorize(selected_account, C.CYAN)}')
        else:
            print_centered(f"Selected Account: {colorize('None (use current)', C.GREY)}")
        print()
        options = [f"{('Disable' if hop_config.get('enabled', False) else 'Enable')} Server Hopping", 'Set Hop Interval', 'Set Max Retries', 'Select Account', 'Back']
        choice = get_choice('Select an option', options)
        if choice == 1:
            hop_config['enabled'] = not hop_config.get('enabled', False)
            chat_config['server_hop'] = hop_config
            config['chat_spammer'] = chat_config
            save_config(config)
            status = 'enabled' if hop_config['enabled'] else 'disabled'
            print_centered(colorize(f'Server hopping {status}.', C.GREEN))
            time.sleep(1)
        elif choice == 2:
            try:
                new_interval = int(get_input('Enter hop interval in minutes (5-60)'))
                if 5 <= new_interval <= 60:
                    hop_config['interval'] = new_interval
                    chat_config['server_hop'] = hop_config
                    config['chat_spammer'] = chat_config
                    save_config(config)
                    print_centered(colorize(f'Hop interval set to {new_interval} minutes.', C.GREEN))
                    time.sleep(1)
                else:
                    print_centered(colorize('Interval must be between 5 and 60 minutes.', C.RED))
                    time.sleep(1)
            except ValueError:
                print_centered(colorize('Please enter a valid number.', C.RED))
                time.sleep(1)
        elif choice == 3:
            try:
                new_retries = int(get_input('Enter max retries (1-5)'))
                if 1 <= new_retries <= 5:
                    hop_config['max_retries'] = new_retries
                    chat_config['server_hop'] = hop_config
                    config['chat_spammer'] = chat_config
                    save_config(config)
                    print_centered(colorize(f'Max retries set to {new_retries}.', C.GREEN))
                    time.sleep(1)
                else:
                    print_centered(colorize('Max retries must be between 1 and 5.', C.RED))
                    time.sleep(1)
            except ValueError:
                print_centered(colorize('Please enter a valid number.', C.RED))
                time.sleep(1)
        elif choice == 4:
            select_account_for_hopping(hop_config, chat_config, config)
        elif choice == 5:
            break

def select_account_for_hopping(hop_config, chat_config, config):
    """Select account for server hopping from account manager"""
    draw_header('SELECT ACCOUNT FOR SERVER HOPPING')
    try:
        accounts = load_roblox_accounts()
        if not accounts:
            print_centered(colorize('No accounts found in account manager.', C.RED))
            print_centered('Please add accounts first using the Roblox Account Manager.')
            time.sleep(2)
            return
        print_centered('Available Accounts:')
        print()
        account_list = list(accounts.keys())
        for (i, account_name) in enumerate(account_list, 1):
            print(f"  {colorize(f'[{i}]', C.CYAN)} {account_name}")
        print(f"  {colorize(f'[{len(account_list) + 1}]', C.GREY)} None (use current logged-in account)")
        print()
        try:
            choice = int(get_input('Select account number'))
            if 1 <= choice <= len(account_list):
                selected_account = account_list[choice - 1]
                hop_config['account'] = selected_account
                chat_config['server_hop'] = hop_config
                config['chat_spammer'] = chat_config
                save_config(config)
                print_centered(colorize(f'Selected account: {selected_account}', C.GREEN))
                time.sleep(1)
            elif choice == len(account_list) + 1:
                hop_config['account'] = None
                chat_config['server_hop'] = hop_config
                config['chat_spammer'] = chat_config
                save_config(config)
                print_centered(colorize('Will use current logged-in account.', C.GREEN))
                time.sleep(1)
            else:
                print_centered(colorize('Invalid selection.', C.RED))
                time.sleep(1)
        except ValueError:
            print_centered(colorize('Please enter a valid number.', C.RED))
            time.sleep(1)
    except Exception as e:
        print_centered(colorize(f'Error loading accounts: {e}', C.RED))
        time.sleep(2)

def delete_multiple_messages(chat_config, config):
    """Delete multiple messages at once"""
    while True:
        draw_header('DELETE MULTIPLE MESSAGES')
        if not chat_config['messages']:
            print_centered(colorize('No messages to delete.', C.RED))
            time.sleep(1)
            return
        print_centered('Current Messages:')
        print()
        for (i, message) in enumerate(chat_config['messages'], 1):
            print(f"  {colorize(f'[{i}]', C.CYAN)} {message}")
        print()
        print_centered(colorize('Enter message numbers to delete (comma-separated)', C.ORANGE))
        print_centered("Examples: '1,3,5' or '2,4' or 'all' to delete all messages")
        print()
        user_input = get_input("Enter message numbers to delete (or 'back' to return)")
        if user_input.lower() == 'back':
            break
        elif user_input.lower() == 'all':
            confirm = get_input(colorize('Are you sure you want to delete ALL messages? (y/n)', C.RED)).lower()
            if confirm == 'y':
                deleted_count = len(chat_config['messages'])
                chat_config['messages'] = []
                config['chat_spammer'] = chat_config
                save_config(config)
                print_centered(colorize(f'All {deleted_count} messages deleted successfully.', C.GREEN))
                time.sleep(2)
                break
            else:
                print_centered(colorize('Deletion cancelled.', C.ORANGE))
                time.sleep(1)
                continue
        else:
            try:
                numbers_str = user_input.replace(' ', '').split(',')
                numbers = []
                for num_str in numbers_str:
                    if num_str.strip():
                        num = int(num_str.strip())
                        if 1 <= num <= len(chat_config['messages']):
                            numbers.append(num)
                        else:
                            print_centered(colorize(f'Invalid message number: {num}', C.RED))
                            time.sleep(1)
                            break
                else:
                    if numbers:
                        numbers = sorted(list(set(numbers)), reverse=True)
                        print_centered('Messages to be deleted:')
                        deleted_messages = []
                        for num in sorted(numbers):
                            message = chat_config['messages'][num - 1]
                            deleted_messages.append(message)
                            print(f"  {colorize(f'[{num}]', C.RED)} {message}")
                        print()
                        confirm = get_input(f'Delete {len(numbers)} message(s)? (y/n)').lower()
                        if confirm == 'y':
                            for num in numbers:
                                chat_config['messages'].pop(num - 1)
                            config['chat_spammer'] = chat_config
                            save_config(config)
                            print_centered(colorize(f'Successfully deleted {len(numbers)} message(s).', C.GREEN))
                            time.sleep(2)
                            if not chat_config['messages']:
                                break
                        else:
                            print_centered(colorize('Deletion cancelled.', C.ORANGE))
                            time.sleep(1)
                    else:
                        print_centered(colorize('No valid message numbers provided.', C.RED))
                        time.sleep(1)
            except ValueError:
                print_centered(colorize('Invalid input. Please enter numbers separated by commas.', C.RED))
                time.sleep(1)

def configure_chat_timing(chat_config, config):
    """Configure chat spammer timing settings"""
    while True:
        draw_header('CHAT TIMING CONFIGURATION')
        print_centered(f'Current Settings:')
        print_centered(f"Spam Interval: {chat_config['interval']} seconds")
        print_centered(f"Messages per spam: {chat_config['message_count']}")
        print_centered(f"Delay between messages: {chat_config['delay_between_messages']} seconds")
        print()
        options = ['Change Spam Interval', 'Change Messages per Spam', 'Change Delay Between Messages', 'Back']
        choice = get_choice('Select an option', options)
        if choice == 1:
            draw_header('SELECT SPAM INTERVAL')
            print_centered('Choose a preset interval or enter custom:')
            print()
            interval_options = ['30 seconds', '1 minute (60 seconds)', '2 minutes (120 seconds)', '5 minutes (300 seconds)', '10 minutes (600 seconds)', '15 minutes (900 seconds)', '30 minutes (1800 seconds)', '1 hour (3600 seconds)', '2 hours (7200 seconds)', 'Custom interval']
            interval_choice = get_choice('Select interval', interval_options)
            if interval_choice == 1:
                new_interval = 30
            elif interval_choice == 2:
                new_interval = 60
            elif interval_choice == 3:
                new_interval = 120
            elif interval_choice == 4:
                new_interval = 300
            elif interval_choice == 5:
                new_interval = 600
            elif interval_choice == 6:
                new_interval = 900
            elif interval_choice == 7:
                new_interval = 1800
            elif interval_choice == 8:
                new_interval = 3600
            elif interval_choice == 9:
                new_interval = 7200
            elif interval_choice == 10:
                try:
                    new_interval = int(get_input('Enter custom interval in seconds (10-7200)'))
                    if not 10 <= new_interval <= 7200:
                        print_centered(colorize('Interval must be between 10 seconds and 2 hours (7200 seconds).', C.RED))
                        time.sleep(2)
                        continue
                except ValueError:
                    print_centered(colorize('Please enter a valid number.', C.RED))
                    time.sleep(1)
                    continue
            else:
                continue
            chat_config['interval'] = new_interval
            config['chat_spammer'] = chat_config
            save_config(config)
            if new_interval < 60:
                time_str = f'{new_interval} seconds'
            elif new_interval < 3600:
                minutes = new_interval // 60
                time_str = f"{minutes} minute{('s' if minutes != 1 else '')}"
            else:
                hours = new_interval // 3600
                remaining_minutes = new_interval % 3600 // 60
                if remaining_minutes > 0:
                    time_str = f"{hours} hour{('s' if hours != 1 else '')} {remaining_minutes} minute{('s' if remaining_minutes != 1 else '')}"
                else:
                    time_str = f"{hours} hour{('s' if hours != 1 else '')}"
            print_centered(colorize(f'Spam interval set to {time_str}.', C.GREEN))
            time.sleep(2)
        elif choice == 2:
            try:
                new_count = int(get_input('Enter messages per spam (1-10)'))
                if 1 <= new_count <= 10:
                    chat_config['message_count'] = new_count
                    config['chat_spammer'] = chat_config
                    save_config(config)
                    print_centered(colorize(f'Messages per spam set to {new_count}.', C.GREEN))
                    time.sleep(1)
                else:
                    print_centered(colorize('Message count must be between 1 and 10.', C.RED))
                    time.sleep(1)
            except ValueError:
                print_centered(colorize('Please enter a valid number.', C.RED))
                time.sleep(1)
        elif choice == 3:
            try:
                new_delay = float(get_input('Enter delay between messages in seconds (0.5-10)'))
                if 0.5 <= new_delay <= 10:
                    chat_config['delay_between_messages'] = new_delay
                    config['chat_spammer'] = chat_config
                    save_config(config)
                    print_centered(colorize(f'Delay between messages set to {new_delay} seconds.', C.GREEN))
                    time.sleep(1)
                else:
                    print_centered(colorize('Delay must be between 0.5 and 10 seconds.', C.RED))
                    time.sleep(1)
            except ValueError:
                print_centered(colorize('Please enter a valid number.', C.RED))
                time.sleep(1)
        elif choice == 4:
            break

def test_chat_spammer(chat_config):
    """Test the chat spammer functionality"""
    draw_header('CHAT SPAMMER TEST')
    if not chat_config['messages']:
        print_centered(colorize('No messages configured. Please add messages first.', C.RED))
        time.sleep(2)
        return
    print_centered('This will test the chat spammer by sending messages to the active Roblox window.')
    print_centered(colorize("Make sure Roblox is open and you're in a game!", C.ORANGE))
    print_centered('The test will send 1 message only.')
    print()
    confirm = get_input('Continue with test? (y/n)').lower()
    if confirm != 'y':
        return
    roblox_hwnd = get_roblox_hwnd()
    if not roblox_hwnd:
        print_centered(colorize('Roblox window not found. Please open Roblox first.', C.RED))
        time.sleep(2)
        return
    print_centered(colorize('Sending test message in 3 seconds...', C.CYAN))
    time.sleep(3)
    message = random.choice(chat_config['messages'])
    success = send_chat_message(roblox_hwnd, message, 'Test')
    if success:
        print_centered(colorize('Test completed successfully!', C.GREEN))
    else:
        print_centered(colorize('Test failed - check the error message above.', C.RED))
    time.sleep(2)

def select_game_for_spam_session():
    """Select game/place ID for spam session using existing GAMES_DB"""
    draw_header('SELECT GAME FOR SPAM SESSION')
    print_centered('Choose a game to spam:')
    print()
    game_list = list(GAMES_DB.keys())
    options = []
    for (i, game_name) in enumerate(game_list, 1):
        place_id = GAMES_DB[game_name]
        options.append(f'{game_name} (ID: {place_id})')
        print(f"  {colorize(f'[{i}]', C.CYAN)} {game_name} {colorize(f'(ID: {place_id})', C.GREY)}")
    print(f"  {colorize(f'[{len(game_list) + 1}]', C.ORANGE)} Enter Custom Place ID")
    print(f"  {colorize(f'[{len(game_list) + 2}]', C.GREY)} Back")
    print()
    try:
        choice = int(get_input('Select game'))
        if 1 <= choice <= len(game_list):
            selected_game = game_list[choice - 1]
            place_id = GAMES_DB[selected_game]
            print_centered(colorize(f'Selected: {selected_game} (ID: {place_id})', C.GREEN))
            time.sleep(1)
            return place_id
        elif choice == len(game_list) + 1:
            try:
                custom_id = int(get_input('Enter Custom Roblox Place ID'))
                print_centered(colorize(f'Custom Place ID: {custom_id}', C.GREEN))
                time.sleep(1)
                return custom_id
            except ValueError:
                print_centered(colorize('Invalid Place ID. Please enter numbers only.', C.RED))
                time.sleep(2)
                return None
        elif choice == len(game_list) + 2:
            return None
        else:
            print_centered(colorize('Invalid selection.', C.RED))
            time.sleep(1)
            return None
    except ValueError:
        print_centered(colorize('Invalid selection.', C.RED))
        time.sleep(1)
        return None

def launch_roblox_for_spam_session(place_id, account_name):
    """Launch Roblox for spam session using account manager integration with selenium fallback"""
    try:
        accounts = load_roblox_accounts()
        if account_name not in accounts:
            print_centered(colorize(f"Account '{account_name}' not found.", C.RED))
            return False
        account_cookie = accounts[account_name]
        if not account_cookie:
            print_centered(colorize(f"No cookie found for account '{account_name}'.", C.RED))
            return False
        print_centered(colorize(' Getting authentication ticket...', C.CYAN))
        auth_ticket = get_auth_ticket(clean_cookie(account_cookie))
        if not auth_ticket:
            print_centered(colorize(' Auth ticket failed. Trying browser-based authentication...', C.ORANGE))
            return selenium_auth_fix_for_spam(account_cookie, place_id, account_name)
        browser_tracker_id = random.randint(100000000000, 999999999999)
        placelauncher_url = f'https%3A%2F%2Fassetgame.roblox.com%2Fgame%2FPlaceLauncher.ashx%3Frequest%3DRequestGame%26browserTrackerId%3D{browser_tracker_id}%26placeId%3D{place_id}%26isPlayTogetherGame%3Dfalse'
        launch_url = f'roblox-player:1+launchmode:play+gameinfo:{auth_ticket}+launchtime:{int(time.time() * 1000)}+placelauncherurl:{placelauncher_url}+browsertrackerid:{browser_tracker_id}+robloxLocale:en_us+gameLocale:en_us+channel:+LaunchExp:InApp'
        print_centered(colorize(' Launching Roblox...', C.GREEN))
        os.startfile(launch_url)
        print_centered(colorize(' Roblox launch command sent!', C.GREEN))
        return True
    except Exception as e:
        print_centered(colorize(f' Launch failed: {e}', C.RED))
        return False

def launch_roblox_for_spam_session(place_id, account_name):
    """Launch Roblox for spam session using account manager integration with selenium fallback"""
    try:
        accounts = load_roblox_accounts()
        if account_name not in accounts:
            print_centered(colorize(f"Account '{account_name}' not found.", C.RED))
            return False
        account_cookie = accounts[account_name]
        if not account_cookie:
            print_centered(colorize(f"No cookie found for account '{account_name}'.", C.RED))
            return False
        print_centered(colorize(' Getting authentication ticket...', C.CYAN))
        auth_ticket = get_auth_ticket(clean_cookie(account_cookie))
        if not auth_ticket:
            print_centered(colorize(' Auth ticket failed. Trying browser-based authentication...', C.ORANGE))
            return selenium_auth_fix_for_spam(account_cookie, place_id, account_name)
        browser_tracker_id = random.randint(100000000000, 999999999999)
        placelauncher_url = f'https%3A%2F%2Fassetgame.roblox.com%2Fgame%2FPlaceLauncher.ashx%3Frequest%3DRequestGame%26browserTrackerId%3D{browser_tracker_id}%26placeId%3D{place_id}%26isPlayTogetherGame%3Dfalse'
        launch_url = f'roblox-player:1+launchmode:play+gameinfo:{auth_ticket}+launchtime:{int(time.time() * 1000)}+placelauncherurl:{placelauncher_url}+browsertrackerid:{browser_tracker_id}+robloxLocale:en_us+gameLocale:en_us+channel:+LaunchExp:InApp'
        print_centered(colorize(' Launching Roblox...', C.GREEN))
        os.startfile(launch_url)
        print_centered(colorize(' Roblox launch command sent!', C.GREEN))
        return True
    except Exception as e:
        print_centered(colorize(f' Launch failed: {e}', C.RED))
        return False

def selenium_auth_fix_for_spam(cookie, place_id, account_name):
    """Browser auth fix for spammer"""
    driver = None
    try:
        print_centered(colorize(' Starting browser-based authentication fix...', C.CYAN))
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(f'user-data-dir={CHROME_PROFILE_PATH}')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-logging')
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_argument('--window-size=1000,700')
        chrome_options.add_argument('--disable-features=ExternalProtocolPrompt')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        prefs = {'protocol_handler.excluded_schemes': {'roblox-player': False, 'roblox': False}}
        chrome_options.add_experimental_option('prefs', prefs)
        service = ChromeService(ChromeDriverManager().install())
        service.creation_flags = subprocess.CREATE_NO_WINDOW
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(20)
        print_centered(colorize(' Setting up authentication...', C.CYAN))
        driver.get('https://www.roblox.com')
        time.sleep(2)
        driver.delete_all_cookies()
        clean_cookie_value = clean_cookie(cookie)
        cookie_dict = {'name': '.ROBLOSECURITY', 'value': clean_cookie_value, 'domain': '.roblox.com'}
        try:
            driver.add_cookie(cookie_dict)
            print_centered(colorize(' Account cookie injected successfully.', C.GREEN))
        except Exception as e:
            print_centered(colorize(f' Cookie injection failed: {e}', C.RED))
            return False
        print_centered(colorize(' Verifying account login...', C.CYAN))
        driver.get('https://www.roblox.com/home')
        time.sleep(5)
        current_url = driver.current_url.lower()
        print_centered(colorize(f'Current URL after login attempt: {current_url}', C.DIM))
        if 'login' in current_url:
            print_centered(colorize(' Still on login page - cookie may be invalid/expired', C.RED))
            try:
                page_title = driver.title
                print_centered(colorize(f'Page title: {page_title}', C.DIM))
                error_elements = driver.find_elements(By.XPATH, "//*[contains(@class, 'alert') or contains(@class, 'error') or contains(@class, 'message')]")
                for elem in error_elements:
                    if elem.is_displayed() and elem.text.strip():
                        print_centered(colorize(f'Found message: {elem.text[:100]}...', C.ORANGE))
            except Exception:
                pass
            print_centered(colorize('Trying alt method...', C.ORANGE))
            driver.delete_all_cookies()
            driver.execute_script(f"\n                document.cookie = '.ROBLOSECURITY={clean_cookie_value}; domain=.roblox.com; path=/';\n            ")
            time.sleep(2)
            driver.refresh()
            time.sleep(3)
            current_url_2 = driver.current_url.lower()
            if 'login' in current_url_2:
                print_centered(colorize(' Cookie appears to be invalid or expired for this account', C.RED))
                print_centered(colorize('This account may need to be re-authenticated manually', C.ORANGE))
                return False
            else:
                print_centered(colorize(' Alternative method worked!', C.GREEN))
        try:
            logged_in_indicators = ["//div[contains(@class, 'navbar-right')]//a[contains(@href, '/users/')]", "//span[contains(@class, 'text-nav')]", "//div[contains(@class, 'navbar-right')]//li[contains(@class, 'navbar-icon-item')]", "//a[contains(@href, '/my/avatar')]", "//div[contains(@class, 'navbar-right')]//span[contains(@class, 'icon-robux')]"]
            logged_in = False
            for indicator in logged_in_indicators:
                try:
                    element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, indicator)))
                    if element:
                        logged_in = True
                        print_centered(colorize(f' Login confirmed via element: {indicator[:50]}...', C.GREEN))
                        break
                except:
                    continue
            if not logged_in:
                try:
                    page_source = driver.page_source.lower()
                    if 'logout' in page_source or 'robux' in page_source:
                        logged_in = True
                        print_centered(colorize(' Login confirmed via page content', C.GREEN))
                except:
                    pass
            if not logged_in:
                print_centered(colorize(' Could not confirm login - cookie may be invalid', C.RED))
                return False
        except Exception as e:
            print_centered(colorize(f' Error during login verification: {e}', C.ORANGE))
        auth_fix_place_id = 82818809
        game_url = f'https://www.roblox.com/games/{auth_fix_place_id}'
        print_centered(colorize(f'Opening game {auth_fix_place_id}...', C.CYAN))
        driver.get(game_url)
        time.sleep(3)
        print_centered(colorize('Finding play button...', C.CYAN))
        play_button_found = False
        play_selectors = ["//button[contains(@class, 'btn-full-width')]", "//button[contains(@class, 'btn-primary-xl')]", "//button[contains(@class, 'btn-primary-md')]", "//button[contains(@class, 'play-button')]", "//button[contains(@data-testid, 'play-button')]", "//button[contains(@class, 'game-launch-button')]", "//div[contains(@class, 'game-play-button')]//button", "//button[contains(@class, 'btn') and contains(@class, 'primary')]", "//a[contains(@class, 'btn-full-width')]", "//button[@id='game-start-button']", "//button[.//span[contains(@class, 'icon-play')]]", "//button[contains(@class, 'roblox-button')]"]
        for selector in play_selectors:
            try:
                play_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, selector)))
                button_text = play_button.text.lower()
                button_class = play_button.get_attribute('class').lower()
                print_centered(colorize(f"Found button: '{button_text}' with class: '{button_class[:50]}...'", C.DIM))
                driver.execute_script('arguments[0].scrollIntoView(true);', play_button)
                time.sleep(1)
                driver.execute_script('arguments[0].click();', play_button)
                print_centered(colorize('Clicked play', C.GREEN))
                play_button_found = True
                break
            except (TimeoutException, Exception) as e:
                continue
        if not play_button_found:
            print_centered(colorize('Searching for button...', C.ORANGE))
            try:
                all_buttons = driver.find_elements(By.TAG_NAME, 'button')
                for button in all_buttons:
                    try:
                        if button.is_displayed() and button.is_enabled():
                            button_text = button.text.lower()
                            button_class = button.get_attribute('class').lower()
                            print_centered(colorize(f"Found button: '{button_text}' | Class: '{button_class[:30]}...'", C.DIM))
                            if any((keyword in button_class for keyword in ['primary', 'play', 'game', 'launch', 'btn-full'])):
                                driver.execute_script('arguments[0].scrollIntoView(true);', button)
                                time.sleep(1)
                                driver.execute_script('arguments[0].click();', button)
                                print_centered(colorize(f" Clicked button: '{button_text}'", C.GREEN))
                                play_button_found = True
                                break
                    except Exception:
                        continue
            except Exception:
                pass
        if not play_button_found:
            print_centered(colorize('Using protocol launch...', C.ORANGE))
            driver.get(f'roblox://placeId={auth_fix_place_id}')
        print_centered(colorize(' Waiting for Roblox to launch (authentication fix)...', C.CYAN))
        roblox_launched = False
        for attempt in range(25):
            try:
                if sys.platform == 'win32':
                    import win32gui

                    def find_roblox_windows(hwnd, windows):
                        if win32gui.IsWindowVisible(hwnd):
                            window_text = win32gui.GetWindowText(hwnd)
                            class_name = win32gui.GetClassName(hwnd)
                            if 'Roblox' in window_text and window_text != 'Roblox' or 'ROBLOXCORPORATION.ROBLOX' in class_name or window_text.startswith('Roblox -'):
                                windows.append((hwnd, window_text))
                        return True
                    roblox_windows = []
                    win32gui.EnumWindows(find_roblox_windows, roblox_windows)
                    if roblox_windows:
                        print_centered(colorize(f' Roblox launched! Found {len(roblox_windows)} window(s).', C.GREEN))
                        roblox_launched = True
                        print_centered(colorize('Loading game...', C.CYAN))
                        time.sleep(8)
                        print_centered(colorize(' Closing Roblox (authentication complete)...', C.ORANGE))
                        for (hwnd, title) in roblox_windows:
                            win32gui.PostMessage(hwnd, 16, 0, 0)
                        time.sleep(2)
                        break
            except Exception as e:
                pass
            time.sleep(1)
            if attempt % 5 == 0 and attempt > 0:
                print_centered(colorize(f'Waiting... ({attempt}/25)', C.DIM))
        if not roblox_launched:
            print_centered(colorize(" Roblox didn't launch within timeout, but authentication may have worked", C.ORANGE))
        print_centered(colorize(' Now launching target game...', C.GREEN))
        time.sleep(3)
        target_game_url = f'https://www.roblox.com/games/{place_id}'
        driver.get(target_game_url)
        time.sleep(5)
        current_url = driver.current_url
        print_centered(colorize(f'Current URL: {current_url[:80]}...', C.DIM))
        if 'login' in current_url.lower():
            print_centered(colorize(' Got redirected to login page. Re-injecting cookie...', C.ORANGE))
            driver.delete_all_cookies()
            cookie_dict = {'name': '.ROBLOSECURITY', 'value': clean_cookie(cookie), 'domain': '.roblox.com'}
            driver.add_cookie(cookie_dict)
            driver.get(target_game_url)
            time.sleep(3)
        print_centered(colorize(' Looking for play button on target game...', C.CYAN))
        target_play_found = False
        for selector in play_selectors:
            try:
                play_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, selector)))
                button_text = play_button.text.lower()
                button_class = play_button.get_attribute('class').lower()
                print_centered(colorize(f"Found target button: '{button_text}' with class: '{button_class[:50]}...'", C.DIM))
                driver.execute_script('arguments[0].scrollIntoView(true);', play_button)
                time.sleep(1)
                driver.execute_script('arguments[0].click();', play_button)
                print_centered(colorize(' Target game launch initiated!', C.GREEN))
                target_play_found = True
                break
            except (TimeoutException, Exception):
                continue
        if not target_play_found:
            print_centered(colorize(' Could not find play button on target game, but authentication should be fixed', C.ORANGE))
        time.sleep(8)
        print_centered(colorize(' Authentication fix completed successfully!', C.GREEN))
        return True
    except Exception as e:
        print_centered(colorize(f' Browser authentication fix failed: {str(e)[:100]}...', C.RED))
        return False
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass
        print_centered(colorize(' Browser authentication process completed', C.DIM))

def start_manual_spam_session(chat_config):
    """Start a manual chat spam session with optional server hopping"""
    draw_header('MANUAL SPAM SESSION')
    if not chat_config['messages']:
        print_centered(colorize('No messages configured. Please add messages first.', C.RED))
        time.sleep(2)
        return
    place_id = select_game_for_spam_session()
    if not place_id:
        return
    selected_account = None
    hop_manager = ServerHopManager(chat_config)
    config = load_config()
    if 'link_code' not in chat_config:
        chat_config['link_code'] = None
    if hop_manager.enabled:
        hop_manager.reset_hop_timer(chat_config, config)
    if hop_manager.enabled:
        selected_account = hop_manager.selected_account
    if not selected_account:
        accounts = load_roblox_accounts()
        if not accounts:
            print_centered(colorize('No accounts found. Please add accounts first using the Account Manager.', C.RED))
            time.sleep(2)
            return
        print_centered('Select account to launch Roblox:')
        print()
        account_list = list(accounts.keys())
        for (i, account_name) in enumerate(account_list, 1):
            print(f"  {colorize(f'[{i}]', C.CYAN)} {account_name}")
        print()
        try:
            choice = int(get_input('Select account number'))
            if 1 <= choice <= len(account_list):
                selected_account = account_list[choice - 1]
            else:
                print_centered(colorize('Invalid selection.', C.RED))
                time.sleep(1)
                return
        except ValueError:
            print_centered(colorize('Invalid selection.', C.RED))
            time.sleep(1)
            return
    print_centered(colorize(' Launching Roblox...', C.GREEN))
    success = launch_roblox_for_spam_session(place_id, selected_account)
    if not success:
        print_centered(colorize('Failed to launch Roblox. Please check your account settings.', C.RED))
        time.sleep(2)
        return
    print_centered(colorize(' Waiting for Roblox to start...', C.ORANGE))
    time.sleep(10)
    roblox_hwnd = get_roblox_hwnd()
    if not roblox_hwnd:
        print_centered(colorize(' Could not find Roblox window. Waiting a bit longer...', C.ORANGE))
        time.sleep(10)
        roblox_hwnd = get_roblox_hwnd()
        if not roblox_hwnd:
            print_centered(colorize(' Roblox window not found. Please check if Roblox launched correctly.', C.RED))
            time.sleep(2)
            return
    config = load_config()
    print_centered(colorize(' Roblox found! Starting spam session...', C.GREEN))
    print_centered('Manual spam session will start in 5 seconds.')
    print_centered(colorize('Press Ctrl+C to stop the session.', C.ORANGE))
    print_centered(f"Messages will be sent every {chat_config['interval']} seconds.")
    if hop_manager.enabled:
        print_centered(colorize(f" Server hopping enabled: every {chat_config['server_hop']['interval']} minutes", C.MAGENTA))
        print_centered(f'Next hop: {hop_manager.get_next_hop_time()}')
    print()
    confirm = get_input('Start manual spam session? (y/n)').lower()
    if confirm != 'y':
        return
    print_centered(colorize('Starting spam session...', C.GREEN))
    time.sleep(5)
    spam_count = 0
    try:
        while True:
            if hop_manager.enabled and place_id and hop_manager.should_hop():
                print_centered(colorize(' Time to hop servers!', C.MAGENTA))
                link_code = chat_config.get('link_code', None)
                (success, message) = hop_manager.perform_hop(place_id, chat_config, config, selected_account, link_code)
                if success:
                    time.sleep(2)
                    new_hwnd = get_roblox_hwnd()
                    if new_hwnd:
                        roblox_hwnd = new_hwnd
                        print_centered(colorize(' Resuming spam session in new server...', C.GREEN))
                    else:
                        print_centered(colorize(' Could not find Roblox window after hop. Continuing with current window.', C.ORANGE))
                else:
                    print_centered(colorize(f' Server hop failed: {message}', C.ORANGE))
                    print_centered(colorize('Continuing spam session in current server...', C.CYAN))
            spam_count += 1
            status_line = f'Spam cycle #{spam_count}'
            if hop_manager.enabled and place_id:
                status_line += f' | Next hop: {hop_manager.get_next_hop_time()}'
            print_centered(colorize(status_line, C.CYAN))
            for i in range(chat_config['message_count']):
                if chat_config['messages']:
                    message = random.choice(chat_config['messages'])
                    send_chat_message(roblox_hwnd, message, f'Manual-{spam_count}')
                    if i < chat_config['message_count'] - 1:
                        time.sleep(chat_config['delay_between_messages'])
            print_centered(colorize(f"Waiting {chat_config['interval']} seconds until next spam...", C.DIM))
            time.sleep(chat_config['interval'])
    except KeyboardInterrupt:
        print_centered(colorize('\nSpam session stopped by user.', C.ORANGE))
        time.sleep(2)
    except Exception as e:
        print_centered(colorize(f'Spam session error: {e}', C.RED))
        time.sleep(2)

def send_chat_message(target_hwnd, message, session_name):
    """Send a single chat message to the target window using the proven lite.py method"""
    try:
        if not win32gui.IsWindow(target_hwnd):
            print_centered(colorize(f'Window handle for {session_name} is no longer valid.', C.ORANGE))
            return False
        if not (win32gui.IsWindowVisible(target_hwnd) and win32gui.IsWindowEnabled(target_hwnd)):
            print_centered(colorize(f'Window for {session_name} is not visible or enabled.', C.ORANGE))
            return False
        win32gui.SetForegroundWindow(target_hwnd)
        time.sleep(0.2)
        current_window = win32gui.GetForegroundWindow()
        if current_window != target_hwnd:
            print_centered(colorize(f'Failed to bring {session_name} to foreground.', C.ORANGE))
            return False
        keyboard.press_and_release('/')
        time.sleep(0.5)
        time.sleep(5.0)
        keyboard.write(message)
        time.sleep(1.0)
        keyboard.press_and_release('enter')
        print_centered(colorize(f"Message sent to {session_name}: {message[:50]}{('...' if len(message) > 50 else '')}", C.GREEN))
        return True
    except Exception as e:
        print_centered(colorize(f'Failed to send message to {session_name}: {e}', C.RED))
        return False

def Focus_window(hwnd):
    """Window focuser"""
    try:
        try:
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            if win32gui.GetForegroundWindow() == hwnd:
                return True
        except:
            pass
        try:
            win32gui.ShowWindow(hwnd, 9)
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            if win32gui.GetForegroundWindow() == hwnd:
                return True
        except:
            pass
        try:
            win32gui.BringWindowToTop(hwnd)
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            if win32gui.GetForegroundWindow() == hwnd:
                return True
        except:
            pass
        try:
            import win32process
            current_thread = win32api.GetCurrentThreadId()
            (target_thread, _) = win32process.GetWindowThreadProcessId(hwnd)
            if current_thread != target_thread:
                win32process.AttachThreadInput(current_thread, target_thread, True)
                try:
                    win32gui.SetForegroundWindow(hwnd)
                    time.sleep(0.1)
                    success = win32gui.GetForegroundWindow() == hwnd
                finally:
                    win32process.AttachThreadInput(current_thread, target_thread, False)
                if success:
                    return True
        except:
            pass
        try:
            window_title = win32gui.GetWindowText(hwnd)
            if window_title:
                keyboard.press('alt')
                keyboard.press_and_release('tab')
                time.sleep(0.1)
                keyboard.release('alt')
                time.sleep(0.2)
                if win32gui.GetForegroundWindow() == hwnd:
                    return True
        except:
            pass
        return False
    except Exception:
        return False

def get_roblox_hwnd():
    """Find the Roblox window handle"""
    try:
        roblox_pid = None
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == 'RobloxPlayerBeta.exe':
                roblox_pid = proc.info['pid']
                break
        if not roblox_pid:
            return None

        def callback(hwnd, hwnds):
            if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
                (_, found_pid) = win32process.GetWindowThreadProcessId(hwnd)
                if found_pid == roblox_pid:
                    hwnds.append(hwnd)
            return True
        hwnds = []
        win32gui.EnumWindows(callback, hwnds)
        return hwnds[0] if hwnds else None
    except Exception:
        return None

def is_in_game(roblox_hwnd):
    """Check if the user is actually in a game (not in main menu/lobby)"""
    try:
        if not roblox_hwnd or not win32gui.IsWindow(roblox_hwnd):
            return False
        window_title = win32gui.GetWindowText(roblox_hwnd)
        if not window_title or window_title.strip() == '' or window_title.strip().lower() == 'roblox':
            debug_log_only('User appears to be in main menu/lobby - skipping spam', 'WARN')
            return False
        if len(window_title.strip()) > 6:
            debug_log_only(f'User appears to be in game: {window_title[:30]}...', 'INFO')
            return True
        debug_log_only('Cannot determine if user is in game - skipping spam for safety', 'WARN')
        return False
    except Exception as e:
        debug_log_only(f'Error checking game state: {e}', 'ERROR')
        return False

def main():
    if not acquire_singleton_mutex():
        input('\nPress Enter to exit.')
        return
    while True:
        config = load_config()
        apply_theme(config)
        last_profile_name = config.get('last_used_profile')
        profiles = config.get('profiles', {})
        draw_header('RejoinTool')
        main_options = []
        main_options.append(colorize('Monitor All Dashboard', C.ORANGE + C.BOLD))
        if last_profile_name and last_profile_name in profiles:
            mode = profiles[last_profile_name].get('mode', 'N/A').capitalize()
            main_options.append(f"Launch Last ('{last_profile_name}' - {mode})")
        main_options.append(colorize('Roblox Account Manager', C.YELLOW))
        main_options.extend(['Manage Profiles', 'Settings', 'About', 'Exit'])
        CREDIT_TEXT = colorize('Made by Isaac, also known as Kirsh', C.DIM + C.CYAN)
        print()
        print_centered(CREDIT_TEXT)
        choice = get_choice('Select an option', main_options)
        if not choice:
            continue
        option_map = []
        option_map.append('monitor_all')
        if last_profile_name and last_profile_name in profiles:
            option_map.append('launch_last')
        option_map.append('account_manager')
        option_map.append('manage')
        option_map.append('settings')
        option_map.append('about')
        option_map.append('exit')
        action = option_map[choice - 1] if choice <= len(option_map) else None
        if action == 'monitor_all':
            launch_monitor_all_dashboard()
        elif action == 'launch_last':
            profile_data = profiles[last_profile_name]
            if not confirm_launch_with_warning():
                continue
            manage_profiles_launch_logic(profile_data, last_profile_name)
        elif action == 'account_manager':
            manage_roblox_accounts()
        elif action == 'manage':
            manage_profiles()
        elif action == 'settings':
            show_settings_menu()
        elif action == 'about':
            show_about_section()
        elif action == 'exit':
            break
    os.system('cls' if os.name == 'nt' else 'clear')
    print_centered(colorize('\nGoodbye!', C.BOLD + C.CYAN))

def manage_profiles_launch_logic(profile_data, profile_to_launch_name):
    config = load_config()
    if profile_data.get('mode') == 'desktop':
        associated_accounts = profile_data.get('accounts', [])
        if not associated_accounts:
            print_centered(colorize(f"Profile '{profile_to_launch_name}' has no accounts associated.", C.RED))
            time.sleep(3)
            return
        all_saved_accounts = load_roblox_accounts()
        profiles_to_run = []
        for acc_name in associated_accounts:
            if acc_name not in all_saved_accounts:
                log_event(f"Account '{acc_name}' in profile is no longer saved. Skipping.", 'WARN', 'system')
                continue
            launch_profile = profile_data.copy()
            launch_profile['profile_name'] = f'{profile_to_launch_name} - {acc_name}'
            launch_profile['roblox_account_name'] = acc_name
            launch_profile['roblox_cookie'] = all_saved_accounts[acc_name]
            profiles_to_run.append(launch_profile)
        if not profiles_to_run:
            print_centered(colorize('None of the associated accounts could be found.', C.RED))
            time.sleep(3)
            return
        config['last_used_profile'] = profile_to_launch_name
        save_config(config)
        launch_monitor(profiles_to_run)
    elif profile_data['mode'] in ['mumu', 'ldplayer', 'bluestacks']:
        active_emulators = find_active_emulator_instances(profile_data['mode'])
        if not active_emulators:
            print_centered(colorize(f"No active {profile_data['mode'].capitalize()} instances found.", C.RED))
            time.sleep(3)
            return
        profiles_to_run = []
        for emul in active_emulators:
            new_profile = profile_data.copy()
            new_profile['profile_name'] = profile_to_launch_name
            new_profile['instance_target'] = emul
            profiles_to_run.append(new_profile)
        config['last_used_profile'] = profile_to_launch_name
        save_config(config)
        launch_monitor(profiles_to_run)

def scan_and_configure_existing_instances():
    draw_header('SCANNING FOR EXISTING INSTANCES')
    profiles = []
    print_centered('Scanning for active emulator instances...')
    active_emulators = find_active_mumu_emulators() + find_active_ldplayer_emulators() + find_active_bluestacks_emulators()
    time.sleep(1)
    print_centered('Scanning for active desktop instances...')
    desktop_pids = {p.pid for p in psutil.process_iter(['name']) if p.info['name'] == ROBLOX_PROCESS_NAME}
    time.sleep(1)
    if not active_emulators and (not desktop_pids):
        print_centered(colorize('No running instances found.', C.ORANGE))
        time.sleep(3)
        return []
    for emul in active_emulators:
        draw_header(f"CONFIGURE: {emul['name']}")
        print_centered(colorize('Please configure this existing emulator instance.', C.YELLOW))
        (place_id, link_code) = select_game(context_title=f"Game for {emul['name']}")
        if place_id is None:
            print_centered(colorize('No game selected. Skipping instance.', C.ORANGE))
            time.sleep(2)
            continue
        (restarter_on, interval) = configure_scheduled_restart()
        profiles.append({'profile_name': f"Existing - {emul['name']}", 'mode': emul['type'], 'instance_target': emul, 'place_id': place_id, 'private_server_link_code': link_code, 'restarter_on': restarter_on, 'restarter_interval': interval})
    if desktop_pids:
        accounts = load_roblox_accounts()
        if not accounts:
            print_centered(colorize('Found desktop instances, but you have no saved accounts to assign for relaunches.', C.RED))
            time.sleep(4)
        else:
            print_centered(colorize('NOTE: You must assign a saved account to each existing desktop instance.', C.YELLOW))
            print_centered(colorize('This allows the tool to relaunch it correctly if it crashes.', C.YELLOW))
            input('Press Enter to continue...')
            for (i, pid) in enumerate(desktop_pids):
                draw_header(f'CONFIGURE: Desktop PID {pid}')
                account_names = list(accounts.keys())
                account_options = [f'{name}' for name in account_names]
                account_choice = get_choice(f'Assign an account to PID {pid} for relaunches', account_options + ['Skip'])
                if not account_choice or account_choice > len(account_names):
                    print_centered(colorize(f'Skipping PID {pid}.', C.ORANGE))
                    time.sleep(2)
                    continue
                selected_account_name = account_names[account_choice - 1]
                (place_id, link_code) = select_game(context_title=f'Game for {selected_account_name}')
                if place_id is None:
                    print_centered(colorize('No game selected. Skipping instance.', C.ORANGE))
                    time.sleep(2)
                    continue
                (restarter_on, interval) = configure_scheduled_restart()
                profiles.append({'profile_name': f'Existing - {selected_account_name}', 'mode': 'desktop', 'pid': pid, 'place_id': place_id, 'private_server_link_code': link_code, 'restarter_on': restarter_on, 'restarter_interval': interval, 'roblox_account_name': selected_account_name, 'roblox_cookie': accounts[selected_account_name]})
    return profiles
if __name__ == '__main__':
    clear_screen()
    if not check_and_install_libraries(REQUIRED_LIBRARIES):
        print('\n[X] A dependency error occurred. The application cannot start.')
        print_centered(colorize('Please ensure all required libraries are installed.', C.RED))
        input('Press Enter to exit.')
        sys.exit(1)
    show_splash_screen()
    try:
        main()
    except KeyboardInterrupt:
        MONITORING_ACTIVE = False
        os.system('cls' if os.name == 'nt' else 'clear')
        print_centered(colorize('\nOperation cancelled by user. Exiting.', C.ORANGE))
        time.sleep(2)
        sys.exit(0)
    except Exception as e:
        MONITORING_ACTIVE = False
        os.system('cls' if os.name == 'nt' else 'clear')
        print_centered(colorize(f'\nA critical error occurred: {e}', C.BRIGHT_RED))
        import traceback
        with open(CRITICAL_LOG_FILENAME, 'w') as f:
            f.write(f'Error: {e}\n')
            f.write(traceback.format_exc())
            print_centered(colorize(f"A detailed error log has been saved to '{CRITICAL_LOG_FILENAME}'", C.GREY))
            input('\nPress Enter to exit...')
