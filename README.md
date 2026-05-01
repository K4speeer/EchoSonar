# 🛰️ EchoSonar

**EchoSonar** is a professional-grade Telegram monitoring user bot built with [Telethon](https://telethon.dev). It acts as an automated bridge, monitoring your private or public channels for specific keywords and instantly copying and re-uploading content to a destination of your choice.

[![PyPI version](https://shields.io)](https://pypi.org)
[![License: MIT](https://shields.io)](https://opensource.org)

---

## ✨ Key Features

*   **🛡️ Content Protection Bypass:** Automatically downloads and re-uploads media from restricted channels where "Saving Content" is disabled.
*   **📂 Full Album Support:** Intelligently gathers media groups (albums) and forwards them as a single cohesive unit.
*   **👤 Human-Like Behavior:** Implements randomized delays (3-8s) and manual re-upload flows to mimic human activity and reduce account flagging risks.
*   **🔄 Hot-Reloading:** Update keywords, monitored channels, or destinations via CLI without restarting the running bot.
*   **🕵️ Private Channel Support:** Easily monitor private channels using internal numeric IDs.

---

## 🚀 Installation

EchoSonar is designed to be installed in an isolated environment using [pipx](https://github.io) to avoid dependency conflicts.

```bash
# Install from PyPI (Recommended)
pipx install echosonar

# Or install directly from GitHub
pipx install git+https://github.com
```

---

## 🛠️ Quick Start

### 1. Configuration
Run the setup command to input your Telegram API credentials (get them at [my.telegram.org](https://telegram.org)):
```bash
echosonar setup
```

### 2. Find Private IDs
If you need to monitor private channels, use the following command to see all your joined chats and their internal IDs:
```bash
echosonar list-ids
```

### 3. Add Monitoring Targets
```bash
# Add a public channel by username
echosonar channels add "@PublicChannel"

# Add a private channel by numeric ID (use -- to handle negative numbers)
echosonar channels add -- "-1001234567890"

# Add keywords
echosonar keywords add "urgent"
```

### 4. Run & Authenticate
Start the bot once in your terminal to complete the one-time Telegram login:
```bash
echosonar run
```

---

## 🏠 Running Live 24/7

### On a Server (Linux/VPS)
The professional way to run EchoSonar on a server is using **systemd**. This ensures the bot starts on boot and restarts automatically if it crashes.

1. **Create the service file:**
   `sudo nano /etc/systemd/system/echosonar.service`

2. **Paste configuration:** (Replace `youruser` with your Linux username)
   ```ini
   [Unit]
   Description=EchoSonar Telegram Bot
   After=network.target

   [Service]
   User=youruser
   ExecStart=/home/youruser/.local/bin/echosonar run
   Restart=always
   RestartSec=10
   WorkingDirectory=/home/youruser

   [Install]
   WantedBy=multi-user.target
   ```

3. **Start the service:**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable --now echosonar
   ```

### On a Personal Computer
For local background execution, use a terminal multiplexer like **Screen** or **TMUX**:
```bash
# Create a new session
screen -S echosonar

# Run the bot
echosonar run

# Detach (Press Ctrl+A then D)
# The bot will continue running in the background.
```

---

## 📖 Detailed Documentation
For a full list of all available commands and advanced usage, see [COMMANDS.md](./COMMANDS.md).

## ⚖️ Disclaimer
This tool is for personal automation and research purposes. Please respect Telegram's [Terms of Service](https://telegram.org) and the copyright of content creators. Use of user bots carries a risk of account restriction if used for spam or malicious activity.
