# -solar-challenge-week1

Short project README — how to use the virtual environment and install dependencies.

## Python virtual environment (venv)

This project uses a local virtual environment stored at `.venv`.

Activate the venv (PowerShell):

```powershell
# Activate in the current PowerShell session
.\.venv\Scripts\Activate.ps1

# If Activation is blocked, run this to temporarily bypass execution policy for the script
powershell -ExecutionPolicy ByPass -File .\.venv\Scripts\Activate.ps1
```

Activate the venv (cmd):

```cmd
.\.venv\Scripts\activate
```

Verify:

```powershell
python --version
pip --version
```

Install dependencies from `requirements.txt`:

```powershell
pip install -r requirements.txt
```

## Conda alternative

If you prefer `conda`, create and activate an environment instead:

```powershell
# Create conda env with Python 3.12
conda create -n myenv python=3.12 -y
conda activate myenv
# Install from requirements with pip or conda
pip install -r requirements.txt
```

## Git

The repository ignores the `.venv/` folder and other common artifacts (see `.gitignore`).

## Next steps

- Add your dependencies to `requirements.txt`.
- Optionally add development tools (black, pytest) and a `Makefile` or scripts for common tasks.
