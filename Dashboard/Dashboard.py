import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
def load_data():
    day = pd.read_csv("Data/day.csv", sep=';') 
    hour = pd.read_csv("Data/hour.csv", sep=';')

    # Konversi kolom 'dteday' ke datetime
    day['dteday'] = pd.to_datetime(day['dteday'], dayfirst=True)
    hour['dteday'] = pd.to_datetime(hour['dteday'], dayfirst=True)

    # Tambahkan kolom tanggal agar bisa difilter
    day['date'] = day['dteday'].dt.date
    hour['date'] = hour['dteday'].dt.date
    return day, hour

# Load data dengan perbaikan
day_df, hour_df = load_data()

# Perbaiki inisialisasi tanggal awal dan akhir
min_date = min(day_df['date'])
max_date = max(day_df['date'])

# Sidebar: Filter berdasarkan tanggal
st.sidebar.header("Filter Data")
start_date = st.sidebar.date_input("Pilih Tanggal Awal", min_date)
end_date = st.sidebar.date_input("Pilih Tanggal Akhir", max_date)

# Filter dataset berdasarkan tanggal yang dipilih
filtered_day_df = day_df[(day_df['date'] >= start_date) & (day_df['date'] <= end_date)]
filtered_hour_df = hour_df[(hour_df['date'] >= start_date) & (hour_df['date'] <= end_date)]


# Tampilkan pesan jika tidak ada data
if filtered_day_df.empty or filtered_hour_df.empty:
    st.error("⚠ Tidak ada data untuk rentang tanggal yang dipilih.")
    st.stop()

# Judul utama dashboard
st.title("📊 Dashboard Penyewaan Sepeda 🚴‍♂")

### 🔹 Tren Penyewaan Sepeda per Tahun
st.subheader("Tren Penyewaan Sepeda per Tahun")

# Agregasi jumlah penyewaan per tahun
filtered_day_df['year'] = filtered_day_df['dteday'].dt.year
yearly_trend = filtered_day_df.groupby('year')['cnt'].sum().reset_index()

fig, ax = plt.subplots(figsize=(6, 4))
sns.barplot(x='year', y='cnt', data=yearly_trend, ax=ax)
ax.set_xlabel("Tahun")
ax.set_ylabel("Total Penyewaan")
st.pyplot(fig)

# Menampilkan angka penting
if len(yearly_trend) >= 2:
    total_2011 = yearly_trend.loc[yearly_trend['year'] == 2011, 'cnt'].values[0] if 2011 in yearly_trend['year'].values else 0
    total_2012 = yearly_trend.loc[yearly_trend['year'] == 2012, 'cnt'].values[0] if 2012 in yearly_trend['year'].values else 0
    st.write(f"📌 Peningkatan penyewaan dari 2011 ke 2012: {total_2012 - total_2011} sepeda")


### 🔹 Jam Sibuk Penyewaan Sepeda
st.subheader("Jam Sibuk Penyewaan Sepeda")

if 'hr' in filtered_hour_df.columns:
    hourly_trend = filtered_hour_df.groupby('hr')['cnt'].mean().reset_index()

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(x='hr', y='cnt', data=hourly_trend, marker="o", ax=ax)
    ax.set_xlabel("Jam dalam Sehari")
    ax.set_ylabel("Rata-rata Penyewaan Sepeda")
    st.pyplot(fig)

    # Menampilkan jam puncak
    peak_hour = hourly_trend.loc[hourly_trend['cnt'].idxmax(), 'hr']
    st.write(f"📌 Jam tersibuk: {peak_hour}:00 dengan jumlah penyewaan tertinggi")
else:
    st.error("⚠ Data jam tidak ditemukan dalam dataset.")


### 🔹 Pengaruh Cuaca terhadap Penyewaan
st.subheader("Pengaruh Cuaca terhadap Penyewaan")

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Scatter plot suhu vs penyewaan
sns.scatterplot(ax=axes[0], x=filtered_day_df['temp'], y=filtered_day_df['cnt'], alpha=0.5, color='r')
axes[0].set_title("Suhu vs Penyewaan")

# Scatter plot kelembaban vs penyewaan
sns.scatterplot(ax=axes[1], x=filtered_day_df['hum'], y=filtered_day_df['cnt'], alpha=0.5, color='g')
axes[1].set_title("Kelembaban vs Penyewaan")

# Scatter plot kecepatan angin vs penyewaan
sns.scatterplot(ax=axes[2], x=filtered_day_df['windspeed'], y=filtered_day_df['cnt'], alpha=0.5, color='b')
axes[2].set_title("Kecepatan Angin vs Penyewaan")

st.pyplot(fig)

st.write("📌 Cuaca mempengaruhi penyewaan sepeda:")
st.write("- Penyewaan meningkat pada suhu sedang (tidak terlalu panas atau dingin)")
st.write("- Kelembaban tinggi sedikit menurunkan penyewaan")
st.write("- Kecepatan angin tidak terlalu berdampak signifikan")


### 🔹 Penyewaan Sepeda di Hari Kerja vs Akhir Pekan
st.subheader("Penyewaan Sepeda: Hari Kerja vs Akhir Pekan")

if 'weekday' in filtered_day_df.columns:
    # Menandai apakah hari kerja atau akhir pekan
    filtered_day_df['weekday_type'] = filtered_day_df['weekday'].apply(lambda x: 'Weekday' if x < 5 else 'Weekend')

    # Rata-rata penyewaan per kategori
    avg_rental = filtered_day_df.groupby('weekday_type')['cnt'].mean().reset_index()

    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x='weekday_type', y='cnt', data=avg_rental, ax=ax)
    ax.set_xlabel("Hari")
    ax.set_ylabel("Rata-rata Penyewaan")
    st.pyplot(fig)

    # Menampilkan angka penting
    weekday_avg = avg_rental.loc[avg_rental['weekday_type'] == 'Weekday', 'cnt'].values[0]
    weekend_avg = avg_rental.loc[avg_rental['weekday_type'] == 'Weekend', 'cnt'].values[0]
    st.write(f"📌 Penyewaan lebih tinggi di hari kerja: {weekday_avg:.2f} sepeda/hari dibanding akhir pekan {weekend_avg:.2f} sepeda/hari.")
else:
    st.error("⚠ Data 'weekday' tidak ditemukan dalam dataset.")

# Footer
st.write("📌 Sumber Data: Bike Sharing Dataset")
