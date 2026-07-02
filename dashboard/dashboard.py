import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings

warnings.filterwarnings('ignore')
sns.set_style('whitegrid')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)

st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide"
)

@st.cache_data
def load_data():
    day_df = pd.read_csv(os.path.join(PARENT_DIR, 'day.csv'))
    hour_df = pd.read_csv(os.path.join(PARENT_DIR, 'hour.csv'))

    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

    category_cols = ['season', 'yr', 'mnth', 'holiday', 'weekday', 'workingday', 'weathersit']
    for col in category_cols:
        day_df[col] = day_df[col].astype('category')
        hour_df[col] = hour_df[col].astype('category')
    hour_df['hr'] = hour_df['hr'].astype('category')

    median_hum = hour_df[hour_df['hum'] > 0]['hum'].median()
    hour_df['hum'] = hour_df['hum'].replace(0, median_hum)

    season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    weathersit_map = {1: 'Clear', 2: 'Mist/Cloudy', 3: 'Light Snow/Rain', 4: 'Heavy Rain/Snow'}
    yr_map = {0: '2011', 1: '2012'}

    day_df['season_label'] = day_df['season'].map(season_map)
    day_df['weathersit_label'] = day_df['weathersit'].map(weathersit_map)
    day_df['yr_label'] = day_df['yr'].map(yr_map)

    hour_df['season_label'] = hour_df['season'].map(season_map)
    hour_df['weathersit_label'] = hour_df['weathersit'].map(weathersit_map)
    hour_df['yr_label'] = hour_df['yr'].map(yr_map)

    return day_df, hour_df

day_df, hour_df = load_data()

st.title("🚲 Bike Sharing Dashboard")
st.markdown("Dashboard analisis data penyewaan sepeda di Washington D.C. (2011-2012)")

st.sidebar.title("Filter")

year_filter = st.sidebar.selectbox("Pilih Tahun", ['Semua', '2011', '2012'])

if year_filter != 'Semua':
    yr_val = 0 if year_filter == '2011' else 1
    day_filtered = day_df[day_df['yr'] == yr_val]
    hour_filtered = hour_df[hour_df['yr'] == yr_val]
else:
    day_filtered = day_df.copy()
    hour_filtered = hour_df.copy()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Penyewaan", f"{day_filtered['cnt'].sum():,}")
with col2:
    st.metric("Rata-rata/Hari", f"{day_filtered['cnt'].mean():,.0f}")
with col3:
    st.metric("Total Casual", f"{day_filtered['casual'].sum():,}")
with col4:
    st.metric("Total Registered", f"{day_filtered['registered'].sum():,}")

st.markdown("---")

st.header("📊 Pertanyaan 1: Pengaruh Kondisi Cuaca terhadap Penyewaan")
st.markdown("**SMART Question:** Bagaimana pengaruh kondisi cuaca terhadap rata-rata jumlah penyewaan sepeda harian di Washington D.C. selama periode 2011-2012, dan kondisi cuaca mana yang menyebabkan penurunan penyewaan tertinggi?")

col_left, col_right = st.columns(2)

with col_left:
    fig, ax = plt.subplots(figsize=(8, 5))
    weather_order = ['Clear', 'Mist/Cloudy', 'Light Snow/Rain']
    colors_weather = ['#2ecc71', '#f39c12', '#e74c3c']

    weather_avg = day_filtered.groupby('weathersit_label', observed=True)['cnt'].mean()
    available_weather = [w for w in weather_order if w in weather_avg.index]
    weather_avg = weather_avg.reindex(available_weather)
    colors = [colors_weather[weather_order.index(w)] for w in available_weather]

    bars = ax.bar(weather_avg.index, weather_avg.values, color=colors, edgecolor='black', linewidth=0.5)
    ax.set_title('Rata-rata Penyewaan Harian\nBerdasarkan Kondisi Cuaca', fontsize=13, fontweight='bold')
    ax.set_xlabel('Kondisi Cuaca', fontsize=11)
    ax.set_ylabel('Rata-rata Jumlah Penyewaan', fontsize=11)

    for bar, val in zip(bars, weather_avg.values):
        ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 30,
                f'{val:.0f}', ha='center', va='bottom', fontweight='bold', fontsize=11)

    plt.tight_layout()
    st.pyplot(fig)

with col_right:
    fig, ax = plt.subplots(figsize=(8, 5))
    weather_order = ['Clear', 'Mist/Cloudy', 'Light Snow/Rain']

    weather_yr = day_filtered.groupby(['weathersit_label', 'yr_label'], observed=True)['cnt'].mean().unstack()
    available_weather = [w for w in weather_order if w in weather_yr.index]
    weather_yr = weather_yr.reindex(available_weather)

    x = np.arange(len(available_weather))
    width = 0.35

    if '2011' in weather_yr.columns:
        bars1 = ax.bar(x - width/2, weather_yr['2011'], width, label='2011', color='#3498db', edgecolor='black', linewidth=0.5)
        for bar in bars1:
            ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 20,
                    f'{bar.get_height():.0f}', ha='center', va='bottom', fontsize=9)
    if '2012' in weather_yr.columns:
        bars2 = ax.bar(x + width/2, weather_yr['2012'], width, label='2012', color='#e67e22', edgecolor='black', linewidth=0.5)
        for bar in bars2:
            ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 20,
                    f'{bar.get_height():.0f}', ha='center', va='bottom', fontsize=9)

    ax.set_title('Rata-rata Penyewaan Berdasarkan Cuaca\nPer Tahun', fontsize=13, fontweight='bold')
    ax.set_xlabel('Kondisi Cuaca', fontsize=11)
    ax.set_ylabel('Rata-rata Jumlah Penyewaan', fontsize=11)
    ax.set_xticks(x)
    ax.set_xticklabels(available_weather)
    ax.legend()

    plt.tight_layout()
    st.pyplot(fig)

fig_corr, ax_corr = plt.subplots(figsize=(8, 5))
corr_data = day_filtered[['temp', 'atemp', 'hum', 'windspeed', 'cnt']].corr()
sns.heatmap(corr_data, annot=True, cmap='RdYlGn', center=0, fmt='.3f',
            linewidths=0.5, ax=ax_corr, vmin=-1, vmax=1)
ax_corr.set_title('Korelasi Variabel Cuaca dengan Penyewaan', fontsize=13, fontweight='bold')
plt.tight_layout()
st.pyplot(fig_corr)

weather_stats = day_filtered.groupby('weathersit_label', observed=True)['cnt'].agg(['mean', 'median', 'std', 'count'])
weather_stats.columns = ['Rata-rata', 'Median', 'Std Dev', 'Jumlah Hari']
st.dataframe(weather_stats.round(2))

st.markdown("---")

st.header("📊 Pertanyaan 2: Pola Penyewaan per Jam (Registered vs Casual)")
st.markdown("**SMART Question:** Pada jam berapa terjadi puncak penyewaan sepeda oleh pengguna registered dibandingkan casual pada hari kerja di tahun 2012, dan bagaimana perbedaan pola tersebut dapat digunakan untuk mengoptimalkan distribusi sepeda?")

hour_2012_workday = hour_df[(hour_df['yr'] == 1) & (hour_df['workingday'] == 1)]
hourly_stats = hour_2012_workday.groupby('hr', observed=True)[['casual', 'registered', 'cnt']].mean()

peak_registered = int(hourly_stats['registered'].idxmax())
peak_casual = int(hourly_stats['casual'].idxmax())

col_left2, col_right2 = st.columns(2)

with col_left2:
    fig, ax = plt.subplots(figsize=(8, 5))
    hours = hourly_stats.index.astype(int)

    ax.plot(hours, hourly_stats['registered'], marker='o', linewidth=2.5,
            color='#2980b9', label='Registered', markersize=5)
    ax.plot(hours, hourly_stats['casual'], marker='s', linewidth=2.5,
            color='#e74c3c', label='Casual', markersize=5)
    ax.fill_between(hours, hourly_stats['registered'], alpha=0.1, color='#2980b9')
    ax.fill_between(hours, hourly_stats['casual'], alpha=0.1, color='#e74c3c')

    ax.axvline(x=peak_registered, color='#2980b9', linestyle='--', alpha=0.5)
    ax.axvline(x=peak_casual, color='#e74c3c', linestyle='--', alpha=0.5)

    ax.set_title('Pola Penyewaan per Jam\n(Registered vs Casual) - Hari Kerja 2012',
                 fontsize=13, fontweight='bold')
    ax.set_xlabel('Jam', fontsize=11)
    ax.set_ylabel('Rata-rata Jumlah Penyewaan', fontsize=11)
    ax.set_xticks(range(0, 24))
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    st.pyplot(fig)

with col_right2:
    fig, ax = plt.subplots(figsize=(8, 5))

    hourly_workday = hour_df[(hour_df['yr'] == 1) & (hour_df['workingday'] == 1)].groupby('hr', observed=True)['cnt'].mean()
    hourly_weekend = hour_df[(hour_df['yr'] == 1) & (hour_df['workingday'] == 0)].groupby('hr', observed=True)['cnt'].mean()

    hours_wd = hourly_workday.index.astype(int)
    ax.plot(hours_wd, hourly_workday.values, marker='o', linewidth=2.5,
            color='#27ae60', label='Hari Kerja', markersize=5)
    ax.plot(hours_wd, hourly_weekend.values, marker='s', linewidth=2.5,
            color='#8e44ad', label='Weekend', markersize=5)
    ax.fill_between(hours_wd, hourly_workday.values, alpha=0.1, color='#27ae60')
    ax.fill_between(hours_wd, hourly_weekend.values, alpha=0.1, color='#8e44ad')

    ax.set_title('Pola Penyewaan per Jam\n(Hari Kerja vs Weekend) - 2012',
                 fontsize=13, fontweight='bold')
    ax.set_xlabel('Jam', fontsize=11)
    ax.set_ylabel('Rata-rata Jumlah Penyewaan', fontsize=11)
    ax.set_xticks(range(0, 24))
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    st.pyplot(fig)

col_pie, col_stats = st.columns(2)

with col_pie:
    fig, ax = plt.subplots(figsize=(6, 5))
    total_casual = day_filtered['casual'].sum()
    total_registered = day_filtered['registered'].sum()
    total_all = day_filtered['cnt'].sum()

    sizes = [total_casual, total_registered]
    labels = [f'Casual\n({total_casual/total_all*100:.1f}%)', f'Registered\n({total_registered/total_all*100:.1f}%)']
    colors = ['#e74c3c', '#2980b9']
    explode = (0.05, 0.05)

    ax.pie(sizes, explode=explode, labels=labels, colors=colors,
           autopct='%1.1f%%', shadow=True, startangle=90,
           textprops={'fontsize': 12, 'fontweight': 'bold'})
    ax.set_title('Proporsi Casual vs Registered', fontsize=13, fontweight='bold')

    plt.tight_layout()
    st.pyplot(fig)

with col_stats:
    st.subheader("Statistik per Jam (2012, Hari Kerja)")
    hourly_display = hourly_stats.copy()
    hourly_display.index = [f"Jam {h}:00" for h in hourly_display.index.astype(int)]
    hourly_display.columns = ['Casual', 'Registered', 'Total']
    st.dataframe(hourly_display.round(0).astype(int))

st.markdown("---")

st.header("🔬 Analisis Lanjutan: Clustering")

st.subheader("Clustering Berdasarkan Periode Waktu (Binning)")

def categorize_hour(hr):
    if 0 <= hr <= 4:
        return 'Late Night (0-4)'
    elif 5 <= hr <= 7:
        return 'Early Morning (5-7)'
    elif 8 <= hr <= 10:
        return 'Morning Rush (8-10)'
    elif 11 <= hr <= 14:
        return 'Midday (11-14)'
    elif 15 <= hr <= 17:
        return 'Afternoon Rush (15-17)'
    elif 18 <= hr <= 20:
        return 'Evening (18-20)'
    else:
        return 'Night (21-23)'

hour_filtered['hr_int'] = hour_filtered['hr'].astype(int)
hour_filtered['time_period'] = hour_filtered['hr_int'].apply(categorize_hour)

period_order = ['Late Night (0-4)', 'Early Morning (5-7)', 'Morning Rush (8-10)',
                'Midday (11-14)', 'Afternoon Rush (15-17)', 'Evening (18-20)', 'Night (21-23)']

time_cluster = hour_filtered.groupby('time_period', observed=True).agg({
    'casual': 'mean',
    'registered': 'mean',
    'cnt': 'mean'
}).reindex(period_order)

col_cluster1, col_cluster2 = st.columns(2)

with col_cluster1:
    fig, ax = plt.subplots(figsize=(8, 5))
    colors_period = ['#2c3e50', '#e67e22', '#2980b9', '#27ae60', '#e74c3c', '#8e44ad', '#34495e']
    bars = ax.bar(range(len(period_order)), time_cluster['cnt'],
                  color=colors_period, edgecolor='black', linewidth=0.5)
    ax.set_xticks(range(len(period_order)))
    ax.set_xticklabels(period_order, rotation=45, ha='right')
    ax.set_title('Rata-rata Penyewaan per Periode Waktu', fontsize=13, fontweight='bold')
    ax.set_ylabel('Rata-rata Jumlah Penyewaan')
    for bar, val in zip(bars, time_cluster['cnt']):
        ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 3,
                f'{val:.0f}', ha='center', va='bottom', fontsize=9)
    plt.tight_layout()
    st.pyplot(fig)

with col_cluster2:
    fig, ax = plt.subplots(figsize=(8, 5))
    x = np.arange(len(period_order))
    width = 0.6
    ax.bar(x, time_cluster['registered'], width, label='Registered', color='#2980b9')
    ax.bar(x, time_cluster['casual'], width,
           bottom=time_cluster['registered'], label='Casual', color='#e74c3c')
    ax.set_xticks(x)
    ax.set_xticklabels(period_order, rotation=45, ha='right')
    ax.set_title('Komposisi Casual vs Registered\nper Periode Waktu', fontsize=13, fontweight='bold')
    ax.set_ylabel('Rata-rata Jumlah Penyewaan')
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)

st.subheader("Clustering Berdasarkan Volume Demand Harian")

day_filtered['demand_level'] = pd.cut(day_filtered['cnt'],
                                       bins=[0, 2000, 5000, 8000, float('inf')],
                                       labels=['Very Low (<2000)', 'Low (2000-5000)',
                                               'Medium (5000-8000)', 'High (>8000)'])

col_cluster3, col_cluster4 = st.columns(2)

with col_cluster3:
    fig, ax = plt.subplots(figsize=(8, 5))
    demand_counts = day_filtered['demand_level'].value_counts().sort_index()
    colors_demand = ['#e74c3c', '#f39c12', '#3498db', '#2ecc71']
    ax.bar(demand_counts.index, demand_counts.values, color=colors_demand,
           edgecolor='black', linewidth=0.5)
    ax.set_title('Jumlah Hari per Level Demand', fontsize=13, fontweight='bold')
    ax.set_ylabel('Jumlah Hari')
    for i, (idx, val) in enumerate(demand_counts.items()):
        ax.text(i, val + 1, str(val), ha='center', fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig)

with col_cluster4:
    fig, ax = plt.subplots(figsize=(8, 5))
    demand_workday = pd.crosstab(day_filtered['demand_level'], day_filtered['workingday'], normalize='index') * 100
    demand_workday.columns = ['Weekend/Holiday', 'Working Day']
    demand_workday.plot(kind='bar', stacked=True, ax=ax,
                        color=['#e74c3c', '#2980b9'], edgecolor='black', linewidth=0.5)
    ax.set_title('Distribusi Hari Kerja vs Weekend\nper Level Demand', fontsize=13, fontweight='bold')
    ax.set_ylabel('Persentase (%)')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    ax.legend(loc='upper right')
    plt.tight_layout()
    st.pyplot(fig)

st.subheader("Manual Grouping: Profil Pengguna per Musim")

season_user = day_filtered.groupby('season_label', observed=True).agg({
    'casual': 'sum',
    'registered': 'sum',
    'cnt': 'sum'
})
season_user['casual_ratio'] = (season_user['casual'] / season_user['cnt'] * 100).round(1)

col_cluster5, col_cluster6 = st.columns(2)

with col_cluster5:
    fig, ax = plt.subplots(figsize=(8, 5))
    season_order = ['Spring', 'Summer', 'Fall', 'Winter']
    season_plot = season_user.reindex([s for s in season_order if s in season_user.index])
    x = np.arange(len(season_plot))
    width = 0.6
    ax.bar(x, season_plot['registered'], width, label='Registered', color='#2980b9')
    ax.bar(x, season_plot['casual'], width,
           bottom=season_plot['registered'], label='Casual', color='#e74c3c')
    ax.set_xticks(x)
    ax.set_xticklabels(season_plot.index)
    ax.set_title('Total Penyewaan per Musim\n(Casual vs Registered)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Total Penyewaan')
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)

with col_cluster6:
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(season_plot.index, season_plot['casual_ratio'], marker='o',
            linewidth=2.5, color='#e74c3c', markersize=10)
    ax.fill_between(season_plot.index, season_plot['casual_ratio'], alpha=0.2, color='#e74c3c')
    ax.set_title('Rasio Casual Users per Musim', fontsize=13, fontweight='bold')
    ax.set_ylabel('Rasio Casual (%)')
    for i, (s, v) in enumerate(zip(season_plot.index, season_plot['casual_ratio'])):
        ax.annotate(f'{v}%', (i, v), textcoords='offset points',
                    xytext=(0, 10), ha='center', fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig)

st.markdown("---")

st.header("📝 Kesimpulan & Rekomendasi")

st.subheader("Kesimpulan Pertanyaan 1")
st.markdown("""
- **Kondisi Clear (Cerah)** menghasilkan rata-rata penyewaan tertinggi (~4.876 sepeda/hari)
- **Light Snow/Rain** menyebabkan penurunan hingga **62.9%** dibandingkan cuaca cerah
- **Suhu** memiliki korelasi positif kuat (r=0.627) dengan penyewaan
- Pertumbuhan penyewaan dari 2011 ke 2012 terjadi di **semua kondisi cuaca**
""")

st.subheader("Kesimpulan Pertanyaan 2")
st.markdown("""
- **Registered users** memiliki pola **bimodal**: puncak jam 8:00 dan 17:00-18:00 (jam kerja)
- **Casual users** memiliki pola **unimodal** dengan puncak jam 17:00 pada hari kerja
- Pada **weekend**, puncak terjadi jam 12:00-15:00 untuk kedua tipe pengguna
- **Registered users** mendominasi **81.2%** total penyewaan
""")

st.subheader("Insight Analisis Clustering")
st.markdown("""
- **Morning Rush (8-10)** dan **Afternoon Rush (15-17)** memiliki penyewaan tertinggi (>300), didominasi registered
- **Late Night (0-4)** volume terendah (<50), cocok untuk maintenance sepeda
- **Summer** dan **Spring** memiliki rasio casual tertinggi (>20%), cocok untuk promosi wisatawan
- **Winter** memiliki rasio casual terendah, didominasi pengguna komuter registered
""")

st.subheader("Rekomendasi Action Items")
st.markdown("""
1. **Optimasi Distribusi Sepeda**:
   - Tambah stok sepeda pada jam 7:00-9:00 dan 16:00-18:00 di hari kerja
   - Pada weekend, fokus distribusi jam 10:00-16:00 di area rekreasi

2. **Strategi Cuaca**:
   - Berikan promosi diskon saat cuaca hujan/salju
   - Sediakan aksesori pelindung hujan di stasiun

3. **Konversi Casual ke Registered**:
   - Targetkan promosi pada jam 12:00-16:00 di weekend
   - Buat program loyalitas untuk meningkatkan retensi pengguna casual
""")
