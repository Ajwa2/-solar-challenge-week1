# Scripts

This folder is for lightweight helper scripts related to the project.

To run the Streamlit app locally (after installing requirements):

```powershell
; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app/main.py
```

Notes:
- The Streamlit app expects cleaned CSVs under `data/` named `benin_clean.csv`, `sierraleone_clean.csv`, and `togo_clean.csv` if you want it to auto-load sample datasets.
- This repository does not commit data files — place them locally.
# Scripts

Small utility scripts used by the project. Keep CLI entry points here.
