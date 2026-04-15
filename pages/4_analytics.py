import streamlit as st
import pandas as pd
import plotly.express as px
from storage import load_data

st.title("Price Analytics")

materials = load_data("materials")
price_history = load_data("price_history")

if not materials or not price_history:
    st.info("Not enough data available for analytics.")
else:
    material_map = {}
    for material in materials:
        material_map[material["material_id"]] = material["material_name"]

    history_rows = []
    for record in price_history:
        material_name = material_map.get(record["material_id"], "Unknown")
        history_rows.append({
            "history_id": record["history_id"],
            "material_id": record["material_id"],
            "material_name": material_name,
            "price": record["price"],
            "changed_on": record["changed_on"]
        })

    df = pd.DataFrame(history_rows)
    df["changed_on"] = pd.to_datetime(df["changed_on"])
    df = df.sort_values("changed_on")

    material_names = sorted(df["material_name"].unique())
    selected_material = st.selectbox("Select Material", material_names)

    filtered_df = df[df["material_name"] == selected_material]

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