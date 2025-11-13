import streamlit as st
from app.utils import (
    load_dataframe,
    summarize_metrics,
    boxplot_fig,
    timeseries_fig,
    run_stat_tests,
    posthoc_tukey,
)
import os
import pandas as pd


st.set_page_config(page_title="Solar Comparison", layout="wide")


def load_defaults():
    default_paths = {
        'Benin': os.path.join('data', 'benin_clean.csv'),
        'SierraLeone': os.path.join('data', 'sierraleone_clean.csv'),
        'Togo': os.path.join('data', 'togo_clean.csv'),
    }
    dfs = []
    for name, p in default_paths.items():
        if os.path.exists(p):
            df = load_dataframe(p)
            if not df.empty:
                df['country'] = name
                dfs.append(df)
    return pd.concat(dfs, axis=0, ignore_index=True) if dfs else pd.DataFrame()


def sidebar(df):
    st.sidebar.header('Controls')
    upload = st.sidebar.file_uploader('Upload cleaned CSV (optional)', type=['csv'])
    metric = st.sidebar.selectbox('Metric', options=['GHI', 'DNI', 'DHI'])
    daytime = st.sidebar.checkbox('Daytime only (GHI > 0)', value=False)
    top_n = st.sidebar.slider('Top N countries (by mean metric)', min_value=1, max_value=10, value=3)
    st.sidebar.markdown('---')
    demo = st.sidebar.button('Load demo data')
    return upload, metric, daytime, top_n, demo


def main():
    st.title('Cross-country Solar Dashboard')
    st.write('Interactive dashboard for comparing GHI/DNI/DHI across countries.')

    combined = load_defaults()

    upload, metric, daytime, top_n, demo = sidebar(combined)

    # handle upload
    if upload is not None:
        uploaded = load_dataframe(upload)
        if 'country' not in uploaded.columns:
            uploaded['country'] = st.text_input('Country name for uploaded file', value='Uploaded')
        combined = uploaded

    # demo data
    if demo:
        demo_paths = {
            'Benin': os.path.join('app', 'sample_data', 'benin_demo.csv'),
            'SierraLeone': os.path.join('app', 'sample_data', 'sierraleone_demo.csv'),
            'Togo': os.path.join('app', 'sample_data', 'togo_demo.csv'),
        }
        demo_dfs = []
        for name, p in demo_paths.items():
            if os.path.exists(p):
                d = load_dataframe(p)
                if not d.empty:
                    d['country'] = name
                    demo_dfs.append(d)
        if demo_dfs:
            combined = pd.concat(demo_dfs, axis=0, ignore_index=True)
            st.success('Demo data loaded')

    if combined.empty:
        st.info('No data loaded. Place cleaned CSVs in `data/` or upload one via the sidebar.')
        return

    # country selector
    countries = sorted(combined['country'].dropna().unique().tolist())
    selected = st.multiselect('Select countries', options=countries, default=countries)
    if not selected:
        st.warning('Select at least one country to display')
        return

    df = combined[combined['country'].isin(selected)].copy()
    if daytime and 'GHI' in df.columns:
        df = df[df['GHI'] > 0]

    # Summary
    st.subheader('Summary table')
    summary = summarize_metrics(df, ['GHI', 'DNI', 'DHI'])
    if summary.empty:
        st.info('No metrics found')
    else:
        st.dataframe(summary)

    # Visuals
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader(f'{metric} boxplot')
        fig = boxplot_fig(df, metric)
        if fig is not None:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(f'{metric} missing')

    with col2:
        st.subheader('Top countries by mean metric')
        if metric in df.columns:
            ranking = df.groupby('country')[metric].mean().sort_values(ascending=False).head(top_n).round(2)
            st.table(ranking.reset_index().rename(columns={metric: f'mean_{metric}'}))
        else:
            st.info(f'{metric} missing')

    # Time series
    st.subheader('Time series')
    tfig = timeseries_fig(df, metric)
    if tfig is not None:
        st.plotly_chart(tfig, use_container_width=True)

    # Statistical tests and post-hoc
    if st.button('Run statistical tests (ANOVA & Kruskal-Wallis)'):
        res = run_stat_tests(df, metric)
        st.write('ANOVA F:', res['anova_f'], 'p:', res['anova_p'])
        st.write('Kruskal H:', res['kruskal_h'], 'p:', res['kruskal_p'])

    if st.checkbox('Run post-hoc pairwise tests (Tukey HSD)'):
        ph = posthoc_tukey(df, metric)
        if ph.empty:
            st.info('No post-hoc results (insufficient data or missing metric)')
        else:
            st.subheader('Tukey HSD results')
            st.dataframe(ph)


if __name__ == '__main__':
    main()
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simple Dashboard", layout="wide")

with st.sidebar:
    selected_option = st.radio("Select an option:", [1, 2])

st.title("Simple Streamlit Dashboard")


if selected_option == 1:
    st.header("Option 1: Upload CSV and Plot Data")

    uploaded_file = st.file_uploader("Choose a CSV file to upload", type="csv")

    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.subheader("Uploaded Data Preview")
        st.dataframe(data.head())

        st.subheader("Graph of Uploaded Data")

        if st.checkbox("Show Plot"):
            if data.shape[1] >= 2: 
                x_col = st.selectbox("Select X-axis column", data.columns)
                y_col = st.selectbox("Select Y-axis column", data.columns)

                fig, ax = plt.subplots(figsize=(8, 2))
                ax.plot(data[x_col], data[y_col], marker='o', color='b')
                ax.set_xlabel(x_col)
                ax.set_ylabel(y_col)
                ax.set_title(f"{y_col} vs {x_col}")
                st.pyplot(fig)
            else:
                st.warning("Uploaded data must have at least two columns for plotting.")
    else:
        st.warning("Please upload a CSV file to display and plot the data.")


elif selected_option == 2:
    st.header("Display Sample Data and Plot")

    st.subheader("Sample Data Preview")
    sample_data = {
        "Month": ["January", "February", "March", "April", "May", "June"],
        "Sales": [250, 300, 450, 200, 500, 400]
    }
    df = pd.DataFrame(sample_data)
    st.dataframe(df)

    st.subheader("Sample Data Plot")
    fig, ax = plt.subplots(figsize=(8, 2))
    ax.plot(df["Month"], df["Sales"], marker='o', color='green')
    ax.set_xlabel("Month")
    ax.set_ylabel("Sales")
    ax.set_title("Monthly Sales")
    st.pyplot(fig)

    st.markdown("<h6 style='text-align: center;'>Dashboard Development 📊 using Streamlit</h6>", unsafe_allow_html=True)