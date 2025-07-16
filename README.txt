RejoinTool

[Engine & Core Functionality]
- Multi-threaded session management to monitor multiple game instances simultaneously.
- Dual-mode operation supporting Desktop and Emulator profiles.
- Desktop monitoring uses psutil to check for RobloxPlayerBeta.exe process status.
- Emulator monitoring utilizes the Android Debug Bridge (ADB) to check for the com.roblox.client process on MuMu Player instances.
- Implemented a scheduled restart system for both Desktop and Emulator modes, configurable on a per-profile basis.
- An external launch_roblox.py script is used for desktop launches to provide a clean environment for external tool attachment.
- Includes a system for automatic detection of MuMu Player installation paths through multiple vectors (running processes, shortcuts, registry, common folders).

[User Interface (UI)]
- Rich, text-based UI with a 96-character width, built for command-line interaction.
- A live dashboard displays session name, status, crash count, restart count, and time until the next scheduled restart.
- Includes a toggleable Debug Mode (CTRL+G) that shows a verbose, real-time event log.
- Implemented a robust theming system with 12 unique themes (Default, Modern, Minimalist, Neon, Glitch, Matrix, Vaporwave, KirshStyle, Cyberpunk, Retro).
- Users can override the primary color of any theme.
- Utilizes global hotkeys via the keyboard library for toggling the restart timer (CTRL+T), exiting to the menu (CTRL+X), and toggling debug mode (CTRL+G).

[Configuration & Profiles]
- All settings and profiles are saved locally in a universal_config.json file.
- Full profile management system allowing users to create, edit, and delete profiles.
- Each profile stores its mode (Desktop/Emulator), Place ID, Private Server Link Code, and default restarter settings.
- The application saves the last_used_profile for a quick-launch option on startup.
- Includes a warning prompt to confirm launch, advising the use of alternate accounts when using third-party tools.

[Dependencies & Setup]
- A check_and_install_libraries function automatically checks for and attempts to pip install missing dependencies, including licensing, psutil, keyboard, requests, and pywin32.
- Protected by the licensing library, requiring a valid license key tied to a machine's hardware ID for activation.
- Includes a connection troubleshooter that can kill-server and start-server for ADB.