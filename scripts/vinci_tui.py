import os
import subprocess
import time
from datetime import datetime
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.text import Text
from rich.align import Align
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
        return result.stdout.strip() if result.stdout else "No changes."
    except:
        return "Git error."

def get_recent_chaos():
    try:
        with open(CHAOS_STREAM, "r") as f:
            lines = f.readlines()
        return "".join(lines[-5:]) if lines else "Empty."
    except:
        return "File not found."

def get_daily_focus():
    try:
        with open(CENTRAL_CMD, "r") as f:
            content = f.read()
        section = content.split("## 📅 Daily Focus (Today)")[1].split("##")[0]
        return section.strip()
    except:
        return "No tasks found."

def make_layout() -> Layout:
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="main"),
        Layout(name="footer", size=3)
    )
    layout["main"].split_row(
        Layout(name="left"),
        Layout(name="right")
    )
    layout["left"].split_column(
        Layout(name="menu"),
        Layout(name="tasks")
    )
    return layout

class Header:
    def __rich__(self) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="left", ratio=1)
        grid.add_column(justify="right", ratio=1)
        grid.add_row(
            Text("VINCI COMMAND CENTER", style="bold magenta"),
            Text(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), style="cyan")
        )
        return Panel(grid, style="white on blue")

class Menu:
    def __rich__(self) -> Panel:
        table = Table(box=box.MINIMAL, expand=True)
        table.add_column("Key", style="bold yellow", width=4)
        table.add_column("Action", style="white")
        table.add_row("M", "Morning Protocol")
        table.add_row("S", "Sync Vault")
        table.add_row("C", "Chaos Entry")
        table.add_row("P", "Process Chaos")
        table.add_row("G", "Ghost Service")
        table.add_row("H", "Health Check")
        table.add_row("V", "Validate System")
        table.add_row("B", "Backup System")
        table.add_row("A", "Anki Generation")
        table.add_row("Q", "Quit")
        return Panel(table, title="[bold]🎛️ Control Panel[/bold]", border_style="green")

class Tasks:
    def __rich__(self) -> Panel:
        return Panel(get_daily_focus(), title="[bold]📅 Daily Focus[/bold]", border_style="yellow")

class Status:
    def __rich__(self) -> Panel:
        git = get_git_status()
        chaos = get_recent_chaos()
        content = f"[bold cyan]🛰️ Git Status:[/bold cyan]\n{git}\n\n[bold magenta]🌀 Recent Chaos:[/bold magenta]\n{chaos}"
        return Panel(content, title="[bold]📊 System Status[/bold]", border_style="cyan")

def run_command(cmd_name):
    console.clear()
    console.print(f"🚀 Executing {cmd_name}...", style="bold yellow")
    
    try:
        if cmd_name == "Morning Protocol":
            subprocess.run(["python", os.path.join(SCRIPTS_DIR, "morning_cron.py")])
        elif cmd_name == "Sync Vault":
            subprocess.run(["python", os.path.join(SCRIPTS_DIR, "system_sync.py")])
        elif cmd_name == "Chaos Entry":
            entry = input("\n📝 Enter Chaos Stream entry: ")
            if entry:
                timestamp = datetime.now().strftime("[%I:%M %p]")
                with open(CHAOS_STREAM, "a") as f:
                    f.write(f"\n- `{timestamp}` {entry}")
        elif cmd_name == "Process Chaos":
            subprocess.run(["python", os.path.join(SCRIPTS_DIR, "chaos_processor.py")])
        elif cmd_name == "Ghost Service":
            result = subprocess.run(["pgrep", "-f", "ghost_service.py"], capture_output=True)
            if result.returncode == 0:
                subprocess.run(["pkill", "-f", "ghost_service.py"])
                console.print("\n👻 Ghost Service [bold red]Stopped[/bold red].")
            else:
                subprocess.Popen(["python", os.path.join(SCRIPTS_DIR, "ghost_service.py")])
                console.print("\n👻 Ghost Service [bold green]Started[/bold green] in background.")
        elif cmd_name == "Health Check":
            subprocess.run(["python", os.path.join(SCRIPTS_DIR, "health_check.py")])
        elif cmd_name == "Validate System":
            subprocess.run(["python", os.path.join(SCRIPTS_DIR, "validate_system.py")])
        elif cmd_name == "Backup System":
            subprocess.run(["bash", os.path.join(SCRIPTS_DIR, "backup_system.sh")])
        elif cmd_name == "Anki Generation":
            subprocess.run(["python", os.path.join(SCRIPTS_DIR, "anki_generator.py")])
            
        input("\n[Press Enter to return to Dashboard]")
    except Exception as e:
        console.print(f"\n❌ Error: {e}", style="bold red")
        time.sleep(2)

def main():
    layout = make_layout()
    layout["header"].update(Header())
    layout["menu"].update(Menu())
    layout["tasks"].update(Tasks())
    layout["right"].update(Status())
    layout["footer"].update(Panel(Text("Press Q to quit | M: Morning | S: Sync | G: Ghost", justify="center")))

    import sys
    import termios
    import tty

    def getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    # Interactive loop
    while True:
        console.clear()
        # Re-render to show status
        layout["header"].update(Header())
        layout["menu"].update(Menu())
        layout["tasks"].update(Tasks())
        layout["right"].update(Status())
        layout["footer"].update(Panel(Text("M: Morning | S: Sync | G: Ghost | P: Process | Q: Quit", justify="center")))
        console.print(layout)
        
        console.print("\n[bold green]🕹️ Vinci > [/bold green]", end="")
        choice = input().lower().strip()
        
        if choice == 'q':
            console.clear()
            console.print("[bold yellow]Exiting Vinci Command Center...[/bold yellow]")
            break
        elif choice == 'm': run_command("Morning Protocol")
        elif choice == 's': run_command("Sync Vault")
        elif choice == 'c': run_command("Chaos Entry")
        elif choice == 'p': run_command("Process Chaos")
        elif choice == 'g': run_command("Ghost Service")
        elif choice == 'h': run_command("Health Check")
        elif choice == 'v': run_command("Validate System")
        elif choice == 'b': run_command("Backup System")
        elif choice == 'a': run_command("Anki Generation")
        else:
             if choice:
                 console.print(f"\n[bold cyan]💻 Executing: {choice}[/bold cyan]")
                 try:
                     subprocess.run(choice, shell=True, cwd=VAULT_ROOT)
                     input("\n[Press Enter to continue]")
                 except Exception as e:
                     console.print(f"[bold red]❌ Error: {e}[/bold red]")
                     time.sleep(2)

if __name__ == "__main__":
    main()
