# Licensed under the MIT License.
https://Rejointool.xyz/hi
RejoinTool

Note If you don't see rejointool.py, it's because I'm fixing some issues.
With how much Roblox has updated over the last few months, it broke some features in Rejointool.

# Engine & Core Functionality

- Multi-threaded session management to monitor multiple game instances simultaneously.

- Cross-platform support for Standard Windows Desktop Client, MuMu Player, LDPlayer, and BlueStacks.

- Desktop monitoring uses psutil to check the Process ID (PID) and status of the RobloxPlayerBeta.exe process.

- Emulator monitoring utilizes the Android Debug Bridge (ADB) to check for the com.roblox.client process on emulator instances.

- Includes a secure account management system that saves .ROBLOSECURITY cookies and can bulk-add accounts by using Selenium to log in and extract cookies.

- Implemented a scheduled restart system, configurable on a per-profile basis, to maintain session stability.

- An external launch_roblox.py script is used for desktop launches to provide a clean environment.

- Features a system for automatic detection of emulator installation paths through multiple vectors (running processes, shortcuts, registry, common folders).

# User Interface (UI)

- Rich, text-based UI built for command-line interaction with a well-structured layout.

- A live dashboard displays session name, status, crash count, restart count, and time until the next scheduled restart.

- Includes a toggleable Debug Mode (CTRL+G) that shows a verbose, real-time event log.

- Implemented a robust theming system with 12 unique themes (e.g., Default, Neon, Cyberpunk, Retro).

- Users can override the primary color of any selected theme for further personalization.

- Utilizes global hotkeys via the keyboard library for in-session control:

- CTRL+T: Toggle the restart timer.

- CTRL+X: Exit to the main menu.

- CTRL+G: Toggle debug mode.

# Configuration and Profiles

- All settings and profiles are saved locally in a single universal_config.json file.

- Full profile management system allowing users to create, edit, and delete profiles.

- Each profile stores its mode (Desktop/Emulator), Place ID, Private Server Link Code, and default restarter settings.

- The application saves the last_used_profile for a quick-launch option on startup.

- Includes a warning prompt upon launch, advising the use of alternate accounts.

Note: Some users may use this with executors to autofarm in their favorite games. With that said, I am not responsible for any bans.

I originally made this tool for my personal use and started selling it under a license system.
Then, I realized Python programs shouldn't be sold—there's no point unless it's something crazy—so I decided to host it on GitHub since many people requested it.

![Test Image 0](https://raw.githubusercontent.com/KirshWasHere/KeysTest/d8d75550eae322cb14c592c6f2079a7b5bbb569f/Screenshot%202025-08-04%20175549.png)
![Test image 1](https://raw.githubusercontent.com/KirshWasHere/KeysTest/d8d75550eae322cb14c592c6f2079a7b5bbb569f/test1%20(1).jpg)
![Test image 2](https://raw.githubusercontent.com/KirshWasHere/KeysTest/d8d75550eae322cb14c592c6f2079a7b5bbb569f/test1%20(2).jpg)
![Test image 4](https://raw.githubusercontent.com/KirshWasHere/KeysTest/d8d75550eae322cb14c592c6f2079a7b5bbb569f/test1%20(4).png)
![Test image 5](https://raw.githubusercontent.com/KirshWasHere/KeysTest/d8d75550eae322cb14c592c6f2079a7b5bbb569f/test1%20(5).jpg)
![Test image 6](https://raw.githubusercontent.com/KirshWasHere/KeysTest/d8d75550eae322cb14c592c6f2079a7b5bbb569f/test1%20(6).png)
