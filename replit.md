# AgriBiz AI - Platform Agribusiness Terpadu

## Overview
AgriBiz AI is a comprehensive agribusiness platform for Indonesian farmers, livestock owners, fisheries, and SMEs. It provides AI-based predictions for fertilizer needs, production tracking, market price monitoring, and business analytics. The platform is mobile-optimized for Android/iOS and ready for Google Play Store deployment, with premium subscription features.

The system integrates multiple data sources to predict fertilizer needs for various crops and fertilizer types across Indonesian provinces. It includes a premium subscription system (Free, Pro Rp 99k/month, Enterprise Rp 299k/month) offering advanced features like confidence interval predictions, SMS alerts, professional PDF reports, and expert AI consultation.

## User Preferences
Preferred communication style: Simple, everyday language.

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