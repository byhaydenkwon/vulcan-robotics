#!usr/bin/env python3

"""
Run this Windows/Linux script to automatically copy data from the src/ directory
to an SD card!

(Be careful, this will IMMEDIATELY overwrite any contents matching the names in the
target directory!)

To configure, create a file called ".env" in the project directory and add:

TARGET_PATH_WINDOWS = "C:\\your\\sd\\card\\path\\here"

or

TARGET_PATH_POSIX = "/your/sd/card/path/here"

depending on your operating system. The script will automatically use the one
corresponding to the OS you run from.
"""

# Basically just a hundred lines of error checking.

import os
import shutil
import platform
import subprocess

from pathlib import Path

from dotenv import load_dotenv

from plyer.facades import Notification  # Windows

APP_NAME = "vulcan-robotics"


def notify(title: str, message: str, app_name: str, timeout: int) -> None:
    """
    Send a system notification on Windows or Linux. Timeout in seconds.
    """
    if os.name == "nt":
        Notification().notify(
            title=title,
            message=message,
            app_name=app_name,
            timeout=timeout,
        )
    elif os.name == "posix":
        subprocess.run(
            [
                "notify-send",
                "--app-name",
                app_name,
                "--expire-time",
                str(timeout * 1000),
                title,
                message,
            ]
        )


def notify_and_raise(error: Exception) -> None:
    notify("Couldn't copy files :(", str(error), APP_NAME, 5)
    raise error


def main() -> None:
    notify("Copying files...", "", APP_NAME, 3)

    if not load_dotenv():
        notify_and_raise(FileNotFoundError("No .env file found in source directory!"))

    source_path = Path.cwd() / "src"

    if not source_path.exists() or not source_path.is_dir():
        notify_and_raise(FileNotFoundError("No src/ folder found in source directory!"))

    if os.name == "nt":
        target_env = os.getenv("TARGET_PATH_WINDOWS")
    elif os.name == "posix":
        target_env = os.getenv("TARGET_PATH_POSIX")
    else:
        notify_and_raise(RuntimeError(f'Unsupported operating system "{os.name}"!'))

    if target_env == "":
        notify_and_raise(
            ValueError(f"{platform.system()} target path in .env is empty!")
        )

    if not target_env:
        notify_and_raise(
            EnvironmentError(f"No {platform.system()} target path in .env!")
        )

    assert target_env  # for the checker
    target_path = Path(target_env)

    if not os.access(target_path, os.R_OK) and target_path.exists():
        notify_and_raise(
            PermissionError(
                f'No permission to read provided target path "{target_env}"!'
            )
        )

    if not target_path.exists():
        notify_and_raise(
            FileNotFoundError(f'Provided target path "{target_env}" does not exist!')
        )

    if not target_path.is_dir():
        notify_and_raise(
            ValueError(f'Provided target path "{target_env}" is not a directory!')
        )

    try:
        shutil.copytree(
            source_path, target_path, copy_function=shutil.copy2, dirs_exist_ok=True
        )
        notify("Files successfully copied!", "", APP_NAME, 3)
    except Exception as e:
        notify_and_raise(e)


if __name__ == "__main__":
    main()
