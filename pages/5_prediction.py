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
    material_map = {material["material_id"]: material["material_name"] for material in materials}

    rows = []
    for record in price_history:
        rows.append({
            "material_id": record["material_id"],
            "material_name": material_map.get(record["material_id"], "Unknown"),
            "price": float(record["price"]),
            "changed_on": record["changed_on"]
        })

    df = pd.DataFrame(rows)
    df["changed_on"] = pd.to_datetime(df["changed_on"])

    material_names = sorted(df["material_name"].unique())
    selected_material = st.selectbox("Select Material for Prediction", material_names)

    material_df = (
        df[df["material_name"] == selected_material]
        .sort_values("changed_on")
        .reset_index(drop=True)
    )

    if len(material_df) < 2:
        st.warning("At least 2 price records are needed for prediction.")
    else:
        material_df["day_index"] = np.arange(len(material_df))
        X = material_df[["day_index"]]
        y = material_df["price"]

        model = LinearRegression()
        model.fit(X, y)

        forecast_days = st.slider("Forecast next N periods", min_value=1, max_value=12, value=5)

        future_indexes = np.arange(len(material_df), len(material_df) + forecast_days)
        predicted_prices = model.predict(future_indexes.reshape(-1, 1))

        last_date = material_df["changed_on"].max()
        future_dates = pd.date_range(last_date + pd.Timedelta(days=7), periods=forecast_days, freq="7D")

        forecast_df = pd.DataFrame({
            "Date": future_dates,
            "Predicted Price": np.round(predicted_prices, 2)
        })

        latest_actual = round(material_df["price"].iloc[-1], 2)
        first_predicted = round(float(forecast_df["Predicted Price"].iloc[0]), 2)
        overall_change = round(first_predicted - latest_actual, 2)

        k1, k2, k3 = st.columns(3)
        with k1:
            st.metric("Latest Actual Price", latest_actual)
        with k2:
            st.metric("Next Predicted Price", first_predicted)
        with k3:
            st.metric("Predicted Change", overall_change)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=material_df["changed_on"],
            y=material_df["price"],
            mode="lines+markers",
            name="Historical Price"
        ))
        fig.add_trace(go.Scatter(
            x=forecast_df["Date"],
            y=forecast_df["Predicted Price"],
            mode="lines+markers",
            name="Predicted Price"
        ))

        fig.update_layout(
            title=f"Historical vs Predicted Price for {selected_material}",
            xaxis_title="Date",
            yaxis_title="Price",
            template="plotly_white"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Forecast Table")
        st.dataframe(forecast_df, use_container_width=True)

        st.caption("Prediction uses a simple linear regression on historical price points.")