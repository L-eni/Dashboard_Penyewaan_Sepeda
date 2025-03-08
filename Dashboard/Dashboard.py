import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Load dataset
day = pd.read_csv('Data/day.csv')
hour = pd.read_csv('Data/hour.csv')

# Konversi tanggal
df_day['dteday'] = pd.to_datetime(df_day['dteday'], dayfirst=True)
df_hour['dteday'] = pd.to_datetime(df_hour['dteday'], dayfirst=True)

# Tema warna
sns.set_style("whitegrid")
sns.set_palette(["#5F9EA0"])  # Warna CadetBlue

# Mengatur warna latar belakang Streamlit
st.markdown(
    """
    <style>
        .main {
            background-color: #B0E0E6;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# **📌 Tambahkan gambar sepeda di atas judul**
st.image("logosepeda.png", width=150)
st.title("🚴‍♂️ Dashboard Penyewaan Sepeda")

# Sidebar Pemilihan Dataset
st.sidebar.image("logosepeda.png", width=100)
st.sidebar.title("🚴‍♂️ Dashboard Penyewaan Sepeda")
dataset_choice = st.sidebar.radio("Pilih Dataset:", ["Harian", "Per Jam"])

# Sidebar Rentang Tanggal
start_date = st.sidebar.date_input("Tanggal Mulai", df_day['dteday'].min())
end_date = st.sidebar.date_input("Tanggal Akhir", df_day['dteday'].max())

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filter dataset berdasarkan rentang tanggal
if dataset_choice == "Harian":
    df_filtered = df_day[(df_day['dteday'] >= start_date) & (df_day['dteday'] <= end_date)]
else:
    df_filtered = df_hour[(df_hour['dteday'] >= start_date) & (df_hour['dteday'] <= end_date)]

# **🔢 Ringkasan Data**
col1, col2, col3 = st.columns(3)
col1.metric("Total Penyewaan", df_filtered['cnt'].sum())
col2.metric("Rata-rata Harian", round(df_filtered['cnt'].mean(), 2))
col3.metric("Penyewaan Maksimum", df_filtered['cnt'].max())

# **📊 Tren Penyewaan Sepeda**
st.write("### 📆 Tren Penyewaan Sepeda Harian")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=df_filtered, x="dteday", y="cnt", ax=ax, marker="o", linestyle="-")
ax.set_title("Tren Penyewaan Sepeda Harian", color='black')
ax.set_xlabel("Tanggal", color='black')
ax.set_ylabel("Jumlah Penyewaan", color='black')
plt.xticks(rotation=45, color='black')
plt.yticks(color='black')
st.pyplot(fig)

# **🎯 Pengaruh Musim terhadap Penyewaan**
st.write("### 🌦️ Pengaruh Musim terhadap Penyewaan")
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x="season", y="cnt", data=df_filtered, estimator=sum, palette="viridis", ax=ax)
ax.set_xlabel("Musim")
ax.set_ylabel("Total Penyewaan Sepeda")
ax.set_title("Total Penyewaan Sepeda per Musim")
ax.set_xticks([0, 1, 2, 3])
ax.set_xticklabels(["Spring", "Summer", "Fall", "Winter"])
st.pyplot(fig)

# **🌡️ Hubungan Suhu dengan Penyewaan**
st.write("### 🌡️ Hubungan Suhu dengan Penyewaan Sepeda")
fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(x=df_filtered['temp'], y=df_filtered['cnt'], color="#5F9EA0", alpha=0.6, ax=ax)
ax.set_title("Hubungan Antara Suhu dan Jumlah Penyewaan", color='black')
ax.set_xlabel("Suhu (Normalized)", color='black')
ax.set_ylabel("Jumlah Penyewaan", color='black')
st.pyplot(fig)

# **🛑 Pengaruh Hari Kerja/Libur**
st.write("### 📅 Pengaruh Hari Kerja terhadap Penyewaan")
fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(x="workingday", y="cnt", data=df_filtered, palette=["#5F9EA0", "#B0E0E6"], ax=ax)
ax.set_xlabel("Hari Kerja (0 = Libur, 1 = Kerja)")
ax.set_ylabel("Jumlah Penyewaan")
ax.set_title("Distribusi Penyewaan Berdasarkan Hari Kerja")
st.pyplot(fig)

# **👥 Karakteristik Pengguna**
st.write("### 👥 Perbandingan Pengguna Casual dan Terdaftar")
col1, col2 = st.columns(2)
col1.metric("Total Pengguna Casual", df_filtered['casual'].sum())
col2.metric("Total Pengguna Terdaftar", df_filtered['registered'].sum())

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=["Casual", "Registered"], y=[df_filtered['casual'].sum(), df_filtered['registered'].sum()], palette=["#5F9EA0", "#B0E0E6"], ax=ax)
ax.set_ylabel("Jumlah Pengguna")
ax.set_title("Perbandingan Pengguna Casual dan Terdaftar")
st.pyplot(fig)

# **🌤️ Pengaruh Kondisi Cuaca**
st.write("### 🌤️ Pengaruh Kondisi Cuaca terhadap Penyewaan")
fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(x="weathersit", y="cnt", data=df_filtered, palette="coolwarm", ax=ax)
ax.set_xlabel("Kondisi Cuaca (1 = Cerah, 2 = Berawan, 3 = Hujan)")
ax.set_ylabel("Jumlah Penyewaan")
ax.set_title("Distribusi Penyewaan Berdasarkan Kondisi Cuaca")
st.pyplot(fig)
