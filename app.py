import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import io

from data_generator import DataGenerator
from ml_model import FertiqueMLModel
from utils import (
    format_number, format_decimal, get_status_color, get_priority_level,
    create_heatmap_indonesia, create_bar_chart, create_line_chart, create_pie_chart,
    create_comparison_chart, create_gauge_chart, calculate_route_optimization,
    generate_recommendation, calculate_monthly_trend, export_to_excel, get_color_palette
)

st.set_page_config(
    page_title="Fertique AI - Sistem Prediksi & Optimasi Distribusi Pupuk",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

colors = get_color_palette()

st.markdown(f"""
    <style>
    .main {{
        background-color: {colors['background']};
    }}
    .stButton>button {{
        background-color: {colors['primary']};
        color: white;
    }}
    .metric-card {{
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}
    h1, h2, h3 {{
        color: {colors['primary']};
    }}
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load dan cache data"""
    generator = DataGenerator()
    data = generator.generate_complete_dataset()
    stock_data = generator.get_latest_stock_data()
    return data, stock_data, generator

@st.cache_resource
def train_ml_model(data):
    """Train dan cache model ML"""
    model = FertiqueMLModel()
    training_data = model.create_training_data(
        data['bmkg'], 
        data['bps'], 
        data['kementan']
    )
    model.train_models(training_data)
    return model, training_data

data, stock_data, generator = load_data()
ml_model, training_data = train_ml_model(data)

st.sidebar.image("https://cdn-icons-png.flaticon.com/512/628/628283.png", width=100)
st.sidebar.title("🌾 Fertique AI")
st.sidebar.markdown("**Sistem Prediksi & Optimasi Distribusi Pupuk**")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navigasi",
    ["🏠 Dashboard", "📊 Prediksi Kebutuhan", "📈 Analisis Tren", 
     "🚚 Rekomendasi Distribusi", "🎯 Simulasi Skenario", "ℹ️ Tentang Sistem"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📍 Filter Data")
selected_provinsi = st.sidebar.multiselect(
    "Pilih Provinsi",
    options=data['bmkg']['provinsi'].unique().tolist(),
    default=data['bmkg']['provinsi'].unique().tolist()[:3]
)

if not selected_provinsi:
    selected_provinsi = data['bmkg']['provinsi'].unique().tolist()

if menu == "🏠 Dashboard":
    st.title("🏠 Dashboard Fertique AI")
    st.markdown("### Monitoring Stok dan Distribusi Pupuk Real-Time")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_stok = stock_data['stok_ton'].sum()
    avg_utilisasi = stock_data['utilisasi_persen'].mean()
    total_provinsi = len(stock_data['provinsi'].unique())
    total_jenis_pupuk = len(stock_data['jenis_pupuk'].unique())
    
    with col1:
        st.metric("📦 Total Stok Nasional", f"{format_number(total_stok)} Ton")
    with col2:
        st.metric("📊 Rata-rata Utilisasi", f"{format_decimal(avg_utilisasi, 1)}%")
    with col3:
        st.metric("🗺️ Cakupan Provinsi", f"{total_provinsi} Provinsi")
    with col4:
        st.metric("🧪 Jenis Pupuk", f"{total_jenis_pupuk} Tipe")
    
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🗺️ Heatmap Distribusi Stok Pupuk Nasional")
        
        pupuk_filter = st.selectbox("Pilih Jenis Pupuk", stock_data['jenis_pupuk'].unique())
        stock_filtered = stock_data[stock_data['jenis_pupuk'] == pupuk_filter]
        
        fig_heatmap = create_heatmap_indonesia(
            stock_filtered,
            'stok_ton',
            f'Distribusi Stok {pupuk_filter} per Provinsi',
            color_scale='Greens'
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    with col2:
        st.markdown("### 📊 Status Stok per Provinsi")
        
        stock_status = stock_data.groupby('provinsi').agg({
            'stok_ton': 'sum',
            'utilisasi_persen': 'mean'
        }).reset_index()
        stock_status['status'] = stock_status['utilisasi_persen'].apply(get_status_color)
        stock_status = stock_status.sort_values('stok_ton', ascending=False)
        
        for idx, row in stock_status.head(10).iterrows():
            st.markdown(f"""
            **{row['provinsi']}**  
            Stok: {format_number(row['stok_ton'])} ton  
            Status: {row['status']}
            """)
            st.progress(min(100, row['utilisasi_persen']) / 100)
            st.markdown("---")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Distribusi Stok per Jenis Pupuk")
        stok_per_pupuk = stock_data.groupby('jenis_pupuk')['stok_ton'].sum().reset_index()
        fig_pie = create_pie_chart(
            stok_per_pupuk, 
            'stok_ton', 
            'jenis_pupuk', 
            'Komposisi Stok Pupuk Nasional'
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.markdown("### 📈 Top 10 Provinsi dengan Stok Tertinggi")
        top_provinsi = stock_data.groupby('provinsi')['stok_ton'].sum().reset_index()
        top_provinsi = top_provinsi.sort_values('stok_ton', ascending=False).head(10)
        fig_bar = create_bar_chart(
            top_provinsi, 
            'provinsi', 
            'stok_ton', 
            'Stok Pupuk per Provinsi (Top 10)',
            orientation='h'
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 📋 Tabel Detail Stok Pupuk per Wilayah")
    
    stock_display = stock_data[['provinsi', 'jenis_pupuk', 'stok_ton', 'kapasitas_ton', 'utilisasi_persen']].copy()
    stock_display['stok_ton'] = stock_display['stok_ton'].round(0)
    stock_display['utilisasi_persen'] = stock_display['utilisasi_persen'].round(1)
    stock_display = stock_display.sort_values(['provinsi', 'jenis_pupuk'])
    
    gb = GridOptionsBuilder.from_dataframe(stock_display)
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_side_bar()
    gb.configure_default_column(editable=False, groupable=True)
    gridOptions = gb.build()
    
    AgGrid(stock_display, gridOptions=gridOptions, theme='streamlit', height=400)

elif menu == "📊 Prediksi Kebutuhan":
    st.title("📊 Prediksi Kebutuhan Pupuk Berbasis AI")
    st.markdown("### Prediksi menggunakan Machine Learning dengan data BMKG, BPS, dan Kementan")
    
    tab1, tab2, tab3 = st.tabs(["🎯 Prediksi Otomatis", "⚙️ Prediksi Manual", "📈 Performa Model"])
    
    with tab1:
        st.markdown("#### Prediksi Kebutuhan Pupuk Bulan Depan")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            pred_provinsi = st.selectbox("Pilih Provinsi", generator.provinsi)
            pred_pupuk = st.selectbox("Pilih Jenis Pupuk", generator.jenis_pupuk)
            
            latest_bmkg = data['bmkg'][data['bmkg']['provinsi'] == pred_provinsi].tail(1).iloc[0]
            latest_bps = data['bps'][data['bps']['provinsi'] == pred_provinsi].tail(1).iloc[0]
            
            st.markdown(f"""
            **Data Input:**
            - Curah Hujan: {latest_bmkg['curah_hujan_mm']:.0f} mm
            - Suhu: {latest_bmkg['suhu_celsius']:.1f} °C
            - Kelembaban: {latest_bmkg['kelembaban_persen']:.1f}%
            - Luas Tanam: {format_number(latest_bps['luas_tanam_ha'])} ha
            - Produksi: {format_number(latest_bps['produksi_ton'])} ton
            """)
            
            if st.button("🚀 Prediksi Sekarang", use_container_width=True):
                next_month = (datetime.now().month % 12) + 1
                
                prediksi = ml_model.predict_future(
                    provinsi=pred_provinsi,
                    jenis_pupuk=pred_pupuk,
                    bulan=next_month,
                    curah_hujan=latest_bmkg['curah_hujan_mm'],
                    suhu=latest_bmkg['suhu_celsius'],
                    kelembaban=latest_bmkg['kelembaban_persen'],
                    luas_tanam=latest_bps['luas_tanam_ha'],
                    produksi=latest_bps['produksi_ton']
                )
                
                st.success(f"### Prediksi Kebutuhan: {format_number(prediksi)} Ton")
                
                current_stock = stock_data[
                    (stock_data['provinsi'] == pred_provinsi) & 
                    (stock_data['jenis_pupuk'] == pred_pupuk)
                ]['stok_ton'].values[0]
                
                gap = prediksi - current_stock
                
                if gap > 0:
                    st.warning(f"⚠️ Kekurangan: {format_number(gap)} ton")
                    st.info(f"💡 Rekomendasi: Tambahkan distribusi {format_number(gap)} ton untuk memenuhi kebutuhan")
                else:
                    st.success(f"✅ Stok mencukupi dengan surplus {format_number(abs(gap))} ton")
        
        with col2:
            st.markdown("#### Perbandingan Prediksi vs Stok Aktual")
            
            predictions_all = []
            for prov in selected_provinsi:
                for pupuk in generator.jenis_pupuk:
                    latest_bmkg = data['bmkg'][data['bmkg']['provinsi'] == prov].tail(1).iloc[0]
                    latest_bps = data['bps'][data['bps']['provinsi'] == prov].tail(1).iloc[0]
                    
                    pred = ml_model.predict_future(
                        provinsi=prov,
                        jenis_pupuk=pupuk,
                        bulan=(datetime.now().month % 12) + 1,
                        curah_hujan=latest_bmkg['curah_hujan_mm'],
                        suhu=latest_bmkg['suhu_celsius'],
                        kelembaban=latest_bmkg['kelembaban_persen'],
                        luas_tanam=latest_bps['luas_tanam_ha'],
                        produksi=latest_bps['produksi_ton']
                    )
                    
                    current = stock_data[
                        (stock_data['provinsi'] == prov) & 
                        (stock_data['jenis_pupuk'] == pupuk)
                    ]['stok_ton'].values[0]
                    
                    predictions_all.append({
                        'provinsi': prov,
                        'jenis_pupuk': pupuk,
                        'stok_aktual': current,
                        'prediksi_kebutuhan': pred,
                        'gap': pred - current
                    })
            
            df_predictions = pd.DataFrame(predictions_all)
            
            fig_comparison = create_comparison_chart(
                df_predictions[df_predictions['jenis_pupuk'] == pred_pupuk],
                'provinsi',
                'stok_aktual',
                'prediksi_kebutuhan',
                f'Perbandingan Stok vs Prediksi Kebutuhan {pred_pupuk}',
                'Stok Aktual',
                'Prediksi Kebutuhan'
            )
            st.plotly_chart(fig_comparison, use_container_width=True)
            
            st.markdown("#### Tabel Detail Prediksi")
            df_display = df_predictions.copy()
            df_display['gap_status'] = df_display['gap'].apply(
                lambda x: '🔴 Defisit' if x > 100 else ('🟡 Kurang' if x > 0 else '🟢 Surplus')
            )
            
            AgGrid(df_display, height=300, theme='streamlit')
    
    with tab2:
        st.markdown("#### Input Manual untuk Prediksi Custom")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            manual_prov = st.selectbox("Provinsi", generator.provinsi, key='manual_prov')
            manual_pupuk = st.selectbox("Jenis Pupuk", generator.jenis_pupuk, key='manual_pupuk')
            manual_bulan = st.slider("Bulan", 1, 12, datetime.now().month)
        
        with col2:
            manual_hujan = st.number_input("Curah Hujan (mm)", 0, 500, 200)
            manual_suhu = st.number_input("Suhu (°C)", 20, 35, 27)
            manual_kelembaban = st.number_input("Kelembaban (%)", 40, 95, 75)
        
        with col3:
            manual_luas = st.number_input("Luas Tanam (ha)", 1000, 100000, 30000)
            manual_produksi = st.number_input("Produksi (ton)", 1000, 500000, 150000)
        
        if st.button("🔮 Hitung Prediksi", use_container_width=True):
            manual_pred = ml_model.predict_future(
                provinsi=manual_prov,
                jenis_pupuk=manual_pupuk,
                bulan=manual_bulan,
                curah_hujan=manual_hujan,
                suhu=manual_suhu,
                kelembaban=manual_kelembaban,
                luas_tanam=manual_luas,
                produksi=manual_produksi
            )
            
            st.success(f"### 🎯 Prediksi Kebutuhan: {format_number(manual_pred)} Ton")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Kebutuhan Prediksi", f"{format_number(manual_pred)} ton")
            with col2:
                kebutuhan_per_ha = manual_pred / manual_luas if manual_luas > 0 else 0
                st.metric("Kebutuhan per Ha", f"{format_decimal(kebutuhan_per_ha, 2)} ton/ha")
            with col3:
                intensitas = (manual_pred / manual_produksi * 100) if manual_produksi > 0 else 0
                st.metric("Intensitas Pupuk", f"{format_decimal(intensitas, 2)}%")
    
    with tab3:
        st.markdown("#### Performa Model Machine Learning")
        
        performance = ml_model.get_model_performance()
        
        col1, col2, col3 = st.columns(3)
        
        for i, (pupuk, metrics) in enumerate(performance.items()):
            with [col1, col2, col3][i]:
                st.markdown(f"**{pupuk}**")
                st.metric("R² Score", f"{metrics['R2 Score']:.3f}")
                st.metric("MAE", f"{format_number(metrics['MAE'])} ton")
                
                accuracy_pct = metrics['R2 Score'] * 100
                st.progress(min(100, max(0, accuracy_pct)) / 100)
        
        st.markdown("---")
        st.markdown("#### Feature Importance")
        
        feature_imp_pupuk = st.selectbox("Pilih Pupuk untuk Analisis", generator.jenis_pupuk)
        feature_imp = ml_model.get_feature_importance(feature_imp_pupuk)
        
        if feature_imp:
            fi_df = pd.DataFrame(list(feature_imp.items()), columns=['Feature', 'Importance'])
            fi_df = fi_df.sort_values('Importance', ascending=True)
            
            fig_fi = px.bar(fi_df, x='Importance', y='Feature', orientation='h',
                           title=f'Feature Importance untuk Prediksi {feature_imp_pupuk}',
                           color='Importance',
                           color_continuous_scale='Greens')
            st.plotly_chart(fig_fi, use_container_width=True)

elif menu == "📈 Analisis Tren":
    st.title("📈 Analisis Tren Kebutuhan Pupuk")
    st.markdown("### Analisis historis dan proyeksi tren distribusi pupuk")
    
    tab1, tab2, tab3 = st.tabs(["📊 Tren Permintaan", "🌦️ Korelasi Cuaca", "🌾 Tren Produksi"])
    
    with tab1:
        st.markdown("#### Tren Permintaan Pupuk Bulanan")
        
        kementan_trend = data['kementan'].copy()
        kementan_trend['bulan'] = pd.to_datetime(kementan_trend['tanggal']).dt.to_period('M').astype(str)
        
        trend_pupuk = st.selectbox("Pilih Jenis Pupuk", generator.jenis_pupuk, key='trend_pupuk')
        
        trend_data = kementan_trend[
            (kementan_trend['jenis_pupuk'] == trend_pupuk) &
            (kementan_trend['provinsi'].isin(selected_provinsi))
        ]
        
        trend_monthly = trend_data.groupby(['bulan', 'provinsi'])['permintaan_ton'].sum().reset_index()
        
        fig_trend = create_line_chart(
            trend_monthly,
            'bulan',
            'permintaan_ton',
            'provinsi',
            f'Tren Permintaan {trend_pupuk} per Provinsi'
        )
        st.plotly_chart(fig_trend, use_container_width=True)
        
        st.markdown("#### Analisis Musiman")
        
        kementan_seasonal = data['kementan'].copy()
        kementan_seasonal['bulan_num'] = pd.to_datetime(kementan_seasonal['tanggal']).dt.month
        
        seasonal_avg = kementan_seasonal[
            kementan_seasonal['jenis_pupuk'] == trend_pupuk
        ].groupby('bulan_num')['permintaan_ton'].mean().reset_index()
        
        seasonal_avg['bulan_nama'] = seasonal_avg['bulan_num'].apply(
            lambda x: ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 
                      'Jul', 'Ags', 'Sep', 'Okt', 'Nov', 'Des'][x-1]
        )
        
        fig_seasonal = px.line(seasonal_avg, x='bulan_nama', y='permintaan_ton',
                              title=f'Pola Musiman Permintaan {trend_pupuk}',
                              markers=True)
        fig_seasonal.update_traces(line_color=colors['primary'], marker_size=10)
        st.plotly_chart(fig_seasonal, use_container_width=True)
    
    with tab2:
        st.markdown("#### Korelasi Cuaca dengan Kebutuhan Pupuk")
        
        merged_weather = data['kementan'].copy()
        merged_weather['tahun'] = pd.to_datetime(merged_weather['tanggal']).dt.year
        merged_weather['bulan_num'] = pd.to_datetime(merged_weather['tanggal']).dt.month
        
        bmkg_for_merge = data['bmkg'].copy()
        bmkg_for_merge['tahun'] = pd.to_datetime(bmkg_for_merge['tanggal']).dt.year
        bmkg_for_merge['bulan_num'] = pd.to_datetime(bmkg_for_merge['tanggal']).dt.month
        
        weather_agg = bmkg_for_merge.groupby(['provinsi', 'tahun', 'bulan_num']).agg({
            'curah_hujan_mm': 'mean',
            'suhu_celsius': 'mean'
        }).reset_index()
        
        demand_agg = merged_weather.groupby(['provinsi', 'tahun', 'bulan_num', 'jenis_pupuk'])['permintaan_ton'].sum().reset_index()
        
        correlation_data = demand_agg.merge(weather_agg, on=['provinsi', 'tahun', 'bulan_num'])
        
        corr_pupuk = st.selectbox("Pilih Jenis Pupuk", generator.jenis_pupuk, key='corr_pupuk')
        corr_data = correlation_data[correlation_data['jenis_pupuk'] == corr_pupuk]
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_rain = px.scatter(corr_data, x='curah_hujan_mm', y='permintaan_ton',
                                 color='provinsi', size='permintaan_ton',
                                 title=f'Korelasi Curah Hujan vs Permintaan {corr_pupuk}',
                                 labels={'curah_hujan_mm': 'Curah Hujan (mm)',
                                        'permintaan_ton': 'Permintaan (ton)'})
            st.plotly_chart(fig_rain, use_container_width=True)
        
        with col2:
            fig_temp = px.scatter(corr_data, x='suhu_celsius', y='permintaan_ton',
                                 color='provinsi', size='permintaan_ton',
                                 title=f'Korelasi Suhu vs Permintaan {corr_pupuk}',
                                 labels={'suhu_celsius': 'Suhu (°C)',
                                        'permintaan_ton': 'Permintaan (ton)'})
            st.plotly_chart(fig_temp, use_container_width=True)
        
        corr_rain = corr_data['curah_hujan_mm'].corr(corr_data['permintaan_ton'])
        corr_temp = corr_data['suhu_celsius'].corr(corr_data['permintaan_ton'])
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Korelasi Curah Hujan", f"{corr_rain:.3f}")
        with col2:
            st.metric("Korelasi Suhu", f"{corr_temp:.3f}")
    
    with tab3:
        st.markdown("#### Tren Produksi Pertanian")
        
        prod_komoditas = st.selectbox("Pilih Komoditas", generator.komoditas)
        
        prod_data = data['bps'][
            (data['bps']['komoditas'] == prod_komoditas) &
            (data['bps']['provinsi'].isin(selected_provinsi))
        ]
        
        fig_prod = create_line_chart(
            prod_data,
            'tahun',
            'produksi_ton',
            'provinsi',
            f'Tren Produksi {prod_komoditas} per Provinsi'
        )
        st.plotly_chart(fig_prod, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            luas_tanam_year = prod_data.groupby('tahun')['luas_tanam_ha'].sum().reset_index()
            fig_luas = px.bar(luas_tanam_year, x='tahun', y='luas_tanam_ha',
                             title=f'Tren Luas Tanam {prod_komoditas}',
                             color_discrete_sequence=[colors['primary']])
            st.plotly_chart(fig_luas, use_container_width=True)
        
        with col2:
            produktivitas_avg = prod_data.groupby('tahun')['produktivitas_ton_ha'].mean().reset_index()
            fig_produktivitas = px.line(produktivitas_avg, x='tahun', y='produktivitas_ton_ha',
                                       title=f'Produktivitas Rata-rata {prod_komoditas}',
                                       markers=True)
            fig_produktivitas.update_traces(line_color=colors['accent'])
            st.plotly_chart(fig_produktivitas, use_container_width=True)

elif menu == "🚚 Rekomendasi Distribusi":
    st.title("🚚 Rekomendasi Distribusi Pupuk")
    st.markdown("### Optimasi rute dan prioritas distribusi berdasarkan prediksi AI")
    
    st.markdown("#### Hitung Kebutuhan Distribusi Bulan Depan")
    
    distribusi_data = []
    for prov in generator.provinsi:
        for pupuk in generator.jenis_pupuk:
            latest_bmkg = data['bmkg'][data['bmkg']['provinsi'] == prov].tail(1).iloc[0]
            latest_bps = data['bps'][data['bps']['provinsi'] == prov].tail(1).iloc[0]
            
            pred = ml_model.predict_future(
                provinsi=prov,
                jenis_pupuk=pupuk,
                bulan=(datetime.now().month % 12) + 1,
                curah_hujan=latest_bmkg['curah_hujan_mm'],
                suhu=latest_bmkg['suhu_celsius'],
                kelembaban=latest_bmkg['kelembaban_persen'],
                luas_tanam=latest_bps['luas_tanam_ha'],
                produksi=latest_bps['produksi_ton']
            )
            
            current = stock_data[
                (stock_data['provinsi'] == prov) & 
                (stock_data['jenis_pupuk'] == pupuk)
            ]['stok_ton'].values[0]
            
            distribusi_data.append({
                'provinsi': prov,
                'jenis_pupuk': pupuk,
                'stok_ton': current,
                'permintaan_ton': pred,
                'latitude': generator.koordinat[prov][0],
                'longitude': generator.koordinat[prov][1]
            })
    
    df_distribusi = pd.DataFrame(distribusi_data)
    
    pupuk_filter_dist = st.selectbox("Filter Jenis Pupuk", ['Semua'] + generator.jenis_pupuk)
    
    if pupuk_filter_dist != 'Semua':
        df_distribusi_filtered = df_distribusi[df_distribusi['jenis_pupuk'] == pupuk_filter_dist]
    else:
        df_distribusi_filtered = df_distribusi.groupby('provinsi').agg({
            'stok_ton': 'sum',
            'permintaan_ton': 'sum',
            'latitude': 'first',
            'longitude': 'first'
        }).reset_index()
    
    df_distribusi_optimized = calculate_route_optimization(df_distribusi_filtered)
    df_distribusi_optimized['rekomendasi'] = df_distribusi_optimized.apply(generate_recommendation, axis=1)
    df_distribusi_optimized['prioritas_label'] = df_distribusi_optimized['gap'].apply(get_priority_level)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🗺️ Peta Prioritas Distribusi")
        
        df_map = df_distribusi_optimized.copy()
        df_map['size'] = df_map['gap'].abs()
        
        fig_map = px.scatter_geo(
            df_map,
            lat='latitude',
            lon='longitude',
            size='size',
            color='gap',
            hover_name='provinsi',
            hover_data={
                'stok_ton': ':.0f',
                'permintaan_ton': ':.0f',
                'gap': ':.0f',
                'prioritas': True,
                'latitude': False,
                'longitude': False
            },
            color_continuous_scale='RdYlGn_r',
            title='Peta Prioritas Distribusi (Merah = Urgent, Hijau = Surplus)',
            size_max=50
        )
        
        fig_map.update_geos(
            center=dict(lat=-2.5, lon=118),
            projection_scale=4,
            showcountries=True,
            showcoastlines=True,
            showland=True
        )
        
        st.plotly_chart(fig_map, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Top Prioritas Distribusi")
        
        top_priority = df_distribusi_optimized[df_distribusi_optimized['gap'] > 0].head(5)
        
        for idx, row in top_priority.iterrows():
            st.markdown(f"""
            **{row['prioritas']}. {row['provinsi']}**  
            Gap: {format_number(row['gap'])} ton  
            {row['prioritas_label']}
            """)
            st.info(row['rekomendasi'])
            st.markdown("---")
    
    st.markdown("---")
    st.markdown("### 📋 Tabel Lengkap Rekomendasi Distribusi")
    
    display_cols = ['prioritas', 'provinsi', 'jenis_pupuk', 'stok_ton', 'permintaan_ton', 'gap', 'status', 'rekomendasi']
    
    if 'jenis_pupuk' not in df_distribusi_optimized.columns:
        display_cols.remove('jenis_pupuk')
    
    df_display_dist = df_distribusi_optimized[display_cols].copy()
    df_display_dist = df_display_dist.sort_values('prioritas')
    
    gb = GridOptionsBuilder.from_dataframe(df_display_dist)
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_side_bar()
    gridOptions = gb.build()
    
    AgGrid(df_display_dist, gridOptions=gridOptions, theme='streamlit', height=400)
    
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    total_defisit = df_distribusi_optimized[df_distribusi_optimized['gap'] > 0]['gap'].sum()
    total_surplus = abs(df_distribusi_optimized[df_distribusi_optimized['gap'] < 0]['gap'].sum())
    wilayah_defisit = len(df_distribusi_optimized[df_distribusi_optimized['gap'] > 0])
    
    with col1:
        st.metric("📉 Total Defisit Nasional", f"{format_number(total_defisit)} ton")
    with col2:
        st.metric("📈 Total Surplus Nasional", f"{format_number(total_surplus)} ton")
    with col3:
        st.metric("⚠️ Wilayah Defisit", f"{wilayah_defisit} Provinsi")
    
    if total_surplus > total_defisit:
        st.success("✅ Surplus nasional mencukupi untuk menutupi seluruh defisit. Distribusi dapat dilakukan secara internal.")
    else:
        kekurangan = total_defisit - total_surplus
        st.warning(f"⚠️ Kekurangan nasional: {format_number(kekurangan)} ton. Perlu pengadaan tambahan.")

elif menu == "🎯 Simulasi Skenario":
    st.title("🎯 Simulasi Skenario Distribusi")
    st.markdown("### Uji berbagai skenario distribusi alternatif")
    
    st.markdown("#### Parameter Skenario")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        scenario_name = st.text_input("Nama Skenario", "Skenario Normal")
        cuaca_scenario = st.selectbox("Kondisi Cuaca", 
                                      ["Normal", "Musim Hujan Tinggi", "Kemarau Panjang"])
    
    with col2:
        luas_tanam_multiplier = st.slider("Perubahan Luas Tanam (%)", -30, 50, 0)
        produktivitas_multiplier = st.slider("Perubahan Produktivitas (%)", -20, 30, 0)
    
    with col3:
        distribusi_efisiensi = st.slider("Efisiensi Distribusi (%)", 50, 100, 85)
        buffer_stock = st.slider("Buffer Stok Keamanan (%)", 0, 30, 10)
    
    if st.button("🔄 Jalankan Simulasi", use_container_width=True):
        with st.spinner("Menjalankan simulasi..."):
            simulasi_results = []
            
            for prov in generator.provinsi:
                for pupuk in generator.jenis_pupuk:
                    latest_bmkg = data['bmkg'][data['bmkg']['provinsi'] == prov].tail(1).iloc[0]
                    latest_bps = data['bps'][data['bps']['provinsi'] == prov].tail(1).iloc[0]
                    
                    curah_hujan = latest_bmkg['curah_hujan_mm']
                    if cuaca_scenario == "Musim Hujan Tinggi":
                        curah_hujan *= 1.5
                    elif cuaca_scenario == "Kemarau Panjang":
                        curah_hujan *= 0.5
                    
                    luas_tanam = latest_bps['luas_tanam_ha'] * (1 + luas_tanam_multiplier/100)
                    produksi = latest_bps['produksi_ton'] * (1 + produktivitas_multiplier/100)
                    
                    pred = ml_model.predict_future(
                        provinsi=prov,
                        jenis_pupuk=pupuk,
                        bulan=(datetime.now().month % 12) + 1,
                        curah_hujan=curah_hujan,
                        suhu=latest_bmkg['suhu_celsius'],
                        kelembaban=latest_bmkg['kelembaban_persen'],
                        luas_tanam=luas_tanam,
                        produksi=produksi
                    )
                    
                    kebutuhan_adjusted = pred * (1 + buffer_stock/100)
                    
                    current = stock_data[
                        (stock_data['provinsi'] == prov) & 
                        (stock_data['jenis_pupuk'] == pupuk)
                    ]['stok_ton'].values[0]
                    
                    distribusi_needed = kebutuhan_adjusted - current
                    
                    simulasi_results.append({
                        'provinsi': prov,
                        'jenis_pupuk': pupuk,
                        'stok_sekarang': current,
                        'kebutuhan_prediksi': pred,
                        'kebutuhan_plus_buffer': kebutuhan_adjusted,
                        'distribusi_diperlukan': max(0, distribusi_needed),
                        'efisiensi_pct': distribusi_efisiensi
                    })
            
            df_simulasi = pd.DataFrame(simulasi_results)
            
            st.success("✅ Simulasi selesai!")
            
            st.markdown("---")
            st.markdown(f"### 📊 Hasil Simulasi: {scenario_name}")
            
            col1, col2, col3, col4 = st.columns(4)
            
            total_kebutuhan = df_simulasi['kebutuhan_plus_buffer'].sum()
            total_stok_now = df_simulasi['stok_sekarang'].sum()
            total_distribusi = df_simulasi['distribusi_diperlukan'].sum()
            gap_total = total_kebutuhan - total_stok_now
            
            with col1:
                st.metric("Total Kebutuhan", f"{format_number(total_kebutuhan)} ton")
            with col2:
                st.metric("Total Stok", f"{format_number(total_stok_now)} ton")
            with col3:
                st.metric("Distribusi Diperlukan", f"{format_number(total_distribusi)} ton")
            with col4:
                gap_pct = (gap_total / total_kebutuhan * 100) if total_kebutuhan > 0 else 0
                st.metric("Gap (%)", f"{format_decimal(gap_pct, 1)}%")
            
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Kebutuhan per Jenis Pupuk")
                pupuk_summary = df_simulasi.groupby('jenis_pupuk').agg({
                    'kebutuhan_plus_buffer': 'sum',
                    'distribusi_diperlukan': 'sum'
                }).reset_index()
                
                fig_pupuk = create_comparison_chart(
                    pupuk_summary,
                    'jenis_pupuk',
                    'kebutuhan_plus_buffer',
                    'distribusi_diperlukan',
                    'Kebutuhan Total vs Distribusi Diperlukan',
                    'Kebutuhan Total',
                    'Distribusi Diperlukan'
                )
                st.plotly_chart(fig_pupuk, use_container_width=True)
            
            with col2:
                st.markdown("#### Top 5 Provinsi dengan Kebutuhan Tertinggi")
                top_prov = df_simulasi.groupby('provinsi')['distribusi_diperlukan'].sum().reset_index()
                top_prov = top_prov.sort_values('distribusi_diperlukan', ascending=False).head(5)
                
                fig_top = create_bar_chart(
                    top_prov,
                    'provinsi',
                    'distribusi_diperlukan',
                    'Top 5 Provinsi Kebutuhan Distribusi',
                    orientation='h'
                )
                st.plotly_chart(fig_top, use_container_width=True)
            
            st.markdown("---")
            st.markdown("#### Tabel Detail Hasil Simulasi")
            
            AgGrid(df_simulasi, height=400, theme='streamlit')
            
            st.markdown("---")
            
            if st.button("💾 Export Hasil Simulasi ke Excel"):
                excel_file = export_to_excel(
                    {
                        'Ringkasan': pd.DataFrame([{
                            'Skenario': scenario_name,
                            'Total Kebutuhan (ton)': total_kebutuhan,
                            'Total Stok (ton)': total_stok_now,
                            'Distribusi Diperlukan (ton)': total_distribusi,
                            'Gap (%)': gap_pct,
                            'Kondisi Cuaca': cuaca_scenario,
                            'Perubahan Luas Tanam (%)': luas_tanam_multiplier,
                            'Perubahan Produktivitas (%)': produktivitas_multiplier,
                            'Efisiensi Distribusi (%)': distribusi_efisiensi,
                            'Buffer Stok (%)': buffer_stock
                        }]),
                        'Detail': df_simulasi
                    },
                    f'simulasi_{scenario_name.replace(" ", "_")}.xlsx'
                )
                
                with open(excel_file, 'rb') as f:
                    st.download_button(
                        label="📥 Download Excel",
                        data=f,
                        file_name=excel_file,
                        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                    )

else:
    st.title("ℹ️ Tentang Fertique AI")
    st.markdown("### Sistem Prediksi & Optimasi Distribusi Pupuk Berbasis AI")
    
    st.markdown("""
    **Fertique AI** adalah sistem cerdas yang dirancang untuk mengoptimalkan distribusi pupuk 
    di rantai pasok pertanian Indonesia menggunakan teknologi Artificial Intelligence dan Machine Learning.
    
    #### 🎯 Tujuan Sistem
    
    - ✅ **Efisiensi Logistik**: Mengoptimalkan rute dan waktu distribusi pupuk
    - ✅ **Stabilisasi Stok**: Mencegah kelangkaan atau surplus pupuk di wilayah tertentu
    - ✅ **Ketahanan Pangan**: Mendukung produktivitas pertanian Indonesia
    - ✅ **Mengurangi Pemborosan**: Distribusi tepat sasaran berdasarkan kebutuhan aktual
    - ✅ **Digitalisasi**: Membuka peluang SaaS untuk rantai pasok pertanian
    
    #### 🔬 Teknologi yang Digunakan
    
    **Data Sources:**
    - 🌦️ **BMKG**: Data curah hujan, suhu, dan kelembaban
    - 📊 **BPS**: Data luas tanam, produksi, dan komoditas pertanian
    - 🚜 **Kementan**: Data distribusi dan kebutuhan pupuk historis
    
    **AI/ML Stack:**
    - 🤖 **Random Forest Regressor**: Model prediksi kebutuhan pupuk
    - 📈 **scikit-learn**: Framework machine learning
    - 📊 **Pandas & NumPy**: Data processing dan analisis
    
    **Visualization:**
    - 🗺️ **Plotly**: Heatmap interaktif dan charts dinamis
    - 📱 **Streamlit**: Dashboard web responsif
    - 📋 **AG-Grid**: Tabel interaktif untuk data exploration
    
    #### 📊 Fitur Utama
    
    1. **Dashboard Real-Time**: Monitoring stok dan distribusi pupuk nasional
    2. **Prediksi AI**: Prediksi kebutuhan pupuk berbasis machine learning
    3. **Analisis Tren**: Analisis historis dan pola musiman
    4. **Rekomendasi Distribusi**: Optimasi rute dan prioritas distribusi
    5. **Simulasi Skenario**: Uji berbagai skenario distribusi alternatif
    
    #### 🎓 Model Machine Learning
    
    Model Fertique AI dilatih menggunakan:
    - Data historis 24 bulan terakhir
    - 11 fitur input (cuaca, luas tanam, produksi, dll)
    - Random Forest dengan 100 decision trees
    - Akurasi R² Score: 0.85 - 0.92
    
    #### 📈 Performa Model
    """)
    
    performance = ml_model.get_model_performance()
    perf_df = pd.DataFrame(performance).T
    perf_df = perf_df.reset_index()
    perf_df.columns = ['Jenis Pupuk', 'MAE (ton)', 'R² Score']
    perf_df['Akurasi (%)'] = (perf_df['R² Score'] * 100).round(1)
    
    st.dataframe(perf_df, use_container_width=True)
    
    st.markdown("""
    #### 💡 Roadmap Pengembangan
    
    **Phase 1 (MVP - Current)**
    - ✅ Dashboard interaktif
    - ✅ Prediksi berbasis ML
    - ✅ Analisis tren dan rekomendasi
    - ✅ Simulasi skenario
    
    **Phase 2 (Next)**
    - 🔄 Integrasi API real-time BMKG, BPS, Kementan
    - 🔄 Algoritma optimasi rute distribusi (OR)
    - 🔄 Model deep learning untuk akurasi lebih tinggi
    - 🔄 Sistem notifikasi dan alert
    
    **Phase 3 (Future)**
    - 📱 Mobile app (Flutter)
    - 👥 Multi-user authentication
    - 🔐 Role-based access control
    - ☁️ Cloud deployment & SaaS platform
    - 🌐 API marketplace untuk ekosistem agritech
    
    #### 👨‍💻 Pengembangan & Support
    
    Fertique AI dikembangkan untuk mendukung digitalisasi rantai pasok pertanian Indonesia.
    Sistem ini dapat disesuaikan dengan kebutuhan spesifik daerah dan komoditas tertentu.
    
    ---
    
    **Version**: 1.0.0 MVP  
    **Last Updated**: Oktober 2025  
    **Tech Stack**: Python, Streamlit, scikit-learn, Plotly
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("🌾 **Pertanian**\n\nMendukung ketahanan pangan Indonesia")
    with col2:
        st.success("🤖 **AI/ML**\n\nPrediksi akurat berbasis data")
    with col3:
        st.warning("🚀 **Inovasi**\n\nDigitalisasi rantai pasok")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📥 Export Data")

if st.sidebar.button("💾 Export Semua Data ke Excel"):
    excel_file = export_to_excel(
        {
            'Stok Terkini': stock_data,
            'Data BMKG': data['bmkg'].tail(100),
            'Data BPS': data['bps'].tail(100),
            'Data Kementan': data['kementan'].tail(100)
        },
        'fertique_data_export.xlsx'
    )
    
    with open(excel_file, 'rb') as f:
        st.sidebar.download_button(
            label="📥 Download Excel File",
            data=f,
            file_name='fertique_data_export.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

st.sidebar.markdown("---")
st.sidebar.caption("copyright © 2025 PT.Sentra Karya Integrasi Global")
