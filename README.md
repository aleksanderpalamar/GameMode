# GameMode

Este é um script em Python que permite que você inicie o Steam no modo Big Picture e ajuste a prioridade do processo para melhor desempenho enquanto joga.

## Requisitos

- Python 3.x
- Módulo psutil instalado (você pode instalá-lo executando pip install psutil no terminal)

## Como usar

1. Baixe o script GameMode.py.
2. Certifique-se de ter o Python 3.x instalado e o módulo psutil.
3. Abra um terminal e navegue até o diretório onde o script está localizado.
4. Execute o comando python GameMode.py.

O script irá verificar se o Steam já está em execução e, se estiver, ajustará a prioridade do processo para melhor desempenho. Em seguida, o script iniciará o Steam no modo Big Picture para facilitar a navegação com o controle enquanto joga.

## Observação

Este script é compatível com o Windows e o Linux. Certifique-se de que o Steam esteja instalado em seu sistema operacional antes de executar o script.

## Documentação

```python
steam_cmd = "steam -bigpicture"
name = "steam.exe" if platform.system() == "Windows" else "steam"

if platform.system() == "Windows":
    steam_cmd = "start steam -bigpicture"
elif platform.system() == "Linux":
    steam_cmd = "steam -bigpicture"
```

Este trecho de código define o comando que será usado para abrir o Steam no modo Big Picture, dependendo do sistema operacional em que o código está sendo executado. No Windows, é usado o comando "start steam -bigpicture", enquanto no Linux é usado o comando "steam -bigpicture". O nome do processo do Steam também é definido com base no sistema operacional para que ele possa ser identificado mais tarde.

```python
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
```

Este trecho de código verifica se o processo do Steam já está em execução e, se estiver, aumenta a prioridade do processo para melhorar o desempenho. Para fazer isso, ele obtém o PID do processo do Steam e usa a biblioteca psutil para aumentar a prioridade do processo.

```python
def has_dedicated_gpu():
    return next(
        (
            True
            for gpu in psutil.gpu_devices()
            if gpu.get("memory_total") and gpu.get("memory_total") > 0
        ),
        False,
    )
```
Esta função verifica se o sistema tem uma GPU dedicada instalada. Ele usa a biblioteca psutil para encontrar dispositivos de GPU e verifica se há pelo menos um dispositivo com memória total maior que zero.

```python
def is_game_running():
    return next(
        (
            True
            for p in psutil.process_iter(["pid", "name"])
            if p.info["name"] == "game.exe"
        ),
        False,
    )
```
Esta função verifica se um jogo está em execução. Ele usa a biblioteca psutil para encontrar processos com o nome "game.exe" e retorna True se encontrar pelo menos um processo.

```python
def is_steam_running():
    return next(
        (
            True
            for p in psutil.process_iter(["pid", "name"])
            if p.info["name"] == "steam.exe"
        ),
        False,
    )
```
Esta função verifica se o Steam está em execução. Ele usa a biblioteca psutil para encontrar processos com o nome "steam.exe" e retorna True se encontrar pelo menos um processo.

```python
def set_game_mode():
    nvidia_smi.nvmInit()
    handle = nvidia_smi.nvmlDeviceGetHandleByIndex(0)
    clock_freqs = nvidia_smi.nvmlDeviceGetClockInfo(
        handle, nvidia_smi.NVML_CLOCK_GRAPHICS
    )
    current_freq = clock_freqs["current"]
    target_freq = int(current_freq * 1.05)
    command = f"nvidia-smi -ac {target_freq},{target_freq-100}"
    subprocess.run(command, shell=True) if has_dedicated_gpu() else None
```
Esta função ajusta a frequência da GPU para melhor desempenho. Ele usa a biblioteca nvidia-ml-py3 para obter a frequência atual da GPU e aumentá-la em 5%. Em seguida, ele usa o comando nvidia-smi para definir a frequência da GPU para o novo valor.

## Contribuição

Sinta-se livre para contribuir com este projeto! Se você encontrar algum bug ou tiver alguma sugestão, abra uma issue. Se você quiser implementar uma melhoria, sinta-se à vontade para criar um pull request.
