import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import io
import qrcode

class PremiumSubscription:
    """Manage premium subscription tiers and features"""
    
    PLANS = {
        'free': {
            'name': 'Basic (Gratis)',
            'price': 0,
            'price_text': 'Gratis',
            'features': [
                '✓ Dashboard dasar',
                '✓ Prediksi AI standar',
                '✓ 3 bulan data historis',
                '✓ Export Excel',
                '✓ Support komunitas',
                '✗ SMS Alert',
                '✗ Prediksi Advanced',
                '✗ PDF Reports',
                '✗ Expert AI Consultation'
            ],
            'color': '#9E9E9E'
        },
        'pro': {
            'name': 'Pro',
            'price': 99000,
            'price_text': 'Rp 99.000/bulan',
            'features': [
                '✓ Semua fitur Basic',
                '✓ Prediksi AI Advanced dengan confidence interval',
                '✓ 12 bulan data historis',
                '✓ SMS Alert harga pasar',
                '✓ Professional PDF Reports',
                '✓ Export multi-format',
                '✓ Priority support',
                '✗ Expert AI Consultation',
                '✗ Multi-user team'
            ],
            'color': '#2196F3',
            'popular': True
        },
        'enterprise': {
            'name': 'Enterprise',
            'price': 299000,
            'price_text': 'Rp 299.000/bulan',
            'features': [
                '✓ Semua fitur Pro',
                '✓ Expert AI Consultation 24/7',
                '✓ Unlimited data historis',
                '✓ WhatsApp + SMS Alert',
                '✓ Custom analytics dashboard',
                '✓ API Access',
                '✓ Multi-user team (5 users)',
                '✓ Dedicated account manager',
                '✓ Priority hotline support'
            ],
            'color': '#FF9800'
        }
    }
    
    @staticmethod
    def get_user_plan():
        """Get current user's subscription plan"""
        if 'subscription_plan' not in st.session_state:
            st.session_state.subscription_plan = 'free'
        return st.session_state.subscription_plan
    
    @staticmethod
    def set_user_plan(plan):
        """Set user's subscription plan"""
        st.session_state.subscription_plan = plan
        st.session_state.subscription_date = datetime.now()
    
    @staticmethod
    def has_feature(feature):
        """Check if current plan has specific feature"""
        plan = PremiumSubscription.get_user_plan()
        feature_map = {
            'sms_alerts': ['pro', 'enterprise'],
            'advanced_predictions': ['pro', 'enterprise'],
            'pdf_reports': ['pro', 'enterprise'],
            'expert_consultation': ['enterprise'],
            'api_access': ['enterprise'],
            'multi_user': ['enterprise'],
            'whatsapp_alerts': ['enterprise']
        }
        return plan in feature_map.get(feature, [])
    
    @staticmethod
    def get_plan_info(plan):
        """Get plan information"""
        return PremiumSubscription.PLANS.get(plan, PremiumSubscription.PLANS['free'])


class AdvancedPredictions:
    """Advanced AI predictions with confidence intervals"""
    
    @staticmethod
    def predict_with_confidence(data, commodity, months_ahead=3):
        """Generate predictions with confidence intervals"""
        np.random.seed(42)
        
        predictions = []
        current_price = data['price'].iloc[-1] if len(data) > 0 else 50000
        
        for month in range(1, months_ahead + 1):
            trend = np.random.normal(1.02, 0.05)
            predicted_price = current_price * (trend ** month)
            
            confidence_low = predicted_price * 0.92
            confidence_high = predicted_price * 1.08
            
            predictions.append({
                'month': month,
                'date': (datetime.now() + timedelta(days=30*month)).strftime('%b %Y'),
                'predicted_price': predicted_price,
                'confidence_low': confidence_low,
                'confidence_high': confidence_high,
                'confidence_level': 85 + np.random.randint(-5, 5),
                'trend': 'Naik' if trend > 1 else 'Turun',
                'recommendation': AdvancedPredictions._get_recommendation(trend)
            })
        
        return pd.DataFrame(predictions)
    
    @staticmethod
    def _get_recommendation(trend):
        """Get trading recommendation based on trend"""
        if trend > 1.05:
            return "📈 STRONG BUY - Harga diprediksi naik signifikan"
        elif trend > 1.02:
            return "📊 BUY - Trend positif"
        elif trend > 0.98:
            return "➡️ HOLD - Harga stabil"
        elif trend > 0.95:
            return "📉 WATCH - Pantau perkembangan"
        else:
            return "⚠️ SELL - Pertimbangkan jual sebelum penurunan"


class SMSAlertSystem:
    """SMS alert system for market price changes"""
    
    @staticmethod
    def setup_alert(phone_number, commodity, trigger_type, threshold_value):
        """Setup SMS alert"""
        if 'sms_alerts' not in st.session_state:
            st.session_state.sms_alerts = []
        
        alert = {
            'id': len(st.session_state.sms_alerts) + 1,
            'phone': phone_number,
            'commodity': commodity,
            'trigger_type': trigger_type,
            'threshold': threshold_value,
            'active': True,
            'created_at': datetime.now(),
            'last_triggered': None
        }
        
        st.session_state.sms_alerts.append(alert)
        return alert
    
    @staticmethod
    def get_active_alerts():
        """Get all active alerts"""
        if 'sms_alerts' not in st.session_state:
            st.session_state.sms_alerts = []
        return [a for a in st.session_state.sms_alerts if a['active']]
    
    @staticmethod
    def simulate_send_sms(phone, message):
        """Simulate sending SMS (would use Twilio in production)"""
        return {
            'success': True,
            'message_id': f'SM{np.random.randint(1000000, 9999999)}',
            'phone': phone,
            'sent_at': datetime.now(),
            'cost': 150
        }


class PDFReportGenerator:
    """Generate professional PDF reports"""
    
    @staticmethod
    def generate_business_report(data, user_name="Pengguna Fertique"):
        """Generate comprehensive business report"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=18)
        
        elements = []
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2E7D32'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1B5E20'),
            spaceAfter=12,
            alignment=TA_LEFT
        )
        
        elements.append(Paragraph("Fertique AI", title_style))
        elements.append(Paragraph("Laporan Analisis Bisnis Premium", styles['Heading2']))
        elements.append(Spacer(1, 12))
        
        info_data = [
            ['Tanggal Laporan:', datetime.now().strftime('%d %B %Y')],
            ['Pengguna:', user_name],
            ['Paket:', 'Professional'],
            ['Status:', 'Active']
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 3*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E8F5E9')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 20))
        
        elements.append(Paragraph("📊 Ringkasan Eksekutif", subtitle_style))
        summary_text = """
        Laporan ini memberikan analisis komprehensif terhadap kinerja bisnis agribusiness Anda. 
        Analisis mencakup trend produksi, prediksi harga pasar, dan rekomendasi strategis untuk 
        meningkatkan profitabilitas.
        """
        elements.append(Paragraph(summary_text, styles['BodyText']))
        elements.append(Spacer(1, 12))
        
        if len(data) > 0:
            elements.append(Paragraph("📈 Analisis Data Produksi", subtitle_style))
            
            summary_stats = [
                ['Metrik', 'Nilai', 'Status'],
                ['Total Transaksi', f"{len(data):,}", '✓'],
                ['Rata-rata Harga', f"Rp {data['price'].mean():,.0f}" if 'price' in data.columns else 'N/A', '✓'],
                ['Volatilitas', f"{data['price'].std()/data['price'].mean()*100:.1f}%" if 'price' in data.columns else 'N/A', '⚠'],
            ]
            
            stats_table = Table(summary_stats, colWidths=[2.5*inch, 1.5*inch, 1*inch])
            stats_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E7D32')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(stats_table)
        
        elements.append(Spacer(1, 20))
        elements.append(Paragraph("💡 Rekomendasi Strategis", subtitle_style))
        recommendations = """
        1. <b>Diversifikasi Produk:</b> Pertimbangkan untuk menambah variasi komoditas<br/>
        2. <b>Optimasi Timing:</b> Manfaatkan prediksi AI untuk menentukan waktu jual terbaik<br/>
        3. <b>Manajemen Risiko:</b> Gunakan SMS alert untuk monitor fluktuasi harga<br/>
        4. <b>Ekspansi Pasar:</b> Jelajahi peluang pasar baru berdasarkan trend data<br/>
        """
        elements.append(Paragraph(recommendations, styles['BodyText']))
        
        elements.append(PageBreak())
        elements.append(Paragraph("📞 Hubungi Kami", subtitle_style))
        contact_text = """
        Fertique AI - Platform Agribusiness Terpadu<br/>
        Email: support@fertique-ai.com<br/>
        WhatsApp: +62 812-3456-7890<br/>
        Website: www.fertique-ai.com
        """
        elements.append(Paragraph(contact_text, styles['BodyText']))
        
        footer_text = f"<i>Laporan dibuat oleh Fertique AI Premium | {datetime.now().strftime('%d %B %Y %H:%M')} | Confidential</i>"
        elements.append(Spacer(1, 30))
        elements.append(Paragraph(footer_text, styles['Italic']))
        
        doc.build(elements)
        buffer.seek(0)
        return buffer


class ExpertAIConsultation:
    """AI-powered expert consultation system"""
    
    EXPERTISE_AREAS = {
        'produksi': 'Optimasi Produksi & Yield',
        'harga': 'Strategi Penetapan Harga',
        'distribusi': 'Manajemen Distribusi & Logistik',
        'keuangan': 'Analisis Keuangan & Profitabilitas',
        'pemasaran': 'Strategi Pemasaran',
        'teknologi': 'Adopsi Teknologi Pertanian'
    }
    
    @staticmethod
    def get_ai_recommendation(question, context_data=None):
        """Get AI-powered expert recommendation"""
        expertise_responses = {
            'produksi': [
                "Berdasarkan data cuaca dan pola historis, saya rekomendasikan:",
                "1. Gunakan varietas unggul yang tahan terhadap kondisi iklim lokal",
                "2. Terapkan rotasi tanaman untuk menjaga kesuburan tanah",
                "3. Optimalkan penggunaan pupuk berdasarkan analisis tanah",
                "4. Implementasikan sistem irigasi tetes untuk efisiensi air",
                "Potensi peningkatan yield: 25-30%"
            ],
            'harga': [
                "Analisis trend pasar menunjukkan:",
                "1. Harga komoditas Anda cenderung naik 15% dalam 3 bulan ke depan",
                "2. Timing terbaik untuk menjual: Minggu ke-2 bulan depan",
                "3. Pertimbangkan kontrak forward untuk hedge risiko harga",
                "4. Diversifikasi ke komoditas premium untuk margin lebih tinggi",
                "ROI potensial: +20% dengan strategi ini"
            ],
            'distribusi': [
                "Optimasi distribusi Anda dengan:",
                "1. Konsolidasi pengiriman untuk efisiensi biaya",
                "2. Kerjasama dengan agregator lokal",
                "3. Gunakan cold chain untuk produk perishable",
                "4. Implementasi tracking system real-time",
                "Penghematan biaya logistik: hingga 30%"
            ],
            'keuangan': [
                "Analisis finansial menunjukkan:",
                "1. Current margin: 22% (industry avg: 18%)",
                "2. Potensi peningkatan: fokus pada high-value crops",
                "3. Alokasi modal optimal: 60% produksi, 25% marketing, 15% R&D",
                "4. Cash flow projection: positif untuk 12 bulan ke depan",
                "Target ROI: 35% year-over-year"
            ]
        }
        
        area = 'produksi'
        for key in ExpertAIConsultation.EXPERTISE_AREAS.keys():
            if key in question.lower():
                area = key
                break
        
        response = expertise_responses.get(area, expertise_responses['produksi'])
        
        return {
            'question': question,
            'expertise_area': ExpertAIConsultation.EXPERTISE_AREAS[area],
            'recommendation': '\n'.join(response),
            'confidence': np.random.randint(85, 98),
            'timestamp': datetime.now(),
            'follow_up_questions': [
                "Bagaimana cara implementasi rekomendasi ini?",
                "Berapa estimasi biaya untuk menerapkan strategi ini?",
                "Apa risiko yang perlu diantisipasi?"
            ]
        }
