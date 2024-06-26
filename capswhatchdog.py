import os
import platform
import subprocess
import sys  # Import the sys module
import time

# Path to the lock file
lock_file = "/tmp/capslock_script.lock"


def detect_os():
    if platform.system().lower() == "windows":
        return "Windows"
    elif platform.system().lower() == "linux":
        try:
            with open("/proc/version", "r") as f:
                if "microsoft" in f.read().lower():
                    return "WSL"
        except FileNotFoundError:
            pass
        return "Unix"
    else:
        return platform.system()


def get_caps_lock(os):
    match os:
        case "WSL":
            windows_shell = (
                "pwsh.exe"
                if subprocess.run(
                    "pwsh.exe -v",
                    shell=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                ).returncode
                == 0
                else "powershell.exe"
            )
            result = subprocess.run(
                [windows_shell, "-c", "[console]::CapsLock"],
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                sys.exit(1)
            return result.stdout.strip()


if __name__ == "__main__":
    # Using a lock to just have one instance running. Might log something if there's already a lock
    if os.path.exists(lock_file):
        sys.exit(1)

    open(lock_file, "a").close()

    try:
        pipe_path = "/tmp/capslock_pipe"
        if not os.path.exists(pipe_path):
            os.mkfifo(pipe_path)
        with open(pipe_path, "w") as pipe:
            while True:
                pipe.write(f"{get_caps_lock(detect_os())}\n")
                pipe.flush()
                time.sleep(0.5)
    finally:
        os.remove(lock_file)
