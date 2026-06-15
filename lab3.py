"""
visualizations/heatmap.py
-------------------------
2.3 Heatmap

Purpose: Represent the average fare as colour intensity across a grid of
Passenger Class (x) × Gender (y) cells. Darker blue cells indicate higher
average fares, making patterns visible at a glance.
"""

import altair as alt
import streamlit as st


def render(df):
    st.header("2.3 Heatmap")
    st.write("Average fare for each Passenger Class and Gender combination.")

    # Aggregate: mean fare per class × gender
    heat_data = (
        df.groupby(["pclass_label", "sex"])["fare"]
        .mean()
        .reset_index()
        .rename(columns={"fare": "avg_fare"})
    )

    chart = (
        alt.Chart(heat_data)
        .mark_rect()
        .encode(
            x=alt.X(
                "pclass_label:N",
                title="Passenger Class",
                sort=["1st", "2nd", "3rd"],
                axis=alt.Axis(labelAngle=0),
            ),
            y=alt.Y("sex:N", title="Gender"),
            color=alt.Color(
                "avg_fare:Q",
                scale=alt.Scale(scheme="blues"),
                legend=alt.Legend(title="Avg Fare (£)"),
            ),
            tooltip=[
                alt.Tooltip("pclass_label:N", title="Class"),
                alt.Tooltip("sex:N", title="Gender"),
                alt.Tooltip("avg_fare:Q", title="Avg Fare (£)", format=".2f"),
            ],
        )
        .properties(
            width=500,
            height=200,
            title="Heatmap: Average Fare by Class and Gender",
        )
    )

    st.altair_chart(chart, use_container_width=True)
    st.write(
        "Darker blue cells indicate higher average fares. "
        "Hover over any cell to see the exact value."
    )
    st.info(
        "💡 **Insight:** Female passengers in 1st class paid the highest average fare. "
        "Gender differences narrow significantly in 3rd class, where fares are low for all."
    )
    st.caption(
        "Task: Which Class and Gender combination has the highest average fare? "
        "Does gender always correlate with fare differences?"
    )
