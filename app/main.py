import streamlit as st
from app.utils import load_dataframe, summarize_metrics, boxplot_fig, timeseries_fig, run_stat_tests
import os
import pandas as pd


st.set_page_config(page_title="Solar Comparison", layout="wide")


def sidebar_controls(df):
    st.sidebar.header('Data & filters')
    upload = st.sidebar.file_uploader('Upload cleaned CSV (optional)', type=['csv'])
    daytime_only = st.sidebar.checkbox('Daytime only (GHI > 0)', value=False)
    metric = st.sidebar.selectbox('Metric', options=['GHI', 'DNI', 'DHI'])
    date_range = None
    load_demo = st.sidebar.button('Load demo data')
    if not df.empty and 'Timestamp' in df.columns:
        min_date = pd.to_datetime(df['Timestamp']).min()
        max_date = pd.to_datetime(df['Timestamp']).max()
        date_range = st.sidebar.date_input('Date range', value=(min_date.date(), max_date.date()))
    st.sidebar.markdown('---')
    return upload, daytime_only, metric, date_range


def main():
    st.title('Cross-country Solar Radiation Comparison')
    st.markdown('This app compares cleaned datasets (GHI/DNI/DHI) across countries.')

    # Try loading default cleaned files if present
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

    combined = pd.concat(dfs, axis=0, ignore_index=True) if dfs else pd.DataFrame()

    upload, daytime_only, metric, date_range = sidebar_controls(combined)

    # If user uploaded a file, replace combined with uploaded content
    if upload is not None:
        uploaded_df = load_dataframe(upload)
        if 'country' not in uploaded_df.columns:
            uploaded_df['country'] = st.text_input('Country name for uploaded file', value='Uploaded')
        combined = uploaded_df

    # Load demo data if requested (sample CSVs included in repo)
    if st.sidebar.button('Load demo data'):
        demo_paths = {
            'Benin': os.path.join('app','sample_data','benin_demo.csv'),
            'SierraLeone': os.path.join('app','sample_data','sierraleone_demo.csv'),
            'Togo': os.path.join('app','sample_data','togo_demo.csv'),
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
            st.success('Loaded demo data')

    # Apply filters
    if not combined.empty:
        df = combined.copy()
        if date_range:
            start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
            df = df[(pd.to_datetime(df['Timestamp']) >= start) & (pd.to_datetime(df['Timestamp']) <= end)]
        if daytime_only and 'GHI' in df.columns:
            df = df[df['GHI'] > 0]

        st.subheader('Summary statistics')
        summary = summarize_metrics(df, ['GHI', 'DNI', 'DHI'])
        if summary.empty:
            st.info('No GHI/DNI/DHI columns found in the data.')
        else:
            st.dataframe(summary)

        # Visuals
        st.subheader('Boxplot')
        fig = boxplot_fig(df, metric)
        if fig is not None:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(f'{metric} not available in dataset')

        st.subheader('Time series')
        tfig = timeseries_fig(df, metric)
        if tfig is not None:
            st.plotly_chart(tfig, use_container_width=True)
        else:
            st.info('Timestamp or metric missing for timeseries')

        # Statistical tests
        if st.button('Run statistical tests (ANOVA & Kruskal-Wallis)'):
            results = run_stat_tests(df, metric)
            st.write('ANOVA F:', results['anova_f'], 'p:', results['anova_p'])
            st.write('Kruskal H:', results['kruskal_h'], 'p:', results['kruskal_p'])

        # Post-hoc
        if st.checkbox('Run post-hoc pairwise tests (Tukey HSD)'):
            from app.utils import posthoc_tukey

            ph = posthoc_tukey(df, metric)
            if ph.empty:
                st.info('No post-hoc results (metric/country missing or insufficient data)')
            else:
                st.subheader('Tukey HSD pairwise comparisons')
                st.dataframe(ph)

    else:
        st.info('No data loaded. Place cleaned CSVs in `data/` or upload one via the sidebar.')


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