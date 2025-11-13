import io
from typing import Dict, List, Optional

import pandas as pd
import plotly.express as px
import numpy as np
from scipy import stats


def load_dataframe(src) -> pd.DataFrame:
    """Load a CSV dataframe from a path or file-like object.

    - Accepts a filesystem path (str) or a file-like (e.g., uploaded file).
    - Parses the first column as Timestamp and normalizes column names.
    """
    if src is None:
        return pd.DataFrame()
    if isinstance(src, str):
        df = pd.read_csv(src, parse_dates=[0], index_col=0)
    else:
        # file-like (BytesIO / UploadedFile)
        df = pd.read_csv(io.BytesIO(src.read()), parse_dates=[0], index_col=0)
    # normalize column names
    df.columns = df.columns.str.strip().str.replace('\n', ' ').str.replace(' ', '')
    # ensure Timestamp is a column (reset index)
    df = df.reset_index().rename(columns={'index': 'Timestamp'})
    try:
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
    except Exception:
        pass
    return df


def summarize_metrics(df: pd.DataFrame, metrics: List[str]) -> pd.DataFrame:
    existing = [m for m in metrics if m in df.columns]
    if not existing:
        return pd.DataFrame()
    return df.groupby('country')[existing].agg(['mean', 'median', 'std']).round(2)


def boxplot_fig(df: pd.DataFrame, metric: str):
    if metric not in df.columns:
        return None
    fig = px.box(df, x='country', y=metric, points='outliers', title=f'{metric} by country')
    return fig


def timeseries_fig(df: pd.DataFrame, metric: str):
    if metric not in df.columns:
        return None
    if 'Timestamp' not in df.columns:
        return None
    fig = px.line(df, x='Timestamp', y=metric, color='country', title=f'{metric} time series')
    return fig


def run_stat_tests(df: pd.DataFrame, metric: str) -> Dict[str, Optional[float]]:
    """Run ANOVA and Kruskal-Wallis across countries for metric. Returns dict of results."""
    result = {'anova_f': None, 'anova_p': None, 'kruskal_h': None, 'kruskal_p': None}
    if metric not in df.columns:
        return result
    groups = [g[metric].dropna().values for _, g in df.groupby('country')]
    groups = [g for g in groups if len(g) > 0]
    if len(groups) < 2:
        return result
    try:
        fstat, pval = stats.f_oneway(*groups)
        result['anova_f'] = float(fstat)
        result['anova_p'] = float(pval)
    except Exception:
        pass
    try:
        h, p = stats.kruskal(*groups)
        result['kruskal_h'] = float(h)
        result['kruskal_p'] = float(p)
    except Exception:
        pass
    return result
