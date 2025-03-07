# 🚴‍♂️ Dashboard Penyewaan Sepeda

Proyek ini merupakan dashboard interaktif untuk menganalisis data penyewaan sepeda menggunakan **Google Colab** dan **Streamlit**.

## 🛠️ Teknologi yang Digunakan
- Python  
- Streamlit  
- Pandas  
- Matplotlib  
- Seaborn  

## 📄 Dataset
Dataset yang digunakan:  
- **day.csv** : Data penyewaan sepeda per hari  
- **hour.csv** : Data penyewaan sepeda per jam  

## 📌 Cara Menjalankan Dashboard

### 1. **Buka Google Colab**  
- Masuk ke akun Google Anda.  
- Buka [Google Colab](https://colab.research.google.com/).  
- Upload file **day.csv** dan **hour.csv** melalui menu **Files > Upload**.  
- Upload file kode Python yang berisi kode dashboard.  

### 2. **Instal Library yang Dibutuhkan**  
Jalankan perintah berikut di sel Google Colab:  
```python
!pip install streamlit pandas matplotlib seaborn
```

### 3. **Buat File Python (Dashboard.py)**  
Tambahkan kode berikut pada Colab untuk membuat file program dashboard:  
```python
%%writefile Dashboard.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Dashboard Penyewaan Sepeda")

# Membaca Dataset
day = pd.read_csv("day.csv")
hour = pd.read_csv("hour.csv")
```

### 4. **Menjalankan Streamlit di Google Colab**  
Tambahkan kode berikut di sel baru:  
```python
! wget -q -O - ipv4.icanhazip.com
!streamlit run Dashboard.py & npx localtunnel --port 8501
```
Tunggu beberapa saat hingga link **LocalTunnel** muncul.   

### 5. **Akses Dashboard**  
Klik link yang muncul untuk membuka **Dashboard Penyewaan Sepeda**.

## 📊 Fitur Dashboard
- Ringkasan Data  
- Tren Penyewaan Sepeda  
- Pengaruh Musim terhadap Penyewaan  
- Hubungan Suhu dengan Penyewaan  
- Distribusi Hari Kerja vs Libur  
- Perbandingan Pengguna Casual dan Terdaftar  
- Pengaruh Kondisi Cuaca  

## 📌 Catatan
- Pastikan semua file dataset sudah terupload di Google Colab sebelum menjalankan kode.
- Koneksi internet stabil diperlukan untuk menjalankan **LocalTunnel**.

---
Dibuat oleh: **Leni Gustia**

