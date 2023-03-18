import subprocess
import platform
import psutil
import nvidia_smi

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


def set_game_mode():
    nvidia_smi.nvmInit()
    handle = nvidia_smi.nvmlDeviceGetHandleByIndex(0)
    clock_freqs = nvidia_smi.nvmlDeviceGetClockInfo(
        handle, nvidia_smi.NVML_CLOCK_GRAPHICS
    )
    current_freq = clock_freqs["current"]
    target_freq = int(current_freq * 1.05)
    command = f"nvidia-smi -ac {target_freq},{target_freq-100}"
    subprocess.run


subprocess.run(steam_cmd, shell=True)

