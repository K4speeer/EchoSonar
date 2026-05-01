← [Back to README](./README.md)


# ⌨️ EchoSonar Command Reference

This guide provides a detailed breakdown of all available commands in the **EchoSonar** CLI.

---

## 🏗️ Core Commands

### `echosonar setup`
**Usage:** `echosonar setup`  
The first command you should run. It interactively prompts for:
*   `API_ID` & `API_HASH`: Your Telegram developer credentials.
*   `Source Channels`: Initial list of channels to monitor.
*   `Keywords`: Initial list of trigger words.
*   `Destination`: The bot or user username where messages will be sent.

### `echosonar run`
**Usage:** `echosonar run`  
Starts the monitoring engine. 
*   **First Run:** Will prompt for your phone number and the Telegram login code.
*   **Subsequent Runs:** Uses the saved session file for automatic login.
*   **Live Feedback:** Displays real-time logs of captured and forwarded messages.

### `echosonar list-ids`
**Usage:** `echosonar list-ids`  
Scans all your joined chats and prints a table of names and numeric IDs. Essential for finding the ID of **private channels** that do not have a `@username`.

---

## 📡 Channel Management (`echosonar channels`)

Manage the list of sources the bot is watching.


| Command | Usage | Description |
| :--- | :--- | :--- |
| `list` | `echosonar channels list` | Shows all currently monitored channels. |
| `add` | `echosonar channels add "@name"` | Adds a public channel by username. |
| `add` | `echosonar channels add -- "-100..."` | Adds a private channel by ID (use `--` for negative numbers). |
| `remove` | `echosonar channels remove "@name"` | Stops monitoring a specific channel. |

---

## 🔑 Keyword Management (`echosonar keywords`)

Manage the triggers that cause a message to be copied.


| Command | Usage | Description |
| :--- | :--- | :--- |
| `list` | `echosonar keywords list` | Shows all active keywords. |
| `add` | `echosonar keywords add "word"` | Adds a new trigger word (Case-Insensitive). |
| `remove` | `echosonar keywords remove "word"` | Removes a trigger word. |

---

## 🎯 Destination Management (`echosonar dest`)

Control where the filtered content is sent.


| Command | Usage | Description |
| :--- | :--- | :--- |
| `show` | `echosonar dest show` | Displays the current destination username. |
| `set` | `echosonar dest set "@target"` | Changes the destination to a different bot or user. |

---

## 💡 Pro Tips

### 1. Handling Negative IDs
When adding a private channel ID (which starts with a minus sign `-`), your terminal might mistake it for an option. Always use the double-dash separator:
```bash
echosonar channels add -- "-1001234567890"
```

### 2. Hot-Reloading
You do **not** need to stop the bot to change keywords or channels. Simply open a second terminal window, run your `add` or `remove` commands, and the running bot will pick up the changes on the next incoming message.

### 3. Cleaning Up
If you ever want to clear all data and start over:
```bash
pipx uninstall echosonar
rm -rf ~/.config/echosonar
```



← [Back to README](./README.md)
