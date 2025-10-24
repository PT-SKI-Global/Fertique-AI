import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class DataGenerator:
    """Generator data simulasi untuk BMKG, BPS, dan Kementan"""
    
    def __init__(self):
        self.provinsi = [
            'Jawa Barat', 'Jawa Tengah', 'Jawa Timur', 'Sumatera Utara', 
            'Sumatera Selatan', 'Sulawesi Selatan', 'Kalimantan Selatan',
            'Bali', 'Nusa Tenggara Barat', 'Lampung'
        ]
        
        self.kabupaten = {
            'Jawa Barat': ['Bandung', 'Bogor', 'Sukabumi', 'Cianjur', 'Garut'],
            'Jawa Tengah': ['Semarang', 'Solo', 'Magelang', 'Purworejo', 'Klaten'],
            'Jawa Timur': ['Surabaya', 'Malang', 'Kediri', 'Jember', 'Banyuwangi'],
            'Sumatera Utara': ['Medan', 'Deli Serdang', 'Simalungun', 'Asahan', 'Labuhanbatu'],
            'Sumatera Selatan': ['Palembang', 'Ogan Ilir', 'Banyuasin', 'Muara Enim', 'OKU'],
            'Sulawesi Selatan': ['Makassar', 'Gowa', 'Bone', 'Wajo', 'Sidrap'],
            'Kalimantan Selatan': ['Banjarmasin', 'Hulu Sungai', 'Tapin', 'Barito Kuala', 'Tanah Laut'],
            'Bali': ['Denpasar', 'Tabanan', 'Gianyar', 'Buleleng', 'Karangasem'],
            'Nusa Tenggara Barat': ['Mataram', 'Lombok Tengah', 'Lombok Timur', 'Sumbawa', 'Dompu'],
            'Lampung': ['Bandar Lampung', 'Lampung Tengah', 'Lampung Selatan', 'Lampung Timur', 'Tulang Bawang']
        }
        
        self.komoditas = ['Padi', 'Jagung', 'Kedelai', 'Tebu', 'Kelapa Sawit']
        self.jenis_pupuk = ['Urea', 'NPK', 'ZA']
        
        # Koordinat untuk heatmap (latitude, longitude)
        self.koordinat = {
            'Jawa Barat': (-6.9175, 107.6191),
            'Jawa Tengah': (-7.1504, 110.1403),
            'Jawa Timur': (-7.5361, 112.2384),
            'Sumatera Utara': (3.5952, 98.6722),
            'Sumatera Selatan': (-3.3194, 104.9147),
            'Sulawesi Selatan': (-5.1477, 119.4327),
            'Kalimantan Selatan': (-3.0926, 115.2838),
            'Bali': (-8.4095, 115.1889),
            'Nusa Tenggara Barat': (-8.5833, 116.1167),
            'Lampung': (-5.4500, 105.2667)
        }
        
    def generate_bmkg_data(self, months=12):
        """Generate data cuaca dari BMKG (curah hujan, suhu)"""
        data = []
        base_date = datetime.now() - timedelta(days=30*months)
        
        for prov in self.provinsi:
            for i in range(months):
                date = base_date + timedelta(days=30*i)
                
                # Simulasi curah hujan (mm/bulan) - variasi musiman
                month = date.month
                if month in [11, 12, 1, 2, 3]:  # Musim hujan
                    curah_hujan = np.random.normal(300, 80)
                else:  # Musim kemarau
                    curah_hujan = np.random.normal(100, 40)
                
                # Simulasi suhu (Celsius)
                suhu_rata = np.random.normal(27, 2)
                
                # Kelembaban (%)
                kelembaban = np.random.normal(75, 10)
                
                data.append({
                    'tanggal': date,
                    'provinsi': prov,
                    'curah_hujan_mm': max(0, curah_hujan),
                    'suhu_celsius': suhu_rata,
                    'kelembaban_persen': np.clip(kelembaban, 40, 95)
                })
        
        return pd.DataFrame(data)
    
    def generate_bps_data(self, years=3):
        """Generate data BPS (luas tanam, produksi)"""
        data = []
        base_year = datetime.now().year - years
        
        for year in range(base_year, base_year + years + 1):
            for prov in self.provinsi:
                for komoditas in self.komoditas:
                    # Luas tanam (hektar) - berbeda per provinsi dan komoditas
                    if komoditas == 'Padi':
                        luas_tanam = np.random.normal(50000, 10000)
                    elif komoditas == 'Jagung':
                        luas_tanam = np.random.normal(30000, 8000)
                    elif komoditas == 'Kedelai':
                        luas_tanam = np.random.normal(15000, 5000)
                    elif komoditas == 'Tebu':
                        luas_tanam = np.random.normal(20000, 6000)
                    else:  # Kelapa Sawit
                        luas_tanam = np.random.normal(40000, 12000)
                    
                    # Produktivitas (ton/hektar)
                    if komoditas == 'Padi':
                        produktivitas = np.random.normal(5.5, 0.8)
                    elif komoditas == 'Jagung':
                        produktivitas = np.random.normal(5.0, 0.7)
                    elif komoditas == 'Kedelai':
                        produktivitas = np.random.normal(1.5, 0.3)
                    elif komoditas == 'Tebu':
                        produktivitas = np.random.normal(80, 15)
                    else:  # Kelapa Sawit
                        produktivitas = np.random.normal(20, 4)
                    
                    luas_tanam = max(1000, luas_tanam)
                    produksi = luas_tanam * produktivitas
                    
                    data.append({
                        'tahun': year,
                        'provinsi': prov,
                        'komoditas': komoditas,
                        'luas_tanam_ha': luas_tanam,
                        'produktivitas_ton_ha': produktivitas,
                        'produksi_ton': produksi
                    })
        
        return pd.DataFrame(data)
    
    def generate_kementan_data(self, months=12):
        """Generate data Kementan (distribusi pupuk historis)"""
        data = []
        base_date = datetime.now() - timedelta(days=30*months)
        
        for prov in self.provinsi:
            for kabupaten in self.kabupaten[prov]:
                for i in range(months):
                    date = base_date + timedelta(days=30*i)
                    
                    for pupuk in self.jenis_pupuk:
                        # Kebutuhan pupuk bervariasi per musim tanam
                        month = date.month
                        if month in [10, 11, 12]:  # Musim tanam
                            multiplier = 1.5
                        elif month in [4, 5, 6]:  # Musim tanam kedua
                            multiplier = 1.3
                        else:
                            multiplier = 0.8
                        
                        # Stok gudang (ton)
                        stok_awal = np.random.normal(500, 100) * multiplier
                        
                        # Distribusi/penyaluran (ton)
                        distribusi = np.random.normal(400, 80) * multiplier
                        
                        # Permintaan (ton)
                        permintaan = np.random.normal(450, 90) * multiplier
                        
                        stok_akhir = max(0, stok_awal + distribusi - permintaan)
                        
                        data.append({
                            'tanggal': date,
                            'provinsi': prov,
                            'kabupaten': kabupaten,
                            'jenis_pupuk': pupuk,
                            'stok_awal_ton': max(0, stok_awal),
                            'distribusi_masuk_ton': max(0, distribusi),
                            'permintaan_ton': max(0, permintaan),
                            'stok_akhir_ton': stok_akhir
                        })
        
        return pd.DataFrame(data)
    
    def get_latest_stock_data(self):
        """Get stok pupuk terkini per provinsi"""
        data = []
        for prov in self.provinsi:
            for pupuk in self.jenis_pupuk:
                stok = np.random.normal(5000, 1000)
                kapasitas = 10000
                
                data.append({
                    'provinsi': prov,
                    'jenis_pupuk': pupuk,
                    'stok_ton': max(0, stok),
                    'kapasitas_ton': kapasitas,
                    'utilisasi_persen': (stok / kapasitas) * 100,
                    'latitude': self.koordinat[prov][0],
                    'longitude': self.koordinat[prov][1]
                })
        
        return pd.DataFrame(data)
    
    def generate_complete_dataset(self):
        """Generate dataset lengkap untuk training model"""
        bmkg = self.generate_bmkg_data(months=24)
        bps = self.generate_bps_data(years=3)
        kementan = self.generate_kementan_data(months=24)
        
        return {
            'bmkg': bmkg,
            'bps': bps,
            'kementan': kementan
        }
