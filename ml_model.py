import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import pickle

class FertiqueMLModel:
    """Model Machine Learning untuk prediksi kebutuhan pupuk"""
    
    def __init__(self):
        self.models = {}
        self.label_encoders = {}
        self.feature_names = []
        self.is_trained = False
        
    def prepare_features(self, bmkg_data, bps_data, kementan_data):
        """Gabungkan dan prepare features dari berbagai sumber data"""
        
        # Agregasi data BMKG per provinsi per bulan
        bmkg_agg = bmkg_data.groupby(['provinsi', pd.Grouper(key='tanggal', freq='M')]).agg({
            'curah_hujan_mm': 'mean',
            'suhu_celsius': 'mean',
            'kelembaban_persen': 'mean'
        }).reset_index()
        
        # Agregasi data BPS per provinsi per tahun
        bps_agg = bps_data.groupby(['provinsi', 'tahun']).agg({
            'luas_tanam_ha': 'sum',
            'produksi_ton': 'sum'
        }).reset_index()
        
        # Agregasi data Kementan per provinsi per bulan per jenis pupuk
        kementan_data['bulan'] = pd.to_datetime(kementan_data['tanggal']).dt.to_period('M')
        kementan_agg = kementan_data.groupby(['provinsi', 'bulan', 'jenis_pupuk']).agg({
            'permintaan_ton': 'sum',
            'distribusi_masuk_ton': 'sum',
            'stok_akhir_ton': 'mean'
        }).reset_index()
        
        return bmkg_agg, bps_agg, kementan_agg
    
    def create_training_data(self, bmkg_data, bps_data, kementan_data):
        """Buat dataset training dengan feature engineering"""
        
        # Prepare data
        kementan_data = kementan_data.copy()
        kementan_data['tahun'] = pd.to_datetime(kementan_data['tanggal']).dt.year
        kementan_data['bulan_num'] = pd.to_datetime(kementan_data['tanggal']).dt.month
        kementan_data['kuartal'] = pd.to_datetime(kementan_data['tanggal']).dt.quarter
        
        bmkg_data = bmkg_data.copy()
        bmkg_data['tahun'] = pd.to_datetime(bmkg_data['tanggal']).dt.year
        bmkg_data['bulan_num'] = pd.to_datetime(bmkg_data['tanggal']).dt.month
        
        # Merge datasets
        # Agregasi BMKG per provinsi, tahun, bulan
        bmkg_monthly = bmkg_data.groupby(['provinsi', 'tahun', 'bulan_num']).agg({
            'curah_hujan_mm': 'mean',
            'suhu_celsius': 'mean',
            'kelembaban_persen': 'mean'
        }).reset_index()
        
        # Agregasi BPS per provinsi, tahun
        bps_yearly = bps_data.groupby(['provinsi', 'tahun']).agg({
            'luas_tanam_ha': 'sum',
            'produksi_ton': 'sum'
        }).reset_index()
        
        # Agregasi Kementan per provinsi, tahun, bulan, jenis pupuk
        kementan_agg = kementan_data.groupby(['provinsi', 'tahun', 'bulan_num', 'jenis_pupuk']).agg({
            'permintaan_ton': 'sum',
            'distribusi_masuk_ton': 'sum',
            'stok_akhir_ton': 'mean'
        }).reset_index()
        
        # Merge semua data
        merged = kementan_agg.merge(
            bmkg_monthly, 
            on=['provinsi', 'tahun', 'bulan_num'], 
            how='left'
        )
        
        merged = merged.merge(
            bps_yearly,
            on=['provinsi', 'tahun'],
            how='left'
        )
        
        # Fill missing values
        merged = merged.fillna(method='ffill').fillna(method='bfill')
        
        # Encode categorical variables
        for col in ['provinsi', 'jenis_pupuk']:
            if col not in self.label_encoders:
                self.label_encoders[col] = LabelEncoder()
                merged[f'{col}_encoded'] = self.label_encoders[col].fit_transform(merged[col])
            else:
                merged[f'{col}_encoded'] = self.label_encoders[col].transform(merged[col])
        
        # Feature engineering
        merged['curah_hujan_kategori'] = pd.cut(merged['curah_hujan_mm'], 
                                                 bins=[0, 100, 200, 300, 500, np.inf], 
                                                 labels=[0, 1, 2, 3, 4])
        merged['curah_hujan_kategori'] = merged['curah_hujan_kategori'].astype(int)
        
        merged['musim_tanam'] = merged['bulan_num'].apply(
            lambda x: 1 if x in [10, 11, 12, 1, 2, 3] else 0
        )
        
        # Lag features (permintaan bulan lalu)
        merged = merged.sort_values(['provinsi', 'jenis_pupuk', 'tahun', 'bulan_num'])
        merged['permintaan_lag1'] = merged.groupby(['provinsi', 'jenis_pupuk'])['permintaan_ton'].shift(1)
        merged['permintaan_lag2'] = merged.groupby(['provinsi', 'jenis_pupuk'])['permintaan_ton'].shift(2)
        merged['permintaan_lag1'] = merged['permintaan_lag1'].fillna(merged['permintaan_ton'].mean())
        merged['permintaan_lag2'] = merged['permintaan_lag2'].fillna(merged['permintaan_ton'].mean())
        
        return merged
    
    def train_models(self, training_data):
        """Train model untuk setiap jenis pupuk"""
        
        # Define features
        feature_columns = [
            'provinsi_encoded', 'bulan_num', 'curah_hujan_mm', 'suhu_celsius',
            'kelembaban_persen', 'luas_tanam_ha', 'produksi_ton',
            'curah_hujan_kategori', 'musim_tanam', 'permintaan_lag1', 'permintaan_lag2'
        ]
        
        self.feature_names = feature_columns
        
        # Train model untuk setiap jenis pupuk
        for jenis_pupuk in training_data['jenis_pupuk'].unique():
            pupuk_data = training_data[training_data['jenis_pupuk'] == jenis_pupuk].copy()
            
            X = pupuk_data[feature_columns]
            y = pupuk_data['permintaan_ton']
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Train Random Forest
            model = RandomForestRegressor(
                n_estimators=100,
                max_depth=15,
                min_samples_split=5,
                random_state=42,
                n_jobs=-1
            )
            
            model.fit(X_train, y_train)
            
            # Evaluate
            y_pred = model.predict(X_test)
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            self.models[jenis_pupuk] = {
                'model': model,
                'mae': mae,
                'r2': r2,
                'feature_importance': dict(zip(feature_columns, model.feature_importances_))
            }
        
        self.is_trained = True
        return self.models
    
    def predict(self, input_data):
        """Prediksi kebutuhan pupuk untuk data baru"""
        
        if not self.is_trained:
            raise ValueError("Model belum di-train. Jalankan train_models terlebih dahulu.")
        
        predictions = {}
        
        for jenis_pupuk, model_info in self.models.items():
            # Filter data untuk pupuk ini
            pupuk_data = input_data[input_data['jenis_pupuk'] == jenis_pupuk].copy()
            
            if len(pupuk_data) == 0:
                continue
            
            X = pupuk_data[self.feature_names]
            
            # Predict
            y_pred = model_info['model'].predict(X)
            
            pupuk_data['prediksi_kebutuhan_ton'] = np.maximum(0, y_pred)
            predictions[jenis_pupuk] = pupuk_data
        
        return predictions
    
    def predict_future(self, provinsi, jenis_pupuk, bulan, curah_hujan, suhu, 
                       kelembaban, luas_tanam, produksi, permintaan_lag1=None, permintaan_lag2=None):
        """Prediksi untuk input manual"""
        
        if not self.is_trained:
            raise ValueError("Model belum di-train.")
        
        # Encode provinsi
        provinsi_encoded = self.label_encoders['provinsi'].transform([provinsi])[0]
        
        # Create input features
        curah_hujan_kategori = 0 if curah_hujan < 100 else (1 if curah_hujan < 200 else (2 if curah_hujan < 300 else (3 if curah_hujan < 500 else 4)))
        musim_tanam = 1 if bulan in [10, 11, 12, 1, 2, 3] else 0
        
        # Use average if lag not provided
        if permintaan_lag1 is None:
            permintaan_lag1 = 400
        if permintaan_lag2 is None:
            permintaan_lag2 = 400
        
        features = pd.DataFrame([{
            'provinsi_encoded': provinsi_encoded,
            'bulan_num': bulan,
            'curah_hujan_mm': curah_hujan,
            'suhu_celsius': suhu,
            'kelembaban_persen': kelembaban,
            'luas_tanam_ha': luas_tanam,
            'produksi_ton': produksi,
            'curah_hujan_kategori': curah_hujan_kategori,
            'musim_tanam': musim_tanam,
            'permintaan_lag1': permintaan_lag1,
            'permintaan_lag2': permintaan_lag2
        }])
        
        # Predict
        prediction = self.models[jenis_pupuk]['model'].predict(features)[0]
        
        return max(0, prediction)
    
    def get_feature_importance(self, jenis_pupuk):
        """Dapatkan feature importance untuk jenis pupuk tertentu"""
        if jenis_pupuk in self.models:
            return self.models[jenis_pupuk]['feature_importance']
        return {}
    
    def get_model_performance(self):
        """Dapatkan performa semua model"""
        performance = {}
        for jenis_pupuk, model_info in self.models.items():
            performance[jenis_pupuk] = {
                'MAE': model_info['mae'],
                'R2 Score': model_info['r2']
            }
        return performance
