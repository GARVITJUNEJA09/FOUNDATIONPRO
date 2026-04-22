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
    material_map = {material["material_id"]: material["material_name"] for material in materials}

    history_rows = []
    for record in price_history:
        history_rows.append({
            "History ID": record["history_id"],
            "Material ID": record["material_id"],
            "Material": material_map.get(record["material_id"], "Unknown"),
            "Price": float(record["price"]),
            "Date": record["changed_on"]
        })

    df = pd.DataFrame(history_rows)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")

    categories = sorted({material["category"] for material in materials})
    material_names = sorted(df["Material"].unique())

    c1, c2 = st.columns(2)
    with c1:
        selected_category = st.selectbox("Filter by Category", ["All"] + categories)
    with c2:
        selected_material = st.selectbox("Select Material", material_names)

    if selected_category != "All":
        allowed_material_ids = {
            material["material_id"]
            for material in materials
            if material["category"] == selected_category
        }
        df = df[df["Material ID"].isin(allowed_material_ids)]

    filtered_df = df[df["Material"] == selected_material]

    if filtered_df.empty:
        st.warning("No records found for this filter combination.")
    else:
        latest_price = filtered_df["Price"].iloc[-1]
        avg_price = round(filtered_df["Price"].mean(), 2)
        min_price = filtered_df["Price"].min()
        max_price = filtered_df["Price"].max()

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Latest Price", latest_price)
        with m2:
            st.metric("Average Price", avg_price)
        with m3:
            st.metric("Min Price", min_price)
        with m4:
            st.metric("Max Price", max_price)

        fig = px.line(
            filtered_df,
            x="Date",
            y="Price",
            title=f"Price History for {selected_material}",
            markers=True
        )
        fig.update_layout(template="plotly_white", xaxis_title="Date", yaxis_title="Price")
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Material Price History")
        st.dataframe(filtered_df, use_container_width=True)

        trend_df = (
            df.groupby("Material", as_index=False)["Price"]
            .mean()
            .sort_values("Price", ascending=False)
            .head(10)
        )

        bar_fig = px.bar(
            trend_df,
            x="Material",
            y="Price",
            title="Top 10 Materials by Average Price"
        )
        bar_fig.update_layout(template="plotly_white", xaxis_title="Material", yaxis_title="Average Price")
        st.plotly_chart(bar_fig, use_container_width=True)