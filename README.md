# subway-model

## About

An agent-based model for simulating subway lines.


## Setup


### Running simulations

Use Python 3.12 or a similar version. Create a virtual environment using ``python -m venv venv``, activate it (Windows: ``venv\Scripts\activate`` , Linux/macOS: ``source venv/bin/activate``) and use ``pip install -r requirements.txt`` to install the necessary packages into the venv.

To start a simulation, run the main.py.


### Saving simulations (optional)

To save a simulation run as .mp4, you need to install ffmpeg and imagemagick on your machine.

How it worked on Leon's Windows PC:
- Open PowerShell as admin
- Install chocolatey using ``Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))``
- Install ffmpeg and imagemagick using ``choco install ffmpeg imagemagick -y``
- Restart PC


