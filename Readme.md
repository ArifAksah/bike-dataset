# Bike Sharing Dashboard

Dashboard analisis data penyewaan sepeda di Washington D.C. (2011-2012) menggunakan dataset Bike Sharing dari Capital Bikeshare system.

## Struktur Project

```
submission_fundamental_datascientif_bike/
├── data/
│   ├── day.csv          # Data penyewaan harian (731 records)
│   └── hour.csv         # Data penyewaan per jam (17.379 records)
├── dashboard/
│   └── dashboard.py     # Dashboard Streamlit
├── Proyek_Analisis_Data.ipynb  # Notebook analisis data
├── requirements.txt     # Dependencies
└── Readme.md
```

## Cara Menjalankan

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Menjalankan Dashboard Streamlit

```bash
cd dashboard
streamlit run dashboard.py
```

## Pertanyaan Bisnis

1. **Pengaruh Kondisi Cuaca:** Bagaimana pengaruh kondisi cuaca (weathersit) terhadap rata-rata jumlah penyewaan sepeda harian di Washington D.C. selama periode 2011-2012, dan kondisi cuaca mana yang menyebabkan penurunan penyewaan tertinggi?

2. **Pola Penyewaan per Jam:** Pada jam berapa terjadi puncak penyewaan sepeda oleh pengguna registered dibandingkan casual pada hari kerja di tahun 2012, dan bagaimana perbedaan pola tersebut dapat digunakan untuk mengoptimalkan distribusi sepeda?

## Fitur Dashboard

- **2 Visualisasi utama** dari 2 pertanyaan bisnis:
  - Bar chart rata-rata penyewaan berdasarkan kondisi cuaca
  - Line chart pola penyewaan per jam (Registered vs Casual)
- **Fitur interaktif:** Filter tahun (2011/2012/Semua) untuk eksplorasi data
- **Analisis clustering** berdasarkan periode waktu dan volume demand

## Kesimpulan

- Cuaca Clear menghasilkan rata-rata penyewaan tertinggi (~4.876/hari), Light Snow/Rain terendah (~1.803)
- Registered users memiliki pola bimodal (jam 8 dan 17-18), casual users unimodal (jam 17)
- Registered users mendominasi 81.2% total penyewaan

## Dataset

Dataset Bike Sharing dari [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/Bike+Sharing+Dataset) dengan lisensi dari Fanaee-T, Hadi, and Gama, Joao (2013).
