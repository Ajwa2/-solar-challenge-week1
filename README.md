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

## Streamlit Dashboard — Development & Usage

This repository includes a Streamlit app at `app/main.py` for interactive comparison of solar radiation datasets (GHI/DNI/DHI).

Development notes
- Branch: create feature branches for dashboard work (we use `dashboard-dev` for UI changes).
- Keep the `data/` folder ignored by git. The app reads local CSVs named `benin_clean.csv`, `sierraleone_clean.csv`, and `togo_clean.csv` under `data/` if present.
- Demo CSVs (small synthetic examples) live under `app/sample_data/` and are optional.

Run locally
1. Activate your venv (PowerShell):

```powershell
; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app/main.py
```

2. Use the sidebar to upload a CSV or load demo data. Select metric, countries, and run statistical tests.

Committing & PRs
- Commit message for the first UI commit: `feat: basic Streamlit UI`.
- Create a PR from `dashboard-dev` into `main` when ready.

Deploying to Streamlit Community Cloud
- Create a new app on Streamlit Cloud, point it at this repo and branch `dashboard-dev`, and set the run command to:

```
streamlit run app/main.py
```

Security & data
- Do not commit raw data to the repository. Use the app uploader or an external data host.

