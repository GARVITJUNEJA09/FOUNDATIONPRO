import streamlit as st
import pandas as pd
import plotly.express as px
from storage import load_data

st.title("Price Analytics")

# Load materials and their price history from JSON files.
materials = load_data("materials")
price_history = load_data("price_history")

if not materials or not price_history:
    st.info("Not enough data available for analytics.")
else:
    # Build a quick lookup so we can show material names
    # instead of only material IDs in the chart and table.
    material_map = {
        material["material_id"]: material["material_name"]
        for material in materials
    }

    # Turn raw history records into a cleaner table for pandas and Plotly.
    history_rows = []
    for record in price_history:
        history_rows.append({
            "history_id": record["history_id"],
            "material_id": record["material_id"],
            "material_name": material_map.get(record["material_id"], "Unknown"),
            "price": record["price"],
            "changed_on": record["changed_on"]
        })

    df = pd.DataFrame(history_rows)

    # Convert the saved date text into actual datetime values
    # so sorting and charting work properly.
    df["changed_on"] = pd.to_datetime(df["changed_on"])
    df = df.sort_values("changed_on")

    # Let the user focus on one material at a time.
    material_names = sorted(df["material_name"].unique())
    selected_material = st.selectbox("Select Material", material_names)

    filtered_df = df[df["material_name"] == selected_material]

    # Line chart works best here because we want to show price change over time.
    fig = px.line(
        filtered_df,
        x="changed_on",
        y="price",
        title=f"Price History for {selected_material}",
        markers=True
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Price History Table")
    st.dataframe(filtered_df, use_container_width=True)