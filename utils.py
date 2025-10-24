import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

def format_number(num):
    """Format angka dengan pemisah ribuan"""
    return f"{num:,.0f}"

def format_decimal(num, decimals=2):
    """Format angka desimal"""
    return f"{num:,.{decimals}f}"

def calculate_distribution_efficiency(stok, permintaan):
    """Hitung efisiensi distribusi"""
    if permintaan == 0:
        return 0
    return min(100, (stok / permintaan) * 100)

def get_status_color(utilisasi):
    """Tentukan warna status berdasarkan utilisasi"""
    if utilisasi < 30:
        return '🔴 Kritis'
    elif utilisasi < 50:
        return '🟡 Rendah'
    elif utilisasi < 80:
        return '🟢 Optimal'
    else:
        return '🔵 Tinggi'

def get_priority_level(gap):
    """Tentukan prioritas berdasarkan gap kebutuhan"""
    if gap > 500:
        return '🔴 Sangat Tinggi'
    elif gap > 300:
        return '🟠 Tinggi'
    elif gap > 100:
        return '🟡 Sedang'
    else:
        return '🟢 Rendah'

def create_heatmap_indonesia(data, value_column, title, color_scale='Viridis'):
    """Buat heatmap Indonesia dengan Plotly"""
    
    fig = px.scatter_geo(
        data,
        lat='latitude',
        lon='longitude',
        size=value_column,
        color=value_column,
        hover_name='provinsi',
        hover_data={
            value_column: ':.0f',
            'latitude': False,
            'longitude': False
        },
        color_continuous_scale=color_scale,
        title=title,
        size_max=50
    )
    
    fig.update_geos(
        center=dict(lat=-2.5, lon=118),
        projection_scale=4,
        showcountries=True,
        countrycolor="lightgray",
        showcoastlines=True,
        coastlinecolor="gray",
        showland=True,
        landcolor="rgb(243, 243, 243)"
    )
    
    fig.update_layout(
        height=600,
        margin={"r":0,"t":40,"l":0,"b":0},
        font=dict(size=12)
    )
    
    return fig

def create_bar_chart(data, x, y, title, color=None, orientation='v'):
    """Buat bar chart dengan Plotly"""
    
    if orientation == 'v':
        fig = px.bar(data, x=x, y=y, color=color, title=title,
                     color_discrete_sequence=px.colors.qualitative.Set2)
    else:
        fig = px.bar(data, x=y, y=x, color=color, title=title,
                     orientation='h',
                     color_discrete_sequence=px.colors.qualitative.Set2)
    
    fig.update_layout(
        height=500,
        showlegend=True if color else False,
        hovermode='x unified'
    )
    
    return fig

def create_line_chart(data, x, y, color, title):
    """Buat line chart dengan Plotly"""
    
    fig = px.line(data, x=x, y=y, color=color, title=title,
                  markers=True,
                  color_discrete_sequence=px.colors.qualitative.Bold)
    
    fig.update_layout(
        height=500,
        hovermode='x unified'
    )
    
    return fig

def create_pie_chart(data, values, names, title):
    """Buat pie chart dengan Plotly"""
    
    fig = px.pie(data, values=values, names=names, title=title,
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=500)
    
    return fig

def create_comparison_chart(data, x, y1, y2, title, label1='Aktual', label2='Prediksi'):
    """Buat chart perbandingan dengan dua metrics"""
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=data[x],
        y=data[y1],
        name=label1,
        marker_color='rgb(55, 83, 109)'
    ))
    
    fig.add_trace(go.Bar(
        x=data[x],
        y=data[y2],
        name=label2,
        marker_color='rgb(26, 118, 255)'
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title=x,
        yaxis_title='Ton',
        barmode='group',
        height=500,
        hovermode='x unified'
    )
    
    return fig

def create_gauge_chart(value, title, max_value=100):
    """Buat gauge chart"""
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title},
        gauge={
            'axis': {'range': [None, max_value]},
            'bar': {'color': "darkgreen"},
            'steps': [
                {'range': [0, 30], 'color': "lightcoral"},
                {'range': [30, 50], 'color': "lightyellow"},
                {'range': [50, 80], 'color': "lightgreen"},
                {'range': [80, 100], 'color': "lightblue"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(height=300)
    return fig

def export_to_excel(dataframes_dict, filename):
    """Export multiple dataframes ke Excel"""
    
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        for sheet_name, df in dataframes_dict.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    return filename

def calculate_route_optimization(distribusi_data):
    """Hitung optimasi rute distribusi sederhana berdasarkan prioritas"""
    
    # Hitung gap (selisih permintaan - stok)
    distribusi_data['gap'] = distribusi_data['permintaan_ton'] - distribusi_data['stok_ton']
    
    # Prioritas berdasarkan gap terbesar
    distribusi_data['prioritas'] = distribusi_data['gap'].rank(ascending=False, method='dense').astype(int)
    
    # Status
    distribusi_data['status'] = distribusi_data['gap'].apply(
        lambda x: '🔴 Defisit' if x > 100 else ('🟡 Kurang' if x > 0 else '🟢 Cukup')
    )
    
    return distribusi_data.sort_values('prioritas')

def generate_recommendation(row):
    """Generate rekomendasi aksi untuk distribusi"""
    
    gap = row.get('gap', 0)
    stok = row.get('stok_ton', 0)
    
    if gap > 500:
        return f"URGENT: Kirim {gap:.0f} ton segera dari gudang terdekat"
    elif gap > 300:
        return f"Prioritas Tinggi: Distribusi {gap:.0f} ton dalam 1-2 hari"
    elif gap > 100:
        return f"Distribusi {gap:.0f} ton sesuai jadwal normal"
    elif gap > 0:
        return f"Monitor dan distribusi {gap:.0f} ton jika diperlukan"
    elif stok > 1000:
        return f"Surplus {abs(gap):.0f} ton, pertimbangkan redistribusi ke daerah defisit"
    else:
        return "Stok optimal, lanjutkan monitoring rutin"

def calculate_monthly_trend(data, date_column, value_column, group_column=None):
    """Hitung tren bulanan dari data historis"""
    
    data = data.copy()
    data['bulan'] = pd.to_datetime(data[date_column]).dt.to_period('M')
    
    if group_column:
        trend = data.groupby(['bulan', group_column])[value_column].sum().reset_index()
        trend['bulan'] = trend['bulan'].astype(str)
    else:
        trend = data.groupby('bulan')[value_column].sum().reset_index()
        trend['bulan'] = trend['bulan'].astype(str)
    
    return trend

def get_color_palette():
    """Return color palette untuk tema pertanian"""
    return {
        'primary': '#2E7D32',      # Hijau tua
        'secondary': '#558B2F',    # Hijau olive
        'accent': '#FFA726',       # Orange
        'background': '#F1F8E9',   # Hijau muda
        'warning': '#F57C00',      # Orange gelap
        'danger': '#C62828',       # Merah
        'success': '#43A047',      # Hijau cerah
        'info': '#1976D2'          # Biru
    }
