# subway-model

## About

An agent-based model for simulating subway lines.

You can see recordings of various simulation runs in the ``recordings/`` directory.

## Setup

Please use ``Python >3.12`` or a newer version.

We recommend to use ``uv`` package manager to manage dependencies and the virtual environment for this project. After ensuring Python and ``uv`` are installed on your system, proceed with the Automated or Manual Setup options to install and run simulations.


### Automated Setup

This (currently) only works on Windows.

#### Create environment

Simply run the ``setup.bat``to install the environment. 

#### Running simulations

Run the ``run.bat`` to start a simulation.
You can set different parameters at the top of the ``src/main.py`` file.


### Manual Setup

#### Create environment

First, create a uv venv using ``uv venv``, activate it using `.venv\Scripts\activate` and install packages from the pyproject.toml using ``uv sync``. Optional: Any new packages are added using ``uv add libraryname``. 


#### Running simulations

To start a simulation, run the main.py.

From repo root

```
python -m src.main
```

## Saving simulations (optional)

To save a simulation run as .mp4, you need to install ffmpeg and imagemagick on your machine.

How it worked on Leon's Windows PC:
- Open PowerShell as admin
- Install chocolatey using ``Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))``
- Install ffmpeg and imagemagick using ``choco install ffmpeg imagemagick -y``
- Restart PC


Then, ensure ``SAVE_VIDEO`` is set to `True` in the ``src/main.py`` file.

