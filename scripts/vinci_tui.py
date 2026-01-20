import os
import subprocess
import time
import json
from datetime import datetime
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box

# --- Configuration ---
VAULT_ROOT = "/storage/emulated/0/Download/Vinci"
SCRIPTS_DIR = os.path.join(VAULT_ROOT, "scripts")
CENTRAL_CMD = os.path.join(VAULT_ROOT, "0 - 🌌 Central Command.md")
CHAOS_STREAM = os.path.join(VAULT_ROOT, "1 - 🌀 Chaos Stream.md")

console = Console()

def get_git_status():
    try:
        result = subprocess.run(["git", "status", "--short"], cwd=VAULT_ROOT, capture_output=True, text=True)
        return result.stdout.strip() if result.stdout else "System Synchronized."
    except:
        return "Git error."

def get_recent_chaos():
    try:
        if not os.path.exists(CHAOS_STREAM): return "Stream not found."
        with open(CHAOS_STREAM, "r") as f:
            lines = f.readlines()
        return "".join(lines[-10:]) if lines else "Empty."
    except:
        return "Read error."

def get_daily_focus():
    try:
        with open(CENTRAL_CMD, "r") as f:
            content = f.read()
        if "## 📅 Daily Focus (Today)" in content:
            section = content.split("## 📅 Daily Focus (Today)")[1].split("##")[0]
            return section.strip()
        return "No tasks."
    except:
        return "File error."

def make_layout() -> Layout:
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="main"),
        Layout(name="footer", size=3)
    )
    layout["main"].split_row(
        Layout(name="left", ratio=1),
        Layout(name="right", ratio=1)
    )
    layout["left"].split_column(
        Layout(name="menu", ratio=2),
        Layout(name="status", ratio=1)
    )
    layout["right"].split_column(
        Layout(name="tasks", ratio=1),
        Layout(name="info", ratio=1)
    )
    return layout

class Header:
    def __rich__(self) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="left", ratio=1)
        grid.add_column(justify="right", ratio=1)
        grid.add_row(
            Text("🛰️ VINCI OS v4.0", style="bold blue"),
            Text(datetime.now().strftime("%Y-%m-%d %I:%M %p"), style="cyan")
        )
        return Panel(grid, style="white on blue")

def get_native_input(title, prompt):
    result = subprocess.run(["termux-dialog", "text", "-t", title, "-i", prompt], capture_output=True, text=True)
    try:
        return json.loads(result.stdout).get("text", "").strip()
    except:
        return ""

def main():
    layout = make_layout()
    console.clear()
    
    while True:
        layout["header"].update(Header())
        layout["menu"].update(Panel(
            "[bold yellow]M[/] Morning | [bold yellow]S[/] Sync | [bold yellow]V[/] Voice | [bold yellow]C[/] Chaos | [bold yellow]P[/] Process | [bold yellow]Q[/] Terminate",
            title="Commands", border_style="blue"
        ))
        layout["status"].update(Panel(get_git_status(), title="System Status", border_style="blue"))
        layout["tasks"].update(Panel(get_daily_focus(), title="Daily Focus", border_style="yellow"))
        layout["info"].update(Panel(get_recent_chaos(), title="Recent Chaos Stream", border_style="cyan"))
        layout["footer"].update(Panel(Text("M: Morning | S: Sync | V: Voice | C: Chaos | Q: Quit", justify="center")))
        
        console.clear()
        console.print(layout)
        
        console.print("\n[bold green]vinci@system > [/bold green]", end="")
        user_input = input().strip()
        
        if not user_input: continue
        choice = user_input.lower()
        
        if choice == 'q': break
        elif choice == 'm':
            subprocess.run(["python", os.path.join(SCRIPTS_DIR, "morning_cron.py")])
            input("\n[Press Enter]")
        elif choice == 's':
            subprocess.run(["python", os.path.join(SCRIPTS_DIR, "system_sync.py")])
            input("\n[Press Enter]")
        elif choice == 'c':
            entry = get_native_input("Voice Journal", "Transcribe thoughts...")
            if entry:
                timestamp = datetime.now().strftime("[%I:%M %p]")
                with open(CHAOS_STREAM, "a") as f:
                    f.write(f"\n- `{timestamp}` {entry}")
        elif choice == 'v':
            text = get_native_input("Universal Input", "Command or Entry...")
            if text:
                if text.lower() in ["sync", "sync vault"]:
                    subprocess.run(["python", os.path.join(SCRIPTS_DIR, "system_sync.py")])
                else:
                    timestamp = datetime.now().strftime("[%I:%M %p]")
                    with open(CHAOS_STREAM, "a") as f:
                        f.write(f"\n- `{timestamp}` (Voice) {text}")
        elif choice == 'p':
            subprocess.run(["python", os.path.join(SCRIPTS_DIR, "chaos_processor.py")])
            input("\n[Press Enter]")
        else:
            try:
                subprocess.run(user_input, shell=True, cwd=VAULT_ROOT)
                input("\n[Press Enter]")
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")
                time.sleep(1)

if __name__ == "__main__":
    main()
