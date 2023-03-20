import subprocess
import platform
import psutil
import nvidia_smi
import os

steam_cmd = "steam -bigpicture"
name = "steam.exe" if platform.system() == "Windows" else "steam"

if platform.system() == "Windows":
    steam_cmd = "start steam -bigpicture"
elif platform.system() == "Linux":
    steam_cmd = "steam -bigpicture"

pid = next(
    (
        p.info["pid"]
        for p in psutil.process_iter(["pid", "name"])
        if p.info["name"] == name
    ),
    None,
)
if pid is not None:
    process = psutil.Process(pid)
    process.nice(
        psutil.HIGH_PRIORITY_CLASS
        if platform.system() == "Windows"
        else psutil.BELOW_NORMAL_PRIORITY_CLASS
    )


def has_dedicated_gpu():
    return next(
        (
            True
            for gpu in psutil.gpu_devices()
            if gpu.get("memory_total") and gpu.get("memory_total") > 0
        ),
        False,
    )


def is_game_running():
    return next(
        (
            True
            for p in psutil.process_iter(["pid", "name"])
            if p.info["name"] == "game.exe"
        ),
        False,
    )


def is_steam_running():
    return next(
        (
            True
            for p in psutil.process_iter(["pid", "name"])
            if p.info["name"] == "steam.exe"
        ),
        False,
    )

def active_feral_gamemode():
    if os.path.isfile("/usr/bin/gamemoderun"):
        os.system("gamemoderun steam -bigpicture")


def set_game_mode():  # sourcery skip: extract-method
    nvidia_smi.nvmlInit()
    handle = nvidia_smi.nvmlDeviceGetHandleByIndex(0)
    pci_info = nvidia_smi.nvmlDeviceGetPciInfo(handle)
    if pci_info.busId == "0000:01:00.0":
        power_limit = 90  # power limit in watts
        memory_clock = 7500  # memory clock in MHz
        graphics_clock = 1740  # graphics clock in MHz
        device_uuid = nvidia_smi.nvmlDeviceGetUUID(handle)
        command = f"nvidia-smi -i 0 -ac {memory_clock},{graphics_clock} -pl {power_limit} -g {device_uuid}"
        subprocess.run(command, shell=True)

def main():
    if has_dedicated_gpu():
        if is_game_running():
            if platform.system() == "Windows":
                set_game_mode()
            elif platform.system() == "Linux":
                active_feral_gamemode()
        elif is_steam_running():
            if platform.system() == "Windows":
                set_game_mode()
            elif platform.system() == "Linux":
                active_feral_gamemode()


subprocess.run(steam_cmd, shell=True)
