import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Fungsi untuk memuat data
def load_data():
    day = pd.read_csv("Data/day.csv", sep=';') 
    hour = pd.read_csv("Data/hour.csv", sep=';')
    day['dteday'] = pd.to_datetime(day['dteday'], dayfirst=True)
    hour['dteday'] = pd.to_datetime(hour['dteday'], dayfirst=True)
    day['date'] = day['dteday'].dt.date
    hour['date'] = hour['dteday'].dt.date
    return day, hour

day_df, hour_df = load_data()

# Sidebar untuk filter data
st.sidebar.header("📅 Filter Data")
min_date = min(day_df['date'])
max_date = max(day_df['date'])
start_date = st.sidebar.date_input("Pilih Tanggal Awal", min_date)
end_date = st.sidebar.date_input("Pilih Tanggal Akhir", max_date)

filtered_day_df = day_df[(day_df['date'] >= start_date) & (day_df['date'] <= end_date)].copy()
filtered_hour_df = hour_df[(hour_df['date'] >= start_date) & (hour_df['date'] <= end_date)].copy()

if filtered_day_df.empty or filtered_hour_df.empty:
    st.error("⚠️ Tidak ada data untuk rentang tanggal yang dipilih.")
    st.stop()

st.title("🚲 Dashboard Penyewaan Sepeda")

# Menampilkan jumlah penyewaan dengan tata letak lebih rapi
total_penyewaan = filtered_day_df['cnt'].sum()
filtered_day_df['year'] = filtered_day_df['dteday'].dt.year
penyewaan_tahunan = filtered_day_df.groupby('year')['cnt'].sum().to_dict()

col1, col2, col3 = st.columns(3)
col1.metric("Total Penyewaan", f"{total_penyewaan:,}")
col2.metric("Penyewaan 2011", f"{penyewaan_tahunan.get(2011, 0):,}")
col3.metric("Penyewaan 2012", f"{penyewaan_tahunan.get(2012, 0):,}")

# Tren Penyewaan Sepeda
st.subheader("📈 Tren Penyewaan Sepeda")
yearly_trend = filtered_day_df.groupby('year')['cnt'].sum().reset_index()
fig, ax = plt.subplots(figsize=(5, 3))
sns.barplot(x='year', y='cnt', data=yearly_trend, palette='Blues', ax=ax)
ax.set_xlabel("Tahun")
ax.set_ylabel("Total Penyewaan")
ax.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig)

# Jam Sibuk Penyewaan
st.subheader("⏰ Jam Sibuk Penyewaan")
hourly_trend = filtered_hour_df.groupby('hr')['cnt'].mean().reset_index()
peak_hour = int(hourly_trend.loc[hourly_trend['cnt'].idxmax(), 'hr'])
st.metric("Jam Sibuk", f"{peak_hour}:00")

fig, ax = plt.subplots(figsize=(6, 3))
sns.lineplot(x='hr', y='cnt', data=hourly_trend, marker="o", color='purple', ax=ax)
ax.set_xlabel("Jam dalam Sehari")
ax.set_ylabel("Rata-rata Penyewaan Sepeda")
ax.grid(True, linestyle='--', alpha=0.7)
st.pyplot(fig)

# Korelasi Antar Variabel
st.subheader("📊 Korelasi Antar Variabel Cuaca dan Penyewaan")
selected_columns = ['cnt', 'temp', 'hum', 'windspeed', 'weathersit']
correlation = filtered_day_df[selected_columns].corr()

fig, ax = plt.subplots(figsize=(5, 3))
sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5, ax=ax)
ax.set_title("Heatmap Korelasi Faktor Cuaca dengan Penyewaan Sepeda")
st.pyplot(fig)

# Pengaruh Cuaca terhadap Penyewaan
st.subheader("🌤️ Pengaruh Cuaca")
fig, axes = plt.subplots(1, 3, figsize=(12, 4))
sns.scatterplot(ax=axes[0], x=filtered_day_df['temp'], y=filtered_day_df['cnt'], alpha=0.5, color='r')
axes[0].set_title("Suhu vs Penyewaan")
sns.scatterplot(ax=axes[1], x=filtered_day_df['hum'], y=filtered_day_df['cnt'], alpha=0.5, color='g')
axes[1].set_title("Kelembaban vs Penyewaan")
sns.scatterplot(ax=axes[2], x=filtered_day_df['windspeed'], y=filtered_day_df['cnt'], alpha=0.5, color='b')
axes[2].set_title("Kecepatan Angin vs Penyewaan")
st.pyplot(fig)

# Perbandingan Hari Kerja dan Akhir Pekan
st.subheader("📅 Hari Kerja vs Akhir Pekan")
filtered_day_df['weekday_type'] = filtered_day_df['weekday'].apply(lambda x: 'Weekday' if x < 5 else 'Weekend')
avg_rental = filtered_day_df.groupby('weekday_type')['cnt'].mean().reset_index()

fig, ax = plt.subplots(figsize=(5, 3))
sns.barplot(x='weekday_type', y='cnt', data=avg_rental, palette='coolwarm', ax=ax)
ax.set_xlabel("Hari")
ax.set_ylabel("Rata-rata Penyewaan")
ax.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig)

st.caption("📌 Sumber Data: Bike Sharing Dataset")
