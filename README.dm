https://Reejointool.xyz/hi

RejoinTool

[Engine & Core Functionality]

--Multi-threaded session management to monitor multiple game instances simultaneously.

--Cross-platform support for Standard Windows Desktop Client, MuMu Player, LDPlayer, and BlueStacks.

--Desktop monitoring uses psutil to check the Process ID (PID) and status of the RobloxPlayerBeta.exe process.

--Emulator monitoring utilizes the Android Debug Bridge (ADB) to check for the com.roblox.client process on emulator instances.

--Includes a secure account management system that saves .ROBLOSECURITY cookies and can bulk-add accounts by using Selenium to log in and extract cookies.

--Implemented a scheduled restart system, configurable on a per-profile basis, to maintain session stability.

--An external launch_roblox.py script is used for desktop launches to provide a clean environment.

--Features a system for automatic detection of emulator installation paths through multiple vectors (running processes, shortcuts, registry, common folders).

[User Interface (UI)]

--Rich, text-based UI built for command-line interaction with a well-structured layout.

--A live dashboard displays session name, status, crash count, restart count, and time until the next scheduled restart.

--Includes a toggleable Debug Mode (CTRL+G) that shows a verbose, real-time event log.

--Implemented a robust theming system with 12 unique themes (e.g., Default, Neon, Cyberpunk, Retro).

--Users can override the primary color of any selected theme for further personalization.

--Utilizes global hotkeys via the keyboard library for in-session control:

--CTRL+T: Toggle the restart timer.

--CTRL+X: Exit to the main menu.

--CTRL+G: Toggle debug mode.

[Configuration and Profiles]

--All settings and profiles are saved locally in a single universal_config.json file.

--Full profile management system allowing users to create, edit, and delete profiles.

--Each profile stores its mode (Desktop/Emulator), Place ID, Private Server Link Code, and default restarter settings.

--The application saves the last_used_profile for a quick-launch option on startup.

--Includes a warning prompt upon launch, advising the use of alternate accounts.

[Dependencies and Setup]

--A function automatically checks for and attempts to pip install missing dependencies, including licensing, psutil, keyboard, requests, and pywin32.

--Requires administrator privileges on Windows to ensure full functionality.

--Protected by the licensing library, requiring a valid license key tied to a machine's hardware ID for activation.

--Includes a connection troubleshooter that can kill and restart the ADB server to resolve emulator connection issues.
