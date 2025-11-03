import streamlit as st

# Function for Sektor Agribisnis page
def show_agribisnis():
    st.title("🌾 Sektor Agribusiness")
    st.markdown("### Informasi Sektor Pertanian dan Agribisnis")
    
    tab1, tab2, tab3 = st.tabs(["Komoditas", "Lahan & Produksi", "Supply Chain"])
    
    with tab1:
        st.markdown("#### Data Komoditas Pertanian")
        st.write("Daftar komoditas unggulan:")
        komoditas = ["Padi", "Jagung", "Kedelai", "Cabai", "Bawang"]
        for k in komoditas:
            st.write(f"- {k}")
        
    with tab2:
        st.markdown("#### Informasi Lahan dan Produksi")
        st.write("Status lahan produktif:")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Lahan", "150 Ha")
        with col2:
            st.metric("Produktivitas", "85%")
        
    with tab3:
        st.markdown("#### Supply Chain Management")
        st.write("Alur distribusi produk:")
        st.info("Petani → Pengepul → Distributor → Retail → Konsumen")

# Function for Dashboard Bisnis page
def show_dashboard():
    st.title("📊 Dashboard Bisnis")
    st.markdown("### Analisis Performa Bisnis")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Revenue", "Rp 1.5M", "+12%")
    with col2:
        st.metric("Profit", "Rp 450K", "+8%")
    with col3:
        st.metric("Customers", "250", "+15%")
    with col4:
        st.metric("Growth", "15%", "+2%")
    
    st.markdown("### Grafik Penjualan")
    st.line_chart({"Penjualan": [100, 120, 130, 150, 140, 160]})

# Function for Prediksi & Analisis page
def show_prediksi():
    st.title("🔮 Prediksi & Analisis")
    
    tab1, tab2 = st.tabs(["Prediksi Market", "Analisis Trend"])
    
    with tab1:
        st.markdown("#### Prediksi Market")
        st.write("Prediksi harga komoditas:")
        st.line_chart({"Prediksi Harga": [50, 55, 53, 58, 60, 65]})
        
    with tab2:
        st.markdown("#### Analisis Trend")
        st.write("Trend pasar terkini:")
        st.bar_chart({"Trend": [20, 25, 30, 35, 25, 30]})

# Function for Komunitas & Gamifikasi page
def show_komunitas():
    st.title("👥 Komunitas & Gamifikasi")
    st.markdown("### Platform Komunitas dan Program Loyalitas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🏆 Leaderboard")
        leaderboard = ["Petani A - 1000 pts", "Petani B - 850 pts", "Petani C - 700 pts"]
        for rank, user in enumerate(leaderboard, 1):
            st.write(f"{rank}. {user}")
        
    with col2:
        st.markdown("#### 🎯 Misi & Rewards")
        st.write("Misi Aktif:")
        missions = ["Panen 100kg - 50 pts", "Share Tips - 30 pts", "Upload Foto - 20 pts"]
        for mission in missions:
            st.write(f"- {mission}")

# Main navigation
menu = st.sidebar.radio(
    "Navigasi",
    ["🌾 Sektor Agribusiness", "📊 Dashboard Bisnis", 
     "🔮 Prediksi & Analisis", "👥 Komunitas & Gamifikasi"]
)

# Route to appropriate page based on menu selection
if menu == "🌾 Sektor Agribusiness":
    show_agribisnis()
elif menu == "📊 Dashboard Bisnis":
    show_dashboard()
elif menu == "🔮 Prediksi & Analisis":
    show_prediksi()
elif menu == "👥 Komunitas & Gamifikasi":
    show_komunitas()
