import typer
import yaml
import asyncio
from .config import CONFIG_FILE, ensure_config
from .engine import start_bot, get_client

app = typer.Typer(help="EchoSonar Management CLI")
kw_app = typer.Typer(help="Manage monitoring keywords")
dest_app = typer.Typer(help="Manage destination bot/channel")
chan_app = typer.Typer(help="Manage source channels to monitor")

app.add_typer(chan_app, name="channels")
app.add_typer(kw_app, name="keywords")
app.add_typer(dest_app, name="dest")

def get_config():
    with open(CONFIG_FILE, "r") as f:
        return yaml.safe_load(f)

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        yaml.dump(config, f)

# --- GLOBAL COMMANDS ---

@app.command("list-ids")
def list_ids():
    """List all joined channels/groups and their numeric IDs."""
    async def _list():
        client = get_client()
        async with client:
            typer.secho(f"{'TITLE':<30} | {'ID':<20}", fg=typer.colors.CYAN, bold=True)
            typer.echo("-" * 55)
            async for dialog in client.iter_dialogs():
                if dialog.is_channel or dialog.is_group:
                    typer.echo(f"{dialog.name[:30]:<30} | {dialog.id:<20}")

    asyncio.run(_list())

@app.command()
def setup():
    """Configure API credentials and initial monitoring targets."""
    ensure_config()
    typer.secho("--- EchoSonar Initial Setup ---", fg=typer.colors.CYAN, bold=True)
    
    api_id = typer.prompt("Enter your Telegram API ID", type=int)
    api_hash = typer.prompt("Enter your Telegram API Hash")
    
    source_channels = typer.prompt(
        "Enter source channels to monitor (comma-separated, e.g., @chan1, -100...)"
    )
    keywords = typer.prompt(
        "Enter keywords to trigger forwarding (comma-separated, e.g., crypto, alert)"
    )
    dest_bot = typer.prompt(
        "Enter the destination bot/user username (e.g., @MyAnalyzerBot)"
    )

    config_data = {
        "api_id": api_id,
        "api_hash": api_hash,
        "source_channels": [c.strip() for c in source_channels.split(",")],
        "keywords": [k.strip() for k in keywords.split(",")],
        "dest_bot": dest_bot.strip()
    }

    save_config(config_data)
    typer.secho(f"\n✅ Configuration saved to {CONFIG_FILE}", fg=typer.colors.GREEN)
    typer.echo("Now run 'echosonar run' to start the bot and authenticate.")

@app.command()
def run():
    """Start the monitoring engine."""
    start_bot()

# --- CHANNEL COMMANDS ---

@chan_app.command("list")
def list_channels():
    cfg = get_config()
    channels = cfg.get('source_channels', [])
    typer.echo(f"Monitoring {len(channels)} channels:")
    for c in channels:
        typer.echo(f" - {c}")

@chan_app.command("add")
def add_channel(channel: str):
    """Add a channel username (e.g. @example) or numeric ID."""
    cfg = get_config()
    if 'source_channels' not in cfg:
        cfg['source_channels'] = []
    if channel not in cfg['source_channels']:
        cfg['source_channels'].append(channel)
        save_config(cfg)
        typer.echo(f"Added channel: {channel}")

@chan_app.command("remove")
def remove_channel(channel: str):
    cfg = get_config()
    if channel in cfg.get('source_channels', []):
        cfg['source_channels'].remove(channel)
        save_config(cfg)
        typer.echo(f"Removed channel: {channel}")

# --- KEYWORD COMMANDS ---

@kw_app.command("list")
def list_keywords():
    cfg = get_config()
    typer.echo(f"Current Keywords: {', '.join(cfg.get('keywords', []))}")

@kw_app.command("add")
def add_keyword(word: str):
    cfg = get_config()
    if 'keywords' not in cfg:
        cfg['keywords'] = []
    if word not in cfg['keywords']:
        cfg['keywords'].append(word)
        save_config(cfg)
        typer.echo(f"Added: {word}")

@kw_app.command("remove")
def remove_keyword(word: str):
    cfg = get_config()
    if word in cfg.get('keywords', []):
        cfg['keywords'].remove(word)
        save_config(cfg)
        typer.echo(f"Removed: {word}")

# --- DESTINATION COMMANDS ---

@dest_app.command("show")
def show_dest():
    cfg = get_config()
    typer.echo(f"Current Destination: {cfg.get('dest_bot')}")

@dest_app.command("set")
def set_dest(target: str):
    cfg = get_config()
    cfg['dest_bot'] = target
    save_config(cfg)
    typer.echo(f"Destination updated to: {target}")

if __name__ == "__main__":
    app()
