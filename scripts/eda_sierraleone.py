"""
EDA script for Benin (Malanville) dataset.
Run this script to perform profiling, cleaning, and save a cleaned CSV.
Example: .\.venv\Scripts\python scripts\eda_benin.py --input data/benin-malanville.csv --sample 1000
"""

import argparse
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import zscore


def load_data(path, nrows=None):
    df = pd.read_csv(path, parse_dates=[0], nrows=nrows)
    df.columns = df.columns.str.strip().str.replace(' ', '').str.replace('\n', '')
    df.rename(columns={df.columns[0]: 'Timestamp'}, inplace=True)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
    df = df.set_index('Timestamp')
    return df


def summary_and_missing(df):
    desc = df.describe()
    missing_counts = df.isna().sum()
    missing_pct = (missing_counts / len(df)) * 100
    missing_report = pd.DataFrame({'missing_count': missing_counts, 'missing_pct': missing_pct})
    return desc, missing_report


def flag_outliers(df, cols):
    cols = [c for c in cols if c in df.columns]
    if not cols:
        df['outlier_flag'] = False
        return df
    z = df[cols].apply(lambda x: zscore(x, nan_policy='omit'))
    outlier_mask = (z.abs() > 3)
    df['outlier_flag'] = outlier_mask.any(axis=1)
    return df


def impute_median(df, cols):
    cols = [c for c in cols if c in df.columns]
    for c in cols:
        median = df[c].median()
        df[c] = df[c].fillna(median)
    return df


def plot_timeseries(df, cols, outdir):
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    for c in cols:
        if c in df.columns:
            plt.figure(figsize=(12,3))
            df[c].plot()
            plt.title(c)
            f = outdir / f'{c}_timeseries.png'
            plt.tight_layout()
            plt.savefig(f)
            plt.close()


def correlation_heatmap(df, cols, outdir):
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    cols = [c for c in cols if c in df.columns]
    if not cols:
        return
    plt.figure(figsize=(10,8))
    sns.heatmap(df[cols].corr(), annot=True, fmt='.2f', cmap='coolwarm')
    plt.title('Correlation heatmap')
    plt.tight_layout()
    plt.savefig(outdir / 'correlation_heatmap.png')
    plt.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', default='data/benin_clean.csv')
    parser.add_argument('--sample', type=int, default=None)
    parser.add_argument('--outdir', default='notebooks/outputs')
    args = parser.parse_args()

    df = load_data(args.input, nrows=args.sample)
    desc, missing_report = summary_and_missing(df)
    print('Description:')
    print(desc)
    print('\nMissing report (top):')
    print(missing_report.sort_values('missing_pct', ascending=False).head(20))

    key_cols = ['GHI','DNI','DHI','ModA','ModB','WS','WSgust']
    df = flag_outliers(df, key_cols)
    df = impute_median(df, key_cols)
    df['cleaning_flag'] = df['outlier_flag'] | df[key_cols].isna().any(axis=1)

    # plots
    plot_timeseries(df, ['GHI','DNI','DHI','Tamb'], args.outdir)
    correlation_heatmap(df, ['GHI','DNI','DHI','TModA','TModB','ModA','ModB','Tamb','RH','WS','WSgust'], args.outdir)

    df.to_csv(args.output)
    print('Wrote cleaned CSV to', args.output)


if __name__ == '__main__':
    main()
