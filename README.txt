==================================================
  R E J O I N T O O L - Roblox Session Manager
==================================================
      Made by Isaac (Kirsh)


Thank you for using RejoinTool! This file contains everything you need to know.


-------------------------------
[1] What is RejoinTool?
-------------------------------
RejoinTool is a powerful utility that acts as a "bodyguard" for your Roblox sessions. Its main job is to watch your game 24/7 and automatically get it back up and running if it ever crashes or freezes. This ensures you never lose hours of progress from an unexpected closure again.


-------------------------------
[2] Key Features
-------------------------------
* 24/7 Crash Detection: Constantly watches the Roblox process. If it closes, the tool instantly relaunches the game and rejoins your specified server.

* Anti-Freeze Guard (Emulator Mode): Intelligently detects when the game is completely frozen (not just crashed) and restarts the session.

* Scheduled Restarts: Configure sessions to automatically restart at a set interval (e.g., every 4 hours) to prevent lag and memory leaks.

* Multi-Platform Support: Works with both the standard Windows PC client and MuMu Player for running multiple emulator instances.

* Profile Management: Create and save different profiles for every game, account, or private server link you use.

* Live Dashboard: A clean interface that shows you the real-time status, crash count, and restart timers for all your active sessions.

* Hotkey Support: Use keyboard shortcuts to toggle features on-the-fly without stopping the monitor.


-------------------------------
[3] System Requirements & Setup
-------------------------------
* OS: Windows 10 or Windows 11.
* Administrator Rights: It is highly recommended to run the tool as an Administrator for best performance, especially for finding emulator paths.

* Optional Features:
  For full functionality, you may need to install some libraries if they're missing. The tool will tell you if a feature is disabled.
  - `psutil`: Enables Desktop Mode.
  - `keyboard`: Enables global hotkeys (CTRL+T, CTRL+X).
  - `requests`: Enables resolving Roblox private server share links.


------------------------------------------------
[4] !!! IMPORTANT FIRST-TIME SETUP !!!
------------------------------------------------
To prevent the program from freezing or showing a "black screen," you MUST do this once. This is the most common issue users face and this is the permanent fix.

The Cause: A Windows feature called "QuickEdit Mode" can pause any command-line program if you accidentally click inside the window.

The Fix (For Everybody):
  1. Launch the RejoinTool .exe file.
  2. Right-click the very top title bar of the program window.
  3. A menu will appear. Click on "Properties".
  4. In the new window, make sure you are in the "Options" tab.
  5. UNCHECK the box that says "QuickEdit Mode".
  6. Click "OK" to save.

Now you can restart the tool, and it will never freeze from an accidental click again.


-------------------------------
[5] How to Use
-------------------------------
1. Run RejoinTool.exe and enter your license key.
2. From the main menu, select "Manage Profiles".
3. Select "Create New Profile".
4. Follow the on-screen prompts to choose a mode (Desktop or Emulator), select a game, and configure your settings like scheduled restarts and the anti-freeze guard.
5. Save the profile with a name.
6. From the main menu or the profile manager, launch your new profile to begin monitoring!


-----------------------------------------------------------------
[6] !!! A C C O U N T   S A F E T Y   W A R N I N G !!!
-----------------------------------------------------------------
This tool is often used with executors or other third-party software that may violate Roblox's Terms of Service.

For your safety, it is STRONGLY RECOMMENDED to ONLY use an alternate ("alt") account with this tool. NEVER use your main account.

The developers of this tool are not responsible for any disciplinary action, bans, or other consequences that may occur to your Roblox account. Use at your own risk.
-----------------------------------------------------------------


-------------------------------
[7] Basic Troubleshooting
-------------------------------
Q: The program window froze / went to a black screen!
A: You have not disabled QuickEdit Mode. Please follow the instructions in section [4] of this README file. This is the fix.

Q: The tool can't find my emulator instance!
A: Make sure MuMu Player is fully running BEFORE you try to launch an emulator profile from the tool. If you still have issues, use the "Troubleshoot Connection" option in the Profile Manager menu.

Q: A feature like "Desktop Mode" or "Hotkeys" is disabled.
A: The script is missing an optional Python library. Please see section [3] for details on what each library enables.


-------------------------------
[8] Support & Community
-------------------------------
For more help, questions, or to get the latest updates, please join our Discord server!

[https://discord.gg/jcq58UfD]