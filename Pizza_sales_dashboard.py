# Import libraries
import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(page_title="Pizza Sales Dashboard", layout="wide")

# TITLE
st.title("🍕 Pizza Sales Interactive Dashboard")
st.markdown("Analyze revenue, orders, best sellers, and customer preferences.")

# LOAD DATA
df = pd.read_csv("pizza_sales.csv")

#DATA CLEANING
df = df.drop_duplicates()
df = df.dropna()

df['order_date'] = pd.to_datetime(df['order_date'], format='%d-%m-%Y')
df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
df['total_price'] = pd.to_numeric(df['total_price'], errors='coerce')

df = df[df['quantity'] > 0]
df = df[df['total_price'] > 0]

# Create additional columns
if 'order_time' in df.columns:
    df['hour'] = pd.to_datetime(df['order_time']).dt.hour

# SIDEBAR FILTERS
st.sidebar.header("🔎 Filters")

category_filter = st.sidebar.multiselect(
    "Select Pizza Category",
    options=sorted(df['pizza_category'].unique()),
    default=sorted(df['pizza_category'].unique())
)

size_filter = st.sidebar.multiselect(
    "Select Pizza Size",
    options=sorted(df['pizza_size'].unique()),
    default=sorted(df['pizza_size'].unique())
)

# Apply filters
filtered_df = df[
    (df['pizza_category'].isin(category_filter)) &
    (df['pizza_size'].isin(size_filter))
]

# KPI CALCULATIONS
total_revenue = filtered_df['total_price'].sum()
total_orders = filtered_df['order_id'].nunique()
total_pizzas_sold = filtered_df['quantity'].sum()
avg_order_value = total_revenue / total_orders if total_orders else 0
avg_pizzas_per_order = total_pizzas_sold / total_orders if total_orders else 0

# DISPLAY KPIs
k1, k2, k3, k4, k5 = st.columns(5)

k1.metric("Total Revenue", f"${total_revenue:,.0f}")
k2.metric("Total Orders", f"{total_orders:,}")
k3.metric("Total Pizzas Sold", f"{total_pizzas_sold:,}")
k4.metric("Avg Order Value", f"${avg_order_value:.2f}")
k5.metric("Avg Pizzas / Order", f"{avg_pizzas_per_order:.2f}")

# DAILY TREND
filtered_df['day'] = filtered_df['order_date'].dt.day_name()

day_order = [
    'Monday', 'Tuesday', 'Wednesday',
    'Thursday', 'Friday', 'Saturday', 'Sunday'
]

daily_orders = (
    filtered_df.groupby('day')['order_id']
    .nunique()
    .reindex(day_order)
    .reset_index()
)

fig1 = px.bar(
    daily_orders,
    x='day',
    y='order_id',
    title='Daily Trend for Total Orders'
)

# MONTHLY TREND
filtered_df['month'] = filtered_df['order_date'].dt.month_name()
filtered_df['month_number'] = filtered_df['order_date'].dt.month

monthly_orders = (
    filtered_df.groupby(['month', 'month_number'])['order_id']
    .nunique()
    .reset_index()
    .sort_values('month_number')
)

fig2 = px.line(
    monthly_orders,
    x='month',
    y='order_id',
    markers=True,
    title='Monthly Trend for Total Orders'
)

# SALES BY CATEGORY
category_sales = (
    filtered_df.groupby('pizza_category')['total_price']
    .sum()
    .reset_index()
)

fig3 = px.pie(
    category_sales,
    values='total_price',
    names='pizza_category',
    title='% Sales by Pizza Category'
)

# SALES BY SIZE
size_sales = (
    filtered_df.groupby('pizza_size')['total_price']
    .sum()
    .reset_index()
)

fig4 = px.pie(
    size_sales,
    values='total_price',
    names='pizza_size',
    title='% Sales by Pizza Size'
)

# FUNNEL CHART
category_quantity = (
    filtered_df.groupby('pizza_category')['quantity']
    .sum()
    .reset_index()
    .sort_values(by='quantity', ascending=False)
)

fig5 = px.funnel(
    category_quantity,
    x='quantity',
    y='pizza_category',
    title='Total Pizzas Sold by Category'
)

# TOP 5 BEST SELLERS
top_revenue = (
    filtered_df.groupby('pizza_name')['total_price']
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
)

fig6 = px.bar(
    top_revenue,
    x='pizza_name',
    y='total_price',
    title='Top 5 Best Sellers by Revenue'
)

top_quantity = (
    filtered_df.groupby('pizza_name')['quantity']
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
)

fig7 = px.bar(
    top_quantity,
    x='pizza_name',
    y='quantity',
    title='Top 5 Best Sellers by Quantity'
)

top_orders = (
    filtered_df.groupby('pizza_name')['order_id']
    .count()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
)

fig8 = px.bar(
    top_orders,
    x='pizza_name',
    y='order_id',
    title='Top 5 Best Sellers by Orders'
)

#BOTTOM 5 SELLERS
bottom_revenue = (
    filtered_df.groupby('pizza_name')['total_price']
    .sum()
    .sort_values()
    .head(5)
    .reset_index()
)

fig9 = px.bar(
    bottom_revenue,
    x='pizza_name',
    y='total_price',
    title='Bottom 5 by Revenue'
)

bottom_quantity = (
    filtered_df.groupby('pizza_name')['quantity']
    .sum()
    .sort_values()
    .head(5)
    .reset_index()
)

fig10 = px.bar(
    bottom_quantity,
    x='pizza_name',
    y='quantity',
    title='Bottom 5 by Quantity'
)

bottom_orders = (
    filtered_df.groupby('pizza_name')['order_id']
    .count()
    .sort_values()
    .head(5)
    .reset_index()
)

fig11 = px.bar(
    bottom_orders,
    x='pizza_name',
    y='order_id',
    title='Bottom 5 by Orders'
)

#REVENUE BY HOUR

if 'hour' in filtered_df.columns:
    hourly_sales = (
        filtered_df.groupby('hour')['total_price']
        .sum()
        .reset_index()
    )

    fig12 = px.line(
        hourly_sales,
        x='hour',
        y='total_price',
        markers=True,
        title='Revenue by Hour'
    )

# DASHBOARD LAYOUT

# Row 1
c1, c2 = st.columns(2)
with c1:
    st.plotly_chart(fig1, use_container_width=True)
with c2:
    st.plotly_chart(fig2, use_container_width=True)

# Row 2
c3, c4 = st.columns(2)
with c3:
    st.plotly_chart(fig3, use_container_width=True)
with c4:
    st.plotly_chart(fig4, use_container_width=True)

# Row 3
st.plotly_chart(fig5, use_container_width=True)

# Row 4 (Optional Hourly Revenue)
if 'hour' in filtered_df.columns:
    st.plotly_chart(fig12, use_container_width=True)

# Row 5 – Top 5
st.subheader('🏆 Top 5 Best Sellers')
t1, t2, t3 = st.columns(3)
with t1:
    st.plotly_chart(fig6, use_container_width=True)
with t2:
    st.plotly_chart(fig7, use_container_width=True)
with t3:
    st.plotly_chart(fig8, use_container_width=True)

# Row 6 – Bottom 5
st.subheader('📉 Bottom 5 Sellers')
b1, b2, b3 = st.columns(3)
with b1:
    st.plotly_chart(fig9, use_container_width=True)
with b2:
    st.plotly_chart(fig10, use_container_width=True)
with b3:
    st.plotly_chart(fig11, use_container_width=True)

# KEY INSIGHTS
st.subheader('💡 Key Insights')

if not category_sales.empty:
    best_category = category_sales.sort_values(
        'total_price', ascending=False
    ).iloc[0]['pizza_category']

    best_pizza = top_revenue.iloc[0]['pizza_name']

    st.write(f'• Highest revenue category: **{best_category}**')
    st.write(f'• Best-selling pizza by revenue: **{best_pizza}**')
    st.write(f'• Average order value: **${avg_order_value:.2f}**')

# DOWNLOAD FILTERED DATA
st.subheader('⬇ Download Filtered Data')

csv = filtered_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label='Download CSV',
    data=csv,
    file_name='filtered_pizza_sales.csv',
    mime='text/csv'
)

# DATA PREVIEW
st.subheader('📄 Dataset Preview')
st.dataframe(filtered_df.head(20))


