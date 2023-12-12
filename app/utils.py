import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go


def show_bar_plots(df):
    fig = px.bar(df, x='GENDER', y=['LOAN_NUM_TOTAL', 'LOAN_NUM_CLOSED'], barmode='group',
                 color_discrete_sequence=px.colors.qualitative.Alphabet)
    st.plotly_chart(fig)


def show_scatter_3d(df):
    fig = px.scatter_3d(df, x='AGE', y='TARGET', z='LOAN_NUM_TOTAL', color='TARGET', opacity=0.7)
    st.plotly_chart(fig)


def show_heatmap(df):
    df_features = df[df.columns.difference(['ID', 'AGREEMENT_RK'])]
    fig = plt.figure(figsize=(15, 15))
    sns.heatmap(df_features.corr(), cmap='BuGn', annot=True, linewidths=0.5, fmt=".2f")
    st.pyplot(fig)


def show_hist(df):
    df_features = df[['AGE', 'PERSONAL_INCOME', 'LOAN_NUM_CLOSED', 'TARGET', 'LOAN_NUM_TOTAL']]
    for i, col in enumerate(df_features.columns):
        fig = px.histogram(df, x=col, color_discrete_sequence=px.colors.qualitative.Plotly)
        fig.update_layout(bargap=0.2)
        st.plotly_chart(fig, use_container_width=True)


def show_avg_min_max(df):
    df_features = df[['AGE', 'PERSONAL_INCOME', 'GENDER', 'TARGET', 'LOAN_NUM_CLOSED', 'LOAN_NUM_TOTAL']]
    for col in df_features.columns:
        if col == 'TARGET':
            continue
        grp = df_features.groupby('TARGET').agg({col: {"min", "max", "mean"}})
        grp.columns = ["_".join(col) for col in grp.columns]
        grp = grp.reset_index()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=grp['TARGET'],
                                 y=grp[f"{col}_min"],
                                 mode="markers",
                                 showlegend=False,
                                 marker=dict(color="blue",
                                             size=10)))

        fig.add_trace(go.Scatter(x=grp['TARGET'],
                                 y=grp[f"{col}_mean"],
                                 mode="markers",
                                 showlegend=False,
                                 marker=dict(color="blue",
                                             size=20)))

        fig.add_trace(go.Scatter(x=grp['TARGET'],
                                 y=grp[f"{col}_max"],
                                 mode="markers",
                                 showlegend=False,
                                 marker=dict(color="blue",
                                             size=10)))

        for i, row in grp.iterrows():
            if row[f"{col}_min"] != row[f"{col}_max"]:
                fig.add_shape(
                    dict(type="line",
                         x0=row['TARGET'],
                         x1=row['TARGET'],
                         y0=row[f"{col}_min"],
                         y1=row[f"{col}_max"],
                         line=dict(
                             color="blue",
                             width=2)
                         )
                )
        fig.update_layout(title=f"{' '.join(col.split('_'))} Avg-Max-Min Graph", xaxis_title='TARGET',
                          yaxis_title=' '.join(col.split('_')))
        st.plotly_chart(fig, use_container_width=True)
