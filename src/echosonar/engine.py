import os
import asyncio
import random
import yaml
from telethon import TelegramClient, events
from .config import CONFIG_FILE, SESSION_FILE, CONFIG_DIR

# Cache to store album parts (media groups) before they are sent together
album_cache = {}

def get_latest_config():
    """Reads the current configuration from disk."""
    try:
        with open(CONFIG_FILE, "r") as f:
            return yaml.safe_load(f)
    except Exception:
        return {}

def get_client():
    """Helper used by cli.py to get a client instance for listing IDs."""
    cfg = get_latest_config()
    if not cfg:
        return None
    return TelegramClient(SESSION_FILE, cfg['api_id'], cfg['api_hash'])

def start_bot():
    """The main entry point for the monitoring engine."""
    cfg = get_latest_config()
    if not cfg:
        print("Error: Config not found. Please run 'echosonar setup' first.")
        return

    client = TelegramClient(SESSION_FILE, cfg['api_id'], cfg['api_hash'])

    @client.on(events.NewMessage)
    async def handler(event):
        # 1. Hot-reload current settings
        current_cfg = get_latest_config()
        keywords = current_cfg.get('keywords', [])
        sources = current_cfg.get('source_channels', [])
        dest_bot = current_cfg.get('dest_bot')

        # 2. Identify the chat source (Handles @username or numeric ID)
        chat = event.chat
        chat_id = str(event.chat_id)
        username = getattr(chat, 'username', None)
        
        # Check if source is in our monitored list
        is_monitored = (username and f"@{username}" in sources) or (chat_id in sources)
        if not is_monitored:
            return

        # 3. Check for keywords in the text/caption
        text = (event.raw_text or "").lower()
        has_keyword = any(kw.strip().lower() in text for kw in keywords)

        # 4. Human-like Delay (Simulate reading time)
        delay = random.uniform(3.0, 8.0)
        await asyncio.sleep(delay)

        # 5. Handling Albums (Media Groups)
        if event.grouped_id:
            # Only start tracking the album if the first part we see has the keyword
            if event.grouped_id not in album_cache:
                if has_keyword:
                    album_cache[event.grouped_id] = {'files': [], 'caption': event.text}
                else:
                    return # Skip parts of an album that doesn't match keywords

            # Download this specific part of the album
            file_path = await event.download_media(file=CONFIG_DIR / f"temp_{event.id}")
            album_cache[event.grouped_id]['files'].append(file_path)

            # Wait briefly to ensure all parts of the album have arrived from Telegram
            await asyncio.sleep(2.0)

            # Only the first task to finish the sleep sends the full album
            if event.grouped_id in album_cache:
                data = album_cache.pop(event.grouped_id)
                await client.send_file(dest_bot, data['files'], caption=data['caption'])
                # Immediate cleanup of temporary files
                for f in data['files']:
                    if os.path.exists(f): os.remove(f)
            return

        # 6. Handling Single Messages (Text or Single Media)
        if has_keyword:
            try:
                if event.media:
                    # Downloading and re-uploading bypasses "Restrict Saving Content"
                    path = await event.download_media(file=CONFIG_DIR / f"temp_{event.id}")
                    await client.send_file(dest_bot, path, caption=event.text)
                    if os.path.exists(path): os.remove(path)
                else:
                    # Simple text copy
                    await client.send_message(dest_bot, event.text)
                
                print(f"✅ Forwarded from {username or chat_id} (Delayed {delay:.1f}s)")
            except Exception as e:
                print(f"❌ Failed to forward: {e}")

    # Start the client with the standard interactive login flow
    with client:
        print("--- EchoSonar Monitoring Started ---")
        print("Bypass: Enabled | Albums: Supported | Human-Mode: Active")
        client.run_until_disconnected()
