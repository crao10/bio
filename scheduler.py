"""Scheduler for running the story scout on a cron or manually."""

import subprocess
import sys
from pathlib import Path


CRON_ENTRY = "0 8 * * 1 cd {dir} && {python} -m scout"


def install_cron():
    """Install a cron job to run the scout every Monday at 8am."""
    project_dir = Path(__file__).resolve().parent
    python_path = sys.executable
    entry = CRON_ENTRY.format(dir=project_dir, python=python_path)

    # Read existing crontab
    result = subprocess.run(
        ["crontab", "-l"], capture_output=True, text=True
    )
    existing = result.stdout if result.returncode == 0 else ""

    if "scout" in existing:
        print("Cron job already installed. Current entry:")
        for line in existing.splitlines():
            if "scout" in line:
                print(f"  {line}")
        return

    new_crontab = existing.rstrip() + "\n" + entry + "\n"
    subprocess.run(
        ["crontab", "-"], input=new_crontab, text=True, check=True
    )
    print(f"Cron job installed: {entry}")


def uninstall_cron():
    """Remove the scout cron job."""
    result = subprocess.run(
        ["crontab", "-l"], capture_output=True, text=True
    )
    if result.returncode != 0:
        print("No crontab found.")
        return

    lines = [
        line for line in result.stdout.splitlines() if "scout" not in line
    ]
    new_crontab = "\n".join(lines) + "\n" if lines else ""
    subprocess.run(
        ["crontab", "-"], input=new_crontab, text=True, check=True
    )
    print("Cron job removed.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Manage story scout scheduling")
    parser.add_argument(
        "action",
        choices=["install", "uninstall", "run"],
        help="install/uninstall cron job, or run the scout now",
    )
    args = parser.parse_args()

    if args.action == "install":
        install_cron()
    elif args.action == "uninstall":
        uninstall_cron()
    elif args.action == "run":
        from scout import main
        main()
