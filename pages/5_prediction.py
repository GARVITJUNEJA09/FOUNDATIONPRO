import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from storage import load_data

st.title("Price Prediction")

materials = load_data("materials")
price_history = load_data("price_history")

if not materials or not price_history:
    st.info("Not enough data available for prediction.")
else:
    material_map = {}
    for material in materials:
        material_map[material["material_id"]] = material["material_name"]

    history_rows = []
    for record in price_history:
        history_rows.append({
            "material_id": record["material_id"],
            "material_name": material_map.get(record["material_id"], "Unknown"),
            "price": float(record["price"]),
            "changed_on": record["changed_on"]
        })

    df = pd.DataFrame(history_rows)
    df["changed_on"] = pd.to_datetime(df["changed_on"])

    material_names = sorted(df["material_name"].unique())
    selected_material = st.selectbox("Select Material for Prediction", material_names)

    material_df = df[df["material_name"] == selected_material].sort_values("changed_on").reset_index(drop=True)

    if len(material_df) < 2:
        st.warning("At least 2 price records are needed for prediction.")
    else:
        material_df["day_index"] = range(len(material_df))

        X = material_df[["day_index"]]
        y = material_df["price"]

        model = LinearRegression()
        model.fit(X, y)

        future_days = st.slider("Select number of future days", min_value=1, max_value=30, value=7)

        future_indexes = np.arange(len(material_df), len(material_df) + future_days).reshape(-1, 1)
        predicted_prices = model.predict(future_indexes)

        future_df = pd.DataFrame({
            "day_index": future_indexes.flatten(),
            "predicted_price": predicted_prices
        })

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=material_df["day_index"],
            y=material_df["price"],
            mode="lines+markers",
            name="Historical Price"
        ))

        fig.add_trace(go.Scatter(
            x=future_df["day_index"],
            y=future_df["predicted_price"],
            mode="lines+markers",
            name="Predicted Price"
        ))

        fig.update_layout(
            title=f"Price Prediction for {selected_material}",
            xaxis_title="Time Index",
            yaxis_title="Price",
            template="plotly_white"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Predicted Values")
        st.dataframe(future_df, use_container_width=True)