import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class AgribusinessDataGenerator:
    """Generator data simulasi untuk semua sektor agribusiness"""
    
    def __init__(self):
        self.provinsi = [
            'Jawa Barat', 'Jawa Tengah', 'Jawa Timur', 'Sumatera Utara', 
            'Sumatera Selatan', 'Sulawesi Selatan', 'Kalimantan Selatan',
            'Bali', 'Nusa Tenggara Barat', 'Lampung'
        ]
        
        # Expanded sectors for full agribusiness coverage
        self.sectors = {
            'Pertanian': {
                'komoditas': ['Padi', 'Jagung', 'Kedelai', 'Tebu', 'Kelapa Sawit', 'Kopi', 'Kakao'],
                'input': ['Urea', 'NPK', 'ZA', 'Kompos', 'Pestisida'],
                'unit': 'ton',
                'price_range': (15000, 50000)
            },
            'Hortikultura': {
                'komoditas': ['Cabai', 'Tomat', 'Bawang Merah', 'Kentang', 'Wortel', 'Sawi', 'Kangkung'],
                'input': ['Pupuk Organik', 'NPK', 'Fungisida', 'Insektisida'],
                'unit': 'kg',
                'price_range': (5000, 80000)
            },
            'Peternakan': {
                'komoditas': ['Ayam Broiler', 'Ayam Petelur', 'Sapi Potong', 'Sapi Perah', 'Kambing', 'Domba'],
                'input': ['Pakan Konsentrat', 'Vitamin', 'Obat-obatan', 'Vaksin'],
                'unit': 'ekor/liter',
                'price_range': (3000, 150000)
            },
            'Perikanan': {
                'komoditas': ['Lele', 'Nila', 'Gurame', 'Udang Vaname', 'Bandeng', 'Patin'],
                'input': ['Pelet', 'Probiotik', 'Vitamin Ikan', 'Aerator'],
                'unit': 'kg',
                'price_range': (15000, 120000)
            }
        }
        
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
    
    def generate_weather_data(self, months=12):
        """Generate comprehensive weather data"""
        data = []
        base_date = datetime.now() - timedelta(days=30*months)
        
        for prov in self.provinsi:
            for i in range(months):
                date = base_date + timedelta(days=30*i)
                month = date.month
                
                # Seasonal variations
                if month in [11, 12, 1, 2, 3]:
                    curah_hujan = np.random.normal(300, 80)
                    kelembaban = np.random.normal(85, 5)
                else:
                    curah_hujan = np.random.normal(100, 40)
                    kelembaban = np.random.normal(65, 10)
                
                suhu_rata = np.random.normal(27, 2)
                
                data.append({
                    'tanggal': date,
                    'provinsi': prov,
                    'curah_hujan_mm': max(0, curah_hujan),
                    'suhu_celsius': suhu_rata,
                    'kelembaban_persen': np.clip(kelembaban, 40, 95),
                    'kecepatan_angin': np.random.normal(10, 3),
                    'durasi_sinar_matahari': np.random.normal(6, 2)
                })
        
        return pd.DataFrame(data)
    
    def generate_production_data(self, sector, years=2):
        """Generate production data for specific sector"""
        data = []
        base_year = datetime.now().year - years
        
        sector_info = self.sectors.get(sector, self.sectors['Pertanian'])
        
        for year in range(base_year, base_year + years + 1):
            for prov in self.provinsi:
                for komoditas in sector_info['komoditas']:
                    
                    if sector == 'Pertanian':
                        luas_area = np.random.normal(30000, 8000)
                        produksi = luas_area * np.random.normal(4.5, 1.2)
                    elif sector == 'Hortikultura':
                        luas_area = np.random.normal(5000, 2000)
                        produksi = luas_area * np.random.normal(15, 5)
                    elif sector == 'Peternakan':
                        luas_area = np.random.normal(10000, 3000)
                        produksi = luas_area * np.random.normal(1.8, 0.5)
                    else:  # Perikanan
                        luas_area = np.random.normal(500, 150)
                        produksi = luas_area * np.random.normal(25, 8)
                    
                    harga = np.random.uniform(*sector_info['price_range'])
                    
                    data.append({
                        'tahun': year,
                        'provinsi': prov,
                        'sektor': sector,
                        'komoditas': komoditas,
                        'luas_area': max(100, luas_area),
                        'produksi': max(100, produksi),
                        'unit': sector_info['unit'],
                        'harga_per_unit': harga,
                        'nilai_produksi': produksi * harga
                    })
        
        return pd.DataFrame(data)
    
    def generate_input_needs(self, sector, months=12):
        """Generate input needs (feed, fertilizer, medicine) for sector"""
        data = []
        base_date = datetime.now() - timedelta(days=30*months)
        
        sector_info = self.sectors.get(sector, self.sectors['Pertanian'])
        
        for prov in self.provinsi:
            for i in range(months):
                date = base_date + timedelta(days=30*i)
                month = date.month
                
                # Seasonal multiplier
                if month in [10, 11, 12, 1, 2]:
                    multiplier = 1.5
                elif month in [4, 5, 6]:
                    multiplier = 1.3
                else:
                    multiplier = 0.9
                
                for input_item in sector_info['input']:
                    stok = np.random.normal(3000, 800) * multiplier
                    permintaan = np.random.normal(2500, 600) * multiplier
                    distribusi = np.random.normal(2000, 500) * multiplier
                    
                    data.append({
                        'tanggal': date,
                        'provinsi': prov,
                        'sektor': sector,
                        'jenis_input': input_item,
                        'stok_awal': max(0, stok),
                        'distribusi_masuk': max(0, distribusi),
                        'permintaan': max(0, permintaan),
                        'stok_akhir': max(0, stok + distribusi - permintaan),
                        'harga_satuan': np.random.uniform(10000, 50000)
                    })
        
        return pd.DataFrame(data)
    
    def generate_market_prices(self, sector, days=90):
        """Generate market price trends"""
        data = []
        base_date = datetime.now() - timedelta(days=days)
        
        sector_info = self.sectors.get(sector, self.sectors['Pertanian'])
        
        for komoditas in sector_info['komoditas'][:5]:
            base_price = np.random.uniform(*sector_info['price_range'])
            
            for i in range(days):
                date = base_date + timedelta(days=i)
                
                # Random walk with trend
                price_change = np.random.normal(0, base_price * 0.02)
                price = base_price + price_change
                base_price = price  # Update for next day
                
                data.append({
                    'tanggal': date,
                    'sektor': sector,
                    'komoditas': komoditas,
                    'harga': max(price * 0.5, price),
                    'volume_transaksi': np.random.normal(1000, 300),
                    'sumber': np.random.choice(['Pasar Lokal', 'Distributor', 'Online'])
                })
        
        return pd.DataFrame(data)
    
    def generate_sme_profile(self, num_smes=50):
        """Generate SME business profiles"""
        data = []
        
        for i in range(num_smes):
            sector = np.random.choice(list(self.sectors.keys()))
            prov = np.random.choice(self.provinsi)
            sector_info = self.sectors[sector]
            
            modal = np.random.uniform(10000000, 500000000)
            omzet = modal * np.random.uniform(0.8, 2.5)
            profit = omzet * np.random.uniform(0.1, 0.35)
            
            data.append({
                'id_sme': f'SME{i+1:04d}',
                'nama_usaha': f'{sector_info["komoditas"][0]} {prov[:4]}',
                'provinsi': prov,
                'sektor': sector,
                'komoditas_utama': np.random.choice(sector_info['komoditas']),
                'tahun_berdiri': np.random.randint(2015, 2024),
                'modal_usaha': modal,
                'omzet_bulanan': omzet / 12,
                'profit_margin': (profit / omzet) * 100 if omzet > 0 else 0,
                'jumlah_karyawan': np.random.randint(1, 25),
                'luas_lahan': np.random.uniform(0.5, 20),
                'status': np.random.choice(['Berkembang', 'Stabil', 'Baru Mulai'])
            })
        
        return pd.DataFrame(data)
    
    def get_current_stock_data(self, sector):
        """Get current stock levels for sector inputs"""
        data = []
        sector_info = self.sectors.get(sector, self.sectors['Pertanian'])
        
        for prov in self.provinsi:
            for input_item in sector_info['input']:
                stok = np.random.normal(5000, 1500)
                kapasitas = 12000
                
                data.append({
                    'provinsi': prov,
                    'sektor': sector,
                    'jenis_input': input_item,
                    'stok': max(0, stok),
                    'kapasitas': kapasitas,
                    'utilisasi_persen': (stok / kapasitas) * 100,
                    'latitude': self.koordinat[prov][0],
                    'longitude': self.koordinat[prov][1]
                })
        
        return pd.DataFrame(data)
