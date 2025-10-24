# Fertique AI - Platform Agribusiness Terpadu

## Overview
Fertique AI is a comprehensive agribusiness platform for Indonesian farmers, livestock owners, fisheries, and SMEs. It provides AI-based predictions for fertilizer needs, production tracking, market price monitoring, and business analytics. The platform is mobile-optimized for Android/iOS and ready for Google Play Store deployment, with premium subscription features.

The system integrates multiple data sources to predict fertilizer needs for various crops and fertilizer types across Indonesian provinces. It includes a premium subscription system (Free, Pro Rp 99k/month, Enterprise Rp 299k/month) offering advanced features like confidence interval predictions, SMS alerts, professional PDF reports, and expert AI consultation.

## User Preferences
Preferred communication style: Simple, everyday language.

## Recent Changes (October 24, 2025)

### Complete Rebranding: AgriBiz AI → Fertique AI
**All "AgriBiz" references replaced with "Fertique AI" across:**
1. **Main Application (app_agribusiness.py)**
   - PDF report filenames: `Fertique_Report_*.pdf`
   - Default company name: PT Fertique Indonesia
   - Referral codes: FERTIQUE2024
   - Contact email: support@fertique-ai.com
   - Website: www.fertique-ai.com
   - Share link: fertique-ai.replit.app

2. **PWA Components (Progressive Web App)**
   - Service worker cache names: fertique-ai-v1.0.0, fertique-runtime-v1
   - Push notification tags: fertique-notification
   - Notification titles: "Fertique AI"
   - Install prompts: "Install Fertique AI untuk akses lebih cepat!"
   - Console log messages updated

3. **Deployment Documentation**
   - PLAYSTORE_DEPLOYMENT_GUIDE.md: Complete rebranding
   - Package ID: com.fertique.ai
   - App descriptions and metadata updated
   - Contact information updated throughout

4. **Visual Branding**
   - Fertique AI logo displayed in sidebar (`attached_assets/logo-fertique_1761315091092.jpg`)
   - Professional 3D stock images replaced all emoji icons (11 total)
   - Sector icons: Agriculture, Livestock, Fisheries, Forestry, Horticulture
   - Menu icons: Dashboard, Market, Analytics, Learning, Consultation, Community

5. **Technical Improvements**
   - Fixed Streamlit deprecation warnings: `use_container_width=True` → `width='stretch'`
   - All image displays optimized for Streamlit 1.40+

6. **Copyright Update**
   - Changed footer copyright from "🌾 Fertique AI © 2025" to "copyright © 2025 PT.Sentra Karya Integrasi Global"
   - Applied to both app_agribusiness.py and app.py

### Previous UI/UX Improvements
1. **Redesigned Premium Subscription Cards**
   - Modern card layout with professional appearance
   - Color-coded borders (gray for Free, blue for Pro, gold for Enterprise)
   - Prominent badges ("PALING POPULER", "PAKET AKTIF") positioned at top center
   - Gradient backgrounds for pricing sections
   - Clean feature lists with visual hierarchy
   - Mobile-responsive design with proper spacing

2. **Accessibility Enhancement: Dyslexia-Friendly Mode**
   - Toggle available in sidebar (♿ Mode Dyslexia-Friendly)
   - Increases font size from 15px to 18px
   - Enhanced line-height (1.6 to 2.0) for better readability
   - Added letter-spacing (0.08em) for visual clarity
   - Uses more readable fonts (Arial, Comic Sans MS)
   - Applies globally to all page content
   - Session-based state management

3. **Improved Feature List Presentation**
   - Green checkmarks (✓) for included features (#2E7D32, bold)
   - Gray crosses (✗) for excluded features (#666, normal weight)
   - Icons properly separated from feature text
   - Helper function `_build_feature_list()` for clean HTML generation

4. **Voice Input Warning UX**
   - Changed from intrusive yellow alert to collapsible expander
   - Less distracting, only shows when user opens it
   - Cleaner dashboard appearance

## System Architecture

### Frontend Architecture
The application uses a **Streamlit-based Interactive Dashboard** for rapid development and native Python integration. **Plotly** is used for interactive, high-quality data visualizations, including geographical maps.

### Backend Architecture
A **Python-based Data Processing Pipeline** handles data generation, ML predictions, and utility functions. It follows a **Modular Component Design** to separate concerns for maintainability and testability.

### Machine Learning Architecture
**Ensemble Learning with Random Forest and Gradient Boosting** is employed to predict fertilizer demand by integrating **Multi-source Feature Integration** from BMKG (weather), BPS (agricultural statistics), and Kementan (distribution data).

### Data Management
**In-memory Data Processing with Pandas** is used for current operations, with Streamlit's caching for performance. The system relies on **Simulated Data Generation** for development and testing.

### Geographical Data Handling
**Province-level Granularity with Coordinate Mapping** allows for visualization of fertilizer distribution across Indonesian provinces using Plotly's geo capabilities.

### Export and Reporting
**Excel Export Functionality** is provided for basic data output. **Professional PDF Reports** using ReportLab are available as a premium feature.

### Premium Subscription System
A **Tiered Subscription Model** (Free, Pro, Enterprise) is implemented with **Feature-based Access Control** to gate premium functionalities like advanced predictions and expert consultation.

### Advanced AI Features
Premium tiers offer **Confidence Interval Predictions** for enhanced reliability and an **Expert AI Consultation System** for strategic business guidance.

### Notification System
A **SMS Alert System** (Twilio-based) is available for premium users to receive real-time market notifications.

## External Dependencies

### Core Libraries
- **Streamlit**: Web application framework and UI components.
- **Pandas**: Data manipulation and analysis.
- **NumPy**: Numerical computing.
- **Plotly**: Interactive visualization library.
- **Streamlit AgGrid**: Advanced interactive data tables.
- **Scikit-learn**: Machine learning framework for model training and preprocessing.
- **ReportLab**: PDF generation library for premium reports.
- **QRCode**: QR code generation.

### Data Sources (External Integration Points)
- **BMKG (Badan Meteorologi, Klimatologi, dan Geofisika)**: Weather data (currently simulated).
- **BPS (Badan Pusat Statistik)**: Agricultural statistics (currently simulated).
- **Kementan (Kementerian Pertanian)**: Fertilizer distribution data (currently simulated).

### Third-Party Services
- **Twilio**: SMS/WhatsApp messaging service for premium alerts (mock implementation ready for integration).
- **Stripe**: Payment processing for subscriptions (mock implementation ready for integration).