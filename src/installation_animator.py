import time
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.panel import Panel
from rich.text import Text


class InstallationAnimator:
    def __init__(self):
        self.console = Console()

    def animate_installation(self, packages):
        total_packages = len(packages)

        with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                console=self.console
        ) as progress:
            overall_task = progress.add_task("[green]Installing packages", total=total_packages)

            for package, version in packages:
                package_task = progress.add_task(f"[cyan]Installing {package}@{version}", total=100)

                # Simulate installation steps
                for i in range(100):
                    time.sleep(0.01)  # Simulate some work
                    progress.update(package_task, advance=1)

                progress.update(overall_task, advance=1)

                # Show a fun message when a package is installed
                self.show_package_installed_message(package, version)

    def show_package_installed_message(self, package, version):
        messages = [
            f"🎉 Woohoo! {package}@{version} is ready to rock!",
            f"🚀 {package}@{version} has landed successfully!",
            f"🌟 {package}@{version} is now sparkling in your project!",
            f"🎊 Pop the champagne! {package}@{version} is installed!",
            f"🏆 Victory! {package}@{version} is now part of the team!"
        ]
        message = Text(messages[hash(package) % len(messages)])
        self.console.print(Panel(message, border_style="green", expand=False))

    def show_final_message(self, total_installed, total_time):
        message = Text(f"🎊 Installation complete! 🎊\n\n"
                       f"Installed {total_installed} packages in {total_time:.2f} seconds.\n"
                       f"Your project is now more powerful than ever!")
        self.console.print(Panel(message, border_style="magenta", expand=False))