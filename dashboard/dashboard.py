import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
from babel.numbers import format_currency
sns.set(style='dark')

# Set layout untuk judul di samping (navbar)
st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

@st.cache_data(show_spinner=False, persist=True)
def load_data():
    data = pd.read_csv('/workspaces/ecommerce-data-analysis/dashboard/all_data.csv', parse_dates=['order_purchase_timestamp'])
    required_columns = [
        'order_id', 'customer_id', 'order_purchase_timestamp', 'order_status',
        'customer_unique_id', 'customer_city', 'price', 'product_id',
        'product_category_name', 'review_score'
    ]
    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    return data

data = load_data()


st.sidebar.markdown("### Filter Tanggal")

# Filter tanggal interaktif dengan kalender
start_date = st.sidebar.date_input("Start Date", value=data['order_purchase_timestamp'].min())
end_date = st.sidebar.date_input("End Date", value=data['order_purchase_timestamp'].max())

# Filter data sesuai tanggal
filtered_data = data[(data['order_purchase_timestamp'] >= pd.Timestamp(start_date)) & 
                     (data['order_purchase_timestamp'] <= pd.Timestamp(end_date))]

st.title("E-Commerce Dashboard :sparkles:")

# Visualisasi Daily Orders
st.subheader('Daily Orders')

daily_data = filtered_data.groupby(filtered_data['order_purchase_timestamp'].dt.date).agg(
    order_count=('order_id', 'count'),
    revenue=('price', 'sum')
).reset_index()

col1, col2 = st.columns(2)

with col1:
    total_orders = daily_data['order_count'].sum()
    st.metric("Total Orders", value=total_orders)

with col2:
    total_revenue = format_currency(daily_data['revenue'].sum(), "USD", locale='en_US')
    st.metric("Total Revenue", value=total_revenue)

# Line chart untuk daily orders
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_data["order_purchase_timestamp"],
    daily_data["order_count"],
    marker='o',
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

# Visualisasi top 5 kota dengan customer terbanyak
top_cities = filtered_data['customer_city'].value_counts().head(5).reset_index()
top_cities.columns = ['City', 'Number of Customers']

st.header("Top 5 Cities by Number of Customers")
fig = px.bar(top_cities, x='City', y='Number of Customers', color='City', title="Customer Demographics")
st.plotly_chart(fig)

# Hitung total revenue dan total orders per product
product_performance = filtered_data.groupby('product_category_name').agg(
    total_revenue=('price', 'sum'),
    total_orders=('order_id', 'count')
).reset_index()

# Best and Worst Performing Products (top 5 dan bottom 5)
top_products = product_performance.nlargest(5, 'total_revenue')
worst_products = product_performance.nsmallest(5, 'total_revenue')

# Visualisasi Best & Worst Performing Products
st.subheader("Best & Worst Performing Product")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

# Best Performing Product
best_palette = sns.color_palette("Blues", n_colors=5)  # Palet biru
best_palette = best_palette[::-1]
sns.barplot(x="total_revenue", y="product_category_name", data=top_products, palette=best_palette, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Total Revenue", fontsize=30, labelpad=20)
ax[0].set_title("Best Performing Product", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

# Worst Performing Product
worst_palette = sns.color_palette("Reds", n_colors=5)  # Palet merah
worst_palette = worst_palette[::-1]
sns.barplot(x="total_revenue", y="product_category_name", data=worst_products, palette=worst_palette, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Total Revenue", fontsize=30, labelpad=20)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Performing Product", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

# Display the plot
st.pyplot(fig)

# Menghitung Recency, Frequency, dan Monetary secara terpisah
recency_df = filtered_data.groupby('customer_unique_id').agg(
    recency=('order_purchase_timestamp', lambda x: (pd.Timestamp(end_date) - x.max()).days)
).reset_index()

frequency_df = filtered_data.groupby('customer_unique_id').agg(
    frequency=('order_id', 'nunique')
).reset_index()

monetary_df = filtered_data.groupby('customer_unique_id').agg(
    monetary=('price', 'sum')
).reset_index()

# Gabungkan ketiga metrik
rfm_df = pd.merge(frequency_df, monetary_df, on='customer_unique_id', how='left')
rfm_df = pd.merge(rfm_df, recency_df, on='customer_unique_id', how='left')

# Format customer_unique_id_y to show only the first 2 and last 2 characters, with '...' in between
rfm_df['customer_id_display'] = rfm_df['customer_unique_id'].apply(lambda x: f"{x[:2]}..{x[-2:]}" if isinstance(x, str) else x)

# Visualisasi RFM Analysis
st.subheader("Best Customer Based on RFM Parameters")

# Menampilkan metrik rata-rata Recency, Frequency, dan Monetary
col1, col2, col3 = st.columns(3)

with col1:
    avg_recency = round(rfm_df.recency.mean(), 1)
    st.metric("Average Recency (days)", value=avg_recency)

with col2:
    avg_frequency = round(rfm_df.frequency.mean(), 2)
    st.metric("Average Frequency", value=avg_frequency)

with col3:
    avg_monetary = format_currency(rfm_df.monetary.mean(), "AUD", locale='es_CO') 
    st.metric("Average Monetary", value=avg_monetary)

# Plot RFM Analysis - 3 Bar Plots: Recency, Frequency, and Monetary
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(35, 15))

# Use color palette from seaborn for more aesthetic bar charts
recency_palette = sns.color_palette("Blues", n_colors=5)  # Blue tones for Recency
sns.barplot(y="recency", x="customer_id_display", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette=recency_palette, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Customer ID", fontsize=30, labelpad=20)
ax[0].set_title("By Recency (days)", loc="center", fontsize=40)
ax[0].tick_params(axis='y', labelsize=25)
ax[0].tick_params(axis='x', labelsize=25)

# Frequency Palette (Red tones)
frequency_palette = sns.color_palette("Reds", n_colors=5)
sns.barplot(y="frequency", x="customer_id_display", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette=frequency_palette, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Customer ID", fontsize=30, labelpad=20)
ax[1].set_title("By Frequency", loc="center", fontsize=40)
ax[1].tick_params(axis='y', labelsize=25)
ax[1].tick_params(axis='x', labelsize=25)

# Monetary Palette (Green tones)
monetary_palette = sns.color_palette("Greens", n_colors=5)
sns.barplot(y="monetary", x="customer_id_display", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=monetary_palette, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel("Customer ID", fontsize=30, labelpad=20)
ax[2].set_title("By Monetary", loc="center", fontsize=40)
ax[2].tick_params(axis='y', labelsize=25)
ax[2].tick_params(axis='x', labelsize=25)

# Menampilkan grafik
st.pyplot(fig)

# Copyright caption
st.caption('Copyright (c) Muhammad Abdiel Al Hafiz 2024')
