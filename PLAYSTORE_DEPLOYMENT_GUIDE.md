# 📱 Fertique AI - Panduan Deploy ke Google Play Store

## 🎯 Ringkasan

Fertique AI adalah aplikasi web (Streamlit) yang telah dioptimalkan untuk mobile dan dikonfigurasi sebagai **Progressive Web App (PWA)**. Untuk publish ke Google Play Store, kita akan menggunakan **Trusted Web Activities (TWA)** yang membungkus aplikasi web dalam container Android native.

---

## 📋 Prasyarat

### 1. Akun & Tools
- ✅ Google Play Console Developer Account ($25 one-time fee)
- ✅ Android Studio terinstall
- ✅ Java Development Kit (JDK) 11 atau lebih tinggi
- ✅ Node.js dan npm terinstall

### 2. Aplikasi Sudah Deploy
- ✅ Aplikasi sudah di-publish di Replit atau hosting lain
- ✅ Domain custom (opsional tapi recommended): `https://fertique-ai.com`
- ✅ SSL/HTTPS aktif (wajib untuk TWA)
- ✅ PWA manifest dan service worker sudah dikonfigurasi ✓

---

## 🚀 Metode 1: Menggunakan Bubblewrap (Recommended - Paling Mudah)

Bubblewrap adalah CLI tool dari Google untuk membuat TWA dengan mudah.

### Step 1: Install Bubblewrap

```bash
npm install -g @bubblewrap/cli
```

### Step 2: Inisialisasi Project TWA

```bash
# Buat folder project
mkdir fertique-ai-android
cd fertique-ai-android

# Inisialisasi TWA
bubblewrap init --manifest https://your-app-url.com/static/manifest.json
```

Anda akan ditanya beberapa pertanyaan:
- **Domain**: Masukkan URL aplikasi Anda (e.g., `https://fertique-ai.replit.app`)
- **Package name**: `com.fertique.ai` (format: com.namacompany.namaapp)
- **App name**: Fertique AI
- **Display mode**: `standalone`
- **Icon**: Gunakan icon yang sudah dibuat di folder `static/`

### Step 3: Build APK

```bash
# Build APK
bubblewrap build

# Outputnya ada di: ./app-release-signed.apk
```

### Step 4: Test APK di Android Device

```bash
# Install ke device yang terkoneksi via USB
adb install app-release-signed.apk
```

### Step 5: Generate Android App Bundle (AAB) untuk Play Store

```bash
# Build AAB (required untuk Play Store)
bubblewrap build --skipPwaValidation

# Output: app-release-bundle.aab
```

---

## 🚀 Metode 2: Menggunakan PWABuilder (Paling Cepat - Web-based)

### Step 1: Buka PWABuilder
1. Kunjungi: https://www.pwabuilder.com/
2. Masukkan URL aplikasi Anda: `https://your-app-url.com`
3. Klik "Start"

### Step 2: Review PWA Score
- PWABuilder akan menganalisis aplikasi Anda
- Pastikan score minimal 80/100
- Fix issues jika ada (manifest, service worker, etc.)

### Step 3: Generate Android Package
1. Klik tab "Publish"
2. Pilih platform "Android"
3. Klik "Generate Package"
4. Isi informasi:
   - **Package ID**: `com.fertique.ai`
   - **App name**: Fertique AI
   - **Version code**: 1
   - **Version name**: 1.0.0
   - **Launcher name**: Fertique AI
   - **Theme color**: `#2E7D32`
   - **Background color**: `#F1F8E9`

### Step 4: Download Package
- Download file `.aab` (Android App Bundle)
- Simpan signing key dengan aman (untuk update di masa depan)

---

## 📦 Upload ke Google Play Console

### Step 1: Login ke Play Console
1. Buka: https://play.google.com/console
2. Login dengan akun Google Developer Anda
3. Klik "Create app"

### Step 2: Setup Informasi Aplikasi

#### A. App Details
- **App name**: Fertique AI - Platform Agribusiness Terpadu
- **Default language**: Indonesian (Bahasa Indonesia)
- **App or game**: App
- **Free or paid**: Free
- **Category**: Business / Productivity
- **Tags**: agriculture, farming, business, enterprise, AI, predictions

#### B. Store Listing
Isi informasi berikut:

**Short description** (max 80 characters):
```
Platform AI untuk Petani, Peternak, Nelayan & Pelaku Usaha Indonesia
```

**Full description** (max 4000 characters):
```
Fertique AI - Platform Agribusiness Terpadu Berbasis AI

Solusi digital lengkap untuk seluruh ekosistem agribusiness di Indonesia!

🌾 UNTUK SIAPA?
• Petani - Prediksi kebutuhan pupuk & pestisida
• Petani Hortikultura - Optimasi hasil sayur & buah
• Peternak - Manajemen pakan & kesehatan ternak
• Petani Ikan - Prediksi pakan & kualitas air kolam
• Pemilik Usaha - Analisis bisnis & profitabilitas

🤖 FITUR UNGGULAN:
✓ AI Prediction - Prediksi kebutuhan input berbasis machine learning
✓ Voice Input - Input data dengan suara (hands-free untuk di lapangan)
✓ Real-time Analytics - Monitor produksi & penjualan real-time
✓ Market Prices - Update harga pasar terkini
✓ Stock Management - Kelola stok produk & input
✓ ROI Calculator - Hitung profitabilitas usaha
✓ Community - Forum diskusi & sharing pengalaman
✓ Gamification - Raih badges & rewards

📊 DASHBOARD LENGKAP:
• Overview produksi multi-sektor
• Trend analysis harga pasar
• Prediksi kebutuhan input (pupuk, pakan, benih)
• Analisis cuaca & dampak ke produksi
• Laporan keuangan & profitabilitas

💰 GRATIS & MUDAH DIGUNAKAN:
Tanpa biaya langganan, interface friendly, support Bahasa Indonesia

Bergabunglah dengan 10,000+ pengguna yang sudah meningkatkan produktivitas dengan Fertique AI!

🏆 AWARDS:
• Finalis 5 Besar Lomba Wirausaha Muda Pemula - Kategori Social Enterprise KEMENPORA 2024
• Lolos 225 Besar kompetisi Bisnis Diplomat Success Challenge - Wismilak Group 2024

📧 Support: support@fertique-ai.com
🌐 Website: https://fertique-ai.com
```

#### C. Graphics Assets

**Screenshots** (minimal 2, maksimal 8):
- Phone screenshots: 1080 x 1920 pixels atau 720 x 1280 pixels
- Tablet screenshots (opsional): 1920 x 1080 pixels

Capture dari:
1. Halaman Beranda (Dashboard)
2. Sektor Agribusiness page
3. Prediksi & Analisis page
4. Dashboard Bisnis
5. Community & Gamifikasi

**Feature graphic** (required):
- Size: 1024 x 500 pixels
- Design banner menarik dengan logo + tagline

**App icon** (required):
- Size: 512 x 512 pixels
- Gunakan icon dari `static/icon-512x512.png`

### Step 3: Content Rating
1. Klik "Start questionnaire"
2. Pilih kategori: Utility / Business
3. Jawab semua pertanyaan tentang konten
4. Submit untuk mendapat rating (biasanya: Everyone/3+)

### Step 4: App Content
Lengkapi:
- ✅ Privacy Policy URL (wajib)
- ✅ Target audience: 18+ (professional users)
- ✅ Data safety: Jelaskan data apa yang dikumpulkan
- ✅ Government apps: No (kecuali official app)

### Step 5: Upload App Bundle

1. Klik "Production" → "Create new release"
2. Upload file `.aab` yang sudah dibuat
3. Isi Release notes:
```
Version 1.0.0 - Initial Release

Features:
✓ Multi-sector agribusiness dashboard
✓ AI-powered predictions
✓ Voice input for hands-free operation
✓ Real-time market prices
✓ Business analytics
✓ Community & gamification
✓ Optimized for mobile devices
```

4. Review dan save

### Step 6: Submit for Review
1. Review semua informasi
2. Klik "Send for review"
3. Tunggu review dari Google (biasanya 1-7 hari)

---

## 🔧 Konfigurasi Digital Asset Links (Penting!)

Untuk memverifikasi kepemilikan domain, tambahkan file di web server Anda:

### Step 1: Generate SHA-256 Fingerprint
```bash
# Dari signing key yang digunakan
keytool -list -v -keystore YOUR_KEYSTORE.keystore
```

### Step 2: Buat file `.well-known/assetlinks.json`

Buat file di root domain: `https://your-domain.com/.well-known/assetlinks.json`

```json
[{
  "relation": ["delegate_permission/common.handle_all_urls"],
  "target": {
    "namespace": "android_app",
    "package_name": "com.fertique.ai",
    "sha256_cert_fingerprints": [
      "YOUR_SHA256_FINGERPRINT_HERE"
    ]
  }
}]
```

### Step 3: Verifikasi
Pastikan file dapat diakses:
```
https://your-domain.com/.well-known/assetlinks.json
```

---

## 📱 Optimisasi untuk App Store

### 1. App Store Optimization (ASO)

**Keywords yang baik**:
- agribusiness, pertanian, peternakan, perikanan
- pupuk, pakan, benih, pestisida
- bisnis, UMKM, usaha kecil, korporat, enterprise
- AI, machine learning, prediksi
- Indonesia, petani, peternak, nelayan

### 2. A/B Testing Screenshots
- Test berbagai layout screenshot
- Highlight fitur utama di screenshot pertama
- Gunakan text overlay untuk explain fitur

### 3. Ratings & Reviews
- Minta user untuk rate & review
- Respond to reviews (positif dan negatif)
- Update app berdasarkan feedback

---

## 🔄 Update Aplikasi

### Cara Update Versi Baru:

1. **Update version di manifest.json**:
```json
{
  "version": "1.1.0",
  "version_name": "1.1.0"
}
```

2. **Build ulang dengan Bubblewrap**:
```bash
bubblewrap update
bubblewrap build
```

3. **Upload ke Play Console**:
- Production → Create new release
- Upload AAB baru
- Tambahkan release notes
- Submit

---

## ⚠️ Troubleshooting Common Issues

### Issue 1: "App not installable"
**Solution**: Pastikan:
- Package name unique
- Signing key sama untuk semua update
- minSdkVersion minimal 19

### Issue 2: "Manifest tidak valid"
**Solution**: 
- Pastikan manifest.json accessible via HTTPS
- Validate JSON di: https://manifest-validator.appspot.com/

### Issue 3: "Service Worker tidak terdeteksi"
**Solution**:
- Pastikan SW registered di semua pages
- Test di: Chrome DevTools → Application → Service Workers

### Issue 4: "Digital Asset Links failed"
**Solution**:
- Verifikasi SHA-256 fingerprint benar
- Pastikan assetlinks.json di `/.well-known/assetlinks.json`
- Test di: https://digitalassetlinks.googleapis.com/v1/statements:list?source.web.site=https://your-domain.com

---

## 📊 Analytics & Monitoring

### Recommended Tools:
1. **Google Analytics for Firebase**
   - Track user engagement
   - Monitor crashes
   - User demographics

2. **Play Console Metrics**
   - Install/uninstall rates
   - User retention
   - Reviews & ratings

3. **Custom Events**
   - Track feature usage
   - Monitor prediction requests
   - Voice input usage

---

## 🎉 Checklist Pre-Launch

Sebelum publish, pastikan:

- [ ] App tested di berbagai device Android (min SDK 21 / Android 5.0)
- [ ] PWA score > 80 di Lighthouse
- [ ] HTTPS enabled dan valid SSL certificate
- [ ] Manifest.json accessible dan valid
- [ ] Service Worker registered dan working
- [ ] All icons (72x72 sampai 512x512) ada dan berkualitas
- [ ] Privacy Policy published dan accessible
- [ ] Screenshots high quality (minimal 2)
- [ ] Feature graphic designed (1024x500)
- [ ] Content rating completed
- [ ] Target audience defined
- [ ] Data safety section filled
- [ ] Release notes prepared
- [ ] Digital Asset Links configured
- [ ] App tested in production URL
- [ ] Backup signing key tersimpan aman

---

## 📞 Support & Resources

### Official Documentation:
- [TWA Documentation](https://developer.chrome.com/docs/android/trusted-web-activity/)
- [Bubblewrap Guide](https://github.com/GoogleChromeLabs/bubblewrap)
- [Play Console Help](https://support.google.com/googleplay/android-developer/)
- [PWA Best Practices](https://web.dev/pwa-checklist/)

### Tools:
- [PWABuilder](https://www.pwabuilder.com/)
- [Lighthouse](https://developers.google.com/web/tools/lighthouse)
- [Manifest Validator](https://manifest-validator.appspot.com/)

### Community:
- Stack Overflow: Tag `trusted-web-activity`
- Reddit: r/androiddev
- Google Groups: Chromium TWA

---

## 🔐 Keamanan & Privacy

### Best Practices:
1. **Secure API endpoints** dengan authentication
2. **Enkripsi data sensitif** (user credentials, payment info)
3. **Regular security updates**
4. **Privacy policy compliant** dengan UU Perlindungan Data Indonesia
5. **Request minimal permissions** di Android

---

## 🌟 Tips Sukses di Play Store

1. **Optimize first week**: Push marketing, ask for reviews
2. **Respond to reviews** dalam 24 jam
3. **Update regularly** (minimal sebulan sekali)
4. **Add new features** berdasarkan user request
5. **Monitor analytics** dan optimize conversion funnel
6. **A/B test** screenshots dan descriptions
7. **Localization** ke bahasa daerah jika perlu
8. **Cross-promote** dengan website dan social media

---

## ✅ Ready to Launch!

Setelah mengikuti guide ini, aplikasi Fertique AI siap diluncurkan di Google Play Store!

**Estimasi Timeline:**
- Setup & Build: 2-4 jam
- Play Console setup: 2-3 jam
- Google Review: 1-7 hari
- **Total: 3-10 hari** dari mulai sampai live di Play Store

**Good luck! 🚀🌾**

---

**Note**: Guide ini dibuat untuk Fertique AI v1.0.0. Untuk update atau pertanyaan, hubungi development team.

**Last Updated**: October 24, 2025
