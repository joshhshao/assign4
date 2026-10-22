# Import necessary packages (Make sure to also include in "requirements.txt" in this repository.)
import streamlit as st
import pandas as pd

# Print Title for the App
st.title("Microsoft Stock Data Dashboard by Joshua Shao")

# Read CSV file with stock data (CSV file must be in 'main' folder for your assignment 4 repository) 
df = pd.read_csv("msft.csv")

# Set up the 4 tabs on the Dashboard
tabs = st.tabs(["📋 Raw Data", "📈 Price Chart", "📊 Volume Chart","* Fun Tab"])

# Tab 1: Raw Data
with tabs[0]:
    st.subheader(f"Raw Data for MSFT")
    st.dataframe(df, use_container_width=True)

# Tab 2: Closing Price Chart
with tabs[1]:
    st.subheader(f"Closing Price for MSFT")
    st.line_chart(df['Close'])

# Tab 3: Volume Chart
with tabs[2]:
    st.subheader(f"Volume for MSFT")
    st.bar_chart(df['Volume'])

# Tab 4: Volume Chart
with tabs[3]:
    
    st.header("🏢 Fixed Asset Depreciation Calculator")
    st.write(
        "Calculate and record asset depreciation schedules using standard accounting methods."
    )

    # 1. Asset Input Layout
    col1, col2 = st.columns(2)
    with col1:
        asset_name = st.text_input("Asset Name", value="Delivery Truck")
        asset_cost = st.number_input(
            "Asset Cost ($)", min_value=0.0, value=50000.0, step=1000.0
        )
    with col2:
        salvage_value = st.number_input(
            "Salvage Value ($)", min_value=0.0, value=5000.0, step=500.0
        )
        useful_life = st.number_input(
            "Useful Life (Years)", min_value=1, value=5, step=1
        )

    # Validation check
    if salvage_value > asset_cost:
        st.error("Salvage value cannot be higher than the initial asset cost.")
    else:
        # 2. Accounting Calculation Logic
        depreciable_base = asset_cost - salvage_value
        straight_line_annual = depreciable_base / useful_life

        # Generate the schedule table data
        schedule_data = []
        current_book_value = asset_cost
        accumulated_depreciation = 0.0

        for year in range(1, int(useful_life) + 1):
            expense = straight_line_annual
            accumulated_depreciation += expense
            current_book_value -= expense

            schedule_data.append(
                {
                    "Year": f"Year {year}",
                    "Depreciation Expense": round(expense, 2),
                    "Accumulated Depreciation": round(accumulated_depreciation, 2),
                    "Book Value": round(current_book_value, 2),
                }
            )

        df_schedule = pd.DataFrame(schedule_data)

        # 3. High-Level Summary Metrics
        st.subheader("📊 Financial Summary")
        m1, m2, m3 = st.columns(3)
        m1.metric(
            label="Depreciable Base", value=f"${depreciable_base:,.2f}"
        )
        m2.metric(
            label="Annual Expense (Straight-Line)",
            value=f"${straight_line_annual:,.2f}",
        )
        m3.metric(
            label="Final Book Value (Salvage)",
            value=f"${current_book_value:,.2f}",
        )

        # 4. Interactive Schedule Table
        st.subheader("📅 Depreciation Schedule")
        st.dataframe(df_schedule, use_container_width=True, hide_index=True)

        # 5. Visual Expense Chart
        st.subheader("📉 Book Value Over Time")
        # Creating a simple line chart to visualize the asset's declining value
        chart_df = df_schedule.set_index("Year")[["Book Value"]]
        st.line_chart(chart_df)
